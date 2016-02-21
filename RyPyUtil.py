
class RyPyUtil:
    """
    General purpose utility class
    """

    @staticmethod
    def hasMethod(object, methodName):
        """
        Returns whether or not object has a method named methodName
        """
        func = getattr(object, methodName, None)
        if(func is not None):
            return callable(func)
        else:
            return False
