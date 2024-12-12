from .gui_api_server import GuiApiServer
from .. import svc
from ..cfg import Cfg
from ..logger_null import LoggerNull


# --------------------
## holds functions to interact with tkinter and the server
class GuiApiTkinter:
    # --------------------
    ## constructor
    def __init__(self):
        ## the top level root window for the GUI
        self._window = None
        ## the top level menu
        self._menu = None
        ## the current screen content
        self._screen = None
        ## list of menu paths available
        self._menu_hash = {}
        ## next menu item hash key
        self._menu_hash_key = 0

        svc.guiapi = self
        svc.server = GuiApiServer()

    # --------------------
    ## initialize. Configure and start the server
    #
    # @param ip_address   (optional) the socket address for the server
    # @param ip_port      (optional) the socket port for the server
    # @param logger       (optional) reference to a logger object
    # @param verbose      (optional) flag indicating if verbose logging is required
    # @param callback     (optional) reference to callback function for unknown incoming commands
    # @return None
    def init(self, ip_address=None, ip_port=None, logger=None, verbose=None, callback=None):
        svc.cfg = Cfg()
        if logger is None:
            svc.logger = LoggerNull()
        else:
            svc.logger = logger
        if verbose is not None:
            svc.cfg.verbose = verbose
        if ip_address is not None:
            svc.cfg.ip_address = ip_address
        if ip_port is not None:
            svc.cfg.ip_port = ip_port
        if callback is not None:
            svc.cfg.callback = callback

        svc.server.init()
        self._window = None
        self._menu = None
        self._screen = None
        self._menu_hash_key = 0

    # --------------------
    ## set the TK root window
    #
    # @param window   the TK root window
    # @return None
    def set_window(self, window):
        self._window = window

    # --------------------
    ## run callback in tkinter main thread
    #
    # @param cmd         the incoming command from the client
    # @param is_invalid  indicates if the command is invalid
    # @return None
    def run_callback(self, cmd, is_invalid):
        if self._window is not None:
            # cause the server callback to run under the tkinter thread
            self._window.after(1, svc.server.tkinter_callback, cmd, is_invalid)
        else:
            # no window, so running headless
            svc.server.tkinter_callback(cmd, is_invalid)

    # --------------------
    ## set the top level menu
    #
    # @param menu  the top level menu
    # @return None
    def set_menu(self, menu):
        self._menu = menu

    # --------------------
    ## in the given widget, set an internal name to be used for screen dump purposes
    #
    # @param widget  the widget to set the name in
    # @param name    the name to use
    # @return None
    def set_name(self, widget, name):
        setattr(widget, 'guiapi_name', name)

    # --------------------
    ## generate a left mouse button click at the given screen coordinates
    #
    # @param cmd   the incoming JSON command
    # @return ack/nak response in JSON format
    def click_left(self, cmd):
        rsp = {
            'rsp': cmd['cmd'],
            'value': 'ack',
        }

        x = cmd['x']
        y = cmd['y']
        # svc.logger.info(f'click_left: {x} {y}')
        win = self._window.winfo_containing(x, y)
        # uncomment to debug
        # n = getattr(w, 'guiapi_name', '<unknown>')
        # svc.logger.info(f'DBG click_left: on widget.name: {n}')
        win.event_generate('<Enter>', x=x, y=y)
        win.event_generate('<Button-1>', x=x, y=y)
        win.event_generate('<ButtonRelease-1>', x=x, y=y)

        return rsp

    # --------------------
    ## set the text in the Entry widget
    #
    # @param cmd   the incoming JSON command
    # @return ack/nak response in JSON format
    def set_text(self, cmd):
        rsp = {
            'rsp': cmd['cmd'],
            'value': 'ack',
        }

        x = cmd['x']
        y = cmd['y']
        # svc.logger.info(f'set_text: {x} {y}')
        wgt = self._window.winfo_containing(x, y)

        wgt.focus_set()

        # start with empty text
        if wgt.winfo_class() == 'Text':
            wgt.delete('1.0', 'end')
        else:
            wgt.delete('0', 'end')

        # send a keypress for each character in the incoming string
        for ch in cmd['msg']:
            if ch == '\n':
                # note: ignored by Entry widgets
                wgt.event_generate('<KeyPress-Return>')
            elif ch == '\x01':
                wgt.event_generate('<Left>')
            elif ch == '\x02':
                wgt.event_generate('<Right>')
            elif ch == '\x08':
                wgt.event_generate('<BackSpace>')
            elif ch == ' ':
                wgt.event_generate('<space>')
            elif ch == '<':
                wgt.event_generate('<less>')
            else:
                wgt.event_generate(f'<KeyPress-{ch}>')

        wgt.update()

        return rsp

    # --------------------
    ## get a screen dump in JSON format of the currently displayed screen(s)
    #
    # @return screen content in JSON format
    def get_screen(self):
        # svc.logger.info('get_screen')
        self._screen = self._report_window(self._window)
        # uncomment to debug
        # for hash_key in self._menu_hash:
        #     wgt, index = self._menu_hash[hash_key]
        #     name = wgt.entrycget(index, 'label')
        #     svc.logger.info(f'  hash_key: {hash_key} title:{name}')

        # uncomment to debug
        # import json
        # svc.logger.info(f'screen:\n{json.dumps(self._screen, indent=4)}')
        # svc.logger.info('get_screen done')
        return self._screen

    # --------------------
    ## get screen content for the given window/widget in JSON format
    #
    # @param wgt the widget to get the screen content for
    # @return screen content in JSON format
    def _report_window(self, wgt):
        if wgt is None:
            svc.logger.info('_report_window: wgt is None')
            return None

        node = {
            'class': wgt.winfo_class(),
            'name': getattr(wgt, 'guiapi_name', '<unknown>'),
            'title': wgt.title(),
            'geometry': wgt.geometry(),
        }
        self._get_coordinates(wgt, node)
        # svc.logger.info(f'node: {node}')

        node['children'] = []
        for frame in wgt.winfo_children():
            child = {}
            self._report_child(frame, child)
            if child:
                node['children'].append(child)

        return node

    # --------------------
    ## get screen content for the given wgt in JSON format
    #
    # @param wgt  the wgt to get the screen content for
    # @param node   the node/widget to get the screen content for
    # @return screen content in JSON format
    def _report_child(self, wgt, node):
        node['class'] = wgt.winfo_class()
        node['name'] = getattr(wgt, 'guiapi_name', '<unknown>')

        # menus are handled differently
        if wgt.winfo_class() in ['Menu']:
            node['menu'] = []
            if wgt.index("end") is None:
                svc.logger.info(f'wgt.index is None, class:{wgt.winfo_class()}')
                return

            for index in range(0, wgt.index('end') + 1):
                if wgt.type(index) in ['command', 'cascade']:
                    self._menu_hash[self._menu_hash_key] = (wgt, index)
                    menuitem = {
                        'index': index,
                        'type': wgt.type(index),
                        'label': wgt.entrycget(index, 'label'),
                        'state': wgt.entrycget(index, 'state'),
                        'wgt_hash': self._menu_hash_key,
                    }
                    node['menu'].append(menuitem)
                    self._menu_hash_key += 1
                    # svc.logger.info(f'   index:{index} type:{wgt.type(index)} label:{wgt.entrycget(index, "label")}')
                else:  # tearoff or separator
                    # svc.logger.info(f'   index:{index} type:{wgt.type(index)}')
                    pass
            # svc.logger.info('   ---')
        else:
            foundit = True
            if wgt.winfo_class() in ['Label', 'Button', 'Radiobutton']:
                # text on the screen and the current enable/disable state
                node['value'] = wgt.cget('text')
            elif wgt.winfo_class() in ['Listbox']:
                # value is a list of all possible items in the listbox
                node['value'] = wgt.get(0, wgt.index('end'))
            elif wgt.winfo_class() in ['Entry', 'TCombobox']:
                node['value'] = wgt.get()
            elif wgt.winfo_class() in ['Text']:
                # get from the 1st char to the end. Note: always includes a newline
                node['value'] = wgt.get('1.0', 'end')
            else:
                foundit = False

            if foundit:
                node['state'] = str(wgt.cget('state'))
            else:
                node['value'] = '<unknown>'
                node['state'] = '<unknown>'

        self._get_coordinates(wgt, node)

        node['children'] = []
        for ch in wgt.winfo_children():
            child = {}
            self._report_child(ch, child)
            node['children'].append(child)

    # --------------------
    ## get coordinates for the given widget and add it to the current node
    #
    # @param wgt  the widget to get the screen content for
    # @param node  the node to add the coordinates to
    # @return None
    def _get_coordinates(self, wgt, node):
        x1 = wgt.winfo_rootx()
        y1 = wgt.winfo_rooty()
        x2 = x1 + wgt.winfo_width()
        y2 = y1 + wgt.winfo_height()
        node['coordinates'] = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
        }

    # --------------------
    ## invoke a menu item with menu path
    #
    # @param cmd   the menuitem's hash value
    # @return ack/nak response in JSON format
    def menu_invoke(self, cmd):
        # svc.logger.info(f'DBG menu_invoke enter: {cmd["wgt_hash"]} {cmd["menu_path"]}')
        rsp = {
            'rsp': cmd['cmd'],
            'value': 'ack',
        }
        wgt, index = self._menu_hash[cmd['wgt_hash']]
        wgt.invoke(index)

        return rsp

    # --------------------
    ## select an option on a listbox
    #
    # @param cmd   the incoming JSON command
    # @return ack/nak response in JSON format
    def lbox_select(self, cmd):
        rsp = {
            'rsp': cmd['cmd'],
            'value': 'ack',
        }

        x = cmd['x']
        y = cmd['y']
        # svc.logger.info(f'lbox_select: {x} {y}')
        wgt = self._window.winfo_containing(x, y)
        # uncomment to debug
        # n = getattr(w, 'guiapi_name', '<unknown>')
        # svc.logger.info(f'DBG lbox_select: on widget.name: {n}')
        # w.selection_clear(0, tkinter.END)
        # svc.logger.info(f'lbox_select: current select: {wgt.curselection()}')
        wgt.selection_clear(0, 'end')
        for i in cmd['opt_id']:
            wgt.select_set(i)
        wgt.event_generate('<<ListboxSelect>>')

        return rsp

    # --------------------
    ## set an option on a combobox
    #
    # @param cmd   the incoming JSON command
    # @return ack/nak response in JSON format
    def combobox_set(self, cmd):
        rsp = {
            'rsp': cmd['cmd'],
            'value': 'ack',
        }

        x = cmd['x']
        y = cmd['y']
        # svc.logger.info(f'combobox_set: {x} {y}')
        wgt = self._window.winfo_containing(x, y)
        # uncomment to debug
        # n = getattr(w, 'guiapi_name', '<unknown>')
        # svc.logger.info(f'DBG combobox_set: on widget.name: {n}')

        wgt.set(cmd['opt_id'])
        wgt.event_generate('<<ComboboxSelected>>')

        return rsp
