import os
import re
import sys
import time
import json
import queue
import inspect
import traceback
import builtins
import subprocess
import threading
import requests
class client:
    def __init__(self, interface=None, win_index=None):
        if interface and (not interface.startswith('http')):
            interface = 'http://' + interface
        self.interface = (interface or 'http://127.0.0.1:18089').rstrip('/')
        self.config_url = self.interface + '/config'
        self.quick_start_url = self.interface + '/quick_start'
        self.win_index = win_index or 0
        self.run_script_url = self.interface + '/run_script'
        self.run_script_quick_url = self.interface + '/run_only_script'
        self.default_timeout = 10

    def make_post_data(self, data=None):
        data = data or {}
        if self.win_index: data["win_index"] = self.win_index
        return data

    def post_interface(self, url, data, timeout=None):
        try:
            s = requests.post(url, data=data, timeout=timeout or self.default_timeout)
            s = s.json()
        except Exception as e:
            raise Exception(str(e))
        if s['status'] == 'success':
            return s.get('message', None)
        else:
            try:
                raise Exception(s['message'])
            except:
                raise Exception(str(s))

    def try_json_load(self, jsondata):
        try:
            return json.loads(jsondata)
        except:
            return jsondata

    def quick_cpu_num(self):
        return self.try_json_load(self.post_interface(self.quick_start_url, self.make_post_data({"cpu_num": '1'})))

    def quick_close_all(self):
        return self.try_json_load(self.post_interface(self.quick_start_url, self.make_post_data({"is_close": '1'})))

    def quick_start(self, num=1, vvv=None, limittime=2):
        def is_start():
            try:
                s = self.try_json_load(self.post_interface(self.quick_start_url, self.make_post_data({}), timeout=1.5))
                return True
            except Exception as e:
                time.sleep(0.5)
                return False
        if not is_start():
            if '127.0.0.1' in self.interface or 'localhost' in self.interface:
                v_chrome_target = os.path.join(os.path.split(sys.executable)[0], 'Scripts', 'chrome-win32-x64')
                v_chrome_exec = os.path.join(v_chrome_target, 'chrome-win32-x64', 'v_chrome.exe')
                if not os.path.isfile(v_chrome_exec):
                    raise Exception('v_chrome not install in python.')
                cmd = 'start cmd /k "{}"'.format(v_chrome_exec)
                os.system(cmd)
            while 1:
                if is_start():
                    break
        for _ in range(3):
            try:
                cfg = {
                    "is_start": '1', 
                    "init_num": num
                }
                if vvv:
                    cfg['vvv'] = vvv
                self.try_json_load(self.post_interface(self.quick_start_url, self.make_post_data(cfg)))
                break
            except Exception as e:
                time.sleep(0.5)
        start = time.time()
        while 1:
            try:
                self.clear_catch()
                break
            except Exception as e:
                if time.time() - start > limittime and str(e) == "{'status': 'fail', 'message': 'no config.'}":
                    raise e
                time.sleep(0.3)
        return self

    def init(self, vvv):
        return self.post_interface(self.config_url, self.make_post_data({"vvv": vvv}))

    def go_url(self, url, proxy=None, userAgent=None):
        data = self.make_post_data({"url": url})
        if proxy: self.set_proxy(proxy)
        if userAgent: data['userAgent'] = userAgent
        return self.post_interface(self.config_url, data)

    def debugger_script(self, script):
        return self.post_interface(self.config_url, self.make_post_data({"debugger_script": script}))

    def show(self, check_hidden=True):
        if check_hidden:
            if self.run_script('document.hidden'):
                return self.post_interface(self.config_url, self.make_post_data({"show": True}))
        else:
            return self.post_interface(self.config_url, self.make_post_data({"show": True}))

    def get_urls(self):
        return self.post_interface(self.config_url, self.make_post_data({"clear_catch": True}))

    def clear_catch(self):
        return self.post_interface(self.config_url, self.make_post_data({"clear_catch": True}))

    def get_match_list(self):
        return self.post_interface(self.config_url, self.make_post_data({"show_match_url_list": True}))

    def remove_match_url(self, match_url):
        return self.post_interface(self.config_url, self.make_post_data({"match_url": match_url, "is_remove": True}))

    def set_match_url(self, match_url, value=None, vtype:'None or "base64"'=None, res_headers=None, res_code=None):
        data = self.make_post_data({"match_url": match_url})
        if value: data['value'] = value
        if vtype: data['vtype'] = vtype
        if res_headers: data['res_headers'] = json.dumps(res_headers)
        if res_code: data['res_code'] = res_code
        return self.post_interface(self.config_url, data)

    def run_script_quick(self, script):
        return self.try_json_load(self.post_interface(self.run_script_quick_url, self.make_post_data({"script": script})))

    def run_script(self, scripts, wait_util_true=None, timeout=40000):
        # timeout 毫秒
        data = self.make_post_data({"scripts": scripts})
        if wait_util_true: data["wait_util_true"] = wait_util_true
        if timeout: data["timesout"] = int(timeout / 100)
        return self.try_json_load(self.post_interface(self.run_script_url, data, timeout=(timeout/1000)+10))

    def get_url_by_scripts(self, match_url, scripts, wait_util_true=None, timeout=40000):
        # timeout 毫秒
        data = self.make_post_data({"match_url": match_url, "scripts": scripts})
        if wait_util_true: data["wait_util_true"] = wait_util_true
        if timeout: data["timesout"] = int(timeout / 100)
        return self.try_json_load(self.post_interface(self.run_script_url, data, timeout=(timeout/1000)+10))

    def run_elements(self, elements, timeout=40000):
        # timeout 毫秒
        data = self.make_post_data({"elements": json.dumps(elements)})
        if timeout: data["timesout"] = int(timeout / 100)
        return self.try_json_load(self.post_interface(self.run_script_url, data, timeout=(timeout/1000)+10))

    def get_url_by_elements(self, match_url, elements, timeout=40000):
        # timeout 毫秒
        data = self.make_post_data({"match_url": match_url, "elements": json.dumps(elements)})
        if timeout: data["timesout"] = int(timeout / 100)
        return self.try_json_load(self.post_interface(self.run_script_url, data, timeout=(timeout/1000)+10))

    def clear_add_script(self):
        return self.post_interface(self.config_url, self.make_post_data({"clear_script": True}))

    def add_script_before_load_url(self, add_script, atype=None):
        data = self.make_post_data({"add_script": add_script})
        if atype: data['atype'] = atype
        return self.post_interface(self.config_url, data)

    def set_position(self, x, y):
        if not (type(x) == int and type(y) == int):
            raise TypeError('set_position type error. x:{},y:{}'.format(x, y))
        return self.post_interface(self.config_url, self.make_post_data({"position": "{},{}".format(x, y)}))

    def set_size(self, w, h):
        if not (type(w) == int and type(h) == int):
            raise TypeError('set_size type error. w:{},h:{}'.format(w, h))
        return self.post_interface(self.config_url, self.make_post_data({"size": "{},{}".format(w, h)}))

    def set_screen_size(self, w, h):
        if not (type(w) == int and type(h) == int):
            raise TypeError('set_screen_size type error. w:{},h:{}'.format(w, h))
        return self.post_interface(self.config_url, self.make_post_data({"screen_size": "{},{}".format(w, h)}))

    def restart(self, is_keep_cache=True, random_seed=None):
        data = self.make_post_data({"is_restart": True})
        if random_seed: data['random_seed'] = random_seed
        if is_keep_cache: data['is_keep_cache'] = is_keep_cache
        return self.post_interface(self.config_url, data)

    def cdp(self, commond, parameters):
        data = self.make_post_data({"cdp": True, "commond":commond, "parameters": json.dumps(parameters)})
        return self.post_interface(self.config_url, data)

    def change_finger(self, random_seed): return self.post_interface(self.config_url, self.make_post_data({ "random_seed": random_seed }))
    def is_debugger(self, enable=True): return self.post_interface(self.config_url, self.make_post_data({ "is_debugger": enable }))
    def log_debugger(self, enable=True): return self.post_interface(self.config_url, self.make_post_data({ "log_debugger": enable }))
    def get_debugger(self, match_url=None):
        data = self.make_post_data({"get_debugger": True})
        if match_url: data['match_url'] = match_url
        return self.post_interface(self.config_url, data)

    def get_cookie(self, key):
        data = self.make_post_data({"get_cookie": True, "key": key})
        return self.post_interface(self.config_url, data)

    def get_cookies(self):
        data = self.make_post_data({"get_cookie": True})
        return self.post_interface(self.config_url, data)

    def set_proxy(self, proxy=None): 
        data = self.make_post_data({"set_proxy": True})
        if proxy: data['proxy'] = proxy
        return self.post_interface(self.config_url, data)

    def set_rtc_ip(self, ip):
        if not ip:
            return
        x = re.findall(r'\d+\.\d+\.\d+\.\d+', ip)
        if x:
            self.clear_add_script()
            return self.add_script('window.Range.v_proxy = "%s"' % (x[0]))
        else:
            raise Exception('ip format error. input ip:{}'.format(ip))

    def set_js_filter(self, match_url, jscode): return self.post_interface(self.config_url, self.make_post_data({"js_filter": jscode, "match_url": match_url}))
    def remove_js_filter(self, match_url): return self.post_interface(self.config_url, self.make_post_data({"js_filter": "<remove>", "match_url": match_url}))
    def clear_js_filter(self): return self.post_interface(self.config_url, self.make_post_data({"js_filter": "<remove_all>"}))
    def get_cookie(self): return '; '.join(self.get_cookies())
    def clear_debugger(self, enable=True): return self.post_interface(self.config_url, self.make_post_data({ "clear_debugger": enable }))
    def disabled_redirect(self, enable=True): return self.post_interface(self.config_url, self.make_post_data({ "disabled_redirect": enable }))
    def clear_storage_data(self, enable=True): return self.post_interface(self.config_url, self.make_post_data({ "clear_storage_data": enable }))
    def clear_storage(self): return self.clear_storage_data(True)
    def add_script(self, add_script, atype=None): return self.add_script_before_load_url(add_script, atype)

