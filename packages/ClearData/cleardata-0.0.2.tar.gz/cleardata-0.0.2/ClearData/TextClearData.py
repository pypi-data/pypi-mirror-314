#TODO: Start here... Needs to match interfaces

from .Interfaces import *
from enum import Enum
from pathlib import Path
import clr
import csv
clr.AddReference('System.Data')
import System
from System.Data import DataTable
from System.Data import DataRow
from System.Data import DataColumn
from System.Data import ParameterDirection

class TextFileFormat(Enum):
	CommaWithHeader = 1
	CommaWithoutHeader = 2
	TabWithHeader = 3
	TabWithoutHeader = 4
	PipeWithHeader = 5
	PipeWithoutHeader = 6
	Prettify = 7

class TextQueries(IQueries):
	FilePath:Path = None
	Format:TextFileFormat = TextFileFormat.CommaWithHeader

	def __init__(self, filePath:Path, format:TextFileFormat = TextFileFormat.CommaWithHeader):
		self.FilePath = filePath
		self.Format = format

	def Execute(self, query:str, parameters = None):
		raise NotImplementedError()

	def ExecuteWithScalar(self, query:str, parameters = None):
		raise NotImplementedError()

	def TruncateTable(self):
		header:str = None
		contents:str = self.FilePath.read_text()
		match self.Format:
			case TextFileFormat.CommaWithHeader:
				header = contents.split("\n")[0]
			case TextFileFormat.CommaWithoutHeader:
				header = ""

			case TextFileFormat.TabWithHeader:
				header = contents.split("\n")[0]
			case TextFileFormat.TabWithoutHeader:
				header = ""

			case TextFileFormat.PipeWithHeader:
				header = contents.split("\n")[0]
			case TextFileFormat.PipeWithoutHeader:
				header = ""
		self.FilePath.write_text(header)

	def GetRowCount(self) -> int:
		returnValue:int = None
		if (self.Format != TextFileFormat.Prettify):
			contents:str = self.FilePath.read_text()
			returnValue = len(contents.split("\n"))
			returnValue -= 1
			match self.Format:
				case TextFileFormat.CommaWithHeader:
					returnValue -= 1
				case TextFileFormat.TabWithHeader:
					returnValue -= 1
				case TextFileFormat.PipeWithHeader:
					returnValue -= 1
		return returnValue

