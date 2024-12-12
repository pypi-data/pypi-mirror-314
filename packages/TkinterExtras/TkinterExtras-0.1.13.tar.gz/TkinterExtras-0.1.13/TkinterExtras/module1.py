from collections import defaultdict
from tkinter import Tk, Frame, StringVar, OptionMenu, Label, Entry, messagebox, Button
from typing import Union

class DropdownMenu:
    def __init__(self, root:Union[Tk, Frame], options: list[str], default: str = "Select an option") -> None:
        self.root = root
        self.options = options
        self.__default = default

        self.__selectedOption = StringVar()
        self.__selectedOption.set(self.__default)

        self.dropdownMenu = OptionMenu(self.root, self.__selectedOption, *self.options)
    
    @property
    def selectedOption(self) -> str:
        return self.__selectedOption.get()
    
    @property
    def default(self) -> str:
        return self.__default

    def Select(self, selection:str) -> None:
        if selection in self.options or selection == self.default:
            self.__selectedOption.set(selection)

    def pack(self, anchor = "w") -> None:
        self.dropdownMenu.pack(anchor=anchor) # type: ignore
    
    def grid(self, row:int, column:int, sticky: str = "nw") -> None:
        self.dropdownMenu.grid(row=row, column=column, sticky=sticky)

class EditableTable:
    def __init__(self, root:Union[Tk, Frame], numRows: int, numCols: int, maxRows: int | None = None, maxCols: int | None = None, rowHeaders: list[str] | None = None, colHeaders: list[str] | None = None, headerFontSize: int = 20, cellFontSize: int = 10, editableRows: list[bool] | None = None, editableCols: list[bool] | None = None) -> None:
        self.root = root
        self.MIN_ROWS = 2 if colHeaders != None else 1
        self.MIN_COLS = 2 if rowHeaders != None else 1
        self.numRows = numRows
        self.numCols = numCols
        self.maxRows = maxRows if maxRows != None and 1 <= maxRows else None
        self.maxCols = maxCols if maxCols != None and 1 <= maxCols else None
        self.rowHeaders = rowHeaders
        self.colHeaders = colHeaders
        self.headerFontSize = headerFontSize
        self.cellFontSize = cellFontSize
        self.editableRows = editableRows
        self.editableCols = editableCols

        self.cells = {}
        self.data: defaultdict[tuple[int, int], str] = defaultdict(str)

        # Frames
        self.tableFrame = Frame(self.root)
        self.buttonsFrame = Frame(self.root)
        # Pack Frames
        self.tableFrame.pack(anchor="w")
        self.buttonsFrame.pack(anchor="w")

        # Widgets
        self.addRowButton = Button(self.buttonsFrame, text="Add Row", command=self.AddRow) if rowHeaders == None else None
        self.removeRowButton = Button(self.buttonsFrame, text="Remove Row", command=self.RemoveRow) if rowHeaders == None else None

        self.addColButton = Button(self.buttonsFrame, text="Add Column", command=self.AddColumn) if colHeaders == None else None
        self.removeColButton = Button(self.buttonsFrame, text="Remove Column", command=self.RemoveColumn) if colHeaders == None else None
        # Pack Widgets
        if self.addRowButton != None: self.addRowButton.pack(anchor="w")
        if self.removeRowButton != None: self.removeRowButton.pack(anchor="w")
        if self.addColButton != None: self.addColButton.pack(anchor="w")
        if self.removeColButton != None: self.removeColButton.pack(anchor="w")

        self.RenderTable()
    
    def RenderTable(self):
        self.data = defaultdict(str)
        for row in range(self.numRows):
            for col in range(self.numCols):
                if (col, row) not in self.cells.keys(): continue
                cell = self.cells[(col, row)]
                cellType = type(cell)
                if cellType == Entry:
                    self.data[(col, row)] = cell.get() #type: ignore
                elif cellType == Label:
                    self.data[(col, row)] = cell["text"]
        for cell in self.cells.values(): cell.destroy()
        self.cells: dict[tuple[int, int], Label|Entry] = {}
        for row in range(self.numRows):
            for col in range(self.numCols):
                if self.rowHeaders != None and self.colHeaders != None:
                    if row == 0 and col == 0: continue
                    elif row == 0:
                        label = Label(self.tableFrame, text=self.colHeaders[col-1], font=("Helvetica", self.headerFontSize))
                    elif col == 0:
                        label = Label(self.tableFrame, text=self.rowHeaders[row-1], font=("Helvetica", self.headerFontSize))
                    else:
                        if ((self.editableRows != None and self.editableRows[row]) or (self.editableRows == None)) and ((self.editableCols != None and self.editableCols[col]) or (self.editableCols == None)):
                            label = Entry(self.tableFrame, font=("Helvetica", self.cellFontSize))
                            label.insert(0, self.data[(col, row)])
                        else:
                            label = Label(self.tableFrame, text=self.data[(col, row)], font=("Helvetica", self.cellFontSize), borderwidth=2, relief="solid")
                elif self.rowHeaders != None:
                    if col == 0:
                        label = Label(self.tableFrame, text=self.rowHeaders[row], font=("Helvetica", self.headerFontSize))
                    else:
                        if ((self.editableRows != None and self.editableRows[row]) or (self.editableRows == None)) and ((self.editableCols != None and self.editableCols[col]) or (self.editableCols == None)):
                            label = Entry(self.tableFrame, font=("Helvetica", self.cellFontSize))
                            label.insert(0, self.data[(col, row)])
                        else:
                            label = Label(self.tableFrame, text=self.data[(col, row)], font=("Helvetica", self.cellFontSize), borderwidth=2, relief="solid")
                elif self.colHeaders != None:
                    if row == 0:
                        label = Label(self.tableFrame, text=self.colHeaders[row], font=("Helvetica", self.headerFontSize))
                    else:
                        if ((self.editableRows != None and self.editableRows[row]) or (self.editableRows == None)) and ((self.editableCols != None and self.editableCols[col]) or (self.editableCols == None)):
                            label = Entry(self.tableFrame, font=("Helvetica", self.cellFontSize))
                            label.insert(0, self.data[(col, row)])
                        else:
                            label = Label(self.tableFrame, text=self.data[(col, row)], font=("Helvetica", self.cellFontSize), borderwidth=2, relief="solid")
                else:
                    if ((self.editableRows != None and self.editableRows[row]) or (self.editableRows == None)) and ((self.editableCols != None and self.editableCols[col]) or (self.editableCols == None)):
                        label = Entry(self.tableFrame, font=("Helvetica", self.cellFontSize))
                        label.insert(0, self.data[(col, row)])
                    else:
                        label = Label(self.tableFrame, text=self.data[(col, row)], font=("Helvetica", self.cellFontSize), borderwidth=2, relief="solid")

                self.cells[(col, row)] = label
        for (col, row), label in self.cells.items():
            label.grid(column=col, row=row)
    
    def AddColumn(self) -> None:
        if self.maxCols != None and self.numCols >= self.maxCols: return
        self.numCols += 1
        self.RenderTable()
    def RemoveColumn(self) -> None:
        if self.numCols > self.MIN_COLS:
            self.numCols -= 1
            self.RenderTable()
        else:
            messagebox.showwarning("Warning", "Cannot remove the last column!")
    def AddRow(self) -> None:
        if self.maxRows != None and self.numRows >= self.maxRows: return
        self.numRows += 1
        self.RenderTable()
    def RemoveRow(self) -> None:
        if self.numRows > self.MIN_ROWS:
            self.numRows -= 1
            self.RenderTable()
        else:
            messagebox.showwarning("Warning", "Cannot remove the last row")
    
    def pack(self, anchor="w") -> None:
        self.root.pack(anchor=anchor) #type: ignore
    def grid(self, row: int, column: int, sticky: str = "nw") -> None:
        self.root.grid(row=row, column=column, sticky=sticky) #type: ignore