class server:
    def __init__(self, taskerlist, tasklimit=None):
        self.taskerlist = taskerlist
        self.tasklist = queue.Queue(tasklimit or len(self.taskerlist))
        for idx, tasker in enumerate(self.taskerlist):
            # tasker.taskerlist = self.taskerlist
            td = threading.Thread(target=self.looper, args=(tasker,))
            td.vvv_tasker = tasker
            td.start()
        lock = threading.RLock()

        _org_print = print
        def _new_print(*arg,**kw):
            lock.acquire()
            td = threading.current_thread()
            vvv_tasker = getattr(td, 'vvv_tasker', None)
            if vvv_tasker:
                name = '{} :: {}'.format(vvv_tasker.interface, vvv_tasker.win_index)
                name = "[{}]".format(name.center(34))
                _org_print(name,*arg,**kw)
            else:
                _org_print(*arg,**kw)
            lock.release()
        builtins.print = _new_print

    def put(self, task):
        try:
            self.tasklist.put_nowait(task)
        except:
            raise Exception('over tasklist limit num:{}'.format(len(self.taskerlist)))

    def looper(self, tasker):
        while(1):
            task = self.tasklist.get()
            try:
                task[0](tasker, *task[1], **task[2])
            except:
                print(traceback.format_exc())
                time.sleep(2)

    def __call__(self, func):
        def _(*a, **kw):
            self.put([func, a, kw])
        _.taskerlist = self.taskerlist
        return _

