import numpy as np
import pandas as pd

from .common import Device, Measurement, ParamProxy


class Base(Device):
    """Stanford Research Systems SR785 Signal Analyzer Base Class

    Use the measurement group specific subclasses for actual measurements. They can be imported and accessed through the `SR785` namespace.
    - [`SR785.FFT`](#sr785.FFT) - Measurements using the FFT group very fast but constrained resolution
    - [`SR785.SweptSine`](#sr785.SweptSine) - Measurements using the Swept Sine group slower but more flexible
    """

    _meas_group_map = ParamProxy.CodeMap(
        # {"FFT": "0", "corr": "1", "oct": "2", "swept_sine": "3", "order": "4", "time_hist": "5"}
        {"FFT": "0", "swept_sine": "3"}
    )
    _input_mode_map = ParamProxy.CodeMap({"DC": "0", "AC": "1", "ICP": "2"})
    _peak_units_map = ParamProxy.CodeMap({"off": "0", "pk": "1", "rms": "2", "pp": "3"})
    _sweep_type_map = ParamProxy.CodeMap({"lin": "0", "log": "1"})
    _view_map = ParamProxy.CodeMap(
        {
            "mag": "0",
            "lin_mag": "1",  # avoid use, this should be the same as mag, just a different display scale
            "mag_squared": "2",
            "real": "3",
            "imag": "4",
            "phase": "5",
            "unwrapped_phase": "6",
        }
    )
    _db_unit_map = ParamProxy.CodeMap({"off": "0", "dB": "1", "dBm": "2"})

    # NOTE
    # if there is a list of commands, all are written and the first will be red
    # a lot of the parameters are read only in 0 and 1 and write only in 2 this is exploited here
    _param_map = {
        "meas_group": (["MGRP{Q} 0,", "MGRP{Q} 2,"], *_meas_group_map.de_en_code),
        "meas": ParamProxy.Placeholder,
        "channel_1": {
            "differential": ("I1MD{Q}", ParamProxy.decode_bool, int),
            "ground": ("I1GD{Q}", ParamProxy.decode_bool, int),
            "coupling": ("I1CP{Q}", *_input_mode_map.de_en_code),
            "anti_aliasing": ("I1AF{Q}", ParamProxy.decode_bool, int),
        },
        "channel_2": {
            "differential": ("I2MD{Q}", ParamProxy.decode_bool, int),
            "ground": ("I2GD{Q}", ParamProxy.decode_bool, int),
            "coupling": ("I2CP{Q}", *_input_mode_map.de_en_code),
            "anti_aliasing": ("I2AF{Q}", ParamProxy.decode_bool, int),
        },
        "display_A": {
            "view": ("VIEW{Q} 0,", *_view_map.de_en_code),
            "unit": ("UNIT{Q} 0,", str, ParamProxy.read_only),  # readonly
            "db": ("UNDB{Q} 0,", *_db_unit_map.de_en_code),
            "peak": ("UNPK{Q} 0,", *_peak_units_map.de_en_code),
            "psd": ("PSDU{Q} 0,", ParamProxy.decode_bool, int),
        },
        "display_B": {
            "view": ("VIEW{Q} 1,", *_view_map.de_en_code),
            "unit": ("UNIT{Q} 1,", str, ParamProxy.read_only),  # readonly
            "db": ("UNDB{Q} 1,", *_db_unit_map.de_en_code),
            "peak": ("UNPK{Q} 1,", *_peak_units_map.de_en_code),
            "psd": ("PSDU{Q} 1,", ParamProxy.decode_bool, int),
        },
        "dbm_ref_Ohm": ("DBMR{Q}", float, ParamProxy.no_op),
    }

    _default_defaults = {
        "display_A": {
            "view": "mag",
            "db": "dB",
            "peak": "off",
            "psd": False,
        },
        "display_B": {
            "view": "phase",
            "db": "off",
            "peak": "off",
            "psd": False,
        },
        "dbm_ref_Ohm": 50.0,
        # TODO more defaults
    }

    def __init__(self, address: str, *, defaults: dict = None) -> None:
        """SR785.FFT

        Args:
            address (str): Visa address of device.
            defaults (dict, optional): Default measurement settings on top of class defaults. Defaults to None.
        """

        defaults = defaults or {}
        super().__init__(address, defaults=defaults)
        self._res.timeout = 10000  # allow for slow data transfer
        self._res._encoding = "cp437"  # SR785 still uses weird code pages

    def get_measurement(self, *, name: str = None, comment: str = "", meta: dict = None) -> Measurement:
        """Get the current data from the device without changing any settings

        Args:
            name (str, optional): Measurement Name. Defaults to automatic name from metadata.
            comment (str, optional): Comment to add to metadata. Defaults to "".
            meta (dict, optional): User metadata to store with the measurement. Defaults to None.

        Returns:
            Measurement: The current measurement data.
        """

        # NOTE DSPN and SNPS return different number of points
        # DSPN returns one more point, for fft this is correct,
        # for swept sine only SNPS is correct and the last point should be ignored
        raw_points = int(self._res.query("DSPN? 0"))
        num_points = raw_points if self._meas_group == "FFT" else raw_points - 1
        f_min = float(self._res.query("DBIN? 0, 0"))
        f_max = float(self._res.query(f"DBIN? 0, {num_points-1}"))

        if self._meas_group == "swept_sine" and self._params.get("log_sweep"):
            frequencies = np.logspace(np.log10(f_min), np.log10(f_max), num_points)
        else:
            frequencies = np.linspace(f_min, f_max, num_points)
        assert np.isclose(frequencies[1], float(self._res.query("DBIN? 0, 1"))), "unexpected x scale"

        # disp_a = self._res.query_binary_values(
        #     "DSPB? 0", datatype="f", header_fmt="empty", data_points=raw_points, expect_termination=False
        # )[:num_points]
        # disp_b = self._res.query_binary_values(
        #     "DSPB? 1", datatype="f", header_fmt="empty", data_points=raw_points, expect_termination=False
        # )[:num_points]
        disp_a = self._res.query_ascii_values("DSPY? 0")[:num_points]
        disp_b = self._res.query_ascii_values("DSPY? 1")[:num_points]
        hm = self._params.all()

        df = pd.DataFrame(
            {
                "freq_Hz": frequencies,
                f"{hm['display_A']['view']}_{hm['display_A']['unit']}": disp_a,
                f"{hm['display_B']['view']}_{hm['display_B']['unit']}": disp_b,
            },
        )
        df.set_index("freq_Hz", inplace=True)

        metadata = self._make_metadata(name, comment, "freq_Hz", {}, meta)

        return Measurement(metadata, df)

    def measure(self, **kwargs) -> Measurement:
        raise NotImplementedError(
            "measure is not implemented for the Base class, use on of the measurement group specific subclasses"
        )


