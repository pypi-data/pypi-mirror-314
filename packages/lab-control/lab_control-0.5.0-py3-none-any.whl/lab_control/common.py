import pandas as pd
import numpy as np
from pathlib import Path
from typing import Self, Any, Callable, TextIO
import yaml
from copy import deepcopy
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.colors import DEFAULT_PLOTLY_COLORS
from pyvisa.resources import MessageBasedResource
from pyvisa.highlevel import ResourceManager
from abc import ABC, abstractmethod
from datetime import datetime
from dataclasses import dataclass
from io import TextIOWrapper
from zipfile import ZipFile
from contextlib import contextmanager
from itertools import cycle


class Device(ABC):
    """Base class for devices"""

    _default_defaults: dict[str, Any]
    _res: MessageBasedResource

    _param_map: dict[str, tuple[str, Any, Any]]

    def __init__(self, address: str, *, defaults: dict[str, Any] | None = None) -> None:
        self._rm = ResourceManager()
        self._res = self._rm.open_resource(address, read_termination="\n")  # type: ignore
        self._defaults = ParamProxy.recursive_merge(self._default_defaults, (defaults or {}))
        for name in self._defaults:
            assert name in self._param_map.keys(), f"Unknown parameter {name}!"
        self.flush()
        self.id = self._res.query("*IDN?")
        self._params = ParamProxy(self._res, param_map=self._param_map)

    @property
    def defaults(self) -> dict[str, Any]:
        """The default settings for this instance"""

        def filter_none(d: dict | Any) -> dict:
            if isinstance(d, dict):
                return {k: filter_none(v) for k, v in d.items() if v is not None}
            else:
                return d

        return filter_none(self._defaults)

    def _parse_kwargs(self, kwargs: dict, no_defaults: bool) -> dict:
        for arg in kwargs:
            assert arg in self._param_map.keys(), f"Unknown parameter {arg}!"

        if not no_defaults:
            params = ParamProxy.recursive_merge(self._defaults, kwargs)
        else:
            params = kwargs

        return params

    def _check_params(self, params: dict, param_map: dict = None) -> tuple[dict, list[str | tuple[str, ...]]]:
        """Verify that only valid parameters are passed and filter out and return unspecified parameters

        Args:
            params (dict): The parameters to check.

        Returns:
            tuple[dict, list[str | tuple[str, ...]]]: The valid parameters and the unspecified parameters.
        """
        assert isinstance
        param_map = param_map or self._param_map
        valid_params = {}
        unspecified = []
        for key, val in param_map.items():
            if isinstance(val, ParamProxy.Constant):
                continue
            elif isinstance(val, dict):
                sub_params = params.get(key, {})
                assert isinstance(sub_params, dict), f"Parameter {key} must be a dictionary!"
                new_params, new_unspecified = self._check_params(params.get(key, {}), val)
                valid_params[key] = new_params
                unspecified.extend((key, sub_key) for sub_key in new_unspecified)
            else:
                cmd, from_device, to_device = val
                if to_device == ParamProxy.read_only:
                    continue
                if (p := params.get(key, None)) is not None:
                    valid_params[key] = p
                else:
                    unspecified.append(key)
        illegal_params = set(params.keys()) - set(param_map.keys())
        assert not illegal_params, f"Unknown parameters {illegal_params}!"
        return valid_params, unspecified

    def _set_params(self, params: dict, show_warnings: bool, **kwargs: dict) -> None:
        filtered_params, unspecified = self._check_params(params)
        if show_warnings and unspecified:
            print(f"Warning: unspecified parameters will use current device settings: {unspecified}")
        self._params.update(filtered_params, **kwargs)

    def flush(self) -> None:
        """Flush the read buffer of the device

        Sometimes the device may get de-synced an a read operation will return the result of the previous command.
        This can be used to clear the buffer before a new operation.
        """
        self._res.clear()

    @contextmanager
    def _temporary_timeout(self, timeout: float | None):
        old_timeout = self._res.timeout
        self._res.timeout = timeout
        try:
            yield
        finally:
            self._res.timeout = old_timeout

    def _make_measurement_name(self, parameters: dict, date: datetime) -> str:
        """Generate a measurement name from the measurement parameters which will be used if no name is given

        Args:
            parameters (dict): The measurement parameters
            date (datetime): The time of the measurement

        Returns:
            str: The generated name
        """
        return f"{self.id.split(',')[1].replace(' ','-')}_{parameters['meas']}_{date:%Y-%m-%dT%H:%M:%S}"

    def _make_metadata(self, name: str, comment: str, index_col: str, additional_meta: dict, user_meta: dict) -> dict:
        """Generate the metadata for a measurement

        Args:
            name (str | None): Measurement Name. Defaults to automatic name from metadata if None.
            comment (str): Comment to add to metadata..
            index_col (str): The index column of the measurement
            additional_meta (dict): Additional metadata to add to the measurement
            user_meta (dict): User provided metadata

        Returns:
            dict: The generated metadata
        """
        hardware_metadata = self._params.all()
        date = datetime.today()
        return {
            "file": {
                "name": name or self._make_measurement_name(hardware_metadata, date),
                "comment": comment,
                "date": str(date.isoformat()),
                "index_col": index_col,
            },
            "user": user_meta or {},
            "dev": {"id": self.id} | additional_meta | hardware_metadata,
        }

    @abstractmethod
    def get_measurement(self, name: str = None, comment: str = "", meta: dict = None) -> "Measurement":
        """Get the current data from the device without changing any settings

        Args:
            name (str, optional): Measurement Name. Defaults to automatic name from metadata.
            comment (str, optional): Comment to add to metadata. Defaults to "".
            meta (dict, optional): User metadata to store with the measurement. Defaults to None.

        Returns:
            Measurement: The current measurement data.
        """
        pass

    @abstractmethod
    def measure(
        self,
        *,
        name: str = None,
        comment: str = "",
        meta: dict = None,
        show_warnings: bool = True,
        no_defaults: bool = False,
        **kwargs,
    ) -> "Measurement":
        """Perform a measurement

        This will use the instance measurement defaults.
        Any parameters that is not set will use the current device settings.
        Parameters can be set to None to use the device settings.

        Args:
            name (str, optional): Measurement Name. Defaults to automatic name from metadata.
            comment (str, optional): Comment to add to metadata. Defaults to "".
            meta (dict, optional): User metadata to store with the measurement. Defaults to None.
            show_warnings (bool, optional): Show warnings for unspecified parameters. Defaults to True.
            no_defaults (bool, optional): Ignore default settings. Defaults to False.
            **kwargs: Device specific parameters to set for the measurement.

        Returns:
            Measurement: The data of the measurement that was performed.
        """
        pass


