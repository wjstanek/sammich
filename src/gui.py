import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import time

REFRESH_TIME = 100


class SimpleGUI:
    data = object()

    def __init__(self):
        self.layout = [
            [sg.Text('AutoSammich')],
            [sg.Text(f'Time: \t\t'), sg.Text(key='-TIME-')],
            [sg.Text(f'Speed: \t\t'), sg.Text(key='-SPEED-')],
            [sg.Text(f'Last Message: \t'), sg.Text(key='-MSG-')],
            [sg.Text(f'Rec\'d at: \t\t'), sg.Text(key='-MSG_TIME-')],
            [sg.Button("pause"), sg.Button("resume")],
            [sg.Canvas(size=(640, 240), key='-CANVAS-')],
            [sg.Button("EXIT")],
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
                self.update_window()

        self.window.close()

    def update_window(self, data):
        # Display last time
        elapsed_time = data.get_data_dict()['time']
        self.window['-TIME-'].update(elapsed_time[-1])

        # Keep speed up to date
        speed = data.get_data_dict()['speed']
        self.window['-SPEED-'].update(speed[-1])

        # Use last known message
        msg = data.get_data_dict()['msg']
        for i in range(len(msg)):
            if msg[-i] is None:
                break
            elif msg[-i] != msg[-i-1]:
                self.window['-MSG-'].update(msg[-i])
                self.window['-MSG_TIME-'].update(elapsed_time[-i])

        self.ax.cla()
        self.ax.grid()
        if len(speed) < 100:
            self.ax.plot(range(0, len(speed)), speed, color='red')
        else:
            self.ax.plot(range(0, 100), speed[-100:], color='blue')
        self.fig_agg.draw_idle()



def draw_figure(canvas, figure, loc=(0, 20)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw_idle()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# test run
if __name__ == '__main__':

    gui = SimpleGUI()
    while True:
        time.sleep(REFRESH_TIME/1000)
