# Lab Control

This repository contains classes to control lab equipment in a simple and unified way.

- [Lab Control](#lab-control)
  - [API Reference](#api-reference)
    - [Measurement Devices](#measurement-devices)
    - [Actuation Devices](#actuation-devices)
    - [Other Classes](#other-classes)
  - [Getting Started](#getting-started)
    - [Installation](#installation)
    - [Using Measurement Devices](#using-measurement-devices)
    - [Measurements](#measurements)
      - [`get_measurement()`](#get_measurement)
      - [`measure()`](#measure)
    - [Defaults](#defaults)
    - [Measurement Objects](#measurement-objects)
  - [Other Notes](#other-notes)

## API Reference

### Measurement Devices

- [E5061B](doc/e5061b.md)
- [DSOX2024A](doc/dsox2024a.md)
- [N90X0X](doc/n90x0x.md)
- [SR785](doc/sr785.md)
  - [SR785.FFT](doc/sr785.md#sr785.FFT)
  - [SR785.SweptSine](doc/sr785.md#sr785.SweptSine)

### Actuation Devices

- [StepperBoard](doc/stepper_board.md)

### Other Classes

- [common](doc/common.md)
  - [Device](doc/common.md#common.Device)
  - [Measurement](doc/common.md#common.Measurement)
  - [ParamProxy](doc/common.md#common.ParamProxy)
- [rpc](doc/rpc.md)
  - [BidirectionalLineStream](doc/rpc.md#rpc.BidirectionalLineStream)
  - [SerialBLS](doc/rpc.md#rpc.SerialBLS)
  - [SocketBLS](doc/rpc.md#rpc.SocketBLS)
  - [RpcClient](doc/rpc.md#rpc.RpcClient)
  - [RpcProxy](doc/rpc.md#rpc.RpcProxy)

## Getting Started

### Installation

The package can be installed from PyPI with pip:

```shell
pip install lab-control
```

### Using Measurement Devices

All measurement devices inherit from the `Device` class. This means that they have at least three methods, `__init__()`, `get_measurement()`, and `measure()`, which always have the same basic signature except for some additional keyword arguments.

Some devices also have additional methods like saving a screenshot or automatically adjusting the range.

When creating and instance of a measurement device, you will need to provide the VISA address of the device and you can also provide a dictionary of default settings, more on the default mechanism later.

```python
from lab_control import DSOX2024A

dev = DSOX2024A('USB0::0x0957::0x1796::MY60476362::0::INSTR', defaults={'time_points': 1000})
```

### Measurements

#### `get_measurement()`

The `get_measurement()` method is used to get the current data from the device without changing any settings or explicitly starting a measurement. This is useful when you are mostly working on the device itself and only want to save measurement data.

You can pass a `name`, `comment`, and additional `meta`data about you experiment or the measurement that will be stored in the `'user'` section of the metadata. If you do not specify a `name` the measurement will be named automatically based on the device, some of the parameters, and the current time.

#### `measure()`

To explicably start a measurement with specific parameters you should use the `measure()` method, in addition to the `name`, `comment`, and `meta` parameters that are available in the `get_measurement()` method, you can specify the measurement parameters. A list of the available parameters can be found in the documentation of the specific device. These parameters are generally not exhaustive as most devices have many more settings that are rarely used, the set of available parameters will be extended as needed. You can also set `no_defaults=True` to ignore all default settings and fall back to the current device settings. You will get a warning with a of all parameters that are not specified in the function call or defaults, this can be disabled with `show_warnings=False`.

The parameters are written to the device and read back, this will ensure, that parameters which were adjusted by the device to be within the allowed range are used.

Once the parameters are set, continuous measuring is suspended and the device will perform a single shot measurement as far as applicable for the device. This may also include multiple averaging cycles. Depending on the device, the measurement might take a while. After the measurement is done, the data is read from the device and the device is set back to continuous measuring if it was set to continuous measuring before.

### Defaults

To avoid having to specify all parameters every time everywhere, default settings can be provided on different levels. The fallback order is the following:

- Function parameters that are passed to the `measure()` method
- Instance defaults that were specified in the constructor.
- Class defaults that are sometimes specified in the class definition.
- Current device settings

The higher levels override the lower levels. This means that if a parameter is specified in the `measure()` method, it will override the instance defaults, and so on. You should avoid relying on the class defaults or the current device settings, the class defaults are currently still subject to change and the current device settings depend on the prior usage of the device. **If you expect you script to live longer than a day, you should always specify all parameters in the instance defaults or as function parameters to ensure consistency.**

You can also explicitly ignore a default on any level by setting it to `None`, if this means that the parameters is not specified on any level the device settings will be used. You can use this for example to ignore the class defaults when initializing an instance. Or to use the current device settings when calling the `measure()` method.

You can also use the `no_defaults` parameter in the `measure()` method to ignore all defaults for a single measurement.

### Measurement Objects

Both the `get_measurement()` and `measure()` methods return a `Measurement` object. A measurement has three members, `df` which contains tabular data as a pandas `DataFrame`, `meta` which contains metadata as a dictionary, and `attachments` which contains named binary attachments in a dictionary.

The metadata always contains a `'file'` which contains information about the file itself, like the name, delimiter and index column. The `'user'` section contains user specified data. Finally the `'dev'` section contains the parameters that were used for the measurement.

Measurements can be saved and loaded to and from disk with the `save()` and `load()` methods. If the measurement contains attachments it needs to be saved with `save_zip()` which will save the measurement and its attachments to a zip file. The zip file can be loaded with the normal `load()` method.

Measurements have a `_repr_html_()` method for a nicer display in Jupyter notebooks, they can also be plotted with the `plot()` convenience function. Measurements can also be combined by inserting one measurement into another with the `insert()` method.

## Other Notes

The repository uses symlinks so that the example files can access the `src` directory. Git will only recreate the symlinks when symlinks are enables with

```shell
git config core.symlinks true
```

Or with `--global` to enable it for all repositories.