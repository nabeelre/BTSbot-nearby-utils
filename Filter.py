class Filter:
    """
    A class to represent an alert filter stored on Fritz.

    Filter contains the ID of the alert stream and (optionally) the hash for the
    specific version of the filter on that alert stream. If the hash is not
    specified, the version of the filter marked as active on Fritz is used.
    """

    def __init__(self, stream_id: int, ver_hash: str = "", instrument: str = ""):
        self.stream_id = stream_id
        self.ver_hash = ver_hash
        self.instrument = instrument