def make_WebsocketServer():
    # Author: Johan Hanssen Seferidis
    # License: MIT
    import sys
    import struct
    import ssl
    from base64 import b64encode
    from hashlib import sha1
    import logging
    from socket import error as SocketError
    import errno
    import threading
    from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler
    import threading
    class ThreadWithLoggedException(threading.Thread):
        DIVIDER = "*"*80
        def __init__(self, *args, **kwargs):
            try:
                self.logger = kwargs.pop("logger")
            except KeyError:
                raise Exception("Missing 'logger' in kwargs")
            super().__init__(*args, **kwargs)
            self.exception = None

        def run(self):
            try:
                if self._target is not None:
                    self._target(*self._args, **self._kwargs)
            except Exception as exception:
                thread = threading.current_thread()
                self.exception = exception
                self.logger.exception(f"{self.DIVIDER}\nException in child thread {thread}: {exception}\n{self.DIVIDER}")
            finally:
                del self._target, self._args, self._kwargs
    class WebsocketServerThread(ThreadWithLoggedException):
        """Dummy wrapper to make debug messages a bit more readable"""
        pass
    logger = logging.getLogger(__name__)
    logging.basicConfig()
    '''
    +-+-+-+-+-------+-+-------------+-------------------------------+
     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-------+-+-------------+-------------------------------+
    |F|R|R|R| opcode|M| Payload len |    Extended payload length    |
    |I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
    |N|V|V|V|       |S|             |   (if payload len==126/127)   |
    | |1|2|3|       |K|             |                               |
    +-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
    |     Extended payload length continued, if payload len == 127  |
    + - - - - - - - - - - - - - - - +-------------------------------+
    |                     Payload Data continued ...                |
    +---------------------------------------------------------------+
    '''
    FIN    = 0x80
    OPCODE = 0x0f
    MASKED = 0x80
    PAYLOAD_LEN = 0x7f
    PAYLOAD_LEN_EXT16 = 0x7e
    PAYLOAD_LEN_EXT64 = 0x7f
    OPCODE_CONTINUATION = 0x0
    OPCODE_TEXT         = 0x1
    OPCODE_BINARY       = 0x2
    OPCODE_CLOSE_CONN   = 0x8
    OPCODE_PING         = 0x9
    OPCODE_PONG         = 0xA
    CLOSE_STATUS_NORMAL = 1000
    DEFAULT_CLOSE_REASON = bytes('', encoding='utf-8')
    class API():
        def run_forever(self, threaded=False): return self._run_forever(threaded)
        def new_client(self, client, server): pass
        def client_left(self, client, server): pass
        def message_received(self, client, server, message): pass
        def set_fn_new_client(self, fn): self.new_client = fn
        def set_fn_client_left(self, fn): self.client_left = fn
        def set_fn_message_received(self, fn): self.message_received = fn
        def send_message(self, client, msg): self._unicast(client, msg)
        def send_message_to_all(self, msg): self._multicast(msg)
        def deny_new_connections(self, status=CLOSE_STATUS_NORMAL, reason=DEFAULT_CLOSE_REASON): self._deny_new_connections(status, reason)
        def allow_new_connections(self): self._allow_new_connections()
        def shutdown_gracefully(self, status=CLOSE_STATUS_NORMAL, reason=DEFAULT_CLOSE_REASON): self._shutdown_gracefully(status, reason)
        def shutdown_abruptly(self): self._shutdown_abruptly()
        def disconnect_clients_gracefully(self, status=CLOSE_STATUS_NORMAL, reason=DEFAULT_CLOSE_REASON): self._disconnect_clients_gracefully(status, reason)
        def disconnect_clients_abruptly(self): self._disconnect_clients_abruptly()
    class WebsocketServer(ThreadingMixIn, TCPServer, API):
        allow_reuse_address = True
        daemon_threads = True  
        def __init__(self, host='127.0.0.1', port=0, loglevel=logging.WARNING, key=None, cert=None):
            logger.setLevel(loglevel)
            TCPServer.__init__(self, (host, port), WebSocketHandler)
            self.host = host
            self.port = self.socket.getsockname()[1]
            self.key = key
            self.cert = cert
            self.clients = []
            self.id_counter = 0
            self.thread = None
            self._deny_clients = False
        def _run_forever(self, threaded):
            cls_name = self.__class__.__name__
            try:
                logger.info("Listening on port %d for clients.." % self.port)
                if threaded:
                    self.daemon = True
                    self.thread = WebsocketServerThread(target=super().serve_forever, daemon=True, logger=logger)
                    logger.info(f"Starting {cls_name} on thread {self.thread.getName()}.")
                    self.thread.start()
                else:
                    self.thread = threading.current_thread()
                    logger.info(f"Starting {cls_name} on main thread.")
                    super().serve_forever()
            except KeyboardInterrupt:
                self.server_close()
                logger.info("Server terminated.")
            except Exception as e:
                logger.error(str(e), exc_info=True)
                sys.exit(1)
        def _message_received_(self, handler, msg):
            self.message_received(self.handler_to_client(handler), self, msg)
        def _ping_received_(self, handler, msg):
            handler.send_pong(msg)
        def _pong_received_(self, handler, msg):
            pass
        def _new_client_(self, handler):
            if self._deny_clients:
                status = self._deny_clients["status"]
                reason = self._deny_clients["reason"]
                handler.send_close(status, reason)
                self._terminate_client_handler(handler)
                return
            self.id_counter += 1
            client = {
                'id': self.id_counter,
                'handler': handler,
                'address': handler.client_address
            }
            self.clients.append(client)
            self.new_client(client, self)
        def _client_left_(self, handler):
            client = self.handler_to_client(handler)
            self.client_left(client, self)
            if client in self.clients:
                self.clients.remove(client)
        def _unicast(self, receiver_client, msg):
            receiver_client['handler'].send_message(msg)
        def _multicast(self, msg):
            for client in self.clients:
                self._unicast(client, msg)
        def handler_to_client(self, handler):
            for client in self.clients:
                if client['handler'] == handler:
                    return client
        def _terminate_client_handler(self, handler):
            handler.keep_alive = False
            handler.finish()
            handler.connection.close()
        def _terminate_client_handlers(self):
            for client in self.clients:
                self._terminate_client_handler(client["handler"])
        def _shutdown_gracefully(self, status=CLOSE_STATUS_NORMAL, reason=DEFAULT_CLOSE_REASON):
            self.keep_alive = False
            self._disconnect_clients_gracefully(status, reason)
            self.server_close()
            self.shutdown()
        def _shutdown_abruptly(self):
            self.keep_alive = False
            self._disconnect_clients_abruptly()
            self.server_close()
            self.shutdown()
        def _disconnect_clients_gracefully(self, status=CLOSE_STATUS_NORMAL, reason=DEFAULT_CLOSE_REASON):
            for client in self.clients:
                client["handler"].send_close(status, reason)
            self._terminate_client_handlers()
        def _disconnect_clients_abruptly(self):
            self._terminate_client_handlers()
        def _deny_new_connections(self, status, reason):
            self._deny_clients = {
                "status": status,
                "reason": reason,
            }
        def _allow_new_connections(self):
            self._deny_clients = False
    class WebSocketHandler(StreamRequestHandler):
        def __init__(self, socket, addr, server):
            self.server = server
            assert not hasattr(self, "_send_lock"), "_send_lock already exists"
            self._send_lock = threading.Lock()
            if server.key and server.cert:
                try:
                    socket = ssl.wrap_socket(socket, server_side=True, certfile=server.cert, keyfile=server.key)
                except: 
                    logger.warning("SSL not available (are the paths {} and {} correct for the key and cert?)".format(server.key, server.cert))
            StreamRequestHandler.__init__(self, socket, addr, server)
        def setup(self):
            StreamRequestHandler.setup(self)
            self.keep_alive = True
            self.handshake_done = False
            self.valid_client = False
        def handle(self):
            while self.keep_alive:
                if not self.handshake_done:
                    self.handshake()
                elif self.valid_client:
                    self.read_next_message()
        def read_bytes(self, num):
            return self.rfile.read(num)
        def read_next_message(self):
            try:
                b1, b2 = self.read_bytes(2)
            except SocketError as e:  
                if e.errno == errno.ECONNRESET:
                    logger.info("Client closed connection.")
                    self.keep_alive = 0
                    return
                b1, b2 = 0, 0
            except ValueError as e:
                b1, b2 = 0, 0
            fin    = b1 & FIN
            opcode = b1 & OPCODE
            masked = b2 & MASKED
            payload_length = b2 & PAYLOAD_LEN
            if opcode == OPCODE_CLOSE_CONN:
                logger.info("Client asked to close connection.")
                self.keep_alive = 0
                return
            if not masked:
                logger.warning("Client must always be masked.")
                self.keep_alive = 0
                return
            if opcode == OPCODE_CONTINUATION:
                logger.warning("Continuation frames are not supported.")
                return
            elif opcode == OPCODE_BINARY:
                logger.warning("Binary frames are not supported.")
                return
            elif opcode == OPCODE_TEXT:
                opcode_handler = self.server._message_received_
            elif opcode == OPCODE_PING:
                opcode_handler = self.server._ping_received_
            elif opcode == OPCODE_PONG:
                opcode_handler = self.server._pong_received_
            else:
                logger.warning("Unknown opcode %#x." % opcode)
                self.keep_alive = 0
                return
            if payload_length == 126:
                payload_length = struct.unpack(">H", self.rfile.read(2))[0]
            elif payload_length == 127:
                payload_length = struct.unpack(">Q", self.rfile.read(8))[0]
            masks = self.read_bytes(4)
            message_bytes = bytearray()
            for message_byte in self.read_bytes(payload_length):
                message_byte ^= masks[len(message_bytes) % 4]
                message_bytes.append(message_byte)
            opcode_handler(self, message_bytes.decode('utf8'))
        def send_message(self, message):
            self.send_text(message)
        def send_pong(self, message):
            self.send_text(message, OPCODE_PONG)
        def send_close(self, status=CLOSE_STATUS_NORMAL, reason=DEFAULT_CLOSE_REASON):
            if status < CLOSE_STATUS_NORMAL or status > 1015:
                raise Exception(f"CLOSE status must be between 1000 and 1015, got {status}")
            header = bytearray()
            payload = struct.pack('!H', status) + reason
            payload_length = len(payload)
            assert payload_length <= 125, "We only support short closing reasons at the moment"
            
            header.append(FIN | OPCODE_CLOSE_CONN)
            header.append(payload_length)
            with self._send_lock:
                self.request.send(header + payload)
        def send_text(self, message, opcode=OPCODE_TEXT):
            if isinstance(message, bytes):
                message = try_decode_UTF8(message)  
                if not message:
                    logger.warning("Can\'t send message, message is not valid UTF-8")
                    return False
            elif not isinstance(message, str):
                logger.warning('Can\'t send message, message has to be a string or bytes. Got %s' % type(message))
                return False
            header  = bytearray()
            payload = encode_to_UTF8(message)
            payload_length = len(payload)
            
            if payload_length <= 125:
                header.append(FIN | opcode)
                header.append(payload_length)
            
            elif payload_length >= 126 and payload_length <= 65535:
                header.append(FIN | opcode)
                header.append(PAYLOAD_LEN_EXT16)
                header.extend(struct.pack(">H", payload_length))
            
            elif payload_length < 18446744073709551616:
                header.append(FIN | opcode)
                header.append(PAYLOAD_LEN_EXT64)
                header.extend(struct.pack(">Q", payload_length))
            else:
                raise Exception("Message is too big. Consider breaking it into chunks.")
                return
            with self._send_lock:
                self.request.send(header + payload)
        def read_http_headers(self):
            headers = {}
            
            http_get = self.rfile.readline().decode().strip()
            assert http_get.upper().startswith('GET')
            
            while True:
                header = self.rfile.readline().decode().strip()
                if not header:
                    break
                head, value = header.split(':', 1)
                headers[head.lower().strip()] = value.strip()
            return headers
        def handshake(self):
            headers = self.read_http_headers()
            try:
                assert headers['upgrade'].lower() == 'websocket'
            except AssertionError:
                self.keep_alive = False
                return
            try:
                key = headers['sec-websocket-key']
            except KeyError:
                logger.warning("Client tried to connect but was missing a key")
                self.keep_alive = False
                return
            response = self.make_handshake_response(key)
            with self._send_lock:
                self.handshake_done = self.request.send(response.encode())
            self.valid_client = True
            self.server._new_client_(self)
        @classmethod
        def make_handshake_response(cls, key):
            return \
              'HTTP/1.1 101 Switching Protocols\r\n'\
              'Upgrade: websocket\r\n'              \
              'Connection: Upgrade\r\n'             \
              'Sec-WebSocket-Accept: %s\r\n'        \
              '\r\n' % cls.calculate_response_key(key)
        @classmethod
        def calculate_response_key(cls, key):
            GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
            hash = sha1(key.encode() + GUID.encode())
            response_key = b64encode(hash.digest()).strip()
            return response_key.decode('ASCII')
        def finish(self):
            self.server._client_left_(self)
    def encode_to_UTF8(data):
        try:
            return data.encode('UTF-8')
        except UnicodeEncodeError as e:
            logger.error("Could not encode data to UTF-8 -- %s" % e)
            return False
        except Exception as e:
            raise(e)
            return False
    def try_decode_UTF8(data):
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            return False
        except Exception as e:
            raise(e)
    return WebsocketServer

