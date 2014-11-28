from time import time as now

from flask import Response, render_template, Flask


app = Flask(__name__)


class Camera(object):
    IMAGE_COUNT = 30

    def __init__(self):
        self.frames = [open('images/%d.png' % f, 'rb').read()
                       for f in range(self.IMAGE_COUNT)]

    def get_frame(self):
        return self.frames[int(now()) % self.IMAGE_COUNT]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
