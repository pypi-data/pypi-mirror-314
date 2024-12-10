#! /usr/bin/env python
# -*- coding:Utf-8 -*-
# pylint: disable=fixme,invalid-name,line-too-long
"""Sql system management."""
# ============================================================
#    Linux python path and Library import
# ============================================================
try:
    import pypyodbc as pyodbc
except ImportError:
    # pylint: disable-next=broad-exception-raised,raise-missing-from
    raise Exception(
        """Could not load libSql due to import Error
        Are you sure to installed Extras : pip install mecapacktools[Sql] ?"""
    )
from sortedcontainers import SortedDict

from . import libLog

# ============================================================
#    Class
# ============================================================


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    Sql
# ||||||||||||||||||||||||||||||||||||||||||||||||||
class Sql:
    """Class to manage the Sql system."""

    # //////////////////////////////////////////////////
    #    Variables and Constants
    # //////////////////////////////////////////////////

    #: Variables
    hshParam = {}
    hshParam["Connections"] = {}
    hshParam["Dataname"] = SortedDict()
    hshParam["Queries"] = SortedDict()
    hshData = {}

    @property
    def data(self):
        """
        returns data

        Returns:
            dict: datas
        """
        return self.hshData

    # //////////////////////////////////////////////////
    #     INITIALIZATION
    # //////////////////////////////////////////////////
    # pylint: disable-next=dangerous-default-value
    def __init__(self, phshParam={}):
        # Work variables
        self.connections = {}
        self.cursors = {}
        self._last_count = None
        self._data_flag = False
        self._at_least_one_change = False

        # Start log manager
        self.log = libLog.Log()

        # Update of parameters
        self.hshParam.update(phshParam)

    # //////////////////////////////////////////////////
    #     Connections_Load
    # //////////////////////////////////////////////////
    def Connections_Load(self, penv=None, pconnectionfilter=None, **kw):
        """
        Loading connexion

        Args:
            penv (str, optional): environment define. Ex : prod, dev, test.... Defaults to None.
            pconnectionfilter (str, optional): filter string in connection dictionary. Defaults to None.
            **plogconnect (str, optional): Log level display for connect. "None" for no display. Defaults to "DEBUG".
        """

        hshOption = {"plogconnect": "DEBUG"}

        # Setting dictionary option
        if isinstance(kw, dict):
            hshOption.update(kw)

        # Connection
        for k, v in self.hshParam["Connections"][penv].items():
            self.log.setStep = k
            if (pconnectionfilter or k) == k:
                self.connections[k] = pyodbc.connect(v)
                if hshOption["plogconnect"]:
                    self.log.Write(
                        self.log.LEVEL[hshOption["plogconnect"]],
                        "Connection to %s successfully",
                        self.log.setStep,
                    )

    # //////////////////////////////////////////////////
    #     Execute_Request
    # //////////////////////////////////////////////////
    def Execute_Request(
        self, pqueryfilter, pbind=None, pformat=None, ptransaction=None, **kw
    ):
        """
        Execute SQL request

        Args:
            pqueryfilter (str): filter string in queries dictionary
            pbind (str, optional): the bind variables of queries. Defaults to None.
            pformat (str, optional): the ? info to replace into queries. Defaults to None.
            ptransaction (str, optional): Validation of transaction :
                "commit", "rollback", "standby" and, "None" (default)
                for select statement. Defaults to None.
            **pcnxname -- Name of connection (default=value between point in query key)
            **pcursorname -- Name of cursor (default=value between point in query key)
            **pfetchtype -- Type of data fetch ; "fetchall" (default), fetchone
            **plogrequest -- Log level display for request. "None" for no display (default=DEBUG)
            **plogcolumn -- Log level display for column. "None" for no display (default=None)
            **plogrow -- Log level display for row. "None" for no display (default=DEBUG)
            **plogcount -- Log level display for count. "None" for no display (default=DEBUG)
            **perrnochange -- Raise exception if no change with the request.
                Value expected, message or CustomException code.
                "None" for no display (default=None)
            **perrrequest -- Log level display for request in error. "None" for no display (default=INFO)

        Raises:
            self.log.CustomException: Raise exception if no change with the request.
                Value expected, message or CustomException code
        """

        hshOption = {
            "pcnxname": None,
            "pcursorname": None,
            "pfetchtype": "fetchall",
            "plogrequest": "DEBUG",
            "plogcolumn": None,
            "plogrow": "DEBUG",
            "plogcount": "DEBUG",
            "perrnochange": None,
            "perrrequest": "INFO",
        }
        _transaction = {
            "commit": "commit",
            "rollback": "rollback",
            "standby": "standby",
        }
        _fetchtype = {"fetchall": "fetchall", "fetchone": "fetchone"}

        # Setting dictionary option
        if isinstance(kw, dict):
            hshOption.update(kw)

        self._last_count = None
        self._data_flag = False
        self._at_least_one_change = False

        for k, v in filter(
            lambda x: pqueryfilter == x[0][: len(pqueryfilter)],
            self.hshParam["Queries"].items(),
        ):
            self.log.setStep = f"Q[{k}]"
            cnxname = hshOption["pcnxname"] or k.split(".")[1]
            cursorname = hshOption["pcursorname"] or k.split(".")[1]
            if pbind:
                SQL0 = v.format(**pbind)
            else:
                SQL0 = v
            if hshOption["plogrequest"]:
                self.log.Write(
                    self.log.LEVEL[hshOption["plogrequest"]],
                    "Request %s : %s",
                    k,
                    " ".join(SQL0.split()),
                )
            cnx0 = self.connections[cnxname]
            curs0 = self.cursors.setdefault(cursorname, cnx0.cursor())
            try:
                curs0.execute(SQL0, pformat)
            except Exception as e:
                if hshOption["perrrequest"]:
                    self.log.Write(
                        self.log.LEVEL[hshOption["perrrequest"]],
                        "Request %s : %s has problem : %s",
                        k,
                        " ".join(SQL0.split()),
                        str(e),
                    )
                raise
            count0 = curs0.rowcount
            if ptransaction:
                if count0 <= 0 and hshOption["perrnochange"]:
                    raise self.log.CustomExceptionCode(hshOption["perrnochange"])
                if not ptransaction == "standby":
                    getattr(cnx0, _transaction[ptransaction])()
                if hshOption["plogcount"]:
                    self.log.Write(
                        self.log.LEVEL[hshOption["plogcount"]], "Rowcount : %s", count0
                    )
                if not count0 == 0:
                    self._at_least_one_change = True
            else:
                column0 = curs0.description
                rows0 = getattr(curs0, _fetchtype[hshOption["pfetchtype"]])()
                count0 = len(rows0 or [])
                if hshOption["plogcount"]:
                    self.log.Write(
                        self.log.LEVEL[hshOption["plogcount"]], "Rowcount : %s", count0
                    )
                if hshOption["plogcolumn"]:
                    self.log.Write(
                        self.log.LEVEL[hshOption["plogcolumn"]], "Columns : %s", column0
                    )
                if hshOption["plogrow"]:
                    self.log.Write(
                        self.log.LEVEL[hshOption["plogrow"]], "Rows : %s", rows0
                    )
                self.hshData[f"{self.hshParam['Dataname'].get(k, k)}.H"] = column0
                self.hshData[f"{self.hshParam['Dataname'].get(k, k)}.R"] = rows0
                if not count0 == 0:
                    self._data_flag = True
            self._last_count = count0
            self.log.setStep = ""
