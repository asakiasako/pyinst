# pyinst

## 简述

pyinst 的目的是将具体仪器抽象化，为同类型的仪器提供统一的控制接口，以提高代码对不同型号仪器的兼容性、一致性和可维护性。

对于绝大多数符合VISA接口标准的仪器，使用 pyvisa 模块实现；对于少数无法支持VISA接口标准的仪器，采用独特的方式实现。

每个仪器类型具有一系列通用的方法，但不一定所有型号的仪器都支持所有这些方法。同样的，有些仪器可能也有自己特有的方法。

## 依赖

* pyvisa
    ``` Bash
    pip install pyvisa
    ```

## 基本用法

``` Python
from pyinst import *
with ModelN7752A(resource_name[, **kwargs]) as voa:
    voa.xxx
```

模块的命名空间暴露了所有的仪器类，所有的仪器类存放在 models 文件夹内。

模块同时暴露了一系列的枚举类，存放在 instype/_BaseInstrumentType/constants 内，在调用某些方法时可能会用到。

## 结构

如果你需要编写自己的仪器类，下面的内容将帮助你了解整个模块的架构。

### Instrument Types

BaseInstrumentType 为所有仪器类型的基类。仪器类型为所有以 TypeXXX 格式命名的类，例如 TypeVOA。XXX为仪器类型的后缀，字母全部大写。

仪器类型的后缀来源于 InstrumentType 枚举类，且与对应的枚举名称严格一致。

TypeXXX 的作用是，定义某种仪器类型的通用接口。在使用某种型号的仪器类时，安全的做法是仅使用从 TypeXXX 中继承/重写的方法，这样即使变更型号，也不存在兼容性的问题。仪器所特有的方法通常用作过渡或补充。

由于不同仪器之间的差异，在你添加仪器时，你不必重写所有的方法。当使用缺失的方法时，会抛出一个 AttributeError，来表明该仪器不支持这个方法。

### Instrument Models

VisaInstruments 为所有符合 VISA 接口的仪器的基类。而具体的仪器型号的类继承 VisaInstruments 和 TypeXXX 而来。

由于某种具体的仪器型号可能作为多种类型使用，例如：某些仪器兼具 VOA 和 OPM 的功能；有时候会将 OSA 用作 WM(Wavemeter) 等。因此一个仪器型号可以继承多个 TypeXXX 类，以添加不同功能。

当然，由于 python 是一种动态语言，即使某些仪器没有显式的继承某些仪器类型，但只要实现了你所需的相同的方法，也可以拿来使用。

具体的仪器型号命名为: ModelXXXX，例如：ModelN7752A。这个型号继承了 VOA 和 TypePM。

有时候某些仪器需要一个中间类进行衍生，例如 ModelN7752A 和 ModelN7744A 由于方法类似，所以都从 ModelN77xx 继承。

区别具体仪器型号和中间类的方法是，具体的仪器型号会指定 model 这个类属性，而中间类的 model 属性为空。

### 对于不符合 SCPI 接口的仪器

某些仪器虽然不符合 SCPI 接口（不支持通用的 SCPI 接口命令），但仍可使用 VisaInstrument 进行定义。只是初始化父类 VisaInstrument 时，需要指定 no_idn=True, 来表明它并非标准的（不具有 idn 查询）。例如 ModelTC3625。

某些仪器具有独特的连接方式，例如 ModelNSW。这时你需要自己重新定义一个类。为了保证通用性，你的类必须实现以下属性和方法：

* resource_name
* \_\_enter\_\_()
* \_\_exit\_\_()
* close()
* check_connection()
* 类属性： brand = str，model = str, details = dict, params = list of dicts

如果没有必要，你的方法甚至可以不做任何事情，但它们必须存在。

### Instrument Lib

为了方便上层代码了解 pyinst 中可使用的仪器资源及其基本属性，pyinst 会生成一个对象。

pyinst 会自动搜寻所有以 Model 开头的类，并找出那些属于具体仪器型号的类（具有非空的 model 类属性）来生成这个对象。

你可以通过 get_instrument_lib() 方法获得这个对象。

Instrument Lib 的结构：

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
          "range": [
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

每一个类都可以在类属性中定义 model、brand、params、details 等属性。如果没有某个属性，例如details，则不用定义。

details 可以写入你认为必要的任何信息。

这样做的好处是，上层代码可以快速的知晓已有仪器资源的状况。例如在配置仪器时，可以很方便地生成可用仪器型号的列表；在配置仪器参数时，可以给出需要配置的参数及可选项列表。这样就可以在上层代码中通过一段通用代码来生成仪器配置界面。