class TextBulkData:
	FilePath:Path = None
	Format:TextFileFormat = TextFileFormat.CommaWithHeader

	def __init__(self, filePath:Path, format:TextFileFormat = TextFileFormat.CommaWithHeader):
		self.FilePath = filePath
		self.Format = format

	def __GetDataTableDelimited__(self, rowDelimiter:str, fieldDelimiter:str, includeHeader:bool) -> DataTable:
		returnValue:DataTable = None
		with open(self.FilePath, newline='') as file:
			returnValue = DataTable()
			reader = csv.reader(file, delimiter=fieldDelimiter, lineterminator=rowDelimiter)
			rowNumber:int = 0
			for reader in reader:
				rowNumber += 1
				if (rowNumber == 1):
					columns:list = []
					if (includeHeader):
						for item in reader:
							columnName:str = item
							dupeIndex:int = 0
							while (columns.count(columnName) > 0):
								dupeIndex += 1
								columnName = f"{columnName}_{dupeIndex}"
							columns.append(columnName)
					else:
						columns = ["Field_{}".format(x, y) for (x, y) in enumerate(reader)]
					for columnName in columns:
						dataColumn:DataColumn = DataColumn(columnName)
						dataColumn.DataType = System.Type.GetType("System.String")
						dataColumn.AllowDBNull  = True
						returnValue.Columns.Add(dataColumn)
					if (not includeHeader):
						dataRow:DataRow = returnValue.NewRow()
						for index, item in enumerate(reader):
							dataRow[index] = item
						returnValue.Rows.Add(dataRow)
				else:
					dataRow:DataRow = returnValue.NewRow()
					for index, item in enumerate(reader):
						dataRow[index] = item
					returnValue.Rows.Add(dataRow)
		return returnValue

	def GetDataTable(self) -> DataTable:
		returnValue:DataTable | None = None
		match self.Format:
			case TextFileFormat.CommaWithHeader:
				returnValue = self.__GetDataTableDelimited__("\n", ",", True)
			case TextFileFormat.CommaWithoutHeader:
				returnValue = self.__GetDataTableDelimited__("\n", ",", False)

			case TextFileFormat.TabWithHeader:
				returnValue = self.__GetDataTableDelimited__("\n", "\t", True)
			case TextFileFormat.TabWithoutHeader:
				returnValue = self.__GetDataTableDelimited__("\n", "\t", False)

			case TextFileFormat.PipeWithHeader:
				returnValue = self.__GetDataTableDelimited__("\n", "|", True)
			case TextFileFormat.PipeWithoutHeader:
				returnValue = self.__GetDataTableDelimited__("\n", "|", False)
		return returnValue

	def __WriteDataTableDelimited__(self, dataTable:DataTable, rowDelimiter:str, fieldDelimiter:str, includeHeader:bool):
		returnValue:str = None
		exception = None
		try:
			lines:list = []
			line:str = None
			line = ""
			if (includeHeader):
				for dataColumn in dataTable.Columns:
					line += f"{dataColumn.ColumnName}{fieldDelimiter}"
				if (line.endswith(fieldDelimiter)):
					line = line[:-len(fieldDelimiter)]
				lines.append(line)
				line = ""
			for dataRow in dataTable.Rows:
				line = ""
				for dataColumn in dataTable.Columns:
					if (str(dataColumn.DataType) in [
						"System.Byte",
						"System.Int16",
						"System.Int32",
						"System.Int64",
						"System.Decimal"]):
						line += f"{str(dataRow[dataColumn.ColumnName])}{fieldDelimiter}"
					else:
						line += f"{str(dataRow[dataColumn.ColumnName])}{fieldDelimiter}"
				if (line.endswith(fieldDelimiter)):
					line = line[:-len(fieldDelimiter)]
				lines.append(line)
			returnValue = ""
			for ln in lines:
				returnValue += f"{ln}{rowDelimiter}"
		except Exception as e:
			exception = e
		if exception is not None:
			raise exception
		elif returnValue is not None:
			return returnValue

	def __WriteDataTablePrettify__(self, dataTable:DataTable):
		returnValue:str = None
		exception = None
		try:
			totalColumnWidth:int = 0
			columnWidth:dict = {}
			lines:list = []
			line:str = None
			allLines:str = ""
			for dataRow in dataTable.Rows:
				for dataColumn in dataTable.Columns:
					if (dataColumn.ColumnName not in columnWidth):
						columnWidth[dataColumn.ColumnName] = len(dataColumn.ColumnName)
					if (columnWidth[dataColumn.ColumnName] < len(str(dataRow[dataColumn]))):
						columnWidth[dataColumn.ColumnName] = len(str(dataRow[dataColumn]))
			for columnName in columnWidth:
				totalColumnWidth += columnWidth[columnName]
			lines.append(" -" + ("-"*totalColumnWidth) + ("--"*len(columnWidth)) + "- ")
			line = ""
			for columnName in columnWidth:
				line += f" {columnName.ljust(columnWidth[columnName])} "
			lines.append(f"| {line} |")
			line = ""
			for columnName in columnWidth:
				headBreak:str = "-"*columnWidth[columnName]
				line += f" {headBreak} "
			lines.append(f"| {line} |")
			for dataRow in dataTable.Rows:
				line = ""
				for dataColumn in dataTable.Columns:
					if (str(dataColumn.DataType) in [
						"System.Byte",
						"System.Int16",
						"System.Int32",
						"System.Int64",
						"System.Decimal"]):
						line += f" {str(dataRow[dataColumn.ColumnName]).rjust(columnWidth[dataColumn.ColumnName])} "
					else:
						line += f" {str(dataRow[dataColumn.ColumnName]).ljust(columnWidth[dataColumn.ColumnName])} "
				lines.append(f"| {line} |")
			lines.append(" -" + ("-"*totalColumnWidth) + ("--"*len(columnWidth)) + "- ")
			returnValue = ""
			for ln in lines:
				returnValue += f"{ln}\n"
		except Exception as e:
			exception = e
		if exception is not None:
			raise exception
		elif returnValue is not None:
			return returnValue

	def WriteDataTable(self, dataTable:DataTable):
		exception = None
		try:
			text:str = None
			match self.Format:
				case TextFileFormat.CommaWithHeader:
					text = self.__WriteDataTableDelimited__(dataTable, "\n", ",", True)
				case TextFileFormat.CommaWithoutHeader:
					text = self.__WriteDataTableDelimited__(dataTable, "\n", ",", False)
				case TextFileFormat.TabWithHeader:
					text = self.__WriteDataTableDelimited__(dataTable, "\n", "\t", True)
				case TextFileFormat.TabWithoutHeader:
					text = self.__WriteDataTableDelimited__(dataTable, "\n", "\t", False)
				case TextFileFormat.PipeWithHeader:
					text = self.__WriteDataTableDelimited__(dataTable, "\n", "|", True)
				case TextFileFormat.PipeWithoutHeader:
					text = self.__WriteDataTableDelimited__(dataTable, "\n", "|", False)
				case TextFileFormat.Prettify:
					text = self.__WriteDataTablePrettify__(dataTable)

			if (text is not None):
				with open(self.FilePath, "w") as file:
					file.write(text)
		except Exception as e:
			exception = e
		if exception is not None:
			raise exception

class TextClearData:
	FilePath:Path = None
	Format:TextFileFormat = TextFileFormat.CommaWithHeader

	def __init__(self, filePath:Path, format:TextFileFormat = TextFileFormat.CommaWithHeader):
		self.FilePath = filePath
		self.Format = format
		self.Queries = TextQueries(filePath, format)
		self.BulkData = TextBulkData(filePath, format)

__all__ = ["TextFileFormat", "TextBulkData", "TextQueries", "TextClearData"]
