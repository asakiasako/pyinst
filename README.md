# pyinst

## 简述

pyinst 的目的是将具体仪器抽象化，为同类型的仪器提供统一的接口，以提高代码对不同型号仪器的兼容性、一致性和可维护性。

对于绝大多数符合VISA接口标准的仪器，使用 pyvisa 模块实现；对于少数无法支持VISA接口标准的仪器，采用独特的方式实现。

## 同类型的仪器拥有统一的接口

所有“仪器型号(Instrument Model)”类都继承自一个或多个“仪器类型(Instrument Type)”类，例如 class TypeOMA。

每个仪器类型都会定义一系列方法，作为该仪器类型的统一接口。具体的仪器型号在继承这些类时，需要重写这些方法。

某个仪器型号并不一定需要实现其所继承的仪器类型的所有方法。如果某个方法在仪器类型中定义，但没有被重写，则会在调用时抛出一个 NotImplementedError。

同样，有些仪器型号可能定义一些特有的方法。特别是对于不同型号之间的操作逻辑差异很大的仪器类型，例如 OSA，它的大多数方法都是该仪器型号所特有的。

通常来说，使用那些继承自仪器类型的统一接口是更安全的，它能最大限度保证你切换仪器型号时的代码兼容性。

## 依赖

* pyvisa
    ``` Bash
    pip install pyvisa
    ```

## 基本用法

``` Python
from pyinst import *
with ModelN7752A(resource_name[, **kwargs]) as voa:
    voa.enable()
    voa.set_att(10)
```

模块的所有接口都直接暴露在模块的顶层空间，包括：仪器型号的类，仪器类型的类，一些常量和一些工具函数。

仪器型号的类以 Model 开头，例如：ModelN7752A。它们的代码存放在 '/models/' 文件夹下，每个文件定义一个仪器型号（或者一系列行为相同的仪器型号）。

仪器类型的类以 Type 开头，例如：TypeOMA。它们存放在 '/instrument_types/' 文件夹下，每个文件定义一个仪器类型。仪器类型的缩写由 pyinst.InstrumentType 枚举常数定义。

模块暴露了一系列常量和枚举常量，它们在 './constants.py' 中被定义。

模块定义了一系列工具函数，它们能够实现获取仪器列表，获取仪器的信息等操作。它们在 './functions.py' 中被定义。

## 扩展

下面的内容将指导你如何添加自己的仪器型号。

为了保证接口的一致性和兼容性，建议以分支的形式向 gitlab 提交代码，然后进行统一的整合，或向贡献者提出进一步的更改意见。

### 符合 VISA 标准的仪器

VisaInstruments 为所有符合 VISA 标准的仪器的基类。仪器型号的类通过继承 VisaInstruments 和 （一个或多个）仪器类型的类实现。

你需要填写仪器型号类的一些基本属性，如 model, brand, detail, etc. 参考其它已实现的仪器型号。

你需要重写所继承的仪器类型里的方法。如果该仪器型号不具备对应的功能，则不必重写，调用该方法时将抛出 NotImplementedError。

除了从仪器类型继承过来的方法，你也可以为该仪器型号添加一些特有的方法。

### 对于不符合 SCPI 接口的仪器

某些仪器虽然不符合 SCPI 接口（不支持通用的 SCPI 接口命令），但仍可借用 VisaInstrument 进行定义。只是初始化父类 VisaInstrument 时，需要指定 no_idn=True, 来表明它并不具有标准的 SCPI 接口，因而无法进行 idn 查询。（例如 ModelTC3625）

某些仪器具有自己独特的连接方式和命令结构，这时你无法从 VisaInstrument 进行继承，而需要重新实现该仪器型号（例如ModelNSW）。你需要实现以下属性或方法，以保证它和整个 pyinst 模块的兼容性：

* resource_name
* \_\_enter\_\_()
* \_\_exit\_\_()
* close()
* check_connection()
* 类属性： brand = str，model = str, details = dict, params = list of dicts

## 获取整个仪器库的基本信息

为了方便上层代码了解 pyinst 中可使用的仪器资源及其基本属性，你可以使用get_instrument_lib() 方法。

该方法会自动搜寻所有以 Model 开头的类，并生成一个包含所有仪器信息的对象。

``` json
{
  "OPM": [
    {
      "model": "N7744A",
      "brand": "Keysight",
      "class_name": "ModelN7744A",
      "params": [
        {
          "name": "channel",
          "type": "int",
          "options": [
            1,
            2,
            3,
            4
          ]
        }
      ],
      "details": {
        "Wavelength Range": "1260~1640 nm"
      }
    },
    ...
    ...
    ...
```
