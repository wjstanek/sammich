from time import time
import random


class BaseData:
    init_time = time()

    raw_data = []

    def __init__(self):
        self._update_raw_data(self._time_since_init(), 0, 'init')
        print("Data initialized!")
        print(self.raw_data)

    def _time_since_init(self):
        current_time = time()
        return current_time - self.init_time

    def _update_raw_data(self, elapsed_time: float, speed: float, msg: str):
        raw_data_string = f"{round(elapsed_time, 3)} {speed} {msg}"
        self.raw_data.append(raw_data_string)

    def get_data_dict(self):
        time_list = []
        speed_list = []
        msg_list = []
        data_dict = {}
        for line in self.raw_data:
            time_list.append(
                float(
                    line.split(" ", 2)[0]
                )
            )
            speed_list.append(
                float(
                    line.split(" ", 2)[1]
                )
            )
            msg_list.append(line.split(" ", 2)[2])
        data_dict['time'] = time_list
        data_dict['speed'] = speed_list
        data_dict['msg'] = msg_list
        return data_dict


class FakeData(BaseData):
    ramp_up = True

    def update(self):
        update_time = self._time_since_init()

        # linear speed to 5mph
        last_known_time = self.get_data_dict()['time'][-1]
        last_known_speed = self.get_data_dict()['speed'][-1]
        speed_ramp_rate = 1   # mph / sec
        message = None
        if self.ramp_up:
            interval = update_time - last_known_time
            new_speed = (interval * speed_ramp_rate) + last_known_speed     # y = mx + b
            if new_speed >= 5.0:
                self.ramp_up = False
            self._update_raw_data(update_time, round(new_speed, 2), message)
            return
        else:
            new_speed = last_known_speed + 0.1 * random.randrange(-5, 5)
            if new_speed > 6:
                new_speed = 6
                message = "Max Speed Hit"
            elif new_speed < 3:
                new_speed = 3
                message = "Min Speed Hit"

            self._update_raw_data(update_time, round(new_speed, 2), message)
