# --------------------
## holds common code for handling widgets
class WidgetBase:  # pylint: disable=too-few-public-methods
    # --------------------
    ## constructor
    #
    # @param harness    reference to the harness object
    # @param client     reference to the client object
    def __init__(self, harness, client):
        ## reference to the harness
        self._harness = harness
        ## reference to the client
        self._client = client

    # --------------------
    ## calculate the center x,y coordinates for the given item
    #
    # @param item  the item to calculate the center coordinates on
    # @return the x,y coordinates of the center of the widget
    def _get_coords_from(self, item):
        x = int((item['coordinates']['x1'] + item['coordinates']['x2']) / 2)
        y = int((item['coordinates']['y1'] + item['coordinates']['y2']) / 2)
        return x, y
