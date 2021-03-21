import xlrd


loc = "Input.xls"

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(2)

# Extracting number of columns
print(sheet.col_values(4))

