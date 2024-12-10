#! /usr/bin/env python
# -*- coding:Utf-8 -*-
# pylint: disable=fixme,invalid-name,line-too-long
"""Log system management."""
# ============================================================
#    Linux python path and Library import
# ============================================================

import logging
import logging.handlers
import os.path
import sys
import time

# ============================================================
#    Variables and Constants
# ============================================================

# Process time initialization
time.perf_counter()

# Constants status
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"

# ============================================================
#    Class
# ============================================================


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    Log
# ||||||||||||||||||||||||||||||||||||||||||||||||||
class Log(object):
    """Class to manage the log of systems."""

    # //////////////////////////////////////////////////
    #    Constants, Variables and Properties
    # //////////////////////////////////////////////////

    # Constants
    STATUS_UNKNOWN, STATUS_OK, STATUS_WARNING, STATUS_CRITICAL = range(-1, 3)
    LEVEL_LOW, LEVEL_MEDIUM, LEVEL_HIGH = range(1, 4)
    #: list of LEVEL
    LEVEL = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }
    CRLF = "\n"

    #: Variables
    hshParam = {}
    hshParam["process"] = ""
    hshParam["part"] = ""
    hshParam["section"] = ""
    hshParam["step"] = ""
    hshParam["level"] = "INFO"
    hshParam["relativeProfilDirectory"] = False
    hshParam["directoryPath"] = "..\\log"
    hshParam["fileName"] = "main.log"
    hshParam["oneLogByLaunch"] = False
    hshParam["maxBytes"] = 1000000
    hshParam["backupCount"] = 5
    hshParam["startDateTime"] = time.localtime(time.time() - time.perf_counter())
    hshParam["directoryPathForFiles"] = "files"
    hshParam["messages"] = []
    hshParam["trackingByDatabase"] = False
    hshParam["trackingByFile"] = True
    hshParam["trackingByConsole"] = True
    hshParam["trackingByConsole_debugPause"] = False

    logging = logging
    #: default __formatter
    __formatter = logging.Formatter(
        "[%(asctime)s] - {%(name)s} - %(levelname)s - %(message)s", DATETIME_FORMAT
    )

    # Properties
    @property
    def getLevel(self):
        """
        get current level

        Returns:
            str: LEVEL
        """
        return self.hshParam["level"]

    @property
    def setLog(self):
        """
        returns params

        Returns:
            dict: dict of params
        """
        return self.hshParam

    @property
    def setProcess(self):
        """
        returns process

        Returns:
            str: process
        """
        return self.hshParam.get("process")

    @setProcess.setter
    def setProcess(self, value):
        """
        set process

        Args:
            value (str): process
        """
        self.hshParam["process"] = str(value)
        self.hshParam["part"] = ""
        self.hshParam["section"] = ""
        self.hshParam["step"] = ""

    @property
    def setPart(self):
        """
        return part

        Returns:
            str: part
        """
        return self.hshParam.get("part")

    @setPart.setter
    def setPart(self, value):
        """
        set part

        Args:
            value (str): part
        """
        self.hshParam["part"] = str(value)
        self.hshParam["section"] = ""
        self.hshParam["step"] = ""

    @property
    def setSection(self):
        """
        return section

        Returns:
            str: section
        """
        return self.hshParam.get("section")

    @setSection.setter
    def setSection(self, value):
        """
        set section

        Args:
            value (str): section
        """
        self.hshParam["section"] = str(value)
        self.hshParam["step"] = ""

    @property
    def setStep(self):
        """
        return step

        Returns:
            str: step
        """
        return self.hshParam.get("step")

    @setStep.setter
    def setStep(self, value):
        """
        set step

        Args:
            value (str): step
        """
        self.hshParam["step"] = str(value)

    # //////////////////////////////////////////////////
    #     CustomException
    # //////////////////////////////////////////////////
    class CustomException(Exception):
        """
        write into log CustomException
        """

        def __init__(self, pmessage, *pargs, **pkwargs):
            self.args = tuple(pargs)
            self.message = pmessage
            if pargs:
                self.message = self.message % tuple(pargs)
            if pkwargs:
                self.message = self.message.format(**pkwargs)

        def __str__(self):
            return self.message

    # //////////////////////////////////////////////////
    #     CustomExceptionCode
    # //////////////////////////////////////////////////
    class CustomExceptionCode(Exception):
        """
        write into log CustomException
        """

        def __init__(self, perr_code, *pargs, **pkwargs):
            self.err_code = perr_code
            self.args = tuple(pargs)
            self.message = Log.hshParam["messages"].get(perr_code, perr_code)
            if pargs:
                self.message = self.message % tuple(pargs)
            if pkwargs:
                self.message = self.message.format(**pkwargs)

        def __str__(self):
            return self.message

    # //////////////////////////////////////////////////
    #     INITIALIZATION
    # //////////////////////////////////////////////////
    def __init__(self, pprocessname=""):
        """
        Initialization of the class

        Args:
            pprocessname (str, optional): the name of the process. Defaults to "".
        """

        # Work variable
        if not len(pprocessname) == 0:
            self.setProcess = pprocessname

        self.__msg = ""
        self.__args = None

    # //////////////////////////////////////////////////
    #     LogDirectoryPath
    # //////////////////////////////////////////////////
    def LogDirectoryPath(self):
        """
        Directory of log

        Returns:
            str: log directory path
        """

        # Work variable
        dirPath_temp = self.hshParam["directoryPath"]

        # Get head directory of log
        headDirectory = os.path.dirname(sys.argv[0])
        if self.hshParam["relativeProfilDirectory"]:
            headDirectory = os.path.join(os.getenv("HOMEDRIVE"), os.getenv("HOMEPATH"))

        # Build the specify log directory if need
        if self.hshParam["oneLogByLaunch"]:
            dirPath_temp = os.path.join(
                dirPath_temp,
                f"{self.hshParam['process']}_{time.strftime('%Y%m%d_%H%M%S', self.hshParam['startDateTime'])}",
            )

        # Get absolute path
        if not os.path.isabs(dirPath_temp):
            dirPath_temp = os.path.abspath(os.path.join(headDirectory, dirPath_temp))

        # Creation of the log directory if does not exist
        if not os.path.isdir(dirPath_temp):
            os.makedirs(dirPath_temp)

        # Return absolute path
        return dirPath_temp

    # //////////////////////////////////////////////////
    #     LogDirectoryPath_ForFiles
    # //////////////////////////////////////////////////
    def LogDirectoryPath_ForFiles(self):
        """
        Directory of log for files

        Returns:
            str: log directory path for files
        """

        # Work variable
        dirPath_temp = os.path.join(
            self.LogDirectoryPath(), self.hshParam["directoryPathForFiles"]
        )

        # Get absolute path
        dirPath_temp = os.path.abspath(dirPath_temp)

        # Creation of the log directory if does not exist
        if not os.path.isdir(dirPath_temp):
            os.makedirs(dirPath_temp)

        # Return absolute path
        return dirPath_temp

    # //////////////////////////////////////////////////
    #     ClearConsole
    # //////////////////////////////////////////////////
    def ClearConsole(self):
        """
        Clearing of output console
        """

        print(os.name)
        if os.name == "posix":
            os.system("clear")
        else:
            os.system("cls")

    # //////////////////////////////////////////////////
    #     Write
    # //////////////////////////////////////////////////
    def Write(self, plevel, pmsg, *args, **kwargs):
        """
        write log

        Args:
            plevel (str): LEVEL
            pmsg (str): text to write
        """

        # Manage message
        self.__msg = pmsg
        self.__args = list(args)
        for i, arg in enumerate(self.__args):
            if isinstance(arg, Exception):
                if hasattr(arg, "message"):
                    self.__args[i] = arg.message
                else:
                    self.__args[i] = str(arg)
        if isinstance(self.__msg, Exception):
            if hasattr(self.__msg, "message"):
                self.__msg = self.__msg.message
            else:
                self.__msg = str(self.__msg)
        self.__args = tuple(self.__args)

        # Build the logger name hierarchical
        if len(self.hshParam["process"]) == 0:
            # Get the logger root
            loggerMaster = logging.getLogger()
            loggerTemp = loggerMaster
        else:
            nameTemp = self.hshParam["process"]
            loggerMaster = logging.getLogger(nameTemp)
            if not len(self.hshParam["part"]) == 0:
                nameTemp += "." + self.hshParam["part"]
                if not len(self.hshParam["section"]) == 0:
                    nameTemp += "." + self.hshParam["section"]
                    if not len(self.hshParam["step"]) == 0:
                        nameTemp += "." + self.hshParam["step"]
            # Get the logger
            loggerTemp = logging.getLogger(nameTemp)

        # Check if the master logger is already set
        if len(loggerMaster.handlers) == 0:
            # Tracking by console
            if self.hshParam["trackingByConsole"]:
                # Setting the default handler of new logger
                handleTemp = logging.StreamHandler()
                handleTemp.setFormatter(self.__formatter)
                loggerMaster.addHandler(handleTemp)

            # Tracking by file
            if self.hshParam["trackingByFile"]:
                # Definition of the log file path
                logFilePathTemp = os.path.join(
                    self.LogDirectoryPath(), self.hshParam["fileName"]
                )
                # Setting the handler file of new logger
                if self.hshParam["oneLogByLaunch"]:
                    handleTemp = logging.FileHandler(logFilePathTemp, "a")
                else:
                    handleTemp = logging.handlers.RotatingFileHandler(
                        logFilePathTemp,
                        "a",
                        self.hshParam["maxBytes"],
                        self.hshParam["backupCount"],
                    )
                handleTemp.setFormatter(self.__formatter)
                loggerMaster.addHandler(handleTemp)

        # Define level of log write
        loggerTemp.setLevel(self.LEVEL[self.hshParam["level"].upper()])
        # Write log
        loggerTemp.log(plevel, self.__msg, *self.__args, **kwargs)

    # //////////////////////////////////////////////////
    #     Debug
    # //////////////////////////////////////////////////
    def Debug(self, pmsg, *args, **kwargs):
        """
        Write debug message

        Args:
            pmsg (str): the message
        """

        self.Write(logging.DEBUG, pmsg, *args, **kwargs)

    # //////////////////////////////////////////////////
    #     Info
    # //////////////////////////////////////////////////
    def Info(self, pmsg, *args, **kwargs):
        """
        Write information message

        Args:
            pmsg (str): the message
        """

        self.Write(logging.INFO, pmsg, *args, **kwargs)

    # //////////////////////////////////////////////////
    #     Warning
    # //////////////////////////////////////////////////
    def Warning(self, pmsg, *args, **kwargs):
        """
        Write warning message

        Args:
            pmsg (str): the message
        """

        self.Write(logging.WARNING, pmsg, *args, **kwargs)

    # //////////////////////////////////////////////////
    #     Error
    # //////////////////////////////////////////////////
    def Error(self, pmsg, *args, **kwargs):
        """
        Write error message

        Args:
            pmsg (str): the message
        """

        self.Write(logging.ERROR, pmsg, *args, **kwargs)

    # //////////////////////////////////////////////////
    #     Critical
    # //////////////////////////////////////////////////
    def Critical(self, pmsg, *args, **kwargs):
        """
        Write critical message

        Args:
            pmsg (str): the message
        """

        self.Write(logging.CRITICAL, pmsg, *args, **kwargs)
