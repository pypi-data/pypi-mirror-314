import copy
import time
from typing import Union

from .client import Client
from .response import Response
from .widget_click import WidgetClick
from .widget_combobox import WidgetCombobox
from .widget_listbox import WidgetListbox
from .widget_text import WidgetText
from .. import svc
from ..cfg import Cfg
from ..constants import Constants
from ..logger_null import LoggerNull


# --------------------
## test harness used to communicate with GuiApi Server
class GuiApiHarness:  # pylint: disable=too-many-public-methods
    # --------------------
    ## constructor
    def __init__(self):
        ## holds reference to common configuration information
        self.cfg = None
        ## holds reference to logger object
        self.logger = None
        ## holds current screen content
        self._content = None
        ## holds current menu paths found in the current screen content
        self._menu_paths = None
        ## holds reference to the socket client
        self._client = None

    # --------------------
    ## initialize
    #
    # @param logger   (optional) a reference to a logger object
    # @return None
    def init(self, logger=None):
        self.cfg = Cfg()
        svc.cfg = self.cfg
        if logger is None:
            self.logger = LoggerNull()
        else:
            self.logger = logger
        svc.logger = self.logger

        svc.cfg.init()
        self._client = Client()

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        if self._client is not None:
            self._client.term()
            self._client = None

    # --------------------
    ## the version string
    #
    # @return the version
    @property
    def version(self) -> str:
        return Constants.version

    # === connection related

    # --------------------
    ## connect to the GUI API server running inside the GUI
    #
    # @return False
    def connect(self):
        ok = False
        if self.is_connected():
            self.logger.info('connect(): already connected, ignoring')
        else:
            self._client.init()
            time.sleep(0.5)
            ok = True

        return ok

    # --------------------
    ## check if connected to the server
    #
    # @return True if connected, False otherwise
    def is_connected(self):
        if self._client is None:
            return False

        return self._client.is_connected()

    # --------------------
    ## send a command and wait for a response
    #
    # @param cmd  the command to send
    # @return the response
    def send_recv(self, cmd: dict) -> dict:
        return self._client.send_recv(cmd)

    # --------------------
    ## send a command, no response expected
    #
    # @param cmd  the command to send
    # @return None
    def send(self, cmd: dict):
        self._client.send(cmd)

    # === Screen related

    # --------------------
    ## get the current screen contents in JSON format
    #
    # @return screen content in JSON format
    def get_screen(self) -> list:
        screen = self._client.get_screen()
        # currently can only handle 1 root window,
        # therefore content is a list of one item
        self._content = [screen]

        # calc all menu_paths from current screen content
        # if there is a Menu it is the first child of the root
        # print(f'@@@ menu: {self._content[0]["children"][0]}')
        self._menu_paths = {}
        if self._content[0]['children'][0]['class'] == 'Menu':
            all_menus = self._content[0]['children'][0]
            self._get_menus([], all_menus)
        # if there is no menu, then _menu_paths is empty

        return self._content

    # --------------------
    ## recurse through the screen content looking for all menu paths.
    #
    # @param parent     the current list of menus until this one
    # @param menu_info  the current menu info from tkinter
    def _get_menus(self, parent, menu_info):
        cascade_posn = 0
        for menu_item in menu_info['menu']:
            menu_type = menu_item['type']
            menu_label = menu_item['label']

            # make a local copy of the path so far
            path = copy.deepcopy(parent)
            path.append(menu_label)
            if menu_type == 'cascade':
                # recurse on child menus in this cascade
                children = menu_info['children']
                self._get_menus(path, children[cascade_posn])
                # the children are ordered based on the nth cascade position
                cascade_posn += 1
            else:  # menu_type == 'command'
                # found the end of a menu path, save the info
                self._menu_paths[tuple(path)] = menu_item

    # --------------------
    ## the current menu paths in use.
    # the keys to the dictionary are the paths, the values
    # are menuitem info e.g. state
    #
    # @return a dict of menu info
    @property
    def menu_paths(self) -> dict:
        return self._menu_paths

    # --------------------
    ## the current screen contents in JSON format
    #
    # @return the current screen contents in JSON format
    @property
    def content(self) -> dict:
        return self._content

    # === Search related

    # --------------------
    ## determine if the widget matching the path exists or not
    #
    # @param search_path  a list of widget names
    # @returns True if path exists, False otherwise
    def exists(self, search_path: list):
        foundit = False
        rsp = Response('exists')
        if rsp.check_is_none(self._content, 'content'):
            return foundit

        if rsp.check_is_set(search_path, 'search path'):
            return foundit

        item = self._search_content(self._content, search_path, 0)
        if rsp.check_is_not_found(item, 'search path'):
            return foundit

        # it was found, no errors
        foundit = True
        return foundit

    # --------------------
    ## find the widget matching the path given in the search list
    #
    # @param search_path  a list of widget names
    # @return the widget item if found, nak otherwise
    def search(self, search_path: list):
        rsp = Response('search')

        if rsp.check_is_none(self._content, 'content'):
            return rsp.ack_nak

        if rsp.check_is_set(search_path, 'search path'):
            return rsp.ack_nak

        item = self._search_content(self._content, search_path, 0)
        if rsp.check_is_not_found(item, 'search path'):
            return rsp.ack_nak

        # it was found, no errors
        return item

    # --------------------
    ## recursive function to find the widget item that matches the search list
    #
    # @param content      the screen content to search
    # @param search_path  the list of widget names to search
    # @param index        the current entry in the search_list
    # @return the widget item if matches the last entry in search_list, None otherwise
    def _search_content(self, content, search_path, index=0):
        if content is None or \
                search_path is None or \
                len(search_path) == 0:
            return None

        # uncomment to debug
        # self.logger.info(f'DBG searching index={index} srch={search_path}')
        search_name = search_path[index]
        for item in content:
            if item['name'] == search_name:
                if index == len(search_path) - 1:
                    # uncomment to debug
                    # self.logger.info(f'DBG found it  index={index} node={item}')
                    return item

                # it matched, but not at the end of the search list, so check the children
                # uncomment to debug
                # self.logger.info(f'DBG children  index={index} srch={search_name} curr={item["name"]}')
                node = self._search_content(item['children'], search_path, index + 1)
                if node is not None:
                    return node

        # uncoment to debug
        # self.logger.info(f'DBG not_found index={index} {search_name}')
        return None

    # === Menu related

    # --------------------
    ## select the menu item at the given menu path
    #
    # @param menu_path   the list of menu indices to search
    # @return ack_nak response
    def menu_click(self, menu_path: Union[list | tuple]):
        rsp = Response('menu_click')

        if rsp.check_is_set(menu_path, 'menu path'):
            return rsp.ack_nak

        # if path is not in set of menu_paths, then return nak
        if isinstance(menu_path, list):
            menu_path = tuple(menu_path)
        item = self._menu_paths.get(menu_path)

        if rsp.check_is_not_found(item, 'menu path'):
            return rsp.ack_nak

        wgt_hash = item['wgt_hash']

        ack_nak = self._client.menu_click(menu_path, wgt_hash)
        rsp.check_response(ack_nak)
        return rsp.ack_nak

    # --------------------
    ## report paths to menu items
    #
    # @return list of paths to each menu item available
    def menu_report(self):
        if self._content is None:
            svc.logger.info('menu_report: content is empty')
            return None

        return list(self._menu_paths.keys())

    # --------------------
    ## return menu item for given path
    #
    # @param menu_path  the path to the menu item
    # @return the menu item content
    def menu_item(self, menu_path: list):
        rsp = Response('menu_item')

        if rsp.check_is_none(self._content, 'content'):
            return rsp.ack_nak

        if rsp.check_is_set(menu_path, 'menu path'):
            return rsp.ack_nak

        if isinstance(menu_path, list):
            menu_path = tuple(menu_path)
        item = self._menu_paths.get(menu_path)

        if rsp.check_is_not_found(item, 'menu path'):
            return rsp.ack_nak

        # it was found, no errors
        return item

    # === Click related

    # --------------------
    ## click left mouse button at given screen coordinates
    #
    # @param x   the x value in screen coordinates
    # @param y   the y value in screen coordinates
    # @return ack_nak response
    def click_left_at(self, x: int, y: int):
        wd = WidgetClick(self, self._client)
        return wd.click_left_at(x, y)

    # --------------------
    ## click the left mouse button on the given widget item
    #
    # @param item  the widget item to click on
    # @return ack_nak response
    def click_left_on(self, item: dict):
        wd = WidgetClick(self, self._client)
        return wd.click_left_on(item)

    # --------------------
    ## click the left mouse button on the widget at the given search list
    #
    # @param click_path  the path to the widget
    # @return ack_nak response
    def click_left(self, click_path: list):
        wd = WidgetClick(self, self._client)
        return wd.click_left(click_path)

    # === Entry, Text box

    # --------------------
    ## set text in widget at given screen coordinates
    #
    # @param x    the x value in screen coordinates
    # @param y    the y value in screen coordinates
    # @param msg  the text to set
    # @return ack_nak response
    def set_text_at(self, x: int, y: int, msg: str):
        wd = WidgetText(self, self._client)
        return wd.set_text_at(x, y, msg)

    # --------------------
    ## set text on the given item
    #
    # @param item  the widget item to set the text on
    # @param msg   the text to set
    # @return ack_nak response
    def set_text_on(self, item: dict, msg: str):
        wd = WidgetText(self, self._client)
        return wd.set_text_on(item, msg)

    # --------------------
    ## set text on the widget at the given search list
    #
    # @param set_path  the path to the widget
    # @param msg       the text to set
    # @return ack_nak response
    def set_text(self, set_path: list, msg: str):
        wd = WidgetText(self, self._client)
        return wd.set_text(set_path, msg)

    # === List Box

    # --------------------
    ## select list box option(s) with the given indexes
    #
    # @param x        the x value in screen coordinates
    # @param y        the y value in screen coordinates
    # @param opt_ids  one or more options to select
    # @return ack_nak response
    def lbox_select_at(self, x: int, y: int, opt_ids):
        wd = WidgetListbox(self, self._client)
        return wd.lbox_select_at(x, y, opt_ids)

    # --------------------
    ## select option(s) on the given item
    #
    # @param item      the widget item to set the text on
    # @param opt_ids   one or more options to select
    # @return ack_nak response
    def lbox_select_on(self, item: dict, opt_ids):
        wd = WidgetListbox(self, self._client)
        return wd.lbox_select_on(item, opt_ids)

    # --------------------
    ## select option(s) on the widget with the given path
    #
    # @param set_path  the path to the widget
    # @param opt_ids   the option id(s) to set
    # @return ack_nak response
    def lbox_select(self, set_path: list, opt_ids):
        wd = WidgetListbox(self, self._client)
        return wd.lbox_select(set_path, opt_ids)

    # === Combo Box

    # --------------------
    ## set combobox option
    #
    # @param x         the x value in screen coordinates
    # @param y         the y value in screen coordinates
    # @param opt_id    the option to set
    # @return ack_nak response
    def combobox_set_at(self, x: int, y: int, opt_id: str):
        wd = WidgetCombobox(self, self._client)
        return wd.combobox_set_at(x, y, opt_id)

    # --------------------
    ## set option on the given item
    #
    # @param item      the widget item to set the option on
    # @param opt_id    the option to set
    # @return ack_nak response
    def combobox_set_on(self, item: dict, opt_id: str):
        wd = WidgetCombobox(self, self._client)
        return wd.combobox_set_on(item, opt_id)

    # --------------------
    ## set option on the widget with the given path
    #
    # @param set_path  the path to the widget
    # @param opt_id    the option to set
    # @return ack_nak response
    def combobox_set(self, set_path: list, opt_id: str):
        wd = WidgetCombobox(self, self._client)
        return wd.combobox_set(set_path, opt_id)
