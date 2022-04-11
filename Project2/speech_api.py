from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from scipy.io.wavfile import write
from rq import Queue
import wave
import redis
import os
import subprocess
import numpy as np
import werkzeug
import time

app = Flask(__name__)
r = redis.Redis()
q = Queue(connection = r)

def speech_to_text_task(filename):
    Mozilla_pretrained_model()
    output = predict(filename)
    time.sleep(2)
    print(output)
    return output

@app.route("/task", methods = ['POST'])
def add_task():
    parse = reqparse.RequestParser()
    parse.add_argument('audio', type=werkzeug.datastructures.FileStorage, location='files')
    args = parse.parse_args()
    # print(args)
    name = args["audio"].filename
    stream = args['audio'].stream
    try:
        wav_file = wave.open(stream, 'rb')
    except Exception:
        return f'Error! No wav file named {name}. Please post the whole name with .wav'
    signal = wav_file.readframes(-1)
    signal = np.frombuffer(signal, np.int16)
    fr = wav_file.getframerate()
    wav_file.close()
    save_name = f'./client_{name}.wav'
    save_file = open(f'./{save_name}','wb')
    write(save_file, fr, signal)
    save_file.close()
    from speech_api import speech_to_text_task
    job = q.enqueue(speech_to_text_task, save_name)
    q_len = len(q)
    return f'Task {job.id} added to queue at {job.enqueued_at}. {q_len} tasks in the queue.'

def Mozilla_pretrained_model():
    if not os.path.exists('deepspeech-0.9.3-models.scorer'):
        os.popen('curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer')
    if not os.path.exists('deepspeech-0.9.3-models.pbmm'):
        os.popen('curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm')

def predict(name):
    retcode, str = subprocess.getstatusoutput(f'deepspeech --model deepspeech-0.9.3-models.pbmm --scorer deepspeech-0.9.3-models.scorer --audio {name}')
    output = str.split('\n')
    if retcode == 0:
        return output[-1]
    else:
        return f"Error! No file called {name}."

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug = True)
