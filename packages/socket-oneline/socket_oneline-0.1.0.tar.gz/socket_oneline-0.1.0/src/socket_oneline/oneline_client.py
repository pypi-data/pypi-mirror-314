import socket
import sys
import time

from .constants import Constants


# --------------------
## holds the Oneline Client
class OnelineClient:
    # --------------------
    ## initialize
    def __init__(self):
        ## the IP address to use for socket
        self._ip_address = None
        ## the IP port to use for socket
        self._ip_port = None
        ## holds reference to the outgoing socket
        self._sock = None
        ## indicates if the client is currently connected to a Server
        self._connected = False
        ## holds reference to a logger, if any
        self._logger = None
        ## indicates logging verbosity, if False, no logging is done
        self._verbose = False

    # -------------------
    ## returns the current version
    #
    # @return the version string
    @property
    def version(self):
        return Constants.version

    # --------------------
    ## getter for ip_address
    #
    # @return None
    @property
    def ip_address(self):
        return self._ip_address

    # --------------------
    ## setter for ip_address
    #
    # @param val  the value to set to
    # @return None
    @ip_address.setter
    def ip_address(self, val):
        self._ip_address = val

    # --------------------
    ## getter for ip_port
    #
    # @return the port
    @property
    def ip_port(self):
        return self._ip_port

    # --------------------
    ## setter for ip_port
    #
    # @param val  the value to set to
    # @return None
    @ip_port.setter
    def ip_port(self, val):
        self._ip_port = val

    # --------------------
    ## getter for logger
    #
    # @return a reference to the logger
    @property
    def logger(self):
        return self._logger

    # --------------------
    ## setter for logger
    #
    # @param val  the value to set to
    # @return None
    @logger.setter
    def logger(self, val):
        self._logger = val

    # --------------------
    ## getter for verbose
    #
    # @return True if verbose mode, False otherwise
    @property
    def verbose(self):
        return self._verbose

    # --------------------
    ## setter for verbose
    #
    # @param val  the value to set to
    # @return None
    @verbose.setter
    def verbose(self, val):
        self._verbose = val

    # --------------------
    ## Check if there is an active connection to the server
    # Note: this will normally take an extra send or usually two to
    # cause the broken connection to be detected.
    #
    # @return True if there is an active connection, False otherwise
    @property
    def connected(self):
        return self._sock is not None and self._connected

    # --------------------
    ## initialize; handles any incoming parameters and checks if they are all set correctly
    #
    # @param ip_address  the IP address to use
    # @param ip_port     the IP port to use
    # @param logger      reference to a logger to use
    # @param verbose     indicates whether to log or not
    # @return True if all parameters are set correctly, False otherwise
    def init(self,
             ip_address: str = None,
             ip_port: int = None,
             logger=None,
             verbose: bool = None):
        if ip_address is not None:
            self._ip_address = ip_address
        if ip_port is not None:
            self._ip_port = ip_port
        if logger is not None:
            self._logger = logger
        if verbose is not None:
            self._verbose = verbose

        return self._params_ok()

    # --------------------
    ## checks of all parameters are set correctly
    #
    # @return returns True if they are set, otherwise False
    def _params_ok(self) -> bool:
        ok = True

        if self._ip_address is None:
            ok = False
            self._log('ERR  ip address is not set')

        if self._ip_port is None:
            ok = False
            self._log('ERR  ip port is not set')

        return ok

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        self._disconnect_from_server()

    # --------------------
    ## create and start tcp socket to OnelineServer
    #
    # @return True if connection worked ok, False otherwise
    def connect(self):
        if self._sock is not None:
            self.disconnect()

        # Create a socket (SOCK_STREAM means a TCP socket)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self._sock.connect((self._ip_address, self._ip_port))
            self._sock.settimeout(0.5)
            self.send('ping')
            rsp = self.recv()
            if rsp == 'pong':
                self._log(f'connected on {self._ip_address}:{self._ip_port}')
                self._connected = True
        except socket.error:
            self._log(f'ERR connection failed on {self._ip_address}:{self._ip_port}')
            self._sock = None

        return self._connected

    # --------------------
    ## request shutdown the server
    #
    # @return None
    def shutdown(self):
        self.send('shutdown')
        self._disconnect_from_server()

    # --------------------
    ## request disconnect from the server
    #
    # @return None
    def disconnect(self):
        self.send('disconnect')
        self._disconnect_from_server()

    # --------------------
    ## close the socket
    #
    # @return None
    def _disconnect_from_server(self):
        if self._sock is None:
            self._log('already disconnected from server')
        else:
            try:
                if self._connected:
                    self._sock.shutdown(socket.SHUT_RDWR)

                self._sock.close()
            except OSError:  # pragma: no cover
                # coverage: cannot not cause this scenario to occur in UT
                pass

            self._log('disconnected from server')

        self._sock = None
        self._connected = False

    # --------------------
    ## send the given command to the OneLineServer
    #
    # @param cmd  the command to send
    # @return None
    def send(self, cmd):
        if self._sock is None:
            return

        try:
            self._sock.sendall(f'{cmd}\x0A'.encode())
        except ConnectionResetError:
            self._log('send(): ConnectionResetError occurred')
            self._sock = None
            self._connected = False
        except BrokenPipeError:
            self._log('send(): BrokenPipeError occurred')
            self._sock = None
            self._connected = False

    # --------------------
    ## wait for a message from the OneLineServer
    #
    # @param timeout (optional) max time to wait for response
    # @return if recv succeeded the received response, otherwise ''
    def recv(self, timeout=3):
        rsp = b''
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            try:
                if self._sock is None:
                    self._log('recv(): socket is None')
                    break

                ch = self._sock.recv(1)
                if ch == b'\x0A':
                    break
                rsp += ch
            except socket.timeout:
                # happens frequently, no need to log
                pass
            except (OSError, socket.error) as excp:
                self._log(f'recv(): socket exception occurred: {excp}')
                break

        rsp = rsp.decode()
        rsp = rsp.strip()
        return rsp

    # --------------------
    ## log the message
    # if verbose is False, then nothing is logged
    # if verbose is True, and logger is defined, the msg is logged
    # if verbose is True, and logger is not defined, the msg is printed to stdout
    #
    # @param msg  the message to log
    # @return None
    def _log(self, msg):
        # handle verbose/quiet
        if not self._verbose:
            return

        buf = f'oneline clnt: {msg}'
        if self._logger is None:
            print(buf)
            sys.stdout.flush()
        else:
            self._logger.info(buf)
