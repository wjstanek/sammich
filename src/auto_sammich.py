import gui
import data_proc
import time


class Sammich:
    data = None

    def __init__(self, fake=False) -> None:
        if fake:
            self.data = data_proc.FakeData()

    def run(self):
        pass


if __name__ == '__main__':
    # Determine if we should spoof data or not
    fake_data = None
    while fake_data not in ['y', 'n']:
        fake_data = input("Use fake data? y/n: ")

    if fake_data == 'y':
        print("\t...loading Sammich with FAKE data inputs.")
        sammich = Sammich(fake=True)
    else:
        print("\t...loading Sammich with REAL data inputs.")

    sammich.run()
