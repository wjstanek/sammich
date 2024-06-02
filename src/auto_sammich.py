import gui
import data_proc
import time
import PySimpleGUI as sg
from obdii_logger import OBDIILogger


class Sammich:
    data = None
    processes = []

    def __init__(self, fake=False) -> None:
        if fake:
            self.data = data_proc.FakeData()

        # self.mygui = gui.SimpleGUI()

    def run(self):
        paused = False
        while True:
            self.data.update()
            event, values = self.mygui.window.read(timeout=100)
            if event in (None, 'EXIT', sg.WIN_CLOSED):
                break
            elif event == 'pause':
                paused = True
            elif event == 'resume':
                paused = False
            if not paused:
                self.mygui.update_window(self.data)

        self._cleanup()

    def _cleanup(self):
        self.mygui.window.close()


if __name__ == '__main__':
    # Determine if we should spoof data or not
    fake_data = None
    while fake_data not in ['y', 'n']:
        fake_data = input("Use fake data? y/n: ")

    if fake_data == 'y':
        print("\t...loading Sammich with FAKE data inputs.")
        sammich = Sammich(fake=True)
    else:
        print("\t...loading Sammich with REAL data inputs. PLACEHOLDER.")

    sammich.run()
