class ClientException(Exception):
    pass

class SessionNotFoundException(ClientException):
    pass

class SendUplinkException(ClientException):
    pass