WebsocketServer = make_WebsocketServer()

def local_client(host='127.0.0.1', port=19001):
    cu_connector = None
    start_connect = False
    que = queue.Queue()
    cache_p = {}
    def new_client(client, connector): pass
    def client_left(client, connector): 
        print("[*] client_left", connector)
        nonlocal cu_connector
        if cu_connector == connector:
            cu_connector = None
    def message_received(client, connector, message):
        nonlocal cu_connector
        cu_connector = connector
        msg = json.loads(message)
        if msg['type'] == 'start':
            data = json.dumps({ "type": "start" })
            connector.send_message_to_all(data)
        if msg['type'] == 'result':
            que.put(message)
        if msg['type'] == 'result_p':
            cache_p[msg['uid']] = cache_p.get(msg['uid']) or []
            cache_p[msg['uid']].append(msg)
            if len(cache_p[msg['uid']]) == msg['length']:
                cache_p[msg['uid']] = sorted(cache_p[msg['uid']], key=lambda a: a['index'])
                r = ''
                for i in cache_p[msg['uid']]:
                    r += i['data']
                del cache_p[msg['uid']]
                que.put(r)
    def try_json_result(data):
        try:
            data = json.loads(data)['data']
            return data
        except:
            return data
    def try_run_result(data):
        is_err = False
        try:
            data = try_json_result(data)
            if data['message']['result'].get('type') == 'undefined':
                return None
            elif data['message']['result'].get('subtype') == 'null':
                return '<None>'
            elif data['message']['result'].get('value', None) != None:
                return data['message']['result']['value']
            elif data['message']['result'].get('description'):
                is_err = data['message']['result']['description']
            else:
                raise Exception('err')
        except:
            return data
        if is_err:
            raise Exception(is_err)
    def wait_connector():
        start = time.time()
        has_alert = False
        while 1:
            if not cu_connector:
                if time.time() - start > 5 and has_alert == False:
                    has_alert = True
                    raise Exception('wait over time. 5sec')
                time.sleep(0.15)
            else:
                break
    def ensure_connect(func):
        def _(*a, **kw):
            nonlocal start_connect
            if not start_connect:
                start_connect = True
                s = threading.Thread(target=server.run_forever)
                s.daemon = True
                s.start()
            if not cu_connector:
                wait_connector()
            return func(*a, **kw)
        return _
    server = WebsocketServer(host=host, port=port)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    def J(data):
        return json.dumps(data)
    class Ftree:
        def __init__(self, rootjson):
            self.F = rootjson
            self.uniqueId = self.F['local_frame_uniqueid']['context']['uniqueId']
        def __getattr__(self, name):
            if name == 'frames':
                r = []
                for i in self.F['childrens']:
                    r.append(Ftree(i))
                return r
            if name == 'run_script' or name == 'run_scripts':
                def f(*a, **kw):
                    kw['uniqueId'] = self.uniqueId
                    return _().run_script(*a, **kw)
                return f
        def __repr__(self):
            # "adFrameStatus": {
            #     "adFrameType": "none"
            # },
            # "crossOriginIsolatedContextType": "NotIsolated",
            # "domainAndRegistry": "",
            # "gatedAPIFeatures": [],
            # "id": "3AE0E2177D69DA197610683B7EA60F3B",
            # "loaderId": "97C4EF7BDAC6EE70E3EF7DF90233DB36",
            # "mimeType": "text/html",
            # "secureContextType": "InsecureScheme",
            # "securityOrigin": "http://8.130.117.18:8098",
            # "url": "http://8.130.117.18:8098/",
            # "local_frame_uniqueid": {
            #     "context": {
            #         "auxData": {
            #             "frameId": "3AE0E2177D69DA197610683B7EA60F3B",
            #             "isDefault": true,
            #             "type": "default"
            #         },
            #         "id": 1,
            #         "name": "",
            #         "origin": "http://8.130.117.18:8098",
            #         "uniqueId": "-7927091712392069697.-2546048121026538995"
            #     }
            # },
            return '<[{}]: childrens[{}]>'.format(self.F['url'], len(self.F['childrens']))
    class _:
        debug = False
        @ensure_connect
        def set_match_url(self, match_url=None, fakeresponse=None, timeout=5000, qtimeout=5):
            data = json.dumps({ 
                "type": "set_match_url", 
                "match_url": match_url, 
                "fakeresponse": fakeresponse, 
                "timeout": timeout 
            })
            cu_connector.send_message_to_all(data)
            return try_json_result(que.get(timeout=qtimeout))
        @ensure_connect
        def remove_match_url(self, match_url=None, qtimeout=5):
            data = json.dumps({ "type": "remove_match_url", "match_url": match_url })
            cu_connector.send_message_to_all(data)
            return try_json_result(que.get(timeout=qtimeout))
        @ensure_connect
        def clear_catch(self, qtimeout=5):
            data = json.dumps({ "type": "clear_catch" })
            cu_connector.send_message_to_all(data)
            return try_json_result(que.get(timeout=qtimeout))
        @ensure_connect
        def get_url_by_scripts(self, match_url=None, script=None, fakeresponse=None, timeout=5000, qtimeout=15):
            data = json.dumps({ 
                "type": "get_url_by_scripts", 
                "match_url": match_url, 
                "script": script,
                "fakeresponse": fakeresponse, 
                "timeout": timeout 
            })
            cu_connector.send_message_to_all(data)
            return try_json_result(que.get(timeout=qtimeout))
        get_url_by_script = get_url_by_scripts
        @ensure_connect
        def run_scripts(self, script, uniqueId=None, timeout=5000, qtimeout=15):
            data = json.dumps({ 
                "type": "run_script", 
                "script": script,
                "timeout": timeout,
                "uniqueId": uniqueId,
            })
            cu_connector.send_message_to_all(data)
            return try_run_result(que.get(timeout=qtimeout))
        run_script = run_scripts
        @ensure_connect
        def get_url_by_elements(self, match_url=None, elements=None, fakeresponse=None, timeout=5000, qtimeout=15):
            data = json.dumps({ 
                "type": "get_url_by_elements", 
                "match_url": match_url, 
                "elements": elements,
                "fakeresponse": fakeresponse, 
                "timeout": timeout 
            })
            cu_connector.send_message_to_all(data)
            return try_json_result(que.get(timeout=qtimeout))
        get_url_by_element = get_url_by_elements
        @ensure_connect
        def run_elements(self, elements, timeout=5000, qtimeout=15):
            data = json.dumps({ "type": "run_element", "elements": elements })
            cu_connector.send_message_to_all(data)
            return try_run_result(que.get(timeout=qtimeout))
        run_element = run_elements
        @ensure_connect
        def set_size(self, width, height, qtimeout=5):
            data = json.dumps({ "type": "set_size", "width": width,"height": height })
            cu_connector.send_message_to_all(data)
            return try_run_result(que.get(timeout=qtimeout))
        @ensure_connect
        def set_position(self, left, top, qtimeout=5):
            data = json.dumps({ "type": "set_position", "left": left,"top": top })
            cu_connector.send_message_to_all(data)
            return try_run_result(que.get(timeout=qtimeout))
        @ensure_connect
        def go_url(self, url, userAgent=None, referrer=None, proxy=None, qtimeout=15):
            if proxy: self.set_proxy(proxy)
            data = json.dumps({ "type": "go_url", "url": url,"referrer": referrer,"userAgent": userAgent })
            cu_connector.send_message_to_all(data)
            return try_run_result(que.get(timeout=qtimeout))
        @ensure_connect
        def set_proxy(self, proxy=None, qtimeout=15):
            proxy = proxy.replace('http://', '').replace('https://', '').rstrip('/')
            data = json.dumps({ "type": "set_proxy", "proxy": proxy })
            cu_connector.send_message_to_all(data)
            return try_run_result(que.get(timeout=qtimeout))
        @ensure_connect
        def add_script(self, script=None, qtimeout=15):
            data = json.dumps({ "type": "add_script", "script": script })
            cu_connector.send_message_to_all(data)
            return try_run_result(que.get(timeout=qtimeout))
        @ensure_connect
        def clear_add_script(self, qtimeout=15):
            data = json.dumps({ "type": "clear_add_script" })
            cu_connector.send_message_to_all(data)
            return try_run_result(que.get(timeout=qtimeout))
        @ensure_connect
        def emulation_iphone(self, ):
            # demo for dev
            self.cdp("Emulation.setDeviceMetricsOverride", {
                "width": 430,
                "height": 932,
                "deviceScaleFactor": 3,
                "mobile": True,
                "scale": 0.84,
                "screenWidth": 430,
                "screenHeight": 932,
                "positionX": 0,
                "positionY": 0,
                "dontSetVisibleSize": True,
                "devicePosture": {
                    "type": "continuous"
                },
                "screenOrientation": {
                    "type": "portraitPrimary",
                    "angle": 0
                }
            })
            self.cdp("Network.setUserAgentOverride", {
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
            })
            self.cdp("Emulation.setTouchEmulationEnabled", {
                "enabled": True,
                "maxTouchPoints": 5
            })
            self.cdp("Emulation.setEmitTouchEventsForMouse", {
                "enabled": True,
                "configuration": "mobile"
            })
        @ensure_connect
        def cdp(self, protocal, data=None, qtimeout=15):
            data = json.dumps({ "type": "cdp", "protocal": protocal, "data": data })
            cu_connector.send_message_to_all(data)
            ret = try_run_result(que.get(timeout=qtimeout))
            if self.debug: print('[@] debug: {}: {}'.format(protocal, ret))
            return ret
        @ensure_connect
        def auto_change_resp(self, match_url, script, qtimeout=15):
            # only for html/script
            data = json.dumps({ "type": "auto_change_resp", "match_url": match_url, "script": script })
            cu_connector.send_message_to_all(data)
            ret = try_run_result(que.get(timeout=qtimeout))
            return ret
        @ensure_connect
        def get_frametree(self, qtimeout=15):
            data = json.dumps({ "type": "frametree" })
            cu_connector.send_message_to_all(data)
            return try_run_result(que.get(timeout=qtimeout))
        @ensure_connect
        def get_framelist(self, qtimeout=15):
            data = json.dumps({ "type": "framelist" })
            cu_connector.send_message_to_all(data)
            return try_run_result(que.get(timeout=qtimeout))
        @property
        def frames(self):
            root = self.get_frametree()
            if root['status'] != 'success':
                raise Exception('error get frametree.')
            root = root['message']
            return Ftree(root).frames
        class vvv_requests:
            def __init__(self, vvv):
                self.vvv = vvv
            def pack_return(self, ret):
                class Response:
                    def __init__(self, ret):
                        self.status_code = ret[0]
                        self.content = ret[1].encode()
                        self.text = ret[1]
                    def __repr__(self):
                        return '<RPC Response [{}]>'.format(self.status_code)
                    def json(self):
                        return json.loads(self.text)
                return Response(ret)
            def get(self, url, params=None, **kwargs):
                pr = requests.Request('GET', url, params=params, **kwargs).prepare()
                url = pr.url
                headers = dict(pr.headers)
                ret = self.vvv.run_scripts('''
                new Promise(function(a,b){
                    var xhr = new XMLHttpRequest()
                    xhr.open("GET", %s)
                    var headers = %s
                    var hkeys = Object.keys(headers)
                    for (var i = 0; i < hkeys.length; i++) {
                        xhr.setRequestHeader(hkeys[i], headers[hkeys[i]])
                    }
                    xhr.onload = function () {
                        if (xhr.status >= 200 && xhr.status < 300) {
                            a([xhr.status, xhr.responseText])
                        } else {
                            b([xhr.status, 'not in 200-299'])
                        }
                    }
                    xhr.onerror = function () { b([0, 'Request failed']); }
                    xhr.send()
                })
                ''' % (J(url), J(headers)))
                return self.pack_return(ret)
            def post(self, url, data=None, json=None, **kwargs):
                pr = requests.Request('POST', url, data=data, json=json, **kwargs).prepare()
                url = pr.url
                headers = dict(pr.headers)
                body = pr.body
                ret = self.vvv.run_scripts('''
                new Promise(function(a,b){
                    var xhr = new XMLHttpRequest()
                    xhr.open("GET", %s)
                    var headers = %s
                    var hkeys = Object.keys(headers)
                    for (var i = 0; i < hkeys.length; i++) {
                        xhr.setRequestHeader(hkeys[i], headers[hkeys[i]])
                    }
                    xhr.onload = function () {
                        if (xhr.status >= 200 && xhr.status < 300) {
                            a([xhr.status, xhr.responseText])
                        } else {
                            b([xhr.status, 'not in 200-299'])
                        }
                    }
                    xhr.onerror = function () { b([0, 'Request failed']); }
                    xhr.send(%s)
                })
                ''' % (J(url), J(headers), J(body)))
                return self.pack_return(ret)
        @property
        def requests(self):
            return self.vvv_requests(self)
        @ensure_connect
        def test(self, qtimeout=15):
            data = json.dumps({ "type": "test" })
            cu_connector.send_message_to_all(data)
            return try_run_result(que.get(timeout=qtimeout))
    return _()