class FFT(Base):
    _meas_group = "FFT"
    _meas_map = ParamProxy.CodeMap(
        {
            "FFT_1": "0",
            "FFT_2": "1",
            "power_spectrum_1": "2",
            "power_spectrum_2": "3",
        }
    )
    _fft_base_freq_map = ParamProxy.CodeMap({"100kHz": "0", "102.4kHz": "1"})

    def _verify_fft_span(val: str | float) -> str:
        freqs_100k = [round(f, 2) for f in 100e3 / 2 ** np.arange(20)]
        freqs_102_4k = [round(f, 2) for f in 102.4e3 / 2 ** np.arange(20)]
        all_freqs = freqs_100k + freqs_102_4k
        if isinstance(val, float) or isinstance(val, int):
            rounded = round(val, 2)
            if rounded in all_freqs:
                return rounded
            else:
                raise ValueError(
                    f"Invalid stop frequency {val}!\n Base 100kHz: {freqs_100k}\n Base 102.4kHz: {freqs_102_4k}"
                )
        elif isinstance(val, str):
            if not (val.startswith("div") and val[3:].isdigit()):
                raise ValueError(f'Invalid span string "{val}"!\n Must be "divN" for f = f_base / 2^N')
            return 102.4e3 / 2 ** int(val[3:])
        else:
            raise ValueError(f"Invalid span {val}! Must be float or str.")

    _fft_res_map = ParamProxy.CodeMap({100: "0", 200: "1", 400: "2", 800: "3"})
    _fft_win_map = ParamProxy.CodeMap({"uniform": "0", "flattop": "1", "hanning": "2", "BMH": "3"})

    _param_map = Base._param_map | {
        "meas": (["MEAS{Q} 0,", "MEAS{Q} 2,"], *_meas_map.de_en_code),
        "fft_base_freq": (["FBAS{Q} 0,", "FBAS{Q} 2,"], *_fft_base_freq_map.de_en_code),
        "fft_res": (["FLIN{Q} 0,", "FLIN{Q} 2,"], *_fft_res_map.de_en_code),
        "fft_win": (["FWIN{Q} 0,", "FWIN{Q} 2,"], *_fft_win_map.de_en_code),
        "start_Hz": (["FSTR{Q} 0,", "FSTR{Q} 2,"], float, ParamProxy.ValSet({0})),
        "stop_Hz": (["FSPN{Q} 0,", "FSPN{Q} 2,"], float, _verify_fft_span),
        "average": (["FAVG{Q} 0,", "FAVG{Q} 2,"], ParamProxy.decode_bool, int),  # TODO must always be true for FFT
        "average_count": (["FAVN{Q} 0,", "FAVN{Q} 2,"], int, ParamProxy.no_op),
        # "fft_span": (["FSPN{Q} 0,", "FSPN{Q} 2,"], float, ParamProxy.no_op),
        # TODO maybe differentiate between stop and span
    }

    _default_defaults = ParamProxy.recursive_merge(
        Base._default_defaults,
        {
            "meas_group": _meas_group,
            "fft_base_freq": "100kHz",
            "stop_Hz": 0,
        },
    )

    def measure(
        self,
        *,
        name: str = None,
        comment: str = "",
        meta: dict = None,
        show_warnings: bool = True,
        no_defaults: bool = False,
        **kwargs,
    ):
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
            meas (Literal["FFT_1", "FFT_2", "power_spectrum_1", "power_spectrum_2"], optional): Measurement to perform. Passed in **kwargs.
            channel_1 (dict, optional): Channel 1 settings. Passed in **kwargs.
                - `differential` _bool, optional_ - differential mode.
                - `ground` _bool, optional_ - ground mode.
                - `coupling` _Literal["DC", "AC", "ICP"], optional_ - coupling mode.
                - `anti_aliasing` _bool, optional_ - anti-aliasing filter.
            channel_2 (dict, optional): Channel 2 settings. Passed in **kwargs.
            display_A (dict, optional): Display A settings. Passed in **kwargs.
                - `view` _Literal["mag", "mag_squared", "real", "imag", "phase", "unwrapped_phase"], optional_ - View quantity.
                - `db` _Literal["off", "dB", "dBm"], optional_ - dB units.
                - `peak` _Literal["off", "pk", "rms", "pp"], optional_ - Peak units.
                - `psd` _bool, optional_ - Power spectral density units.
                - `rad` _bool, optional_ - Radian phase units.
            display_B (dict, optional): Display B settings. Passed in **kwargs.
            dbm_ref_Ohm (float, optional): dBm reference impedance. Passed in **kwargs.
            fft_base_freq (Literal["100kHz", "102.4kHz"], optional): FFT base frequency. Passed in **kwargs.
            fft_res (Literal[100, 200, 400, 800], optional): FFT resolution. Passed in **kwargs.
            fft_win (Literal["uniform", "flattop", "hanning", "BMH"], optional): FFT window. Passed in **kwargs.
            stop_Hz (float | str, optional): Stop frequency in Hz or "divN" for f = f_base / 2^N. Passed in **kwargs.
            average (bool, optional): Averaging. Passed in **kwargs.
            average_count (int, optional): Averaging count. Passed in **kwargs.
        """

        params = self._parse_kwargs(kwargs, no_defaults)

        self._set_params(params, show_warnings)

        old_auto_offset = ParamProxy.decode_bool(self._res.query("IAOM?"))
        self._res.write("IAOM 0")  # disable auto offset during measurement

        if self._params.get("average"):
            exp_average = ParamProxy.decode_bool(self._res.query("FAVT? 0"))
            self._res.write("FAVT 2, 0")  # set to linear average
            self._res.write("*CLS")
            self._res.write("STRT")  # start single shot
            while not ParamProxy.decode_bool(self._res.query("DSPS? 1")):  # read AVGA (averaging complete)
                pass
            measurement = self.get_measurement(name=name, comment=comment, meta=meta)
            self._res.write(f"FAVT 2, {int(exp_average)}")  # restore previous state
        else:
            old_trigger_source = int(self._res.query("TSRC? 0"))
            self._res.write("TSRC 0, 6")  # set to manual trigger
            self._res.write("*CLS")
            self._res.write("TMAN")
            while not ParamProxy.decode_bool(self._res.query("DSPS? 0")):  # read NEWA (new data available)
                pass
            measurement = None
            self._res.write(f"TSRC 0, {old_trigger_source}")  # restore previous state

        self._res.write(f"IAOM {int(old_auto_offset)}")  # restore previous state

        return measurement

    def measure_stitched(
        self,
        *,
        name: str = None,
        comment: str = "",
        meta: dict = None,
        show_warnings: bool = True,
        no_defaults: bool = False,
        stop_Hz: float | str,
        segments: int,
        **kwargs,
    ) -> Measurement:
        """Perform a stitched measurement

        This will perform multiple measurements with decreasing stop frequencies and insert the smaller higher resolution measurements into the larger lower resolution measurements.
        The next measurement will always have half the stop frequency of the previous measurement.
        The default rules and **kwargs are the same as [`SR785.FFT.measure`](#sr785.FFT.measure).

        Args:
            name (str, optional): Measurement Name. Defaults to automatic name from metadata.
            comment (str, optional): Comment to add to metadata. Defaults to "".
            meta (dict, optional): User metadata to store with the measurement. Defaults to None.
            show_warnings (bool, optional): Show warnings for unspecified parameters. Defaults to True.
            no_defaults (bool, optional): Ignore default settings. Defaults to False.
            stop_Hz (float | str): Stop frequency in Hz or "divN" for f = f_base / 2^N.
            segments (int): Number of segments to divide the stop frequency into.
            **kwargs: Other measurement parameters, see [`SR785.FFT.measure`](#sr785.FFT.measure) for details.

        """
        stop_Hz_parsed = self._verify_fft_span(stop_Hz)
        spans = [stop_Hz_parsed / 2**n for n in range(segments)]
        assert spans[-1] >= 100e3 / 2**19, "Last segment must be at least 190 mHz"
        meas_base = self.measure(
            stop_Hz=stop_Hz_parsed,
            **kwargs,
            name=name,
            comment=comment,
            meta=meta,
            show_warnings=show_warnings,
            no_defaults=no_defaults,
        )
        for span in spans[1:]:
            meas = self.measure(stop_Hz=span, **kwargs, show_warnings=show_warnings, no_defaults=True)
            meas_base.insert(meas, inplace=True)
        return meas_base


class SweptSine(Base):
    _meas_group = "swept_sine"
    _meas_map = ParamProxy.CodeMap(
        {
            "spectrum_1": "42",
            "spectrum_2": "43",
            "normalized_variance_1": "44",
            "normalized_variance_2": "45",
            "frequency_response": "47",
        }
    )

    def _decode_unit_voltage(raw: str) -> float:
        val, unit = raw.split(",")
        if unit == "2":
            return 10 ** (float(val) / 10)
        else:
            return float(val) * {"0": 0.001, "1": 1}[unit]

    _auto_level_map = ParamProxy.CodeMap({"off": "0", "channel_1": "1", "channel_2": "2"})

    _param_map = Base._param_map | {
        "meas": (["MEAS{Q} 0,", "MEAS{Q} 2,"], *_meas_map.de_en_code),
        "start_Hz": (["SSTR{Q} 0,", "SSTR{Q} 2,"], float, ParamProxy.no_op),
        "stop_Hz": (["SSTP{Q} 0,", "SSTP{Q} 2,"], float, ParamProxy.no_op),
        "sweep_points": (["SNPS{Q} 0,", "SNPS{Q} 2,"], int, ParamProxy.no_op),
        "log_sweep": (["SSTY{Q} 0,", "SSTY{Q} 2,"], ParamProxy.decode_bool, int),
        "source": {
            "auto_level": ("SSAL{Q}", *_auto_level_map.de_en_code),
            "amplitude_V": ("SSAM{Q}", _decode_unit_voltage, lambda x: f"{x}V"),
            "amplitude_ideal_V": ("SSRF{Q}", _decode_unit_voltage, lambda x: f"{x}V"),
            "amplitude_max_V": ("SMAX{Q}", _decode_unit_voltage, lambda x: f"{x}V"),
        },
    }

    _default_defaults = ParamProxy.recursive_merge(
        Base._default_defaults,
        {
            "meas_group": _meas_group,
        },
    )

    def measure(
        self,
        *,
        name: str = None,
        comment: str = "",
        meta: dict = None,
        show_warnings: bool = True,
        no_defaults: bool = False,
        **kwargs,
    ):
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
            meas (Literal["spectrum_1", "spectrum_2", "normalized_variance_1", "normalized_variance_2", "frequency_response"], optional): Measurement to perform. Passed in **kwargs.
            channel_1 (dict, optional): Channel 1 settings. Passed in **kwargs.
                - `differential` _bool, optional_ - differential mode.
                - `ground` _bool, optional_ - ground mode.
                - `coupling` _Literal["DC", "AC", "ICP"], optional_ - coupling mode.
                - `anti_aliasing` _bool, optional_ - anti-aliasing filter.
            channel_2 (dict, optional): Channel 2 settings. Passed in **kwargs.
            display_A (dict, optional): Display A settings. Passed in **kwargs.
                - `view` _Literal["mag", "mag_squared", "real", "imag", "phase", "unwrapped_phase"], optional_ - View quantity.
                - `db` _Literal["off", "dB", "dBm"], optional_ - dB units.
                - `peak` _Literal["off", "pk", "rms", "pp"], optional_ - Peak units.
                - `psd` _bool, optional_ - Power spectral density units.
                - `rad` _bool, optional_ - Radian phase units.
            display_B (dict, optional): Display B settings. Passed in **kwargs.
            dbm_ref_Ohm (float, optional): dBm reference impedance. Passed in **kwargs.
            start_Hz (float, optional): Start frequency in Hz. Passed in **kwargs.
            stop_Hz (float, optional): Stop frequency in Hz. Passed in **kwargs.
            sweep_points (int, optional): Sweep points. Passed in **kwargs.
            log_sweep (bool, optional): Logarithmic sweep. Passed in **kwargs.
            source (dict, optional): Source settings. Passed in **kwargs.
                - `auto_level` _Literal["off", "channel_1", "channel_2"], optional_ - Auto level source.
                - `amplitude_V` _float, optional_ - Amplitude in V.
                - `amplitude_ideal_V` _float, optional_ - Ideal amplitude in V for auto level.
                - `amplitude_max_V` _float, optional_ - Maximum amplitude in V for auto level.
        """

        params = self._parse_kwargs(kwargs, no_defaults)

        self._set_params(params, show_warnings)

        old_auto_offset = ParamProxy.decode_bool(self._res.query("IAOM?"))
        self._res.write("IAOM 0")

        with self._temporary_timeout(None):
            continuous = ParamProxy.decode_bool(self._res.query("SRPT? 0"))
        self._res.write("SRPT 2, 0")  # set to single shot
        self._res.write("*CLS")
        self._res.write("STRT")  # start single shot
        while not ParamProxy.decode_bool(self._res.query("DSPS? 4")):  # read SSA (swept since complete)
            pass
        measurement = self.get_measurement(name=name, comment=comment, meta=meta)
        self._res.write(f"SRPT 2, {int(continuous)}")

        self._res.write(f"IAOM {int(old_auto_offset)}")

        return measurement


class SR785:
    Base = Base
    FFT = FFT
    SweptSine = SweptSine

    def __init__(self) -> None:
        raise NotImplementedError("This class only serves as a namespace and should not be instantiated.")
