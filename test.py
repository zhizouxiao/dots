from flask import Flask

import time
import socket
from gevent.pywsgi import WSGIServer, WSGIHandler
import traceback
import errno
import sys

MAX_REQUEST_LINE = 8192
_REQUEST_TOO_LONG_RESPONSE = "HTTP/1.1 414 Request URI Too Long\r\nConnection: close\r\nContent-length: 0\r\n\r\n"
_BAD_REQUEST_RESPONSE = "HTTP/1.1 400 Bad Request\r\nConnection: close\r\nContent-length: 0\r\n\r\n"


app = Flask(__name__)
app.debug = True

@app.route("/", methods=["GET"])
def poll():
    #i = 0
    #while True:
        #i += 1
    return "hello"

class MyHandler(WSGIHandler):
    """docstring for MyHandler"""
    def handle(self):
        """docstring for hander"""
        print("handle=================", self.socket)
        try:
            while self.socket is not None:
                self.time_start = time.time()
                self.time_finish = 0
                result = self.handle_one_request()
                print("handle_one_request %s" % result)
                if result is None:
                    break
                if result is True:
                    continue
                self.status, response_body = result
                self.socket.sendall(response_body)
                if self.time_finish == 0:
                    self.time_finish = time.time()
                self.log_request()
                break
        finally:
            if self.socket is not None:
                try:
                    # read out request data to prevent error: [Errno 104] Connection reset by peer
                    try:
                        print("heeeeeeeeeeeee1")
                        self.socket._sock.recv(16384)
                        print("heeeeeeeeeeeee2")
                    finally:
                        print("heeeeeeeeeeeee3")
                        self.socket._sock.close()  # do not rely on garbage collection
                        self.socket.close()
                except socket.error:
                    pass
            self.__dict__.pop('socket', None)
            self.__dict__.pop('rfile', None)


    def handle_one_request(self):
        if self.rfile.closed:
            return
        try:
            print("handle_one_request============1", self.rfile)
            self.requestline = self.read_requestline()
            print("handle_one_request============2", self.requestline)
        except socket.error:
            # "Connection reset by peer" or other socket errors aren't interesting here
            return

        if not self.requestline:
            return

        self.response_length = 0

        if len(self.requestline) >= MAX_REQUEST_LINE:
            return ('414', _REQUEST_TOO_LONG_RESPONSE)

        try:
            # for compatibility with older versions of pywsgi, we pass self.requestline as an argument there
            if not self.read_request(self.requestline):
                return ('400', _BAD_REQUEST_RESPONSE)
        except Exception:
            ex = sys.exc_info()[1]
            if not isinstance(ex, ValueError):
                traceback.print_exc()
            self.log_error('Invalid request: %s', str(ex) or ex.__class__.__name__)
            return ('400', _BAD_REQUEST_RESPONSE)

        self.environ = self.get_environ()
        self.application = self.server.application
        try:
            self.handle_one_response()
        except socket.error:
            ex = sys.exc_info()[1]
            # Broken pipe, connection reset by peer
            if ex.args[0] in (errno.EPIPE, errno.ECONNRESET):
                sys.exc_clear()
                return
            else:
                raise

        if self.close_connection:
            return

        if self.rfile.closed:
            return

        return True  # read more requests
    def run_application(self):
        self.result = self.application(self.environ, self.start_response)
        self.process_result()

    def handle_one_response(self):
        self.time_start = time.time()
        self.status = None
        self.headers_sent = False

        self.result = None
        self.response_use_chunked = False
        self.response_length = 0

        try:
            try:
                self.run_application()
            finally:
                close = getattr(self.result, 'close', None)
                print("result %s" % self.result)
                print(close)
                self.socket.close()
                if close is not None:
                    close()
                self.wsgi_input._discard()
        except:
            self.handle_error(*sys.exc_info())
        finally:
            self.time_finish = time.time()
            self.log_request()

    def read_request(self, raw_requestline):
        self.requestline = raw_requestline.rstrip()
        words = self.requestline.split()
        print("read_request %s" % len(words))
        if len(words) == 3:
            self.command, self.path, self.request_version = words
            if not self._check_http_version():
                self.log_error('Invalid http version: %r', raw_requestline)
                return
        elif len(words) == 2:
            self.command, self.path = words
            if self.command != "GET":
                self.log_error('Expected GET method: %r', raw_requestline)
                return
            self.request_version = "HTTP/0.9"
            # QQQ I'm pretty sure we can drop support for HTTP/0.9
        else:
            self.log_error('Invalid HTTP method: %r', raw_requestline)
            return

        self.headers = self.MessageClass(self.rfile, 0)
        if self.headers.status:
            self.log_error('Invalid headers status: %r', self.headers.status)
            return

        if self.headers.get("transfer-encoding", "").lower() == "chunked":
            try:
                del self.headers["content-length"]
            except KeyError:
                pass

        content_length = self.headers.get("content-length")
        if content_length is not None:
            content_length = int(content_length)
            if content_length < 0:
                self.log_error('Invalid Content-Length: %r', content_length)
                return
            if content_length and self.command in ('HEAD', ):
                self.log_error('Unexpected Content-Length')
                return

        self.content_length = content_length

        print("request_version", self.request_version, self.headers.get("Connection", "").lower())
        if self.request_version == "HTTP/1.1":
            conntype = self.headers.get("Connection", "").lower()
            if conntype and conntype=="keep-alive":
                self.close_connection = False
            else:
                self.close_connection = True
        else:
            self.close_connection = True

        return True

if __name__ == "__main__":
    #http = WSGIServer(('', 5000), app, handler_class=MyHandler)
    #print(type(http))
    #http.serve_forever()
    try:
        a = 1/0
    except Exception, e:
        print("1", e)
    except IOError, e:
        print("IOError", e)
    except:
        print("last")

