from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from random import random, randint
from time import sleep
from threading import Thread, Event
from scraper import Scraper
import datetime as dt


CANVAS_X = 1000
CANVAS_Y = 1000
COLOR_LIMIT = 250

app = Flask(__name__)
socketio = SocketIO(app)

thread = Thread()
thread_stop_event = Event()


@app.route('/')
def hello():
    return render_template('visualisation.html', name='Test')


class StreamThread(Thread):
    
    # This class grabs our data from the Scraper class, puts it in a queue for delivery. 
    def __init__(self):
        self.time_delay = 5
        self.selection = 10
        super(StreamThread, self).__init__()

    def text_generator(self):
        # Generate a list first
        while not thread_stop_event.isSet():
            text = Scraper('George Floyd', self.selection, dt.date.today() - dt.timedelta(weeks=2)).get_text()[randint(0, self.selection-1)]
            data = {'text': text,
                    'number_1': round(random() * CANVAS_X, 3),
                    'number_2': round(random() * CANVAS_Y, 3),
                    'c_1': round(random() * COLOR_LIMIT, 3),
                    'c_2': round(random() * COLOR_LIMIT, 3),
                    'c_3': round(random() * COLOR_LIMIT, 3)}
            socketio.emit('textoutput', data, namespace='/test')
            sleep(self.time_delay)

    def position_generator(self):
        pass

    def run(self):
        self.text_generator()

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random stream generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = StreamThread()
        thread.start()


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