class Measurement:
    meta: dict
    df: pd.DataFrame
    attachments: dict[str, bytearray]

    def __init__(self, meta: dict, df: pd.DataFrame, attachments: dict[str, bytearray] = None) -> None:
        assert "file" in meta, "Metadata must contain a file section!"
        assert "name" in meta["file"], "Metadata must contain a name!"
        self.meta = meta
        self.df = df
        self.attachments = attachments or {}

    def __getattr__(self, name: str) -> Any:
        if name in self.meta:
            return self.meta[name]
        raise AttributeError(f"Measurement has no attribute {name}")

    def _make_filename(self, ext: str = "tsv") -> str:
        char_map = {"/": "_", "<": "", ">": "", ":": "-", '"': "'", "\\": "_", "|": "", "?": "", "*": "", " ": "_"}
        filename = f"{self.meta['file']['name']}.{ext}"
        for char, repl in char_map.items():
            filename = filename.replace(char, repl)
        return filename

    @staticmethod
    def _handle_overwrite(filename: Path, overwrite: bool, prompt: bool, no_raise: bool) -> bool:
        # returns wether to overwrite or not, or raises FileExistsError if no_raise is False
        if not filename.exists():
            return True
        if prompt:
            answer = input(f"File {filename} exists, overwrite? [y/N] ")
            return answer.lower() == "y"
        if overwrite:
            print(f"Warning: overwriting file {filename}!")
            return True
        if no_raise:
            print(f"Warning: File {filename} exists and will NOT be overwritten!")
            return False
        raise FileExistsError(f"File {filename} exists!")

    def _serialize_to(self, writable: TextIO, delim: str) -> None:
        self.meta["file"]["index_col"] = self.meta["file"].get("index_col", self.df.index.name)
        assert self.df.index.name == self.meta["file"]["index_col"], "Index column does not match!"
        data_copy = deepcopy(self.meta)
        data_copy["file"]["table_delim"] = delim
        pretty = yaml.dump(data_copy, sort_keys=False)
        for line in pretty.split("\n"):
            writable.write(f"# {line}\n")
        self.df.to_csv(writable, sep=delim, lineterminator="\n")

    def save(
        self,
        filename: Path = None,
        *,
        dir: Path = None,
        delim: str = "\t",
        attachment_warn: bool = True,
        overwrite: bool = False,
        prompt: bool = False,
    ) -> Path:
        """Save measurement to file

        Args:
            filename (Path, optional): Filename to save to. Defaults to automatic filename from measurement name.
            dir (Path, optional): Directory to save to. Defaults to working directory if no filename is specified.
            delim (str, optional): Delimiter to use. Defaults to "\\t".
            overwrite (bool, optional): Overwrite file if it exists. Defaults to False.
            prompt (bool, optional): Prompt before overwriting. Defaults to False.

        Returns:
            Path: The path to the file that was saved.
        """
        SUFFIX = ".csv"
        if filename is None:
            filename = self._make_filename(SUFFIX[1:])
            if dir is not None:
                filename = Path(dir) / filename
        filename = Path(filename)
        if not self._handle_overwrite(filename, overwrite, prompt, False):
            return filename
        assert filename.suffix == SUFFIX, f"Filename must end with {SUFFIX}!"
        with open(filename, "w") as f:
            self._serialize_to(f, delim)
        if self.attachments and attachment_warn:
            print(f"Warning: attachments {list(self.attachments.keys())} were not saved!")
        return filename

    def save_zip(
        self,
        filename: Path = None,
        *,
        dir: Path = None,
        delim: str = "\t",
        overwrite: bool = False,
        prompt: bool = False,
    ) -> Path:
        """Save measurement and attachments to zip file

        Args:
            filename (Path, optional): Filename to save to. Defaults to automatic filename from measurement name.
            dir (Path, optional): Directory to save to. Defaults to working directory if no filename is specified.
            delim (str, optional): Delimiter to use. Defaults to "\\t".
            overwrite (bool, optional): Overwrite file if it exists. Defaults to False.
            prompt (bool, optional): Prompt before overwriting. Defaults to False.

        Returns:
            Path: The path to the file that was saved.
        """
        SUFFIX = ".zip"
        if filename is None:
            filename = Path(self._make_filename(SUFFIX[1:]))
            if dir is not None:
                filename = Path(dir) / filename
        filename = Path(filename)
        if not self._handle_overwrite(filename, overwrite, prompt, False):
            return filename
        assert filename.suffix == SUFFIX, f"Filename must end with {SUFFIX}!"
        with ZipFile(filename, "w") as archive:
            with TextIOWrapper(archive.open(self._make_filename("tsv"), "w")) as f:
                self._serialize_to(f, delim)
            for name, attachment in self.attachments.items():
                with archive.open(name, "w") as f:
                    f.write(attachment)
        return filename

    @staticmethod
    def _dict_to_html(data: dict) -> str:
        return yaml.dump(data, indent=4, sort_keys=False).replace("\n", "<br>").replace(" ", "&nbsp;")

    def _repr_html_(self):
        return (
            self._dict_to_html(self.meta)
            + "<br>"
            + f"attachments = {list(self.attachments.keys())}"
            + "<br>"
            + self.df._repr_html_()
        )

    @staticmethod
    def _deserialize_from(readable: TextIO, delim: str) -> Self:
        raw_meta = ""
        readable.seek(0)
        for line in readable.readlines():
            if not line.startswith("#"):
                break
            raw_meta += line[1:]
        meta = yaml.safe_load(raw_meta)
        delim = delim or meta["file"].pop("table_delim", "\t")
        readable.seek(0)
        df = pd.read_csv(readable, sep=delim, comment="#", index_col=meta["file"].get("index_col", None))
        return Measurement(meta, df)

    @staticmethod
    def load(filename: Path, delim: str = None) -> "Measurement":
        """Load measurement from file

        Args:
            filename (Path): Filename to load from.
            delim (str, optional): Force a delimiter, otherwise the delimiter is read from the metadata or "\\t" if not present. Defaults to None.

        Returns:
            Measurement: The loaded measurement.
        """
        filename = Path(filename)
        if filename.suffix == ".zip":
            with ZipFile(filename, "r") as archive:
                with TextIOWrapper(archive.open(archive.namelist()[0], "r")) as f:
                    measurement = Measurement._deserialize_from(f, delim)
                for name in archive.namelist()[1:]:
                    with archive.open(name, "r") as f:
                        measurement.attachments[name] = bytearray(f.read())
            return measurement

        with open(filename) as f:
            return Measurement._deserialize_from(f, delim)

    def insert(self, other: Self, inplace: bool = False) -> Self:
        """Insert another measurement into this one

        Args:
            other (Measurement): The measurement to insert.
            inplace (bool, optional): Insert inplace. Defaults to False.

        Returns:
            Measurement: The combined measurement.
        """
        assert self.df.index.name == other.df.index.name, "Index column does not match!"
        assert self.df.columns.equals(other.df.columns), "Column names do not match!"

        insert_min, insert_max = other.df.index.min(), other.df.index.max()  # noqa: F841
        df = self.df.query("index < @insert_min or index > @insert_max")
        new_df = pd.concat([df, other.df]).sort_index()

        new_meta = deepcopy(self.meta)
        new_meta["inserts"] = self.meta.get("inserts", []) + [other.meta]

        if inplace:
            self.df = new_df
            self.meta = new_meta
            return self
        else:
            return Measurement(new_meta, new_df)

    @staticmethod
    def plot_multiple(
        measurements: list["Measurement"],
        log_x: bool = False,
        log_y: bool = False,
        colors: list[str] = DEFAULT_PLOTLY_COLORS,
        unwrap_phase: bool = False,
        height: int = None,
    ) -> go.Figure:
        """Plot multiple measurements

        Args:
            measurements (list[Measurement]): List of measurements to plot.
            colors (list[str], optional): List of colors to use, will repeat if not enough. Defaults to DEFAULT_PLOTLY_COLORS.
            log_x (bool, optional): Logarithmic scale for the x-axis. Defaults to False.
            log_y (bool, optional): Logarithmic scale for the y-axis. Defaults to False.
            unwrap_phase (bool, optional): Unwrap phase data for columns containing "phase". Defaults to False.

        Returns:
            go.Figure: The plotly figure.
        """
        fig = make_subplots(rows=len(list(measurements[0].df.columns)), shared_xaxes=True)
        for i, (meas, color) in enumerate(zip(measurements, cycle(colors))):
            meas._add_to_fig(fig, color, log_x=log_x, log_y=log_y, legend_group=i, unwrap_phase=unwrap_phase)
        fig.update_layout(height=height)

        return fig

    def _add_to_fig(
        self,
        fig: go.Figure,
        color: str = None,
        legend: bool = True,
        log_x: bool = False,
        log_y: bool = False,
        legend_group: int = 0,
        unwrap_phase: bool = False,
    ) -> None:
        for i, col in enumerate(self.df.columns):
            y_data = self.df[col]
            if unwrap_phase and "phase" in col.lower():
                y_data = np.unwrap(y_data, discont=180, period=360)
            row_col = dict(row=i + 1, col=1)
            fig.add_trace(
                go.Scatter(
                    x=self.df.index,
                    y=y_data,
                    line=dict(color=color),
                    name=self.meta["file"]["name"],
                    showlegend=legend and i == 0,
                    legendgroup=legend_group,
                ),
                **row_col,
            )
            fig["layout"][f"yaxis{i+1}"]["title"] = col
            fig.update_xaxes(type="log" if log_x else "linear", **row_col)
            fig.update_yaxes(type="log" if log_y else "linear", **row_col)

        fig["layout"][f"xaxis{len(self.df.columns)}"]["title"] = self.df.index.name

    def plot(
        self, log_x: bool = False, log_y: bool = False, unwrap_phase: bool = False, height: int = None
    ) -> go.Figure:
        """Plot the measurement

        Args:
            log_x (bool, optional): Logarithmic scale for the x-axis. Defaults to False.
            log_y (bool, optional): Logarithmic scale for the y-axis. Defaults to False.
            unwrap_phase (bool, optional): Unwrap phase data for columns containing "phase". Defaults to False.

        Returns:
            go.Figure: The plotly figure.
        """
        fig = make_subplots(rows=len(self.df.columns), shared_xaxes=True)
        self._add_to_fig(fig, legend=False, log_x=log_x, log_y=log_y, unwrap_phase=unwrap_phase)
        fig["layout"]["title"]["text"] = self.meta["file"]["name"]
        fig.update_layout(height=height)
        return fig

    def query(self, query: str) -> Self:
        """Execute a query on the internal DataFrame

        Args:
            query (str): The query to execute.

        Returns:
            Measurement: A new measurement with the result of the query.
        """
        new_df = self.df.query(query, level=1)
        return Measurement(deepcopy(self.meta), new_df)