import sys
def get_current_os():
    if sys.platform.startswith('win'):
        return 'Windows'
    elif sys.platform.startswith('linux'):
        return 'Linux'
    elif sys.platform.startswith('darwin'):
        return 'Mac OS'
    else:
        return 'Other'

def execute():
    argv = sys.argv
    print('v_rpc :::: [ {} ]'.format(' '.join(argv)))
    currpath = os.path.split(os.path.abspath(__file__))[0]
    print('v_rpc currpath:', currpath)
    print('extension for linux:')
    print('    sudo apt-get install p7zip-full')
    print('    7z x ' + currpath + '/v_jshook_linux.zip -o./v_jshook_linux -psparklehorse')
    current_os = get_current_os()
    if current_os == 'Windows':
        os.system('explorer ' + currpath)
    if current_os == 'Mac OS':
        os.system('open ' + currpath)

def fjson(data):
    return json.dumps(data, indent=4, ensure_ascii=False)

import re
import json
import types
from json import JSONDecodeError
try:
    from websocket import WebSocketTimeoutException, WebSocketConnectionClosedException, WebSocketException, create_connection
except:
    from .websocket import WebSocketTimeoutException, WebSocketConnectionClosedException, WebSocketException, create_connection
from threading import Thread, Event
from urllib import request
def remote_client(host, port=18999, debug=False):
    def myget(url):
        r = request.Request(url, method='GET')
        proxies = None # {'http':'http://127.0.0.1:8888', 'https':'http://127.0.0.1:8888'}
        opener = request.build_opener(request.ProxyHandler(proxies))
        return json.loads(opener.open(r).read().decode())
    def adj_wsurl(wsurl): return re.sub('ws://[^/]+/devtools/', 'ws://{}:{}/devtools/'.format(host, port), wsurl)
    s = myget('http://{}:{}/json'.format(host, port))
    wsurl = adj_wsurl(s[0]['webSocketDebuggerUrl'])
    def try_json_result(data):
        try:
            data = json.loads(data)['result']
            return data
        except:
            return data
    def try_run_result(data):
        is_err = False
        try:
            if data['result'].get('type') == 'undefined':
                return None
            elif data['result'].get('subtype') == 'null':
                return '<NULL>'
            elif data['result'].get('value', None) != None:
                return data['result']['value']
            elif data['result'].get('description'):
                is_err = data['result']['description']
            else:
                raise Exception('err')
        except:
            return data
        if is_err:
            raise Exception(is_err)
    def is_function(obj):
        return type(obj) == types.FunctionType
    class Err: pass
    class _:
        def __init__(self, wsurl):
            self.ws = create_connection(wsurl)
            self.id = 0
            self.qret = {}
            self._xid = 0
            self.irun = {}
            self.loop_recv = Thread(target=self.start_loop)
            self.loop_recv.daemon = True
            self.loop_recv.start()
            self.cdp("Page.enable", {})
            # self.cdp("Network.enable", {})
            # self.cdp("Fetch.enable", {})
            # self.set_method_callback("Fetch.requestPaused", func)
        def start_loop(self):
            while True:
                try:
                    rdata = json.loads(self.ws.recv())
                    if debug:
                        print('------------------------------')
                        print(rdata)
                except WebSocketTimeoutException:
                    continue
                except (WebSocketException, OSError, WebSocketConnectionClosedException, JSONDecodeError) as e:
                    raise e
                method = rdata.get('method')
                if method in self.irun:
                    for xid in self.irun[method]:
                        m = self.irun[method].get(xid, None)
                        if m:
                            if is_function(m):
                                m(rdata)
                            if isinstance(m, queue.Queue):
                                m.put(rdata['params'])
                if rdata.get('id') in self.qret:
                    if rdata.get('result', Err) != Err:
                        self.qret[rdata.get('id')].put(rdata['result'])
                    elif rdata.get('error', Err) != Err:
                        self.qret[rdata.get('id')].put(rdata['error'])
                    else:
                        print(rdata, repr(rdata.get('result')))
                        raise Exception('un expect err.' + repr(rdata.get('result')))
        def get_id(self):
            self.id += 1
            return self.id
        def get_xid(self):
            self._xid += 1
            return self._xid
        def cdp(self, protocal, data, only_send=False):
            rid = self.get_id()
            cmd = { "id": rid, "method": protocal, "params": data }
            if debug:
                print('====>', rid, protocal)
            self.qret[rid] = queue.Queue()
            try:
                self.ws.send(json.dumps(cmd))
            except (OSError, WebSocketConnectionClosedException):
                self.qret.pop(rid, None)
                return
            if only_send:
                return
            while True:
                try:
                    ret = self.qret[rid].get(timeout=.15)
                    self.qret.pop(rid, None)
                    return try_run_result(ret)
                except queue.Empty:
                    continue
        def wait_once_method(self, method, timeout=10):
            self.irun[method] = self.irun.get(method, {})
            xid = self.get_xid()
            self.irun[method][xid] = queue.Queue()
            start = time.time()
            while True:
                try:
                    ret = self.irun[method][xid].get(timeout=0.15)
                    self.irun[method].pop(xid, None)
                    return ret
                except:
                    if time.time() - start > timeout:
                        raise Exception('wait_once_method {} timeout: {}'.format(method, timeout))
                    continue
        def go_url(self, url):
            self.cdp("Page.navigate", {"url": url})
            self.wait_once_method("Page.domContentEventFired")
        def set_method_callback(self, method, func):
            self.irun[method] = self.irun.get(method, {})
            self.irun[method][self.get_xid()] = func
        def run_script(self, script):
            return self.cdp('Runtime.evaluate', { 
                "expression": script, 
                "awaitPromise": True, 
                "returnByValue": True 
            })
        def add_script(self, script):
            ret = self.cdp("Page.addScriptToEvaluateOnNewDocument", {"source": script})
            return int(ret['identifier'])
        def remove_script(self):
            idx = self.add_script("")
            for i in range(1, idx+1):
                self.cdp("Page.removeScriptToEvaluateOnNewDocument", {"identifier": str(i)})
    return _(wsurl)

