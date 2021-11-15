# MIT License

# Copyright (c) 2021 悦妃云

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# website   : https://www.yfyun.xin
# bolg      : https://blog.csdn.net/u012168125
# project   : https://gitee.com/yfyun/raspberry-pico-expand-card

import json
import utime
import machine as Pico

class card:
    def __init__(self) -> None:
        self.cmd = ''
        self.adc = {}
        self.pwm = {}
        self.digit = {}
        self.stTime = utime.time()
        self.counter = {2:-1,3:-1,4:-1,5:-1}
        self.uart0 = Pico.UART(0, baudrate=115200, tx=Pico.Pin(0), rx=Pico.Pin(1))
        self.irqfunc = {2:self.COUNTER_GPIO2,3:self.COUNTER_GPIO3,4:self.COUNTER_GPIO4,5:self.COUNTER_GPIO5}

    def loop(self) -> None:
        try : 
            if self.uart0.any() > 0 :
                self.cmd += str(self.uart0.read(),'utf-8')
                try : 
                    cmd = json.loads(self.cmd)
                    self.executionTask(cmd)
                    self.cmd = ''
                except Exception as msg: pass

            if (utime.time() - self.stTime) > 0.015 and self.cmd != '' : 
                self.cmd = ''
                self.stTime = utime.time()
        except Exception as msg : pass

    def print(self,cmd:str):
        self.uart0.write(cmd)

    def println(self,cmd:dict):
        self.uart0.write(json.dumps(cmd).replace(' ','') + '\r\n')

    def ConverInt(self,value,Evalue = -1)->int:
        if value == None : return Evalue
        try : return int(value)
        except : return Evalue

    def COUNTER_GPIO2(self,pin) : 
        if self.counter[2] < 0 : return
        self.counter[2] += 1
    
    def COUNTER_GPIO3(self,pin) : 
        if self.counter[3] < 0 : return
        self.counter[3] += 1

    def COUNTER_GPIO4(self,pin) : 
        if self.counter[4] < 0 : return
        self.counter[4] += 1

    def COUNTER_GPIO5(self,pin) : 
        if self.counter[5] < 0 : return
        self.counter[5] += 1

    def executionTask(self,cmd:dict):
        mType = cmd.get('type')
        if mType == None : return

        if  mType == 'CARD-INFO' : 
            self.println({'type':mType,'name':'ExpandingBoard - rpi pico','version':'1.0','website':'www.yfyun.xin'})
        elif mType ==  'REBOOT' : 
            self.println({'type':mType,'status':'OK'})
            Pico.reset()
        elif mType == 'IO-SET' :
            mChannel = self.ConverInt(cmd.get('channel'))
            mMode = cmd.get('mode')
            if mChannel == -1 or mMode == None : return
            if mMode.lower() == 'digit' :
                mWork = cmd.get('work')
                mPull = cmd.get('pull')
                if mWork == None : mWork = 'DEFAULT'
                if mPull == None : mPull = 'DEFAULT'
                mWorkRef = {'DEFAULT':-1,'INPUT':Pico.Pin.IN,'OUTPUT':Pico.Pin.OUT}
                mPullRef = {'DEFAULT':-1,'PULL_UP':Pico.Pin.PULL_UP,'PULL_DOWN':Pico.Pin.PULL_DOWN}
                self.digit[mChannel] = Pico.Pin(mChannel,mWorkRef.get(mWork),mPullRef.get(mPull))
                self.println({'type':mType,'channel':mChannel,'mode':mMode,'work':mWork,'pull':mPull})
            elif mMode.lower() == 'adc' :
                self.adc[mChannel] = Pico.ADC(mChannel)
                self.println({'type':mType,'channel':mChannel,'mode':mMode})
            elif mMode.lower() == 'pwm' :
                mFreq = self.ConverInt(cmd.get('freq'),1000)
                self.pwm[mChannel] = Pico.PWM(Pico.Pin(mChannel))
                self.pwm[mChannel].freq(mFreq)
                self.println({'type':mType,'channel':mChannel,'mode':mMode,'freq':mFreq})
            elif mMode.lower() == 'counter' :
                mPull = cmd.get('pull')
                if mPull == None : mPull = 'PULL_UP'
                if self.counter[mChannel] == None or self.counter[mChannel] != -1 : return
                mPullRef = {'DEFAULT':-1,'PULL_UP':Pico.Pin.PULL_UP,'PULL_DOWN':Pico.Pin.PULL_DOWN}
                self.digit[mChannel] = Pico.Pin(mChannel,Pico.Pin.IN,mPullRef.get(mPull))
                self.digit[mChannel].irq(self.irqfunc[mChannel], Pico.Pin.IRQ_FALLING)
                self.counter[mChannel] = 0
                self.println({'type':mType,'channel':mChannel,'mode':mMode,'pull':mPull})
        elif mType == 'DIGIT-WRITE' :
            mChannel = self.ConverInt(cmd.get('channel'))
            mSignal = cmd.get('signal')
            if mChannel == -1 or mSignal == None: return
            mPin = self.digit.get(mChannel)
            if mPin == None : return
            mPin.value(1 if mSignal == 'HIGH' else 0)
            self.println({'type':mType,'channel':mChannel,'signal':mSignal})
        elif mType == 'DIGIT-READ' :
            mChannel = self.ConverInt(cmd.get('channel'))
            if mChannel == -1 : return
            mPin = self.digit.get(mChannel)
            if mPin == None : return
            self.println({'type':mType,'channel':mChannel,'signal':'HIGH' if mPin.value() == 1 else 'LOW'})
        elif mType == 'ADC-READ' : 
            mChannel = self.ConverInt(cmd.get('channel'))
            if mChannel == -1 : return
            mADC = self.adc.get(mChannel)
            if mADC == None : return
            self.println({'type':mType,'channel':mChannel,'value':Pico.ADC(mChannel).read_u16()})
        elif mType == 'ADC-TEMPERATURE' : 
            mTemp = Pico.ADC(4).read_u16() * (3.3 / 65535)
            mTemp = round(27 - (mTemp - 0.706) / 0.001721,2)
            self.println({'type':mType,'temperature':mTemp})
        elif mType == 'PWM-WRITE' : 
            mChannel = self.ConverInt(cmd.get('channel'))
            mValue = self.ConverInt(cmd.get('value'),-1)
            if mChannel == -1 or mValue == -1 : return
            if self.pwm.get(mChannel) == None : return
            self.pwm[mChannel].duty_u16(mValue)
            self.println({'type':mType,'channel':mChannel,'value':mValue})
        elif mType == 'COUNTER-READ' :
            mChannel = self.ConverInt(cmd.get('channel'))
            if mChannel == -1 : return
            if self.counter[mChannel] == None : return
            mValue = self.counter[mChannel]
            if mValue > -1 : self.counter[mChannel] = 0
            self.println({'type':mType,'channel':mChannel,'value':mValue})
        elif mType == 'COUNTER-CLOSE' :
            mChannel = self.ConverInt(cmd.get('channel'))
            if mChannel == -1 : return
            if self.counter[mChannel] == None : return
            self.digit[mChannel].irq(handler=None)
            self.println({'type':mType,'channel':mChannel})
            self.counter[mChannel] = -1
        elif mType == 'PIN-READ':
            mPin = {'type':mType}
            mPin['counter'] = 'GPIO2:2,GPIO2:3,GPIO2:4,GPIO2:5'
            mPin['adc'] = 'GPIO26:0/26,GPIO27:1/27,GPIO28:2/28'
            mPin['digital/pwm'] = 'GPIO2:2,GPIO3:3,GPIO4:4,GPIO5:5,GPIO6:6,GPIO7:7,GPIO8:8,GPIO9:9,GPIO10:10,GPIO11:11,GPIO12:12,GPIO13:13,GPIO14:14,GPIO15:15,GPIO16:16,GPIO17:17,GPIO18:18,GPIO19:19,GPIO20:20,GPIO21:21,GPIO22:22,GPIO23:23,GPIO24:24,GPIO25:25,GPIO26:26,GPIO27:27,GPIO28:28'
            self.println(mPin)

def run_main():
    """ 正常使用时切换到此方法 """
    Pico.Pin(25, Pico.Pin.OUT).value(1)
    run = card()
    while True : run.loop()

def run_debug():
    """ DEBUG 使用，启动后运行指定时长 """
    state = False
    led = Pico.Pin(25, Pico.Pin.OUT)
    
    run = card()
    sTtime = utime.time()
    ruTime = utime.time()
    while utime.time() - ruTime < 60 : # 运行 60 秒
        run.loop()
        if utime.time() - sTtime > 0.2 : 
            led.value(0 if state else 1)
            sTtime = utime.time()
            state = not state

if __name__ == '__main__' : 
    """ 程序入口 """
    run_main()