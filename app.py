from time import sleep, time as now
from functools import wraps

from flask import Response, render_template, Flask


FRAMES_PER_SECOND = 3
SLEEP_TIME = 1.0 / FRAMES_PER_SECOND

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen(func, *args, **kwargs):
    @wraps(func)
    def _():
        return Response(func(*args, **kwargs),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    return _


@app.route('/video_feed')
@gen
def video_feed():
    camera = Camera()

    while 1:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        sleep(SLEEP_TIME)


class Camera(object):
    IMAGE_COUNT = 30

    def __init__(self):
        self.frames = [open('images/%d.png' % f, 'rb').read()
                       for f in range(self.IMAGE_COUNT)]

    def get_frame(self):
        return self.frames[int(now() * FRAMES_PER_SECOND) % self.IMAGE_COUNT]


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
