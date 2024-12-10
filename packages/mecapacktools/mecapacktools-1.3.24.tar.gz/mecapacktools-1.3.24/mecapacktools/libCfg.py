# -*- coding:Utf-8 -*-
# pylint: disable=fixme,invalid-name,line-too-long
"""Configuration system management."""
# ============================================================
#    Linux python path and Library import
# ============================================================

import os.path
import sys
from collections import UserDict
from configparser import ConfigParser

from . import libLog

# ============================================================
#    Variables and Constants
# ============================================================

# None

# ============================================================
#    Class
# ============================================================


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    Cfg
# ||||||||||||||||||||||||||||||||||||||||||||||||||
class Cfg(UserDict):
    """Class to manage the configuration of systems."""

    # //////////////////////////////////////////////////
    #    Variables and Constants
    # //////////////////////////////////////////////////

    # None

    # //////////////////////////////////////////////////
    #     INITIALIZATION
    # //////////////////////////////////////////////////
    def __init__(self, pfilePath=None, plogfileexists="WARNING"):
        """
        Initialization of the class

        Args:
            pfilePath (_type_, optional): the cfg file path. Defaults to None.
            plogfileexists (str, optional): Log level display for check exist file.
                "None" for no display.
                Defaults to "WARNING".
        """

        # Base initialization
        UserDict.__init__(self)

        # Work variables
        self.__CfgParser = ConfigParser()

        # Configure the parser for sensitive case
        self.__CfgParser.optionxform = str

        # Start log manager
        self.log = libLog.Log()

        # Load of cfg file
        if pfilePath is not None:
            headDirectory = os.path.dirname(sys.argv[0])
            if not os.path.isabs(pfilePath):
                pfilePath = os.path.abspath(os.path.join(headDirectory, pfilePath))
            if os.path.isfile(pfilePath):
                self.LoadFile(pfilePath)
            else:
                if plogfileexists:
                    self.log.Write(
                        self.log.LEVEL[plogfileexists],
                        "cfg file does not exist : %s",
                        pfilePath,
                    )

    # //////////////////////////////////////////////////
    #     LoadFile
    # //////////////////////////////////////////////////
    def LoadFile(self, pfilePath):
        """
        _summary_

        Args:
            pfilePath (str): the cfg file path

        Raises:
            self.log.CustomException: Error file path
        """
        # pylint: disable=eval-used,broad-exception-caught
        # Reading file
        if os.path.isfile(pfilePath):
            self.__CfgParser.read(pfilePath)
        else:
            raise self.log.CustomException(f"cfg file does not exist : {pfilePath}")

        # Reading section
        for sectionTemp in self.__CfgParser.sections():
            # Reading parameters
            for optionTemp in self.__CfgParser.options(sectionTemp):
                # Adding section in dictionary if does not exist
                if sectionTemp not in self:
                    self[sectionTemp] = {}
                # Adding parameter
                nameTemp = optionTemp
                typeTemp = ""
                if "|" in optionTemp:
                    nameTemp, typeTemp = optionTemp.split("|", 1)
                if typeTemp.upper() == "BOOLEAN":
                    valueTemp = self.__CfgParser.getboolean(sectionTemp, optionTemp)
                elif typeTemp.upper() == "INTEGER":
                    valueTemp = self.__CfgParser.getint(sectionTemp, optionTemp)
                elif typeTemp.upper() == "FLOAT":
                    valueTemp = self.__CfgParser.getfloat(sectionTemp, optionTemp)
                elif typeTemp.upper() == "EVAL":
                    valueTemp = eval(self.__CfgParser.get(sectionTemp, optionTemp))
                else:
                    valueTemp = self.__CfgParser.get(sectionTemp, optionTemp)
                    try:
                        valueTemp = self.__CfgParser.getboolean(sectionTemp, optionTemp)
                    except Exception:
                        pass
                    try:
                        valueTemp = self.__CfgParser.getfloat(sectionTemp, optionTemp)
                        valueTemp = self.__CfgParser.getint(sectionTemp, optionTemp)
                    except Exception:
                        pass
                    try:
                        valueTemp = eval(self.__CfgParser.get(sectionTemp, optionTemp))
                    except Exception:
                        pass

                self[sectionTemp][nameTemp] = valueTemp

    # //////////////////////////////////////////////////
    #     WriteFile
    # //////////////////////////////////////////////////
    def WriteFile(self, pfilePath):
        """
        Writing of the configuration file in system

        Args:
            pfilePath (str): the cfg file path

        Raises:
            self.log.CustomException: Error file path
        """
        # pylint: disable-next=consider-using-dict-items
        for sectionTemp in self.keys():
            if sectionTemp not in self.__CfgParser.sections():
                self.__CfgParser.add_section(sectionTemp)
            for optionTemp in self[sectionTemp].keys():
                self.__CfgParser.set(sectionTemp, optionTemp, self[sectionTemp][optionTemp])

        # Reading file
        if os.path.isfile(pfilePath):
            with open(pfilePath, "w", encoding="utf-8") as f:
                self.__CfgParser.write(f)
        else:
            raise self.log.CustomException(f"cfg file does not exist : {pfilePath}")

    # //////////////////////////////////////////////////
    #     UpdateKeyDict
    # //////////////////////////////////////////////////
    def UpdateKeyDict(self, pdict):
        """
        Update target dict by common group keys

        Args:
            pdict (dict): the target dict
        """

        for key in pdict.keys():
            if key in self.keys():
                pdict[key].update(self[key])
