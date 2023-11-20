
import os
import json
import time
import threading
import subprocess
import asyncio

from flask import Flask, send_from_directory, request, abort
from pixelcontrol import PixelControl
from stock import Stock
from db import Db


app = Flask(__name__)
pixels = PixelControl()
stock = Stock()
db = Db("crystalball.db")

_CONTENT_TYPE = {
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.png': 'image/png',
    '.ico': 'image/x-icon',
    '.html': 'text/html',
    '.mp3': 'adio/mpeg',
}


def ok(resp: dict):
    return json.dumps(resp), 200, {'Content-Type': 'application/json'}


def async_os_system(cmd: str):
    asyncio.ensure_future(os.system(f'sleep 1 && {cmd}'))


def run_cmd(cmd: str, capture_stdout=True, capture_stderr=True) -> str:
    stdout = subprocess.PIPE if capture_stdout else None
    stderr = subprocess.PIPE if capture_stderr else None
    process = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, shell=True)
    process.wait()
    if process.returncode:
        raise Exception(f'command {cmd} failed with exit code {process.returncode}')
    if capture_stdout:
        return str(process.communicate()[0].strip(), 'UTF-8')


@app.route('/')
def serve_index():
    return send_from_directory('www', 'index.html')


@app.route('/<path:path>')
def static_files(path):
    mime_type = _CONTENT_TYPE.get(os.path.splitext(path)[1], 'text/plain')
    if mime_type == 'text/plain':
        abort(405)
    return send_from_directory('www', path, mimetype=mime_type)


@app.route('/quips')
def quips():
    quips = [
        'animotion.mp3',
        'closing-bell.mp3',
        'deductions.mp3',
        'financial-panther.mp3',
        'financial-situation.mp3',
        'have-a-look.mp3',
        'long-term-man.mp3',
        'musk-dinner-party.mp3',
        'paid-last-years-taxes.mp3',
        'taxes-pay-stubs.mp3',
        'yahoo-quote.mp3'
    ]
    return ok({'resp': quips})


@app.route('/advice')
def advice():
    advice = [
        'aggressive-trading-stategy.mp3',
        'buy-the-dip.mp3',
        'conventional-wisdom.mp3',
        'DontBuy.mp3',
        'fix-this-myself.mp3',
        'get-out-now.mp3',
        'hell-hole.mp3',
        'higher-62-million-shares.mp3',
        'in-the-money.mp3',
        'make-the-trade.mp3',
        'move-out-banks-house.mp3',
        'opera-hat-company.mp3',
        'SELSELLSELL.mp3',
        'spread-sheet-nonsense.mp3',
        'super-duper-bankruptcy.mp3',
        'totally-insane.mp3',
        'TripleBuy.mp3',
        'we-like-the-stock.mp3',
        'what-a-good-call.mp3',
        'who-knows.mp3',
        'widthdraw-life-savings.mp3',
        'world-will-end.mp3',
        'you-chose-them.mp3',
    ]
    return ok({'resp': advice})


@app.route('/system/<command>', methods=['POST'])
def system(command):
    print(command)
    resp = f"unknown command: '{command}'"
    if command == 'uptime':
        resp = run_cmd("uptime")
    elif command == 'status':
        resp = 'awake' if db.get_awake_status() else 'asleep'
    elif command == 'reboot':
        resp = "rebooting..."
        pixels.off()
        async_os_system('sudo reboot')
    elif command == 'shutdown':
        resp = "shutdown..."
        pixels.off()
        async_os_system('sudo shutdown now')
    elif command == 'sleep':
        db.set_awake_status(0)
        pixels.off()
        resp = 'sleeping...'
    elif command == 'wake':
        db.set_awake_status(1)
        pixels.blue()
        resp = 'awake'
    return ok({'resp': resp})


@app.route('/led/<command>', methods=['POST'])
def led(command):
    print(command)
    if command == 'green':
        pixels.green()
    elif command == 'red':
        pixels.red()
    elif command == 'blue':
        pixels.blue()
    elif command == 'rainbow':
        pixels.rainbow()
    elif command == 'custom':
        rgb = request.get_json()
        print(rgb)
        command = (rgb['r'], rgb['g'], rgb['b'])
        pixels.fill(command)
    else:
        pixels.off()
    return ok({'resp': command})


@app.route('/market/<command>', methods=['POST'])
def market(command):
    print(command)
    resp = f"unknown command: '{command}'"
    if command == 'set-symbol':
        symbol = request.get_json()
        db.set_stock(symbol)
        resp = symbol
    elif command == 'check':
        symbol, date = db.get_stock()
        resp = f"{symbol} {date}"
    return ok({'resp': resp})


if __name__ == '__main__':
    pixels.blue()
    try:
        db.get_stock()
    except:
        db.set_stock("SPY")
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=80, debug=True, use_reloader=False)).start()

    while True:
        if db.get_awake_status():
            print("running")
            symbol, date = db.get_stock()
            if stock.is_symbol_up(symbol):
                pixels.green()
            else:
                pixels.red()
        else:
            print("not running")
        time.sleep(60 * 5)
