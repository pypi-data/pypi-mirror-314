
def getHostname():
    import socket
    # method one
    name = socket.gethostname()
    return name