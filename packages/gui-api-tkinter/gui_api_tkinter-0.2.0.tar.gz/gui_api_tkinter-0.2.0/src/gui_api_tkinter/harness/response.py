# --------------------
## hold current ack_nak response to reply to the user
class Response:
    # --------------------
    ## constructor
    #
    # @param tag       response tag to use
    def __init__(self, tag):
        ## holds the response tag to use
        self.tag = tag
        ## holds the current ack_nak response
        self.ack_nak = {
            'rsp': self.tag,
        }

    # --------------------
    ## check: if val is invalid i.e. None or empty
    #
    # @param val          the value to check
    # @param err_msg      the error message to print
    # @param check_empty  (optional) check if value is empty
    # @return True if val is invalid, False otherwise
    def check_is_set(self, val, err_msg, check_empty=True):
        if self.check_is_none(val, err_msg):
            return True

        if check_empty and self._check_is_empty(val, err_msg):
            return True

        return False

    # --------------------
    ## check: if the item is valid and the coordinates field is present
    #
    # @param item     the item to check
    # @param err_msg  the error message to print
    # @return True if val is invalid, False otherwise
    def check_coordinates_set(self, item, err_msg):
        if self.check_is_none(item, err_msg):
            return True
        if self._check_missing_coord(item, err_msg):
            return True

        return False

    # --------------------
    ## check: if item is missing coordinates field
    #
    # @param item     the item to check
    # @param err_msg  the error message to print
    # @return True if val is missing coordinates field, False otherwise
    def _check_missing_coord(self, item, err_msg):
        if 'coordinates' not in item:
            self.ack_nak['value'] = 'nak'
            self.ack_nak['reason'] = f'{err_msg} missing coordinates values'
            return True

        return False

    # --------------------
    ## check: if coordinate values are not integers
    #
    # @param x        the x-coordinate to check
    # @param y        the y-coordinate to check
    # @param err_msg  the error message to print
    # @return True if val is either was not an integer, False otherwise
    def check_coordinate_values(self, x, y, err_msg):
        if self._check_is_not_int(x, 'x', err_msg):
            return True
        if self._check_is_not_int(y, 'y', err_msg):
            return True

        return False

    # --------------------
    ## check: if coordinate value is not an integer
    #
    # @param val      the value to check
    # @param name     the name of coordinate for logging purposes
    # @param err_msg  the error message to print
    # @return True if val is not an integer, False otherwise
    def _check_is_not_int(self, val, name, err_msg):
        if not isinstance(val, int):
            self.ack_nak['value'] = 'nak'
            self.ack_nak['reason'] = f'{err_msg} {name}-coordinate is not an integer'
            return True

        return False

    # --------------------
    ## check: if response has failed or passed
    #
    # @param ack_nak  the response to check
    # @return None
    def check_response(self, ack_nak):
        # if there is a nak reason then the call failed
        if self.check_for_failure(ack_nak):
            self.ack_nak = ack_nak
        else:
            # ... otherwise just return an ack
            self._check_ack()

    # --------------------
    ## check: if there was a failure ('reason' field exists)
    # then reset the response reason field to the given tag
    #
    # @param rsp    the response object
    # @return True if tag was reset, False otherwise
    def check_for_failure(self, rsp):
        if 'reason' in rsp:
            rsp['rsp'] = self.tag
            return True

        return False

    # --------------------
    ## check: set the response value to ack
    #
    # @return a response object
    def _check_ack(self):
        self.ack_nak = {
            'rsp': self.tag,
            'value': 'ack',
        }

    # --------------------
    ## check: if value is None
    #
    # @param val      the value to check
    # @param err_msg  the error message to print
    # @return True if val is None, False otherwise
    def check_is_none(self, val, err_msg):
        if val is None:
            self.ack_nak['value'] = 'nak'
            self.ack_nak['reason'] = f'{err_msg} is None'
            return True

        return False

    # --------------------
    ## check: if value is empty
    #
    # @param val      the value to check
    # @param err_msg  the error message to print
    # @return True if val is empty, False otherwise
    def _check_is_empty(self, val, err_msg):
        if not val:
            self.ack_nak['value'] = 'nak'
            self.ack_nak['reason'] = f'{err_msg} is empty'
            return True

        return False

    # --------------------
    ## check: if item is not found
    #
    # @param item     the item to check
    # @param err_msg  the error message to print
    # @return True if item is None, False otherwise
    def check_is_not_found(self, item, err_msg):
        if item is None:
            self.ack_nak['value'] = 'nak'
            self.ack_nak['reason'] = f'{err_msg} is not found'
            return True

        return False
