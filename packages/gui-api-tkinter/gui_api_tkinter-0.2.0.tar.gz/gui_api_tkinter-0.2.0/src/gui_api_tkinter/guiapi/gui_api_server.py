import json
import threading
import time

from socket_oneline import OnelineServer

from .. import svc


# --------------------
## Server mainline to communication with the socket server
class GuiApiServer:
    # --------------------
    ## constructor
    def __init__(self):
        ## holds reference to the Oneline Server
        self._olserver = OnelineServer()

        # for debug
        # self._last_time = time.time()

    # --------------------
    ## initialize
    # Start the OnelineServer
    #
    # @return None
    def init(self):
        # svc.logger.info('server      : started')

        self._olserver.callback = self._callback
        self._olserver.ip_address = svc.cfg.ip_address
        self._olserver.ip_port = svc.cfg.ip_port
        self._olserver.verbose = svc.cfg.verbose
        self._olserver.logger = svc.logger

        if not self._olserver.start():
            svc.logger.info('ERR failed to set params')
            return
        time.sleep(0.1)

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        if self._olserver is not None:
            self._olserver.term()
            self._olserver = None

    # --------------------
    ## send an ack to the client
    #
    # @param cmd  the command this ack response is for
    # @return None
    def send_ack(self, cmd: dict):
        rsp = {
            'rsp': cmd,
            'value': 'ack',
        }
        self.send(rsp)

    # --------------------
    ## send an nak to the client
    #
    # @param cmd     the command this nak response is for
    # @param reason  the reason for the nak
    # @return None
    def send_nak(self, cmd: dict, reason: str):
        rsp = {
            'rsp': cmd,
            'value': 'nak',
            'reason': reason,
        }
        self.send(rsp)

    # --------------------
    ## send response/message to the client
    #
    # @param msg  the message to send (no newline needed)
    # @return None
    def send(self, msg: dict):
        self._olserver.send(json.dumps(msg))

    # --------------------
    ## callback function used by server to handle incoming commands
    #
    # @param command     the incoming command from the client
    # @param is_invalid  indicates if the command is invalid
    # @return None
    def _callback(self, command, is_invalid):
        # all commands sent here should be json
        cmd = json.loads(command)
        # the id should indicate the server thread id
        svc.logger.info(f'server      : callback: cmd={cmd["cmd"]: <10} is_invalid={is_invalid} '
                        f'id={threading.get_ident()}')
        if is_invalid:
            return

        # cause the function below to be called under the tkinter thread
        svc.guiapi.run_callback(cmd, is_invalid)

    # --------------------
    ## this function executed under tkinter's thread
    #
    # @param cmd         the incoming command from the client
    # @param is_invalid  indicates if the command is invalid
    # @return None
    def tkinter_callback(self, cmd, is_invalid):  # pylint: disable=unused-argument
        # elapsed = time.time() - self._last_time
        # self._last_time = time.time()
        # the id should indicate the tkinter thread id
        # svc.logger.info(f'tkinter_cb  : {elapsed: >0.3f}     cmd={cmd["cmd"]: <10} is_invalid={is_invalid} '
        #                f'id={threading.get_ident()}')

        if cmd['cmd'] == 'get_screen':
            screen = svc.guiapi.get_screen()
            screen['rsp'] = cmd['cmd']
            self.send(screen)
        elif cmd['cmd'] == 'click_left':
            rsp = svc.guiapi.click_left(cmd)
            self.send(rsp)
        elif cmd['cmd'] == 'menu_click':
            rsp = svc.guiapi.menu_invoke(cmd)
            self.send(rsp)
        elif cmd['cmd'] == 'set_text':
            rsp = svc.guiapi.set_text(cmd)
            self.send(rsp)
        elif cmd['cmd'] == 'lbox_select':
            rsp = svc.guiapi.lbox_select(cmd)
            self.send(rsp)
        elif cmd['cmd'] == 'combobox_set':
            rsp = svc.guiapi.combobox_set(cmd)
            self.send(rsp)
        elif svc.cfg.callback is not None:
            rsp = svc.cfg.callback(cmd)
            if rsp is None:
                pass  # no response to send
            else:
                rsp['rsp'] = cmd['cmd']
                self.send(rsp)
        else:
            # unknown command, let client know
            self.send_nak(cmd['cmd'], 'unknown command')
