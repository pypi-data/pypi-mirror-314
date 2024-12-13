import datetime
from typing import Literal
import pandas as pd

from .common import Measurement, ParamProxy, Device


class E5061B(Device):
    """Keysight E5061B Network Analyzer"""

    _meas_set = ParamProxy.ValSet({"S11", "S12", "S21", "S22", "T", "R", "TR"})
    _sweep_type_map = ParamProxy.CodeMap(
        {
            "linear": "LIN",
            "log": "LOG",
            "segment": "SEGM",
            "power": "POW",
            "bias": "BIAS",
        }
    )

    _param_map = {
        # (internal name, command, from device, to device)
        "meas": (["CALC{channel}:PAR1:DEF{Q}", "CALC{channel}:PAR2:DEF{Q}"], *_meas_set.de_en_code),
        "start_Hz": ("SENS{channel}:FREQ:START{Q}", float, ParamProxy.no_op),
        "stop_Hz": ("SENS{channel}:FREQ:STOP{Q}", float, ParamProxy.no_op),
        "source_power_dBm": ("SOUR{channel}:POW:GPP{Q}", float, ParamProxy.no_op),
        "sweep_points": ("SENS{channel}:SWE:POINTS{Q}", int, ParamProxy.no_op),
        "sweep_type": ("SENS{channel}:SWE:TYPE{Q}", *_sweep_type_map.de_en_code),
        "ifbw_Hz": ("SENS{channel}:BAND{Q}", float, ParamProxy.no_op),
        "average": ("SENS{channel}:AVER{Q}", ParamProxy.decode_bool, int),
        "average_count": ("SENS{channel}:AVER:COUNT{Q}", int, ParamProxy.no_op),
    }
    _default_defaults = {}

    def __init__(self, address: str, *, defaults: dict = None, channel: int = 1) -> None:
        """E5061B

        Args:
            address (str): Visa address of device.
            channel (int, optional): Network analyzer channel to Use. Defaults to 1.
            defaults (dict, optional): Default measurement settings on top of class defaults. Defaults to None.
        """
        super().__init__(address, defaults=defaults)
        self._channel = channel
        self._params.default_format_args.update(channel=channel)

    def _make_measurement_name(self, parameters: dict, date: datetime.datetime) -> str:
        return f"{parameters['meas']}_{parameters['start_Hz']}_{parameters['stop_Hz']}_{date:%Y-%m-%dT%H:%M:%S}"

    def _init_param_format(
        self,
        param: int,
        format: Literal["MLOG", "PHASE", "MLIN", "SWR", "REAL", "IMAG", "SLOG"],  # TODO add more
    ):
        self._res.write(f"CALC{self._channel}:PAR{param}:SEL")
        self._res.write(f"CALC{self._channel}:FORM {format}")
        self._res.write(f":DISP:WIND{self._channel}:SPL D1_2")

    def _trigger_and_wait(self):
        self._res.write(f":STAT:OPER:PTR {0}")
        self._res.write(f":STAT:OPER:NTR {0x10}")
        self._res.write(f":STAT:OPER:ENAB {0x10}")
        self._res.write(f"*SRE {0x80}")
        self._res.write("*CLS")
        self._res.write("TRIG:SING")
        with self._temporary_timeout(None):
            complete = int(self._res.query("*OPC?"))
        assert complete, "Measurement did not finish!"

    def get_measurement(self, name: str = None, comment: str = "", meta: dict = None) -> Measurement:
        """Get the current data from the device without changing any settings

        Args:
            name (str, optional): Measurement Name. Defaults to automatic name from metadata.
            comment (str, optional): Comment to add to metadata. Defaults to "".
            meta (dict, optional): User metadata to store with the measurement. Defaults to None.

        Returns:
            Measurement: The current measurement data.
        """
        frequencies = self._res.query_ascii_values("SENS1:FREQ:DATA?")

        self._res.write(f"CALC{self._channel}:PAR{1}:SEL")
        magnitudes = self._res.query_ascii_values(f"CALC{self._channel}:DATA:FDAT?")[::2]

        self._res.write(f"CALC{self._channel}:PAR{2}:SEL")
        phases = self._res.query_ascii_values(f"CALC{self._channel}:DATA:FDAT?")[::2]

        # TODO make sure that refactor works, and automatically detect unit, or assert, that it is in dB and degrees
        df = pd.DataFrame(
            {
                "freq_Hz": frequencies,
                "mag_dB": magnitudes,
                "phase_deg": phases,
            },
        )
        df.set_index("freq_Hz", inplace=True)

        metadata = self._make_metadata(name, comment, "freq_Hz", {}, meta)

        return Measurement(metadata, df)

    def measure(
        self,
        *,
        name: str = None,
        comment: str = "",
        meta: dict = None,
        show_warnings: bool = True,
        no_defaults: bool = False,
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
            meas (str, optional): Measurement type, one of ["S11", "S12", "S21", "S22", "T", "R", "TR"]. Passed in **kwargs.
            start_Hz (float, optional): Start frequency in Hz. Passed in **kwargs.
            stop_Hz (float, optional): Stop frequency in Hz. Passed in **kwargs.
            source_power_dBm (float, optional): Source power in dBm. Passed in **kwargs.
            sweep_points (int, optional): Number of sweep points. Passed in **kwargs.
            sweep_type (str, optional): Sweep type, one of ["linear", "log", "segment", "power", "bias"]. Passed in **kwargs.
            ifbw_Hz (float, optional): IF bandwidth in Hz. Passed in **kwargs.
            average (bool, optional): Enable averaging. Passed in **kwargs.
            average_count (int, optional): Number of samples to average over. Passed in **kwargs.


        Returns:
            Measurement: The data of the measurement that was performed.
        """

        params = self._parse_kwargs(kwargs, no_defaults)

        # trigger over USB
        self._res.write(":TRIG:SOUR BUS")
        if params.get("average", False):
            old_trigger_avg = self._res.query(":TRIG:AVER?")
            self._res.write(":TRIG:AVER ON")

        self._res.write(f"CALC{self._channel}:PAR:COUNT 2")
        self._init_param_format(1, "MLOG")
        self._init_param_format(2, "PHASE")

        self._set_params(params, show_warnings, channel=self._channel)

        self._trigger_and_wait()

        if params.get("average", False):
            self._res.write(f":TRIG:AVER {old_trigger_avg}")
        measurement = self.get_measurement(name=name, comment=comment, meta=meta)

        self._res.write(":TRIG:SOUR INT")  # go back to internal trigger (continuous measurement)

        return measurement
