# this is python 3.12.3
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
import ctypes
 
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        if 'file_path' in data:
            file_path = data['file_path']
            self.open_application(file_path)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode())
            return
 
        if 'help_menu' in data and data['help_menu']:
            self.display_help_menu()
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
            subprocess.Popen(application_path, shell=True)
        except Exception as e:
            print("Error:", e)
 
    @staticmethod
    def display_help_menu():
        help_text = """\
        Command Menu:
        
        1. Ctrl + Alt + Shift + P - Open PowerPoint
        2. Ctrl + Alt + Shift + W - Open Word
        3. Ctrl + Alt + Shift + X - Open Excel
        """
        ctypes.windll.user32.MessageBoxW(0, help_text, "Command Menu", 0)
 
    @classmethod
    def check_key_combination(cls):
        VK_CONTROL = 0x11
        VK_SHIFT = 0x10
        VK_F1 = 0x70
        VK_P = 0x50
        VK_W = 0x57
        VK_X = 0x58
 
        while True:
            if (ctypes.windll.user32.GetAsyncKeyState(VK_CONTROL) & 0x8000) \
                and (ctypes.windll.user32.GetAsyncKeyState(VK_SHIFT) & 0x8000) \
                and (ctypes.windll.user32.GetAsyncKeyState(VK_F1) & 0x8000):
                cls.display_help_menu()
 
            elif (ctypes.windll.user32.GetAsyncKeyState(VK_CONTROL) & 0x8000) \
                and (ctypes.windll.user32.GetAsyncKeyState(VK_SHIFT) & 0x8000) \
                and (ctypes.windll.user32.GetAsyncKeyState(VK_P) & 0x8000):
                cls.open_application(r'')#change to file dir
 
            elif (ctypes.windll.user32.GetAsyncKeyState(VK_CONTROL) & 0x8000) \
                and (ctypes.windll.user32.GetAsyncKeyState(VK_SHIFT) & 0x8000) \
                and (ctypes.windll.user32.GetAsyncKeyState(VK_W) & 0x8000):
                cls.open_application(r'')#change to file dir
 
            elif (ctypes.windll.user32.GetAsyncKeyState(VK_CONTROL) & 0x8000) \
                and (ctypes.windll.user32.GetAsyncKeyState(VK_SHIFT) & 0x8000) \
                and (ctypes.windll.user32.GetAsyncKeyState(VK_X) & 0x8000):
                cls.open_application(r'')#change to file dir
 
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
