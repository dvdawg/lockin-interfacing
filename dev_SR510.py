from measurement_device import measurementDevice
import serial
import subprocess
import time

class devSR510(measurementDevice):

    """ 
        An interface for the SR510 lock in amplifier.
    """
    time_const_settings = {
        1: 0.001,
        2: 0.003,
        3: 0.01,
        4: 0.03,
        5: 0.1,
        6: 0.3,
        7: 1,
        8: 3,
        9: 10,
        10: 30,
        11: 100
    }
    
    def __init__(self, device=None):
        """
            Defining device parameters based on the argument dev_params.

            Args:
            dev_params (dictionary): Dictionary containing the necessary
            parameters to initialize to this device (ie. GPIB address,
            device name, etc.)
        """ 
        self.device = serial.Serial('/dev/tty.usbserial-AB0OJP1V', timeout=5)
        return
    
    def command(self, command):
        """
            Get the values we want from the lock in amplifier (the R
            and theta values) with units.

            R - amplitude of the signal
            theta - phase of the signal

            Returns:
            dict: A dictionary containing the most recent values from
            the instrument and their units. 
        """
        # #if len(command) > 1:
        # #    self.close()
        # #    screen_device = '/dev/tty.usbserial-AB0OJP1V' + self.device.baudrate
        # #    screen_process = subprocess.Popen(['screen', screen_device])
        # #    time.sleep(1) 
        # #    subprocess.run(['screen', '-S', 'screen_session', '-X', 'my device', 'M'])
        # #    time.sleep(1)
        # #    subprocess.run(['screen', '-S', 'screen_session', '-X', 'quit'])
        # #    self.connect()
        # #    return None
        command = command + '\r'
        self.device.write(command.encode('ASCII'))
        response = b''
        while True:
            byte = self.device.read()
            if byte == b'\r':
                break
            response += byte

        return response.decode('ASCII')


        # command = command + '\r'
        # self.device.write(command.encode('utf-8'))
        
        # response = b''
        # while True:
        #     byte = self.device.read(1)
        #     if byte == b'\r':
        #         break
        #     response += byte
        
        # return response.decode('utf-8').strip()

        """
            The following is a sample dictionary that should be returned

            sample = {
                "temperature":
                {
                    "Value": 100,
                    "Units": "degC"
                }
            }            
        """
    def parse_data(self, data):
        if data.__contains__('E'):
            number, exponent = data.split("E")
            return float(number) * (10 ** int(exponent))

    def close(self):
        self.device.close()

    def get_time_const(self):
        return self.time_const_settings[int(self.command('T 1'))]
    
    def get_ref_freq(self):
        return self.parse_data(self.command('F'))
    
    def get_X(self):
        self.command('S 1')
        return self.parse_data(self.command('Q'))
    
    def set_phase(self, phase):
        self.command('P' + str(phase))

    def change_ref_phase(self, phi):
        self.command(f'P {phi}')
        return self.parse_data(self.command('P'))
    
    def set_gain(self, gain):
        return self.command('G' + str(gain))
    
    def overload(self) -> bool:
        """
        Returns whether or not the lock-in amplifier is overloaded.
        """
        self.command('Y4')
    
    def auto_adjust_sensitivity(self, delay=10) -> int:
        """
        Automatically adjust the sensitivity of the lock-in amplifier to the setting just before
        overloading, allowing maximal sensitivity.
        """
        n = int(self.command(f'G'))
        while not self.overload():
            self.command(f'G {n + 1}')
            time.sleep(delay)
            n += 1
        self.command(f'G {n}')
        return int(self.command('G'))


# test

if __name__ == "__name__":
    instance = devSR510('/dev/cu.usbserial-AB0OJP1V')
    print(instance.command('M 1'))