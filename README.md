PyInst 的目的是将具体仪器抽象化，为同类型的仪器提供统一的接口，以提高代码对不同型号仪器的兼容性、一致性和可维护性。

对于绝大多数符合VISA接口标准的仪器，使用 pyvisa 模块实现；对于少数无法支持VISA接口标准的仪器，使用其物理接口对应的方法来实现。

## 基本用法

所有接口都暴露在顶层命名空间中。

1.  model 类
   
    model 类是具体仪器型号的类。以单文件的形式存放在 `/models/` 路径下。每个类都以 Model 开头。例如：

    ``` python
    from pyinst import ModelN7752A
    voa = ModelN7752A('GPIB0::7::INSTR', 3)
    dbm_power = voa.get_att_value()
    ```

    model 类都有一个参数 resource_name, 为该仪器对应的 visa 资源名称(或别名(alias))。如果该仪器不是 visa 仪器对象，则该参数表示仪器的接口地址，如 'COM2' 等。除了该参数以外，model 类还可能有其它一系列特有的参数，例如 N7752A 的第二个参数为通道号。

    需要注意的是，一个 model 对象对应的是逻辑上作为一个功能单元的实体，而非与仪器的物理形态相对应。例如，一个具有4通道的 OPM，它的 4 个通道在逻辑上是 4 个独立的功能单元，每个通道都可以作为一个 OPM 对象使用。一个同时具有光功率监测功能的 VOA，在逻辑上既可以视为 OPM，也可以视为 VOA。

2.  instrument type 类

    instrument type 类是仪器类型的类。以单文件形式存放在 `/instrument_types/` 路径下。每个类都以 Type 开头。例如 ModelOPM。

    instrument type 类是同类型所有仪器 (model 类) 的一个父类 (add-in)，它的作用是为同类型的仪器定义统一的接口，从而使得调用 pyinst 的顶层代码能够较好的在不同型号的仪器间切换。

    每个 model 类可以继承一个或多个 instrument_type 类。

    通常你不需要在外层代码中调用这些类。

3.  constants

    有一些常数被定义在 `/constants.py` 中，有些仪器方法可能会用到里面的某些常数，例如 `OpticalUnit` 枚举量。

4.  functions

    定义了一些顶层的方法，方便你对仪器资源进行管理。路径为 `/functions.py`。

5.  package information

    pyinst 的一些信息。路径为 `/pkg_info.py`。

## 原则

pyinst 的基本原则是**一致性**。

1.  同类型的仪器 (model) 从 instrument type 中继承了一系列标准的方法，model 类必须尽可能重写这些方法以实现其功能。除此之外，一些仪器可能会有其特有的方法。有些仪器由于其功能限制，可能无法实现所有的标准方法。如果该方法没有重写，在调用它时，会 (由 instrument type 类) 抛出一个 `NotImplementedError`。

2.  不同类型的仪器，实现同类型方法时，必须依照标准函数命名列表来命名。例如，对于“开始运行”这个功能，有的仪器命令中可能称为 run，有的仪器命令中可能称为 start，但在 model 的方法中都应依照标准命名列表，命名为 run。

    A. 具有波长 (或频率) 设置功能的仪器，必须同时实现以下方法：
    * set_frequency
    * set_wavelength

    B. 具有波长 (或频率) 查询功能的仪器，必须同时实现以下方法：
    * get_frequency
    * get_wavelength

    C. 功率监测相关的标准命名：
    * get_power_value
    * get_power_unit
    * set_power_unit
    * get_power
    * get_dbm_value
    * get_w_value
    * set_avg_time
    * get_avg_time

    D. 控制相关的标准命名：
    * run
    * stop
    * is_running
    * enable
    * disable
    * is_enabled

    其中，run/enable 可接收一个 bool 参数，若为 True 则 run/enable，为 False 则 stop/disable，该参数缺省为 True。

3.  默认单位：
    
    默认的光功率单位为 dBm/W，默认的光波长单位为 nm，默认的光频率单位为 THz。
    
    缺省的单位前缀应与之相同，例如返回光波长的函数，应返回 nm 为单位的值，而不得返回以 m 为单位的值。

## 扩展

扩展的新 model 类必须符合前面所述的原则。

1. 对于符合 visa 标准接口的类，同时继承 VisaInstrument 类和对应的 instrument type 类。

    需要实现的属性和方法：
    *  类属性：
        * brand = ""
        * model = ""
        * details = {}
        * params = []

        缺少这些属性不会影响对象的功能，但这些信息有助于提供与仪器有关的信息。

2. 对于不符合 visa 标准接口的类，同时继承 BaseInstrument 类和对应的仪器类。

    需要实现的属性和方法：
    *  类属性：
        * brand = ""
        * model = ""
        * details = {}
        * params = []

        缺少这些属性不会影响对象的功能，但这些信息有助于提供与仪器有关的信息。
    *  对象属性和方法：
        * self._resource_name
        * self.close()
        * self.check_connection()

    缺少这些属性或方法将影响对象的基本功能。
