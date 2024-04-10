from time import time


class BaseData:
    # units: MPH
    speed = [
        [
            time(),
            float(0)
        ],
    ]

    # units: rad
    wheel_angle = [
        [float(0)],
        [float(0)],
    ]

    # units: %
    throttle = [
        [float(0)],
        [float(0)],
    ]

    # units: %
    brake = [
        [float(0)],
        [float(0)],
    ]

    msgs = [
        [float(0)],
        [str(None)],
    ]

    data_dict = {
        'speed': speed,
    }

    def __init__(self):
        print("Data initialized!")
        for item in self.data_dict:
            print(f"\t{item}: {self.data_dict[item][0][1]}")


class FakeData(BaseData):

    def update(self):
        update_time = time()

        # linear speed to 5mph
        last_known_time = self.speed[-1][0]
        last_known_speed = self.speed[-1][1]
        speed_ramp_rate = 0.1   # mph / sec
        if last_known_speed < 5.0:
            interval = update_time - last_known_time
            print(interval)
            new_speed = (interval * speed_ramp_rate) + last_known_speed     # y = mx + b
            self.speed.append([update_time, new_speed])
        else:
            self.speed.append([update_time, last_known_speed])
