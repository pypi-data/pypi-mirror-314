from .response import Response
from .widget_base import WidgetBase


# --------------------
## holds all interactions with TCombobox widgets
class WidgetCombobox(WidgetBase):
    # --------------------
    ## select combo box option with the given coordinates
    #
    # @param x        the x value in screen coordinates
    # @param y        the y value in screen coordinates
    # @param opt_id   the option to set
    # @return ack_nak response
    def combobox_set_at(self, x: int, y: int, opt_id):
        rsp = Response('combobox_set_at')
        return self._combobox_set1(rsp, x, y, opt_id)

    # --------------------
    ## select option(s) on the given item
    #
    # @param item      the widget item to set the option on
    # @param opt_id    the option to set
    # @return ack_nak response
    def combobox_set_on(self, item: dict, opt_id):
        rsp = Response('combobox_set_on')
        return self._combobox_set2(rsp, item, opt_id)

    # --------------------
    ## set option on the widget with the given path
    #
    # @param widget_path  the path to the widget
    # @param opt_id       the option to set
    # @return ack_nak response
    def combobox_set(self, widget_path: list, opt_id):
        rsp = Response('combobox_set')
        return self._combobox_set3(rsp, widget_path, opt_id)

    # --------------------
    ## set option on the widget with the given path
    #
    # @param rsp          the current response
    # @param widget_path  the path to the widget
    # @param opt_id       the option to set
    # @return ack_nak response
    def _combobox_set3(self, rsp: Response, widget_path: list, opt_id):
        if rsp.check_is_set(widget_path, 'combobox set path'):
            return rsp.ack_nak

        item = self._harness.search(widget_path)
        if rsp.check_for_failure(item):
            return item

        return self._combobox_set2(rsp, item, opt_id)

    # --------------------
    ## set option on the given item
    #
    # @param rsp       the current response
    # @param item      the item to set the option on
    # @param opt_id    the option to set
    # @return ack_nak response
    def _combobox_set2(self, rsp: Response, item: dict, opt_id):
        if rsp.check_coordinates_set(item, 'combobox set item'):
            return rsp.ack_nak

        x, y = self._get_coords_from(item)
        return self._combobox_set1(rsp, x, y, opt_id)

    # --------------------
    ## set option on the given item
    #
    # @param rsp      the current response
    # @param x        the x value in screen coordinates
    # @param y        the y value in screen coordinates
    # @param opt_id   the option to set
    # @return ack_nak response
    def _combobox_set1(self, rsp: Response, x: int, y: int, opt_id):
        if rsp.check_is_set(opt_id, 'combobox set opt_id'):
            return rsp.ack_nak

        if rsp.check_coordinate_values(x, y, 'combobox set'):
            return rsp.ack_nak

        ack_nak = self._client.combobox_set(x, y, opt_id)
        rsp.check_response(ack_nak)
        return rsp.ack_nak
