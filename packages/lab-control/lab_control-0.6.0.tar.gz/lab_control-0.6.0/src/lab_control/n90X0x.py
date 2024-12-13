from .common import Device, ParamProxy, Measurement
import pandas as pd
from datetime import datetime


class N90X0X(Device):
    """Keysight N90X0X Signal Analyzer

    **Device Specific Functions**:
    - [`get_traces()`](#get_traces)
    """

    _unit_map = ParamProxy.CodeMap(
        {
            "dBm": "DBM",
            "dBmV": "DBMV",
            "dBmA": "DBMA",
            "V": "V",
            "W": "W",
            "A": "A",
            "dBuV": "DBUV",
            "dBuA": "DBUA",
            "dBpW": "DBPW",
            "dBuV/m": "DBUVM",
            "dBuA/m": "DBUAM",
            "dBpT": "DBPT",
            "dBG": "DBG",
        }
    )

    _meas_map = ParamProxy.CodeMap({"spectrum": "SAN"})
    _preamp_band_map = ParamProxy.CodeMap({"low": "LOW", "full": "FULL"})

    _param_map = {
        # (internal name, command, from device, to device)
        "meas": ("CONF{Q}", _meas_map.decode, ParamProxy.read_only),
        "start_Hz": ("FREQ:START{Q}", float, ParamProxy.no_op),
        "stop_Hz": ("FREQ:STOP{Q}", float, ParamProxy.no_op),
        "rbw_Hz": ("BAND{Q}", float, ParamProxy.no_op),
        "rbw_auto": ("BAND:AUTO{Q}", ParamProxy.decode_bool, int),
        "vbw_Hz": ("BAND:VID{Q}", float, ParamProxy.no_op),
        "vbw_auto": ("BAND:VID:AUTO{Q}", ParamProxy.decode_bool, int),
        "sweep_time_s": ("SWE:TIME{Q}", float, ParamProxy.no_op),
        "sweep_time_auto": ("SWE:TIME:AUTO{Q}", ParamProxy.decode_bool, int),
        "sweep_points": ("SWE:POINTS{Q}", int, ParamProxy.no_op),
        "att_dB": ("POW:ATT{Q}", float, ParamProxy.no_op),
        "att_auto": ("POW:ATT:AUTO{Q}", ParamProxy.decode_bool, int),
        "preamp": ("POW:GAIN{Q}", ParamProxy.decode_bool, int),
        "preamp_band": ("POW:GAIN:BAND{Q}", *_preamp_band_map.de_en_code),
        "input_coupling": ("INP:COUP{Q}", str, ParamProxy.no_op),  # AC, DC
        "y_unit": ("UNIT:POW{Q}", *_unit_map.de_en_code),
    }

    _default_defaults = {"meas": "spectrum"}  # TODO add more defaults

    _trace_type_map = ParamProxy.CodeMap(
        {
            "write": "WRIT",
            "average": "AVER",
            "max_hold": "MAX",
            "min_hold": "MIN",
        }
    )

    _trace_param_map = {
        "type": ("TRACE{trace}:TYPE{Q}", *_trace_type_map.de_en_code),
        "update": ("TRACE{trace}:UPDATE{Q}", ParamProxy.decode_bool, int),
        "display": ("TRACE{trace}:DISP{Q}", ParamProxy.decode_bool, int),
    }

    def __init__(self, address: str, *, defaults: dict = None) -> None:
        """N90X0X (N9010B, N9020A, ...)

        Args:
            address (str): Visa address of device.
            defaults (dict, optional): Default measurement settings on top of class defaults. Defaults to None.
        """

        super().__init__(address, defaults=defaults)
        self._trace_params = ParamProxy(self._res, param_map=self._trace_param_map)

    def _make_measurement_name(self, parameters: dict, date: datetime) -> str:
        return f"{parameters['meas']}_{parameters['start_Hz']}_{parameters['stop_Hz']}_{date:%Y-%m-%dT%H:%M:%S}"

    def get_measurement(self, *, name: str = None, comment: str = "", meta: dict = None, trace: int = 1) -> Measurement:
        """Get the current data from the device without changing any settings

        Args:
            name (str, optional): Measurement Name. Defaults to automatic name from metadata.
            comment (str, optional): Comment to add to metadata. Defaults to "".
            meta (dict, optional): User metadata to store with the measurement. Defaults to None.
            trace (int, optional): The trace to get data from. Defaults to 1.

        Returns:
            Measurement: The current measurement data.
        """
        with self._temporary_timeout(None):
            # wait until the current measurement is done
            raw_data = self._res.query_ascii_values(f"FETCH:SAN{trace}?")
        frequencies = raw_data[::2]
        y_data = raw_data[1::2]

        df = pd.DataFrame(
            {
                "freq_Hz": frequencies,
                f"spectrum_{self._params.get('y_unit')}": y_data,
            },
        )
        df.set_index("freq_Hz", inplace=True)

        metadata = self._make_metadata(
            name, comment, "freq_Hz", {f"trace_{trace}": self._trace_params.all(trace=trace)}, meta
        )
        assert (
            metadata["dev"]["meas"] == self._default_defaults["meas"]
        ), f"Unexpected device state, should be {self._default_defaults['meas']} measurement."

        return Measurement(metadata, df)

    def measure(
        self,
        *,
        name: str = None,
        comment: str = "",
        meta: dict = None,
        show_warnings: bool = True,
        no_defaults: bool = False,
        trace: int = 1,
        **kwargs,
    ) -> Measurement:
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
            meas (str, optional): Measurement type, always "spectrum". Passed in **kwargs.
            trace (int, optional): The trace to measure on. Defaults to 1.
            start_Hz (float, optional): Start frequency in Hz. Passed in **kwargs.
            stop_Hz (float, optional): Stop frequency in Hz. Passed in **kwargs.
            rbw_Hz (float, optional): Resolution bandwidth in Hz. Passed in **kwargs.
            rbw_auto (bool, optional): Automatic resolution bandwidth. Passed in **kwargs.
            vbw_Hz (float, optional): Video bandwidth in Hz. Passed in **kwargs.
            vbw_auto (bool, optional): Automatic video bandwidth. Passed in **kwargs.
            sweep_time_s (float, optional): Sweep time in seconds. Passed in **kwargs.
            sweep_time_auto (bool, optional): Automatic sweep time. Passed in **kwargs.
            sweep_points (int, optional): Number of sweep points. Passed in **kwargs.
            att_dB (float, optional): Attenuation in dB. Passed in **kwargs.
            att_auto (bool, optional): Automatic attenuation. Passed in **kwargs.
            preamp (bool, optional): Preamp on/off. Passed in **kwargs.
            preamp_band (str, optional): Preamp band, one of ["low", "full"]. Passed in **kwargs.
            input_coupling (str, optional): Input coupling, one of ["AC", "DC"]. Passed in **kwargs.
            y_unit (str, optional): Unit of the y axis, one of ["dBm", "dBmV", "dBmA", "V", "W", "A", "dBuV", "dBuA", "dBpW", "dBuV/m", "dBuA/m", "dBpT", "dBG"]. Passed in **kwargs.

        Returns:
            Measurement: The data of the measurement that was performed.
        """

        params = self._parse_kwargs(kwargs, no_defaults)

        self._res.write(":INIT:CONT OFF")  # disable continuous sweep while interacting with device
        old_type = self._trace_params.get("type", trace=trace)
        self._trace_params.set("type", "write", trace=trace)

        self._set_params(params, show_warnings)

        self._res.write(":INIT:SAN")
        measurement = self.get_measurement(name=name, comment=comment, meta=meta, trace=trace)

        self._trace_params.set("type", old_type, trace=trace)
        self._res.write(":INIT:CONT ON")  # re-enable continuous sweep

        return measurement

    def get_traces(
        self,
        traces: list[int] = [1, 2, 3, 4, 5, 6],  # noqa: B006
        name: str = None,
        comment: str = "",
        meta: dict = None,
        only_visible: bool = True,
    ) -> Measurement:
        """Fetch multiple traces from the device

        Args:
            traces (list[int], optional): The trace numbers to fetch. Defaults to [1, 2, 3, 4, 5, 6].
            name (str, optional): Measurement Name. Defaults to automatic name from metadata.
            comment (str, optional): Comment to add to metadata. Defaults to "".
            meta (dict, optional): User metadata to store with the measurement. Defaults to None.
            only_visible (bool, optional): Only fetch visible traces. Defaults to True.

        Returns:
            Measurement: A Measurement with the selected traces as columns.
        """

        cols = {}
        trace_info = {}
        for trace in traces:
            trace_meta = self._trace_params.all(trace=trace)
            if not trace_meta["display"] and only_visible:
                continue
            with self._temporary_timeout(None):
                raw_data = self._res.query_ascii_values(f"FETCH:SAN{trace}?")
            cols["freq_Hz"] = raw_data[::2]
            cols[f"trace_{trace}_{self._params.get('y_unit')}"] = raw_data[1::2]
            trace_info[f"trace_{trace}"] = self._trace_params.all(trace=trace)

        df = pd.DataFrame(cols)
        df.set_index("freq_Hz", inplace=True)

        metadata = self._make_metadata(name, comment, "freq_Hz", trace_info, meta)
        assert (
            metadata["dev"]["meas"] == self._default_defaults["meas"]
        ), f"Unexpected device state, should be {self._default_defaults['meas']} measurement."

        return Measurement(metadata, df)
