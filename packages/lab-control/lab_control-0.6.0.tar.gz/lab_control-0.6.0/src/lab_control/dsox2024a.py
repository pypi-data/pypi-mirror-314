from .common import Device, Measurement, ParamProxy
from collections import namedtuple
import numpy as np
import pandas as pd
from pathlib import Path
from IPython.display import Image


class DSOX2024A(Device):
    """Keysight DSOX2024A Oscilloscope to measure time series data.

    **Device Specific Functions**:
    - [`make_scalar_measurement()`](#make_scalar_measurement)
    - [`set_auto_trigger()`](#set_auto_trigger)
    - [`save_screenshot()`](#save_screenshot)
    - [`screenshot()`](#screenshot)
    - [`save_settings()`](#save_settings)
    """

    NUM_CHANNELS = 4

    _time_ref_map = ParamProxy.CodeMap({"left": "LEFT", "center": "CENT", "right": "RIGH"})
    _acquire_type_map = ParamProxy.CodeMap({"normal": "NORM", "average": "AVER", "peak": "PEAK", "high_res": "HRES"})
    _trigger_mode_map = ParamProxy.CodeMap(
        {
            "edge": "EDGE",
            "glitch": "GLIT",
            "pattern": "PATT",
            "tv": "TV",
            "delay": "DEL",
            "edge_burst": "EBUR",
            # TODO what are the important ones?
        }
    )

    @staticmethod
    def _make_channel_maps(NUM_CHANNELS: int = NUM_CHANNELS) -> dict:
        _unit_map = ParamProxy.CodeMap({"V": "VOLT", "A": "AMP"})
        _coupling_set = ParamProxy.ValSet({"AC", "DC"})
        return {
            f"channel_{channel}": {
                "label": (f"CHAN{channel}:LAB{{Q}}", *ParamProxy.TruncatedCachedString(length=10).de_en_code),
                "range_V": (f"CHAN{channel}:RANG{{Q}}", float, ParamProxy.no_op),
                "offset_V": (f"CHAN{channel}:OFFS{{Q}}", float, ParamProxy.no_op),
                "invert": (f"CHAN{channel}:INV{{Q}}", ParamProxy.decode_bool, int),
                "unit": (f"CHAN{channel}:UNIT{{Q}}", *_unit_map.de_en_code),
                "bandwidth_limit": (f"CHAN{channel}:BWL{{Q}}", ParamProxy.decode_bool, int),
                "bandwidth_Hz": (f"CHAN{channel}:BAND{{Q}}", float, ParamProxy.no_op),
                "coupling": (f"CHAN{channel}:COUP{{Q}}", *_coupling_set.de_en_code),
                "display": (f"CHAN{channel}:DISP{{Q}}", ParamProxy.decode_bool, int),
                "trig_level_low": (f"TRIG:LEVel:LOW{{Q}} CHAN{channel}", float, ParamProxy.no_op),
                "trig_level_high": (f"TRIG:LEVel:HIGH{{Q}} CHAN{channel}", float, ParamProxy.no_op),
                "probe_att": (f"CHAN{channel}:PROBE{{Q}}", float, ParamProxy.no_op),
            }
            for channel in range(1, NUM_CHANNELS + 1)
        }

    _param_map = {
        "meas": ParamProxy.Constant("time_series"),
        "time_range_s": ("TIM:RANGE{Q}", float, ParamProxy.no_op),  # TODO what about time base window range?
        "time_offset_s": ("TIM:DELAY{Q}", float, ParamProxy.no_op),
        "time_ref": ("TIM:REF{Q}", *_time_ref_map.de_en_code),
        "time_points": ("WAVeform:POINts{Q}", int, ParamProxy.no_op),  # TODO can also be "max"
        "acquire_type": ("ACQ:TYPE{Q}", *_acquire_type_map.de_en_code),
        "average_count": ("ACQ:COUNt{Q}", int, ParamProxy.no_op),
        "trig_hf_reject": ("TRIG:HFReject{Q}", ParamProxy.decode_bool, int),
        "trig_holdoff": ("TRIG:HOLDoff{Q}", float, ParamProxy.no_op),
        "trig_noise_reject": ("TRIG:NREJect{Q}", ParamProxy.decode_bool, int),  # TODO important?
        # sadly this additional function ist necessary, because fo the weird scoping of dict comprehensions in class definitions
        # **_make_channel_maps(NUM_CHANNELS),
        **_make_channel_maps(),
    }

    _default_defaults = {}

    _measure_map = {
        "duty_cycle": ("MEASure:DUTYcycle{Q} CHAN{channel}", float, ParamProxy.read_only),
        "fall_time_s": ("MEASure:FALLtime{Q} CHAN{channel}", float, ParamProxy.read_only),
        "frequency_Hz": ("MEASure:FREQuency{Q} CHAN{channel}", float, ParamProxy.read_only),
        "duty_cycle_neg": ("MEASure:NDUTy{Q} CHAN{channel}", float, ParamProxy.read_only),
        "neg_edge_count": ("MEASure:NEDGes{Q} CHAN{channel}", ParamProxy.float_as_int, ParamProxy.read_only),
        "neg_pulse_count": ("MEASure:NPULses{Q} CHAN{channel}", ParamProxy.float_as_int, ParamProxy.read_only),
        "neg_pulse_width_s": ("MEASure:NWIDth{Q} CHAN{channel}", float, ParamProxy.read_only),
        "pos_edge_count": ("MEASure:PEDGes{Q} CHAN{channel}", ParamProxy.float_as_int, ParamProxy.read_only),
        "pos_pulse_count": ("MEASure:PPULses{Q} CHAN{channel}", ParamProxy.float_as_int, ParamProxy.read_only),
        "pos_pulse_width_s": ("MEASure:PWIDth{Q} CHAN{channel}", float, ParamProxy.read_only),
        "overshoot_pc": ("MEASure:OVERshoot{Q} CHAN{channel}", float, ParamProxy.read_only),
        "preshoot_pc": ("MEASure:PREShoot{Q} CHAN{channel}", float, ParamProxy.read_only),
        "period_s": ("MEASure:PERiod{Q} CHAN{channel}", float, ParamProxy.read_only),
        "phase_deg": ("MEASure:PHASe{Q} CHAN{channel}, CHAN{channel_2}", float, ParamProxy.read_only),
        "delay_s": ("MEASure:DELay{Q} CHAN{channel}, CHAN{channel_2}", float, ParamProxy.read_only),
        "rise_time_s": ("MEASure:RISEtime{Q} CHAN{channel}", float, ParamProxy.read_only),
        "amplitude_V": ("MEASure:VAMPlitude{Q} CHAN{channel}", float, ParamProxy.read_only),
        "average_V": ("MEASure:VAVerage{Q} CHAN{channel}", float, ParamProxy.read_only),
        "base_V": ("MEASure:VBASe{Q} CHAN{channel}", float, ParamProxy.read_only),
        "top_V": ("MEASure:VTOP{Q} CHAN{channel}", float, ParamProxy.read_only),
        "max_V": ("MEASure:VMAX{Q} CHAN{channel}", float, ParamProxy.read_only),
        "min_V": ("MEASure:VMIN{Q} CHAN{channel}", float, ParamProxy.read_only),
        "peak_to_peak_V": ("MEASure:VPP{Q} CHAN{channel}", float, ParamProxy.read_only),
        "t_of_max_s": ("MEASure:XMAX{Q} CHAN{channel}", float, ParamProxy.read_only),
        "t_of_min_s": ("MEASure:XMIN{Q} CHAN{channel}", float, ParamProxy.read_only),
        "ac_rms_cycle_V": ("MEASure:VRMS{Q} CYCL, AC, CHAN{channel}", float, ParamProxy.read_only),
        "ac_rms_display_V": ("MEASure:VRMS{Q} DISP, AC, CHAN{channel}", float, ParamProxy.read_only),
        "dc_rms_cycle_V": ("MEASure:VRMS{Q} CYCL, DC, CHAN{channel}", float, ParamProxy.read_only),
        "dc_rms_display_V": ("MEASure:VRMS{Q} DISP, DC, CHAN{channel}", float, ParamProxy.read_only),
    }

    def __init__(self, address: str, *, defaults: dict = None) -> None:
        """DSOX2024A

        Args:
            address (str): Visa address of device.
            defaults (dict, optional): Default measurement settings on top of class defaults. Defaults to None.
        """
        super().__init__(address, defaults=defaults)
        self._measurements = ParamProxy(self._res, self._measure_map)

    def _query_ascii_over_binary(self, cmd: str, dtype: type) -> list:
        raw_data = self._res.query_binary_values(cmd, datatype="s", container=bytearray)
        return [dtype(elem) for elem in raw_data.decode().split(",")]

    def _set_channel(self, channel: int) -> None:
        self._res.write(f":WAVeform:SOURce CHAN{channel}")

    Preamble = namedtuple("Preamble", "format, type, points, count, x_inc, x_orig, x_ref, y_inc, y_orig, y_ref")

    def _get_preamble(self, channel: int) -> Preamble:
        self._set_channel(channel)
        fields = self._res.query(":WAVeform:PREamble?").split(",")
        return self.Preamble(
            {0: "BYTE", 1: "WORD", 4: "ASC"}[int(fields[0])],
            {0: "NORMAL", 1: "PEAK", 2: "AVERAGE", 3: "HIGH RESOLUTION"}[int(fields[1])],
            *map(int, fields[2:4]),
            *map(float, fields[4:]),
        )

    def _trigger(self) -> None:
        self._res.write(":TRIG:FORCe")

    ChannelData = namedtuple("ChannelData", ["meta", "x_data", "y_data"])

    def _get_channel_data(self, channel: int, binary: bool = True) -> ChannelData:
        preamble = self._get_preamble(channel)
        self._set_channel(channel)  # technically not necessary, since its done in _get_preamble
        if binary:
            self._res.write(":WAVeform:FORMat WORD")
            is_big_endian = self._res.query(":WAVeform:BYTeorder?") == "MSBF"
            is_unsigned = ParamProxy.decode_bool(self._res.query(":WAVeform:UNSigned?"))
            y_data_raw = self._res.query_binary_values(
                ":WAVeform:DATA?",
                datatype=("H" if is_unsigned else "h"),
                is_big_endian=is_big_endian,
                container=np.array,
            )
            y_data = (y_data_raw - preamble.y_ref) * preamble.y_inc + preamble.y_orig
        else:
            self._res.write(":WAVeform:FORMat ASCII")
            y_data = self._query_ascii_over_binary(":WAVeform:DATA?", float)
        assert len(y_data) == preamble.points
        x_data = np.arange(preamble.points) * preamble.x_inc + preamble.x_orig
        return self.ChannelData(preamble._asdict(), x_data, y_data)

    def get_measurement(
        self, name: str = None, comment: str = "", meta: dict = None, screenshot: bool = False, settings: bool = False
    ) -> Measurement:
        """Get the current data from the device without changing any settings

        Args:
            name (str, optional): Measurement Name. Defaults to automatic name from metadata.
            comment (str, optional): Comment to add to metadata. Defaults to "".
            meta (dict, optional): User metadata to store with the measurement. Defaults to None.
            screenshot (bool, optional): If True, a screenshot of the device screen is saved with the measurement. Defaults to False.
            settings (bool, optional): If True, the current settings are saved with the measurement. Defaults to False.

        Returns:
            Measurement: The current measurement data.
        """

        cols = {}
        x_name = "time_s"
        for i in range(1, self.NUM_CHANNELS + 1):
            channel_name = f"channel_{i}"
            if not self._params.get((channel_name, "display")):
                continue
            data = self._get_channel_data(i)
            if x_name in cols:
                assert np.allclose(cols[x_name], data.x_data), "x data is not the same for all channels!"
            else:
                cols[x_name] = data.x_data
            cols[f"channel_{i}_{self._params.get((channel_name, 'unit'))}"] = data.y_data

        df = pd.DataFrame(cols)
        df.set_index(x_name, inplace=True)

        metadata = self._make_metadata(name, comment, x_name, {}, meta)

        attachments = {}

        if screenshot:
            attachments["screenshot.png"] = self._screenshot_data()
        if settings:
            attachments["settings.xml"] = self._settings_data()

        return Measurement(metadata, df, attachments)

    def measure(
        self,
        *,
        name: str = None,
        comment: str = "",
        meta: dict = None,
        show_warnings: bool = True,
        no_defaults: bool = False,
        screenshot: bool = False,
        settings: bool = False,
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
            screenshot (bool, optional): If True, a screenshot of the device screen is saved with the measurement. Defaults to False.
            settings (bool, optional): If True, the current settings are saved with the measurement. Defaults to False.
            time_range_s (float, optional): The time range of the measurement window in seconds. Passed in **kwargs.
            time_offset_s (float, optional): The time offset of the measurement window in seconds. Passed in **kwargs.
            time_ref (Literal["left", "center", "right"], optional): The reference point of the time axis. Passed in **kwargs.
            time_points (int | str, optional): The number of time points in the measurement window, can also be "MAX". The actual amount of points may be slightly less depending and the time range. Passed in **kwargs.
            acquire_type (Literal["normal", "average", "peak", "high_res"], optional): The acquisition type. Passed in **kwargs.
            average_count (int, optional): The number of averages. Passed in **kwargs.
            trig_hf_reject (bool, optional): Enable high frequency reject. Passed in **kwargs.
            trig_holdoff (float, optional): The trigger holdoff in seconds. Passed in **kwargs.
            trig_noise_reject (bool, optional): Enable noise reject. Passed in **kwargs.
            channel_1 (dict, optional): Channel 1 settings. Passed in **kwargs.
                - `label` _str, optional_ - Channel label, only the first 10 characters are stored on the device.
                - `range_V` _float, optional_ - Voltage range in Volts.
                - `offset_V` _float, optional_ - Vertical offset in Volts.
                - `invert` _bool, optional_ - Invert signal.
                - `unit` _Literal["V", "A"], optional_ - Unit.
                - `bandwidth_limit` _bool, optional_ - Enable bandwidth limit.
                - `bandwidth_Hz` _float, optional_ - Bandwidth in Hz.
                - `coupling` _Literal["AC", "DC"], optional_ - Coupling.
                - `display` _bool, optional_ - Enable display.
                - `trig_level_low` _float, optional_ - Low trigger level in Volts.
                - `trig_level_high` _float, optional_ - High trigger level in Volts.
                - `probe_att` _float, optional_ - Probe attenuation ratio.
            channel_2 (dict, optional): Channel 2 settings. Passed in **kwargs.
            channel_3 (dict, optional): Channel 3 settings. Passed in **kwargs.
            channel_4 (dict, optional): Channel 4 settings. Passed in **kwargs.
        """

        params = self._parse_kwargs(kwargs, no_defaults)

        self._set_params(params, show_warnings)

        continuous = self._res.query("RSTate?") == "RUN"

        self._res.write("DIGITIZE")
        with self._temporary_timeout(None):  # disable timeout for this command
            # the actual command is not important, we need to make sure that digitize is finished and the device accepts new commands
            self._res.query("*OPC?")

        measurement = self.get_measurement(name, comment, meta, screenshot=screenshot, settings=settings)

        if continuous:
            self._res.write("RUN")

        return measurement

    def make_scalar_measurement(self, name: str, channel: int, channel_2: int = 1) -> float | int:
        """Get a scalar measurement from the device

        Args:
            name (str): Name of the measurement.
            channel (int): Channel to measure on.
            channel_2 (int, optional): Second channel for phase and delay measurements. Defaults to 1.

        Available measurements:
            - duty_cycle
            - fall_time_s
            - frequency_Hz
            - duty_cycle_neg
            - neg_edge_count
            - neg_pulse_count
            - neg_pulse_width_s
            - pos_edge_count
            - pos_pulse_count
            - pos_pulse_width_s
            - overshoot_pc
            - preshoot_pc
            - period_s
            - phase_deg
            - delay_s
            - rise_time_s
            - amplitude_V
            - average_V
            - base_V
            - top_V
            - max_V
            - min_V
            - peak_to_peak_V
            - t_of_max_s
            - t_of_min_s
            - ac_rms_cycle_V
            - ac_rms_display_V
            - dc_rms_cycle_V
            - dc_rms_display_V

        Returns:
            float | int: The measurement value.
        """
        # TODO longer timeout since the device actually makes a measurement
        return self._measurements.get(name, channel=channel, channel_2=channel_2)

    def set_auto_trigger(self) -> None:
        """Automatically sets the trigger levels to the 50% point of the waveform."""
        self._res.write(":TRIGger:LEVel:ASETup")

    def _screenshot_data(self) -> bytearray:
        return self._res.query_binary_values(":DISPlay:DATA? PNG, COLOR", datatype="s", container=bytearray)

    def save_screenshot(self, path: Path) -> None:
        """Save a screenshot as a png file."""
        assert Path(path).suffix == ".png", "Screenshot must be saved as a .png file."
        with open(path, "wb") as f:
            f.write(self._screenshot_data())

    def screenshot(self) -> Image:
        """Return a screenshot of the device screen as an IPython Image object."""
        return Image(self._screenshot_data())

    def _settings_data(self) -> bytearray:
        return self._res.query_binary_values(":SYSTem:SETup?", datatype="s", container=bytearray)

    def save_settings(self, path: Path) -> None:
        """Save all device settings to a file in xml format."""
        assert Path(path).suffix == ".xml", "Settings must be saved as a .xml file."
        with open(path, "wb") as f:
            f.write(self._settings_data())
