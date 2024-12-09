from .response import Response
from .widget_base import WidgetBase


# --------------------
## holds all interactions with Listbox widgets
class WidgetListbox(WidgetBase):
    # --------------------
    ## select list box option(s) with the given indexes
    #
    # @param x        the x value in screen coordinates
    # @param y        the y value in screen coordinates
    # @param opt_ids  one or more options to select
    # @return ack_nak response
    def lbox_select_at(self, x: int, y: int, opt_ids):
        rsp = Response('lbox_select_at')
        return self._lbox_select1(rsp, x, y, opt_ids)

    # --------------------
    ## select option(s) on the given item
    #
    # @param item      the widget item to set the text on
    # @param opt_ids   one or more options to select
    # @return ack_nak response
    def lbox_select_on(self, item: dict, opt_ids):
        rsp = Response('lbox_select_on')
        return self._lbox_select2(rsp, item, opt_ids)

    # --------------------
    ## select option(s) on the widget with the given path
    #
    # @param widget_path  the path to the widget
    # @param opt_ids      the option id(s) to set
    # @return ack_nak response
    def lbox_select(self, widget_path: list, opt_ids):
        rsp = Response('lbox_select')
        return self._lbox_select3(rsp, widget_path, opt_ids)

    # --------------------
    ## handle a selection on the wigdet at the given path
    #
    # @param rsp          the current response object
    # @param widget_path  the widget item to set the text on
    # @param opt_ids      one or more options to select
    # @return ack_nak response
    def _lbox_select3(self, rsp: Response, widget_path: list, opt_ids):
        if rsp.check_is_set(widget_path, 'lbox select path'):
            return rsp.ack_nak

        item = self._harness.search(widget_path)
        if rsp.check_for_failure(item):
            return item

        return self._lbox_select2(rsp, item, opt_ids)

    # --------------------
    ## handle a selection on the given item
    #
    # @param rsp       the current response object
    # @param item      the widget item to set the text on
    # @param opt_ids   one or more options to select
    # @return ack_nak response
    def _lbox_select2(self, rsp: Response, item: dict, opt_ids):
        if rsp.check_coordinates_set(item, 'lbox select item'):
            return rsp.ack_nak

        x, y = self._get_coords_from(item)
        return self._lbox_select1(rsp, x, y, opt_ids)

    # --------------------
    ## handle a selection on the given x,y coordinates
    #
    # @param rsp      the current response object
    # @param x        the x value in screen coordinates
    # @param y        the y value in screen coordinates
    # @param opt_ids  one or more options to select
    # @return ack_nak response
    def _lbox_select1(self, rsp: Response, x: int, y: int, opt_ids):
        if rsp.check_is_set(opt_ids, 'lbox select opt_ids'):
            return rsp.ack_nak

        if rsp.check_coordinate_values(x, y, 'lbox select'):
            return rsp.ack_nak

        if not isinstance(opt_ids, list):
            opt_ids = [opt_ids]
        ack_nak = self._client.lbox_select(x, y, opt_ids)
        rsp.check_response(ack_nak)
        return rsp.ack_nak
