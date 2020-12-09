import queue
import time
import threading
import random
import board
import adafruit_ws2801
from flask import Flask, render_template, request, jsonify


NUM_LEDS = 25
leds = adafruit_ws2801.WS2801(board.SCK, board.MOSI, NUM_LEDS, brightness=1.0, auto_write=False)


q = queue.Queue()

def queue_worker():
    while True:
        print("Queue size: %d" % q.qsize())

        item = q.get()
        leds.fill(item)
        leds.show()

        q.task_done()

        time.sleep(1)

threading.Thread(target=queue_worker, daemon=True).start()

COLOURS = {
    "Red": 0xff0000,
    "Green": 0x00ff00,
    "Blue": 0x0000ff,
    "White": 0xffffff,
    "Orange": 0xff6600,
    "Off": 0x000000,
}

def talkback(colour):
    if colour == "Off":
        return "calm down grinch"

    return random.choice([
        "snazzy", "weird flex but ok", "yup",
    ])

app = Flask(__name__)

@app.route("/")
def ui():
    return render_template("app.html", colours=COLOURS.keys())


@app.route("/colour", methods=["POST"])
def colour():
    data = request.json
    if "colour" not in data:
        return jsonify(error="don't try me"), 400

    name = data["colour"]

    if name not in COLOURS:
        return jsonify(error="%s!? %s ain't no colour i ever heard of" % (name.upper(), name)), 400

    colour = COLOURS[name]
    q.put_nowait(colour)

    # Dark magic: format hexadecimal to fixed length
    colour_hex = "{0:#0{1}x}".format(colour, 8)[2:]
    return jsonify(success=talkback(name), colour=colour_hex)
