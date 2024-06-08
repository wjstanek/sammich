import RPi.GPIO as GPIO
import can
import time
import os
import queue
from threading import Thread

# standard OBDII PIDs
ENGINE_COOLANT_TEMP = 0x05
ENGINE_RPM = 0x0C
VEHICLE_SPEED = 0x0D
MAF_SENSOR = 0x10
O2_VOLTAGE = 0x14
THROTTLE_POSITION = 0x11    # verified on Subaru
ACCELERATION = 0x23
STEERING = 0x25
BRAKING = 0x30
SHIFT_LEVER = 0x540
GAS_GAUGE = 0x5A4

PID_REQUEST = 0x7DF
PID_REPLY = 0x7E8

pids = [
    ENGINE_RPM,
    VEHICLE_SPEED,
    THROTTLE_POSITION,
    #ACCELERATION,
    #STEERING,
    #BRAKING,
    #SHIFT_LEVER,
    #GAS_GAUGE
]


class OBDIILogger:
    ledpin = 22
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(ledpin, GPIO.OUT)
    GPIO.output(ledpin, True)

    bus = None
    log_name = f"log{time.strftime('%Y_%m_%d_%H%M', time.gmtime())}.txt"
    outfile = open(f'{log_name}', 'w')
    thread_queue = queue.Queue()
    runtime = 0
    runtime_counter = 0

    def can_rx_task(self):
        print("Starting can_rx_task...")
        while True:
            try:
                message = self.bus.recv()
            except can.CanError as err:
                print(f"Failed can_rx_task: {err=}, {type(err)=}")
            if message.arbitration_id == PID_REPLY:
                self.thread_queue.put(message)

    def can_tx_task(self):
        print("Starting can_tx_task...")
        while True:
            GPIO.output(self.ledpin, True)
            for pid in pids:
                self.send_request(pid)
                time.sleep(0.05)
            GPIO.output(self.ledpin, False)
            time.sleep(0.1)

    def send_request(self, pid):
        msg = can.Message(check=True,
                          arbitration_id=PID_REQUEST,
                          data=[0x02, 0x01, pid, 0x00, 0x00, 0x00, 0x00, 0x00],
                          is_extended_id=False)
        try:
            self.bus.send(msg)
        except can.CanError as err:
            print(f"Failed to send request: {err=}, {type(err)=}")
        except OSError as err:
            print(f"Failed to send request: {err=}, {type(err)=}")

    def __init__(self):
        print('\n\rCAN Rx test')
        print('Bring up CAN0....')

        # Bring up can0 interface at 500kbps
        os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
        time.sleep(0.1)
        print('Ready')

        try:
            self.bus = can.Bus(channel='can0', interface='socketcan')
        except OSError:
            print('Cannot find PiCAN board.')
            GPIO.output(self.ledpin, False)
            exit()

    def run(self):
        rx_thread = Thread(target=self.can_rx_task)
        rx_thread.start()
        tx_thread = Thread(target=self.can_tx_task)
        tx_thread.start()

        self.runtime = time.time()

        try:
            while True:
                value = None
                while self.thread_queue.empty():
                    pass
                message = self.thread_queue.get()

                line_header = '{0:.4f},{1:f},'.format(message.timestamp, message.data[2])
                if message.arbitration_id == PID_REPLY:
                    value = self.convert(message.data[2], message.data[3])

                #line_out = line_header + str(value)
                line_out = f"{message.timestamp}, {message.data[0]}, {message.data[1]}, {message.data[2]}, {message.data[3]}, {message.data[4]}, {message.data[5]}"
                print(line_out, file=self.outfile)
                self.busy_signal()

        except KeyboardInterrupt:
            GPIO.output(self.ledpin, False)
            self.outfile.close()
            os.system("sudo /sbin/ip link set can0 down")
            print("Caught keyboard interrupt")
            rx_thread.join()
            tx_thread.join()
            return

    @staticmethod
    def convert(pid_found, data):
        #if pid_found == THROTTLE_POSITION:
        #    # return round((data*100/255), 2)
        #    print("Received THROTTLE_POSITION: {data}")
        #    return data
        #else:
        #    return data
        return data

    def busy_signal(self):
        os.system("echo -e \"\\033[2K\"")
        if self.runtime - self.runtime_counter > 1.0:
            print("...")
            self.runtime_counter = time.time()
        elif self.runtime - self.runtime_counter > 0.5:
            print("..")
        elif self.runtime - self.runtime_counter > 0.1:
            print(".")
        else:
            pass
        self.runtime = time.time()


if __name__ == '__main__':
    obdlogger = OBDIILogger()
    obdlogger.run()
