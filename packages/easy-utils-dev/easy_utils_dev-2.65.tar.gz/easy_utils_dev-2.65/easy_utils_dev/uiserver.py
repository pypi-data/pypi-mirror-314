from werkzeug.serving import ThreadedWSGIServer
from easy_utils_dev.utils import getRandomKey , generateToken
from flask_socketio import SocketIO
from engineio.async_drivers import gevent
from engineio.async_drivers import threading
from flask_cors import CORS
import logging ,  json
from flask import Flask , send_file
from threading import Thread
from easy_utils_dev.custom_env import cenv
from easy_utils_dev.utils import kill_thread
from multiprocessing import Process


def getClassById( id ) :
    return cenv[id]

class UISERVER :
    def __init__(self ,id=getRandomKey(n=15),secretkey=generateToken(),address='localhost',port=5312 , https=False , template_folder='templates/'  ,**kwargs) -> None:
        self.id = id
        self.app = app = Flask(self.id , template_folder=template_folder)
        app.config['SECRET_KEY'] = secretkey
        CORS(app,resources={r"/*":{"origins":"*"}})
        self.address= address 
        self.port = port
        self.thread = None
        self.enable_test_url=True
        if https :
            self.httpProtocol = 'https'
        else :
            self.httpProtocol = 'http'
        self.socketio = SocketIO(app , cors_allowed_origins="*"  ,async_mode='threading' , engineio_logger=False , always_connect=True ,**kwargs )
        cenv[id] = self
        self.fullAddress = f"{self.httpProtocol}://{self.address}:{self.port}"

    def getInstance(self) :
        return self.getFlask() , self.getSocketio() , self.getWsgi()
    
    def getSocketio( self ):
        return self.socketio
    
    def getFlask( self ):
        return self.app
    
    def getWsgi(self) :
        return self.wsgi_server

    def shutdownUi(self) :
        kill_thread(self.thread)
        self.wsgi_server.server_close()
        self.wsgi_server.shutdown()

    def thrStartUi(self) :
        if self.enable_test_url :
            print(f'URL TEST GET /connection/test/internal')
            @self.app.route('/connection/test/internal' , methods=['GET'])
            def test_connection():
                return f"Status=200<br> ID={self.id}<br> one-time-token={getRandomKey(20)}"
        if self.httpProtocol == 'http' :
            con = None
        elif self.httpProtocol == 'https' :
            con='adhoc'
        self.wsgi_server = wsgi_server = ThreadedWSGIServer(
            host = self.address ,
            ssl_context=con,
            port = self.port,
            app = self.app )
        print(f"web-socket: {self.fullAddress}")
        print(f"UI URL : {self.fullAddress}")
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        wsgi_server.serve_forever()
    
    def startUi(self ,daemon ) :
        self.thread = self.flaskprocess = Thread(target=self.thrStartUi)
        self.flaskprocess.daemon = daemon
        self.flaskprocess.start()
        return self.thread