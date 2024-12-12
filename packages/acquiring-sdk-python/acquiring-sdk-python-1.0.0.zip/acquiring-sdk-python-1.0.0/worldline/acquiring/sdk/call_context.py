class CallContext(object):
    """
    A call context can be used to send extra information with a request, and to receive extra information from a response.

    Please note that this class is not thread-safe. Each request should get its own call context instance.
    """
    def __init__(self):
        pass
