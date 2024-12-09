
class NetworkElementNotReachable(Exception) :
    def __init__(self ,message='Network Element Is Not Reachable.'):
        super().__init__(message)

class NetworkElementConnectionFailure(Exception) :
    def __init__(self ,message=''):
        super().__init__(message)

class NotValid1830PssConnectionMode(Exception) :
    def __init__(self ,message=''):
        super().__init__(message)
        
class PssNodeException(Exception) :
    def __init__(self ,message=''):
        super().__init__(message)


class JumpServerConnectionFailure(Exception) :
    def __init__(self ,message=''):
        super().__init__(message)
