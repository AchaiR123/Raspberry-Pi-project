import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
import ctypes
import platform
import os

combinations = [
    {'keyCombination': 'Ctrl+Shift+H', 'filePath': 'popup.html'}
]

VK_CODE = {
    'CTRL': 0x11,
    'SHIFT': 0x10,
    'ALT': 0x12,
    'CAPS_LOCK': 0x14,
    'SPACE': 0x20,
    'PAGE_UP': 0x21,
    'PAGE_DOWN': 0x22,
    'END': 0x23,
    'HOME': 0x24,
    'LEFT_ARROW': 0x25,
    'UP_ARROW': 0x26,
    'RIGHT_ARROW': 0x27,
    'DOWN_ARROW': 0x28,
    'INSERT': 0x2D,
    'DELETE': 0x2E,
    'F1': 0x70,
    'F2': 0x71,
    'F3': 0x72,
    'F4': 0x73,
    'F5': 0x74,
    'F6': 0x75,
    'F7': 0x76,
    'F8': 0x77,
    'F9': 0x78,
    'F10': 0x79,
    'F11': 0x7A,
    'F12': 0x7B,
    '`': 0xC0,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
    '0': 0x30,
    '-': 0xBD,
    '=': 0xBB,
    'BACKSPACE': 0x08,
    'TAB': 0x09,
    'Q': 0x51,
    'W': 0x57,
    'E': 0x45,
    'R': 0x52,
    'T': 0x54,
    'Y': 0x59,
    'U': 0x55,
    'I': 0x49,
    'O': 0x4F,
    'P': 0x50,
    '[': 0xDB,
    ']': 0xDD,
    '\\': 0xDC,
    'A': 0x41,
    'S': 0x53,
    'D': 0x44,
    'F': 0x46,
    'G': 0x47,
    'H': 0x48,
    'J': 0x4A,
    'K': 0x4B,
    'L': 0x4C,
    ';': 0xBA,
    "'": 0xDE,
    'Z': 0x5A,
    'X': 0x58,
    'C': 0x43,
    'V': 0x56,
    'B': 0x42,
    'N': 0x4E,
    'M': 0x4D,
    ',': 0xBC,
    '.': 0xBE,
    '/': 0xBF,
    'ENTER': 0x0D,
    'ESC': 0x1B,
    'NUM_LOCK': 0x90,
    'NUMPAD0': 0x60,
    'NUMPAD1': 0x61,
    'NUMPAD2': 0x62,
    'NUMPAD3': 0x63,
    'NUMPAD4': 0x64,
    'NUMPAD5': 0x65,
    'NUMPAD6': 0x66,
    'NUMPAD7': 0x67,
    'NUMPAD8': 0x68,
    'NUMPAD9': 0x69,
    'NUMPAD_MULTIPLY': 0x6A,
    'NUMPAD_ADD': 0x6B,
    'NUMPAD_SUBTRACT': 0x6D,
    'NUMPAD_DECIMAL': 0x6E,
    'NUMPAD_DIVIDE': 0x6F,
    'NUMPAD_ENTER': 0x0D,
    'SCROLL_LOCK': 0x91,
}

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        if self.path == '/update_combinations':
            global combinations
            combinations = data.get('combinations', [])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'updated'}).encode())
            return

        if 'file_path' in data:
            file_path = data['file_path']
            self.open_application(file_path)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode())
            return

        self.send_response(400)
        self.end_headers()
        self.wfile.write(b'Invalid request')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    @staticmethod
    def open_application(application_path):
        try:
            if platform.system() == 'Windows':
                if os.path.isfile(application_path):
                    os.startfile(application_path)
                else:
                    subprocess.Popen(['start', '', application_path], shell=True)
            else:
                subprocess.Popen(['xdg-open', application_path])
        except Exception as e:
            print("Error:", e)

    @classmethod
    def check_key_combination(cls):
        while True:
            for combo in combinations:
                keys = combo['keyCombination'].upper().split('+')
                if all(ctypes.windll.user32.GetAsyncKeyState(VK_CODE[key]) & 0x8000 for key in keys):
                    cls.open_application(combo['filePath'])
                    break

            # Sleep to avoid repeated triggering
            ctypes.windll.kernel32.Sleep(200)

class ContinuousServer(HTTPServer):
    def __init__(self, server_address, handler_class):
        super().__init__(server_address, handler_class)

    def run(self):
        print('Starting server...')
        self.serve_forever()

def run_server():
    server = ContinuousServer(('localhost', 8000), RequestHandler)
    key_check_thread = threading.Thread(target=RequestHandler.check_key_combination)
    key_check_thread.start()
    server.run()

if __name__ == '__main__':
    run_server()
