import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import math
import time
import threading

REFRESH_TIME = 100


class Data:
    speed = [float(0)]
    init_time = time.time()

    def update(self):
        self.speed.append(
            1-math.cos(time.time())
        )
        print(self.speed[-1])


class SimpleGUI:
    data = object()

    def __init__(self):
        self.layout = [
            [sg.Text('AutoSammich')],
            [sg.Text(f'Speed: \t'), sg.Text(key='-SPEED-')],
            [sg.Button("pause"), sg.Button("resume")],
            [sg.Canvas(size=(640, 240), key='-CANVAS-')]
        ]
        self.window = sg.Window('AUTOSAMMICH', self.layout, finalize=True)

        canvas_elem = self.window['-CANVAS-']
        canvas = canvas_elem.TKCanvas

        fig = Figure()
        self.ax = fig.add_subplot(111)
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Speed")
        self.ax.grid()
        self.fig_agg = draw_figure(canvas, fig)

    def run(self):
        paused = False
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == 'pause':
                paused = True
            elif event == 'resume':
                paused = False
            if not paused:
                self._update_window()

        self.window.close()

    # def _get_new_data(self):
    #     self.speed.append(round(1-math.cos(time.time()), 2))

    def _update_window(self):
        self.window['-SPEED-'].update(self.data.speed[-1])
        self.ax.cla()
        self.ax.grid()
        if len(self.speed) < 100:
            self.ax.plot(range(0, len(self.speed)), self.speed, color='red')
        else:
            self.ax.plot(range(0, 100), self.speed[-100:], color='blue')
        self.fig_agg.draw()


def draw_figure(canvas, figure, loc=(0, 20)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# test run
if __name__ == '__main__':

    data = Data()
    gui = SimpleGUI()
    gui_thread = threading.Thread(target=gui.run, name='gui')
    gui_thread.start()
    while True:
        data.update()
        gui.data = data
        time.sleep(REFRESH_TIME/1000)