if __name__ == '__main__':
    pass

    vvv = client()
    vvv.quick_start()
    vvv.set_js_filter("//", """
function(response){
    return '<h1>hello world111</h1>' + response
}
        """)

    # vvv.remove_js_filter('//')
    # vvv.clear_js_filter()

    # vvv.log_debugger()
    # vvv.set_match_url('//', "asdf")

    vvv.set_screen_size(400,400)

    vvv.go_url('http://127.0.0.1:18089/debug_prop')




    # vvv = client()
    # vvv.quick_start()
    # x = vvv.cdp("Emulation.enable", {})
    # x = vvv.cdp("Emulation.setTouchEmulationEnabled", {"enabled":True,"maxTouchPoints":1})
    # print(x)
    # x = vvv.cdp("Emulation.setEmitTouchEventsForMouse", {"configuration":"desktop","enabled":True})
    # print(x)
    # x = vvv.cdp("Emulation.setDeviceMetricsOverride", {
    #     "devicePosture": {"type": "continuous"},
    #     "deviceScaleFactor": 2,
    #     "dontSetVisibleSize": True,
    #     "height": 667,
    #     "mobile": True,
    #     "positionX": 0,
    #     "positionY": 0,
    #     "scale": 2.75,
    #     "screenHeight": 667,
    #     "screenOrientation": {"type": "portraitPrimary", "angle": 0},
    #     "screenWidth": 375,
    #     "width": 375,
    # })
    # print(x)
    # vvv.go_url('https://steamdb.info/')


    # vvv = client()
    # vvv.quick_start(2)
    # # vvv.go_url('https://steamdb.info/')


    # vvv = client(win_index=0)
    # vvv.set_proxy('127.0.0.1:7890')
    # # vvv.set_proxy()
    # # vvv.go_url('http://baidu.com')
    # vvv.go_url('https://ipinfo.io/ip')


    # # import time
    # # time.sleep(1)
    # vvv = client(win_index=1)
    # vvv.set_proxy()
    # vvv.go_url('https://ipinfo.io/ip')
    # # print(vvv.clear_storage())
    # # for i in vvv.get_cookies():
    # #     print(i)
    # #     print()

    # vvv = client()
    # vvv.quick_start()
    # vvv.set_proxy('127.0.0.1:7890')
    # vvv.go_url('https://ipinfo.io/ip')
    # vvv.set_proxy()
    # # vvv.go_url('https://ipinfo.io/ip')
    # x = vvv.run_script('''
    # fetch('https://ipinfo.io/ip').then(function(e){
    #     return e.text()
    # })
    # ''')
    # print(x)


    # vvv = client()
    # vvv.quick_start()
    # vvv.change_finger(555)
    # vvv.go_url('https://browserleaks.com/canvas')


    # vvv = local_client()
    # s = vvv.run_script("location.href")
    # print(s)
    # vvv.set_match_url('baidu')
    # vvv.add_script('alert(123)')
    # vvv.clear_add_script()
    # vvv.go_url('http://baidu.com')
    # vvv.set_size(800,800)
    # vvv.set_position(100,100)
    # vvv.run_elements([
    #     {"type":"keydown","key":"a","keyCode":65,"code":"KeyA","timeStamp":24300.59999999404},
    #     {"type":"keydown","key":"s","keyCode":83,"code":"KeyS","timeStamp":24396.79999999702},
    #     {"type":"keydown","key":"d","keyCode":68,"code":"KeyD","timeStamp":24444.70000000298},
    #     {"type":"keyup","key":"a","keyCode":65,"code":"KeyA","timeStamp":24517},
    #     {"type":"keydown","key":"f","keyCode":70,"code":"KeyF","timeStamp":24517.59999999404},
    #     {"type":"keyup","key":"s","keyCode":83,"code":"KeyS","timeStamp":24573.29999999702},
    #     {"type":"keyup","key":"d","keyCode":68,"code":"KeyD","timeStamp":24612.90000000596},
    #     {"type":"keyup","key":"f","keyCode":70,"code":"KeyF","timeStamp":24692.90000000596},
    # ])
    # vvv.debug = True


    # s = vvv.auto_change_resp('/', '''
    # function(body){
    #     return 'alert(123)'
    # }
    # ''')

    # vvv.cdp("Target.enable", {})
    # vvv.cdp("Target.setAutoAttach", {"autoAttach": True, "waitForDebuggerOnStart": True, "flatten": True})

    # vvv.go_url('https://beta.theb.ai/home')
    # print(vvv.frames)
    # print(fjson(vvv.get_frametree()))
    # print(fjson(vvv.get_framelist()))


    # print(fjson(vvv.get_frametree()))
    # s = vvv.frames[0].run_script('window.some = 123')
    # print(s)
    # print(vvv.frames)
    # print(vvv.frames)

    # vvv.cdp("Debugger.setBreakpointsActive", { "active": True })
    # vvv.cdp("Debugger.setBreakpointByUrl", {
    #   "lineNumber": 143,
    #   "url": "http://8.130.117.18:8098/",
    #   "columnNumber": 3601,
    #   "condition": "/** DEVTOOLS_LOGPOINT */ console.log(updatetime)\n\n//# sourceURL=debugger://logpoint"
    # })
    # vvv.cdp("Debugger.setBreakpointsActive", { "active": True })


    # vvv.emulation_iphone()
    # vvv.go_url('http://baidu.com')

    # @server([
    #     client('http://127.0.0.1:18089',0),
    #     client('http://127.0.0.1:18089',1),
    # ])
    # def some(vvv, url):
    #     print(vvv, url)
    #     asdfasdf

    # for i in range(10):
    #     try:
    #         some('123')
    #     except:
    #         pass

    # time.sleep(1)
    # some('123')
    # some('123')
    # vvv = client().quick_start()
    # vvv.go_url('http://baidu.com')


