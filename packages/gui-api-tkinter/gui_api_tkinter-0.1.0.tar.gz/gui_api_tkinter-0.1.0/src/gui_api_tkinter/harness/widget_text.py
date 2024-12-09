from .response import Response
from .widget_base import WidgetBase


# --------------------
## holds all interactions with text-based widgets
class WidgetText(WidgetBase):
    # --------------------
    ## set text in widget at given screen coordinates
    #
    # @param x    the x value in screen coordinates
    # @param y    the y value in screen coordinates
    # @param msg  the text to set
    # @return ack_nak response
    def set_text_at(self, x: int, y: int, msg: str):
        rsp = Response('set_text_at')
        return self._set_text1(rsp, x, y, msg)

    # --------------------
    ## set text on the given item
    #
    # @param item  the widget item to set the text on
    # @param msg   the text to set
    # @return ack_nak response
    def set_text_on(self, item: dict, msg: str):
        rsp = Response('set_text_on')
        return self._set_text2(rsp, item, msg)

    # --------------------
    ## set text on the widget at the given search list
    #
    # @param widget_path  the path to the widget
    # @param msg          the text to set
    # @return ack_nak response
    def set_text(self, widget_path: list, msg: str):
        rsp = Response('set_text')
        return self._set_text3(rsp, widget_path, msg)

    # --------------------
    ## set text on the widget at the given search list
    #
    # @param rsp          the current response
    # @param widget_path  the path to the widget
    # @param msg          the text to set
    # @return ack_nak response
    def _set_text3(self, rsp, widget_path: list, msg: str):
        if rsp.check_is_set(widget_path, 'set text path'):
            return rsp.ack_nak

        item = self._harness.search(widget_path)
        if rsp.check_for_failure(item):
            return item

        return self._set_text2(rsp, item, msg)

    # --------------------
    ## set text on the given item
    #
    # @param rsp   the current response
    # @param item  the widget item to set the text on
    # @param msg   the text to set
    # @return ack_nak response
    def _set_text2(self, rsp, item: dict, msg: str):
        if rsp.check_coordinates_set(item, 'set text item'):
            return rsp.ack_nak

        x, y = self._get_coords_from(item)
        return self._set_text1(rsp, x, y, msg)

    # --------------------
    ## set text in widget at given screen coordinates
    #
    # @param rsp  the current response
    # @param x    the x value in screen coordinates
    # @param y    the y value in screen coordinates
    # @param msg  the text to set
    # @return ack_nak response
    def _set_text1(self, rsp: Response, x: int, y: int, msg: str):
        if rsp.check_is_set(msg, 'set text msg', check_empty=False):
            return rsp.ack_nak

        if rsp.check_coordinate_values(x, y, 'set text'):
            return rsp.ack_nak

        ack_nak = self._client.set_text(x, y, msg)
        rsp.check_response(ack_nak)
        return rsp.ack_nak