class ParamProxy:
    """Proxy for device parameters

    This class is used to get and set parameters on a device.
    It is used to map the device specific commands to a more user friendly interface.
    """

    @dataclass
    class Constant:
        value: Any

    no_op = lambda x: x
    read_only = lambda x: x
    assert no_op != read_only, "Functions must be unique!"
    decode_bool = lambda x: bool(int(x))
    float_as_int = lambda x: int(float(x))

    class ParameterMapping(ABC):
        @abstractmethod
        def encode(self, value: Any) -> str:
            pass

        @abstractmethod
        def decode(self, value: str) -> Any:
            pass

        @property
        def de_en_code(self) -> tuple[Callable[[Any], str], Callable[[str], Any]]:
            return self.decode, self.encode

    class Placeholder:
        pass

    class CodeMap(ParameterMapping):
        # bidirectional map, key is name and value is code
        def __init__(self, mapping: dict[Any, str]) -> None:
            self._mapping = mapping
            self._inverse = {v: k for k, v in mapping.items()}
            assert len(self._mapping) == len(self._inverse), "Mapping is not invertible!"

        def encode(self, name: Any) -> str:
            if name not in self._mapping:
                raise ValueError(f"Name {name} not in mapping {self._mapping.keys()}!")
            return self._mapping[name]

        def decode(self, code: str) -> Any:
            return self._inverse[code]

    class ValSet(ParameterMapping):
        def __init__(self, values: set[Any]) -> None:
            self._values = values
            types = list(map(type, values))
            self._type = types[0]
            assert all(t == self._type for t in types), "Values must be of the same type!"

        def encode(self, value: Any) -> str:
            assert value in self._values, f"Value {value} not in set {self._values}!"
            return str(value)

        def decode(self, value: str) -> Any:
            return self._type(value)

    class TruncatedCachedString(ParameterMapping):
        def __init__(self, length: int) -> None:
            self._length = length
            self._value = ""

        def encode(self, value: str) -> str:
            self._value = value
            return f'"{value[: self._length]}"'

        def decode(self, value: str) -> str:
            cleaned_value = value[1:-1].lower()
            if self._value.lower().startswith(cleaned_value):
                return self._value  # the stored string is most likely the same as the device string
            else:
                return cleaned_value  # if not we return the device string

    @staticmethod
    def recursive_merge(d1: dict, d2: dict) -> dict:
        res = deepcopy(d1)
        for k, v in d2.items():
            if isinstance(v, dict):
                res[k] = ParamProxy.recursive_merge(res.get(k, {}), v)
            else:
                res[k] = v
        return res

    @staticmethod
    def sort_params(params: dict | Any, reference: dict | Any) -> dict:
        # sort parameters according to a reference dict
        return {key: params[key] for key in reference if key in params}

    def __init__(self, res: MessageBasedResource, param_map: dict, **default_format_args) -> None:
        self.res = res
        self.param_map = param_map
        self.default_format_args = default_format_args

    def get(self, name: str | tuple[str, ...], **format_args) -> Any:
        """Get a parameter value

        Args:
            name (str | tuple[str, ...]): The name of the parameter to get or a tuple of names to describe the nested path.
            **format_args (dict): Arguments to format command with.

        Returns:
            Any: The value of the parameter. If there are multiple commands, only the first is returned.

        """
        long_name = name if isinstance(name, tuple) else (name,)
        param_info = self.param_map
        # traverse the parameter map to find the command
        for sub_name in long_name:
            assert sub_name in param_info, f"Unknown parameter {name}!"
            param_info = param_info[sub_name]

        if isinstance(param_info, self.Constant):
            return param_info.value
        elif isinstance(param_info, dict):
            return {sub_name: self.get((*long_name, sub_name), **format_args) for sub_name in param_info}
        else:
            command, from_device, _ = param_info
            if isinstance(command, list):
                command = command[0]
            return from_device(self.res.query(command.format(Q="?", **(self.default_format_args | format_args))))

    def set(self, name: str | tuple[str, ...], value: Any, **format_args) -> None:
        """Set a parameter value

        If there multiple commands for a parameter, all are set.

        Args:
            name (str | tuple[str, ...]): The name of the parameter to set or a tuple of names to describe the nested path.
            value (Any): The value to set the parameter to.
            **format_args (dict): Arguments to format command with.
        """
        long_name = name if isinstance(name, tuple) else (name,)
        param_info = self.param_map
        # traverse the parameter map to find the command
        for sub_name in long_name:
            assert sub_name in param_info, f"Unknown parameter {name}!"
            param_info = param_info[sub_name]

        if isinstance(param_info, self.Constant):
            raise ValueError(f"Parameter {name} is a constant and cannot be set!")
        elif isinstance(param_info, dict):
            # sort params, this is important because some parameters require others to be set first
            value = self.sort_params(value, param_info)
            for sub_name, sub_value in value.items():
                self.set((*long_name, sub_name), sub_value, **format_args)
        else:
            command, _, to_device = param_info
            if to_device == self.read_only:
                return
            kwargs = self.default_format_args | format_args
            if isinstance(command, list):
                for c in command:
                    self.res.write(c.format(Q="", **kwargs) + f" {to_device(value)}")
            else:
                self.res.write(command.format(Q="", **kwargs) + f" {to_device(value)}")

    def update(self, new_params: dict, **format_args) -> None:
        """Update multiple parameters

        Args:
            new_params (dict): The parameters to update.
            **format_args (dict): Arguments to format command with.
        """
        self.set((), new_params, **format_args)

    def __iter__(self):
        return self.param_map.keys().__iter__()

    def all(self, **format_args) -> dict:
        return self.get((), **format_args)
