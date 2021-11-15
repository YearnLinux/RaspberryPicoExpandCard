# RaspberryPicoExpandCard

#### LICENSE
* 本项目使用 MIT 授权协议

#### 介绍
Raspberry Pi Pico 扩展板，基于JSON数据结构，构建简单可快速扩展的通信控制协议。
某宝搜索 树莓派PICO 可以搜索到很多这个板子, 买到板子后烧录这个代码到板子里面即可。
作者使用的IDE是 VSCODE 里面安装了 RT-Thread MicoPython 插件，具体百度使用教程。
烧录代码后如果要Pico启动就立即执行代码，则需要把文件命名为 main.py 即可
MicoPython SDK DOC : https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf

#### MicoPython UF2
本项目基于 MicoPython 编写，请到树莓派官网下载 UF2 文件，拷贝到Pico大容量存储器内
MicoPython UF2 : https://www.raspberrypi.com/documentation/microcontrollers/micropython.html
重置设备时 UF2 : https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#resetting-flash-memory
注意：如果烧录了运行时的代码，导致代码一直运行就无法再次烧录，此时需要重新烧录需要切换到大容量存储器模式把重置设备的UF2文件拷贝进去重启PICO后再次拷贝MicoPython UF2文件后再次重新烧录Python代码即可

#### 引脚编号
* 计数器 : GPIO2:2,GPIO2:3,GPIO2:4,GPIO2:5
* ADC引脚 : GPIO26:0/26,GPIO27:1/27,GPIO28:2/28
* PWM脉冲/数字引脚 : GPIO2:2,GPIO3:3,GPIO4:4,GPIO5:5,GPIO6:6,GPIO7:7,GPIO8:8,GPIO9:9,GPIO10:10,GPIO11:11,GPIO12:12,GPIO13:13,GPIO14:14,GPIO15:15,GPIO16:16,GPIO17:17,GPIO18:18,GPIO19:19,GPIO20:20,GPIO21:21,GPIO22:22,GPIO23:23,GPIO24:24,GPIO25:25,GPIO26:26,GPIO27:27,GPIO28:28

#### 板卡通信控制协议操作类型

* type/操作类型, 支持参数
1) IO-SET
2) PIN-READ
3) CARD-INFO
4) DIGIT-WRITE
5) DIGIT-READ
6) PWM-WRITE
7) ADC-READ
8) ADC-TEMPERATURE
9) COUNTER-READ
10) COUNTER-CLOSE

#### 设置引脚模式
* 参数一 : channel/引脚编号
* 参数二 : mode/工作模式, 支持参数(digit/adc/pwm/counter)
* 参数三 : work/引脚模式, 仅在工作模式为(digit)时生效 (DEFAULT/INPUT/OUTPUT)
* 参数四 : pull/上拉下拉电阻, 仅在工作模式为(digit/counter)时生效 (DEFAULT/PULL_UP/PULL_DOWN)
* 参数五 : freq/输出频率, 仅在工作模式为(pwm)时生效, 请直接输入频率值, 默认频率 1000hz
```
{"type":"IO-SET","channel":0,"mode":"adc"}
{"type":"IO-SET","channel":2,"mode":"counter","pull":"PULL_UP"}
{"type":"IO-SET","channel":3,"mode":"digit","work":"INPUT","pull":"PULL_UP"}
{"type":"IO-SET","channel":4,"mode":"digit","work":"OUTPUT","pull":"DEFAULT"}
{"type":"IO-SET","channel":5,"mode":"pwm","freq":1000}
```

#### 设置引脚数字信号状态
* 参数一 : channel/引脚编号
* 参数二 : signal/工作模式 , 支持参数(LOW/HIGH)
1) LOW 设置引脚输出低电平状态 
2) HIGH 设置引脚输出高电平状态 
```
{"type":"DIGIT-WRITE","channel":4,"signal":"LOW"}
{"type":"DIGIT-WRITE","channel":4,"signal":"HIGH"}
```

#### 读取引脚数字信号状态
* 参数一 : channel/引脚编号

`{"type":"DIGIT-READ","channel":3}`

#### 读取计数器，每次读取后计数器会清理零
* 参数一 : channel/引脚编号(支持引脚: 2,3,4,5)

`{"type":"COUNTER-READ","channel":2}`

#### 关闭计数器
* 参数一 : channel/引脚编号(支持引脚: 2,3,4,5)

`{"type":"COUNTER-CLOSE","channel":2}`

#### 重启板卡

`{"type":"REBOOT"}`

#### 输出PWM信号
* 参数一 : channel/引脚编号
* 参数二 : value / 0-65535 范围的数值

`{"type":"PWM-WRITE","channel":5,"value":65535}`

#### 读取模拟信号
* 参数一 : channel/引脚编号

` {"type":"ADC-READ","channel":0}`

#### 读取板载温度传感器温度

` {"type":"ADC-TEMPERATURE"}`

#### 读取可用引脚信息

`{"type":"PIN-READ"}`

#### 读取板卡信息, 版本号, 板卡名称

`{"type":"CARD-INFO"}`
