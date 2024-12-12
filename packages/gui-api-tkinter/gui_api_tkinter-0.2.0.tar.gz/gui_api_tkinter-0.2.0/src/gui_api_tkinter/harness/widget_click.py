from .response import Response
from .widget_base import WidgetBase


# --------------------
## holds all interactions with widgets that accept a click
class WidgetClick(WidgetBase):
    # --------------------
    ## click left mouse button at given screen coordinates
    #
    # @param x   the x value in screen coordinates
    # @param y   the y value in screen coordinates
    # @return ack_nak response
    def click_left_at(self, x: int, y: int):
        rsp = Response('click_left_at')
        return self._click_left1(rsp, x, y)

    # --------------------
    ## click the left mouse button on the given widget item
    #
    # @param item  the widget item to click on
    # @return ack_nak response
    def click_left_on(self, item: dict):
        rsp = Response('click_left_on')
        return self._click_left2(rsp, item)

    # --------------------
    ## click the left mouse button on the widget at the given search list
    #
    # @param click_path  the path to the widget
    # @return ack_nak response
    def click_left(self, click_path: list):
        rsp = Response('click_left')
        return self._click_left3(rsp, click_path)

    # --------------------
    ## handle a click with a given widget path
    #
    # @param rsp          the current response object
    # @param widget_path  the path to the widget
    # @return ack_nak response
    def _click_left3(self, rsp, widget_path: list):
        if rsp.check_is_set(widget_path, 'click path'):
            return rsp.ack_nak

        item = self._harness.search(widget_path)
        if rsp.check_for_failure(item):
            return item

        return self._click_left2(rsp, item)

    # --------------------
    ## handle a click on the given item
    #
    # @param rsp   the current response object
    # @param item  the widget item to click on
    # @return ack_nak response
    def _click_left2(self, rsp, item: dict):
        if rsp.check_coordinates_set(item, 'click item'):
            return rsp.ack_nak

        x, y = self._get_coords_from(item)
        return self._click_left1(rsp, x, y)

    # --------------------
    ## handle a click on the given x,y coordinates
    #
    # @param rsp   the current response object
    # @param x   the x value in screen coordinates
    # @param y   the y value in screen coordinates
    # @return ack_nak response
    def _click_left1(self, rsp, x, y):
        if rsp.check_coordinate_values(x, y, 'click'):
            return rsp.ack_nak

        ack_nak = self._client.click_left(x, y)
        rsp.check_response(ack_nak)
        return rsp.ack_nak
