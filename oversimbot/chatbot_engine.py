# encoding: utf-8
from http.server import BaseHTTPRequestHandler, HTTPServer
from oversimbot.core import chat_tracker
import cgi

chatTracker = chat_tracker.ChatTracker()

class OversimbotRestHTTPRequestHandler(BaseHTTPRequestHandler):



    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write("Šeškas".encode("utf-8"))
        return

    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile,
                           headers=self.headers, environ={
                                'REQUEST_METHOD':'POST',
                                'CONTENT_TYPE':self.headers['Content-Type']
                           })
        message = form['message'].value
        response_list = chatTracker.find_response(message)
        response = "\n".join(response_list)
        print("[oversimbotRestHTTPRequestHandler]message {}->{}".format(message, response))
        self.send_response(201)
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))
        return



if __name__ == '__main__':
    httpd = HTTPServer(('0.0.0.0', 8000), OversimbotRestHTTPRequestHandler)
    try:
        print("Preparing...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
