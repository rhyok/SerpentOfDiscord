from RyPyUtil import RyPyUtil

loggingLevelNone = 0
loggingLevelError = 1
loggingLevelWarning = 2
loggingLevelInfo = 3
loggingLevelVerbose = 4
loggingLevelDebug = 5
loggingLevel = loggingLevelDebug
loggingEndpoints = []


class ModuLogEndpoint:
    """
    A logging endpoint. Must define how to send a message.
    """

    def logMessage(self, message):
        raise NotImplementedError


class PrintLogEndpoint(ModuLogEndpoint):

    def logMessage(self, message):
        print message


class ModuLog:

    @staticmethod
    def addLoggingEndpoint(endpoint):
        global loggingEndpoints
        loggingEndpoints.append(endpoint)

    @staticmethod
    def setLoggingLevel(level):
        global loggingLevel
        loggingLevel = level

    @staticmethod
    def changeLoggingLevel(level):
        global loggingLevel
        loggingLevel = level
        if level == loggingLevelNone:
            ModuLog.log("", "ModuLog", "Logging Level: None")
            print "logging = none"
        if level == loggingLevelError:
            ModuLog.log("", "ModuLog", "Logging Level: Error")
            print "logging = error"
        if level == loggingLevelWarning:
            ModuLog.log("", "ModuLog", "Logging Level: Warning")
            print "logging = warning"
        if level == loggingLevelVerbose:
            ModuLog.log("", "ModuLog", "Logging Level: Verbose")
            print "logging = verbose"
        if level == loggingLevelDebug:
            ModuLog.log("", "ModuLog", "Logging Level: Debug")
            print "logging = debug"
        if level == loggingLevelInfo:
            ModuLog.log("", "ModuLog", "Logging Level: Info")
            print "logging = info"

    @staticmethod
    def log(tag, module, message):
        """
        Logs a message, sending a message to the admins and prints a message
        to the server console.

        tag - A tag to use in the logging statement
        module - Module the logging statement originated from. Can be None.
        message - Message to log
        """
        prefix = "["
        if tag is not None:
            prefix += tag + ","
        if module is not None:
            prefix += module
        prefix += "]"
        messageString = prefix + message
        for endpoint in loggingEndpoints:
            if(RyPyUtil.hasMethod(endpoint, "logMessage")):
                endpoint.logMessage(messageString)

    @staticmethod
    def debug(module, message):
        """
        Debug level logging

        module - Module the logging statement originated from. Can be None.
        message - Message to log
        """
        if loggingLevel >= loggingLevelDebug:
            ModuLog.log("D", module, message)

    @staticmethod
    def warning(module, message):
        """
        Warning level logging

        module - Module the logging statement originated from. Can be None.
        message - Message to log
        """
        if loggingLevel >= loggingLevelWarning:
            ModuLog.log("W", module, message)

    @staticmethod
    def info(module, message):
        """
        Info level logging

        module - Module the logging statement originated from. Can be None.
        message - Message to log
        """
        if loggingLevel >= loggingLevelInfo:
            ModuLog.log("I", module, message)

    @staticmethod
    def verbose(module, message):
        """
        Verbose level logging

        module - Module the logging statement originated from. Can be None.
        message - Message to log
        """
        if loggingLevel >= loggingLevelVerbose:
            ModuLog.log("V", module, message)

    @staticmethod
    def error(module, message):
        """
        Error level logging

        module - Module the logging statement originated from. Can be None.
        message - Message to log
        """
        if loggingLevel >= loggingLevelVerbose:
            ModuLog.log("E", module, message)

ModuLog.addLoggingEndpoint(PrintLogEndpoint())
