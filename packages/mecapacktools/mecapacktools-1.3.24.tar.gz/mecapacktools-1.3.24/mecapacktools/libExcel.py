#! /usr/bin/env python
# -*- coding:Utf-8 -*-
# pylint: disable=fixme,invalid-name,line-too-long

"""Excel system management."""
import math

# ============================================================
#    Linux python path and Library import
# ============================================================
import os.path

try:
    import win32com
    import win32com.client

    if win32com.client.gencache.is_readonly is True:
        # delete the directory Python\...\Lib\site-packages\win32com\gen_py
        # allow gencache to create the cached wrapper objects
        win32com.client.gencache.is_readonly = False
        # under p2exe the call in gencache to __init__() does not happen
        # so we use Rebuild() to force the creation of the gen_py folder
        win32com.client.gencache.Rebuild()
    import datetime

    from win32com import client as com
    from win32com.client import constants as com_const

    from . import libLog
except ImportError:
    # pylint: disable-next=raise-missing-from,broad-exception-raised
    raise Exception(
        """Could not load libExcel due to import Error
        Are you sure to installed Extras : pip install mecapacktools[Excel] ?"""
    )

# ============================================================
#    Class
# ============================================================


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    Excel
# ||||||||||||||||||||||||||||||||||||||||||||||||||
class Excel:
    """Class to manage the excel system."""

    # //////////////////////////////////////////////////
    #    Variables and Constants
    # //////////////////////////////////////////////////

    #: Variables
    hshParam = {}
    hshParam["visible"] = False

    # //////////////////////////////////////////////////
    #     INITIALIZATION
    # //////////////////////////////////////////////////
    def __init__(self, phshParam={}):  # pylint: disable=dangerous-default-value
        # Work variables
        try:
            self.__ApplicationXL = com.DispatchEx("Excel.Application")
            com.gencache.EnsureDispatch("Excel.Application")
        except Exception as e:
            # pylint: disable-next=raise-missing-from,broad-exception-raised
            raise Exception(
                f"error : {e} \n\n please check folder {win32com.__gen_path__}\n ther might be a problem with this"
            )
        self.constants = com_const
        self.__TemplateWB = object
        self.CurrentRange_Parts = {"ALL": None, "HEADER": None, "DATA": None}

        # Start log manager
        self.log = libLog.Log()

        # Update of parameters
        self.hshParam.update(phshParam)

    # //////////////////////////////////////////////////
    #     TemplateWB_Load
    # //////////////////////////////////////////////////
    def TemplateWB_Load(self, ptemplateWB_path):
        """
        Loading template workbook

        Args:
            ptemplateWB_path (_type_): the excel template path

        Raises:
            self.log.CustomException: Template file does not exist
        """

        # Visible
        self.__ApplicationXL.Visible = self.hshParam["visible"]

        # Optimization of load
        self.__ApplicationXL.ScreenUpdating = self.hshParam["visible"]
        self.__ApplicationXL.DisplayStatusBar = self.hshParam["visible"]
        self.__ApplicationXL.EnableEvents = self.hshParam["visible"]

        # open workbook template
        if os.path.isfile(ptemplateWB_path):
            self.__TemplateWB = self.__ApplicationXL.Workbooks.Open(
                ptemplateWB_path, ReadOnly=True
            )
        else:
            raise self.log.CustomException(
                f"Template file does not exist :{ptemplateWB_path}"
            )

    # //////////////////////////////////////////////////
    #     TemplateWB_LoadData
    # //////////////////////////////////////////////////
    def TemplateWB_LoadData(
        self, psheet_name, pranges_name, pcursrows, pcurscolumns=(), **kw
    ):
        """
        Loading data in excel template

        Args:
            psheet_name (str):  the name of target sheet
            pranges_name (str):  the name of target ranges
            pcursrows (rows): Rows data of cursor
            pcurscolumns (tuple, optional): Columns of cursor. Defaults to ().
            **prowindex -- Start index of row (default=0)
            **pcolindex -- Start index of column (default=0)
            **pdataclean -- Cleaning of old data (default=True)
            **pcursorloadmaxrows -- Cursor to loading : Max rows (default=100000)
            **preferstodata -- New affectation of named range with data size (default=False)
        """
        hshOption = {
            "prowindex": 0,
            "pcolindex": 0,
            "pdataclean": True,
            "pcursorloadmaxrows": 100000,
            "preferstodata": False,
        }
        self.CurrentRange_Parts["HEADER"] = None
        self.CurrentRange_Parts["DATA"] = None
        self.CurrentRange_Parts["ALL"] = None

        # Setting dictionary option
        if isinstance(kw, dict):
            hshOption.update(kw)

        # Select sheet
        sheetTemp = self.__TemplateWB.Worksheets(psheet_name)
        # Disable automatic calculation : optimization of insertion data
        sheetTemp.EnableCalculation = False
        # Define Range
        r = sheetTemp.Range(pranges_name)
        rangeTemp = sheetTemp.Range(
            r.Cells(1 + hshOption["prowindex"], 1 + hshOption["pcolindex"]),
            r.Cells(r.Rows.Count, r.Columns.Count),
        )
        # Delete old data
        if hshOption["pdataclean"]:
            rangeTemp.Value = None
        # Define Start index
        iColumn_Start = rangeTemp.Column
        iRow_Start = rangeTemp.Row
        iRow_Start2 = rangeTemp.Row
        # Define range counter
        iRange_ColumnCount = rangeTemp.Columns.Count
        iRange_RowCount = rangeTemp.Rows.Count
        # Define data counter
        iData_ColumnCount = len(pcurscolumns)
        if iData_ColumnCount == 0:
            iData_Column = False
        else:
            iData_Column = True
        iData_RowCount = len(pcursrows)
        if iData_RowCount == 0:
            iData_Row = False
        else:
            iData_Row = True
            if iData_Column:
                iData_RowCount += 1
            else:
                iData_ColumnCount = len(pcursrows[0])
        # Define counter min
        iColumn_CountMin = iRange_ColumnCount
        iRow_CountMin = iRange_RowCount
        if iColumn_CountMin > iData_ColumnCount:
            iColumn_CountMin = iData_ColumnCount
        if iRow_CountMin > iData_RowCount:
            iRow_CountMin = iData_RowCount
        elif hshOption["preferstodata"]:
            iSheet_RowCount = sheetTemp.Rows.Count - iRow_Start + 1
            if iSheet_RowCount < iData_RowCount:
                iRow_CountMin = iSheet_RowCount
            else:
                iRow_CountMin = iData_RowCount
        # Define end index
        iRow_End = iRow_Start + (iRow_CountMin - 1)
        iColumn_End = iColumn_Start + (iColumn_CountMin - 1)
        # Check to add column names
        if iData_Column:
            self.CurrentRange_Parts["HEADER"] = sheetTemp.Range(
                sheetTemp.Cells(iRow_Start, iColumn_Start),
                sheetTemp.Cells(iRow_Start, iColumn_End),
            )
            self.CurrentRange_Parts["HEADER"].Value2 = next(zip(*pcurscolumns))
            iRow_Start += 1
            if iRow_Start > iRow_End:
                iData_Row = False
        # Check to add data
        if iData_Row:
            c = int(math.ceil(iRow_CountMin / float(hshOption["pcursorloadmaxrows"])))
            s = e = 0
            for n in range(1, c + 1):
                s, e = e, n * hshOption["pcursorloadmaxrows"]
                iRow_Start_TEMP = iRow_Start + s
                if n == c:
                    iRow_End_TEMP = iRow_End
                else:
                    iRow_End_TEMP = iRow_Start + e - 1
                self.CurrentRange_Parts["DATA"] = sheetTemp.Range(
                    sheetTemp.Cells(iRow_Start_TEMP, iColumn_Start),
                    sheetTemp.Cells(iRow_End_TEMP, iColumn_End),
                )
                values = []
                for row in pcursrows[s:e]:
                    r = []
                    for __, item in enumerate(row):
                        if isinstance(item, datetime.date) or isinstance(
                            item, datetime.datetime
                        ):
                            r.append(item.isoformat())
                        else:
                            r.append(item)
                    values.append(r)
                self.CurrentRange_Parts["DATA"].Value2 = values
        else:
            iRow_End = iRow_Start2

        # Enable automatic calculation
        sheetTemp.EnableCalculation = True

        self.CurrentRange_Parts["ALL"] = sheetTemp.Range(
            sheetTemp.Cells(iRow_Start2, iColumn_Start),
            sheetTemp.Cells(iRow_End, iColumn_End),
        )

    # //////////////////////////////////////////////////
    #     TemplateWB_WriteCell
    # //////////////////////////////////////////////////
    def TemplateWB_WriteCell(self, psheet_name, pranges_name, value):
        """
        Writing a cell in excel template

        Args:
            psheet_name (str): the name of target sheet
            pranges_name (str): the name of target ranges
            value (str): data to send
        """
        # Select sheet
        sheetTemp = self.__TemplateWB.Worksheets(psheet_name)
        # Disable automatic calculation : optimization of insertion data
        sheetTemp.EnableCalculation = False
        # copy value
        sheetTemp.Range(pranges_name).Value = value
        # Enable automatic calculation
        sheetTemp.EnableCalculation = True

    # //////////////////////////////////////////////////
    #     TemplateWB_CopyRows
    # //////////////////////////////////////////////////
    def TemplateWB_CopyRows(
        self, psheet_source, prange_source, psheet_dest, prange_dest
    ):
        """
        Copy Rows in excel template

        Args:
            psheet_source (str): the name of sheet where source is
            prange_source (str): the name of source range
            psheet_dest (str): the name of sheet where to copy
            prange_dest (str): the cell destination
        """
        # Select sheet
        self.log.Debug(
            f"EXCEL - Copy source {psheet_source} = {prange_source} to {psheet_dest} = {prange_dest}"
        )
        sheetSource = self.__TemplateWB.Worksheets(psheet_source)
        sheetDest = self.__TemplateWB.Worksheets(psheet_dest)
        # Disable automatic calculation : optimization of insertion data
        sheetSource.EnableCalculation = False
        # copy rows
        sheetSource.Rows(prange_source).Copy()
        sheetDest.Activate()
        sheetDest.Range(prange_dest).Select()
        sheetDest.PasteSpecial()
        # Enable automatic calculation
        sheetSource.EnableCalculation = True

    # //////////////////////////////////////////////////
    #     CurrentRange_Borders
    # //////////////////////////////////////////////////
    def CurrentRange_Borders(self, *pborders, ppart="ALL", **kw):
        """
        Excel template save as

        Args:
            ppart (str, optional): the part of range reference. Defaults to "ALL".
            *pborders -- the border identifier list (default='xlEdgeLeft','xlEdgeTop','xlEdgeBottom','xlEdgeRight'
                ,'xlInsideVertical','xlInsideHorizontal')
                Options : LineStyle, ColorIndex, TintAndShade, Weight
        """

        if len(pborders) == 0:
            pborders = [
                "xlEdgeLeft",
                "xlEdgeTop",
                "xlEdgeBottom",
                "xlEdgeRight",
                "xlInsideVertical",
                "xlInsideHorizontal",
            ]

        if isinstance(kw, dict):
            for b in pborders:
                for k, v in kw.items():
                    if isinstance(v, str):
                        v = getattr(self.constants, v)
                    setattr(
                        self.CurrentRange_Parts[ppart].Borders(
                            getattr(self.constants, b)
                        ),
                        k,
                        v,
                    )

    # //////////////////////////////////////////////////
    #     TemplateWB_SaveAs
    # //////////////////////////////////////////////////
    def TemplateWB_SaveAs(self, pfile_path):
        """
        Excel template save as

        Args:
            pfile_path (str): the path of new file
        """

        # Managed execution
        try:
            # Optimization parameters reset
            self.__ApplicationXL.ScreenUpdating = True
            self.__ApplicationXL.DisplayStatusBar = True
            self.__ApplicationXL.EnableEvents = True
        # pylint: disable-next=broad-exception-caught
        except Exception as e:
            self.log.Warning("Calculation failed", e, exc_info=1)
        # Managed execution
        try:
            # Refresh data and graphs
            self.__ApplicationXL.CalculateFull()
            self.__TemplateWB.RefreshAll()
        # pylint: disable-next=broad-exception-caught
        except Exception as e:
            # Log
            self.log.Warning("Refresh failed", e, exc_info=1)
        # Save and close
        self.__TemplateWB.SaveAs(pfile_path)
        self.__TemplateWB.Close()

    # //////////////////////////////////////////////////
    #     Close
    # //////////////////////////////////////////////////
    def Close(self):
        """Close Excel application"""
        self.__ApplicationXL.Quit()
