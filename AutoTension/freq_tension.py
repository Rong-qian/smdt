#
# sMDT wiring station internal tension measurement
# Reads wave function from the wire at the tensioning station and then does a Fourier transform to obtain
# the frequency at which the wire is vibrating. Then convert that to wire tension.
#
#   Modifications:
#   
#   2023-07, Rongqian: fix the bug in fft peak searching. The FFT function returns the frequency in complex number.
#                      The complex number's modulu is used in searching for the first resonance peak now.
#

import nidaqmx
import time
import pprint
from nidaqmx.constants import TerminalConfiguration, AcquisitionType
from scipy import fftpack
import numpy as np
import time
import matplotlib.pyplot as plt
from time import gmtime, strftime, localtime
class FourierTension:
    def __init__(self,
                ai_channel_name="Dev1/ai0",
                do_channel_name="Dev1/port1/line0",
                sampling_time = 5,
                rate = 5000,
                linear_density = 38.8,
                wire_length = 374.7):
        self.wvf_task = nidaqmx.Task()
        self.ctrl_task = nidaqmx.Task()
        self.wvf_task.ai_channels.add_ai_voltage_chan(ai_channel_name, min_val=-10, max_val=10, terminal_config=TerminalConfiguration.RSE)
        self.wvf_task.timing.cfg_samp_clk_timing(rate=rate, sample_mode=AcquisitionType.FINITE, samps_per_chan=sampling_time * rate)
        self.ctrl_task.do_channels.add_do_chan("Dev1/port1/line0")
        #self.wvf_task.start()
        #self.ctrl_task.start()

        self.sampling_time = sampling_time
        self.rate = rate
        self.linear_density = linear_density
        self.wire_length = wire_length

    #def __del__(self):
    #    self.wvf_task.stop()
    #    self.ctrl_task.stop()

    def get_tension(self):
        self.ctrl_task.write(False)
        time.sleep(3)
        self.ctrl_task.write(True)

        data = self.wvf_task.read(number_of_samples_per_channel=self.sampling_time * self.rate)

        X = fftpack.fft(data)
        # Change time multiplyer after sampling_time can change the window used to search the first resonance peak. Make shure the 1st and 3rd multiplyer is the same.
        frequency = (np.argmax(abs(X)[self.sampling_time * 10: self.sampling_time * 600]) + self.sampling_time * 10) / self.sampling_time
        ### The frequency spectrum 
        #plt.plot((np.linspace(0,len(X)- 1,len(X))) / self.sampling_time, abs(X)) 
        #plt.show() 
        #plt.savefig("FFT_spectrum/667_"+str(frequency)+"_"+str(strftime("%H-%M-%S", localtime()))+".png")
        #plt.close()
        tension = ((((((self.wire_length - 28) / 1000) ** 2) * (self.linear_density / 1000000)) * 4) * (frequency ** 2)) / 0.0098
        print("frequency is:", frequency, ",tension is:", tension)
        return round(tension,2), round(frequency,1)

    def get_tension_test(self):
        self.ctrl_task.write(False)
        time.sleep(3)
        self.ctrl_task.write(True)

        data = self.wvf_task.read(number_of_samples_per_channel=self.sampling_time * self.rate)

        X = fftpack.fft(data)


        frequency = (np.argmax(np.abs(X)[self.sampling_time * 10: self.sampling_time * 600]) + self.sampling_time * 10) / self.sampling_time

        #plt.plot((np.linspace(0,len(X)- 1,len(X))) / self.sampling_time, X) 
        #plt.show() 
        #plt.savefig("FFT_spectrum/667_"+str(frequency)+"_"+str(strftime("%H-%M-%S", localtime()))+".png")
        #plt.close()
        
        tension = ((((((self.wire_length - 28) / 1000) ** 2) * (self.linear_density / 1000000)) * 4) * (frequency ** 2)) / 0.0098
        print("frequency is:", frequency, ",tension is:", tension)
        return round(tension,2), round(frequency,1) , np.abs(X)       


if __name__ == "__main__":
    ft = FourierTension()
    for i in range(5):
        time.sleep(2)
        print(ft.get_tension()[0])
