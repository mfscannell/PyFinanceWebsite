import openpyxl
import tkinter as tk
import tkinter.filedialog as tkfd

from py_finance import YahooFinanceClient

class TestCallback:
    def __init__(self):
        self.top = tk.Tk()
        self.top.geometry( "100x100+10+10" )
        self.top.minsize( 600, 300 )
        self.excelFilePath = tk.StringVar()
        self.selectedExcelTab = tk.StringVar()
        self.excelTabs = ['No file selected yet']

        tk.Button(self.top,
                  text='Exit',
                  command=self.top.quit,
                  bg='red',
                  fg='yellow' ).pack(side="bottom",
                                     fill="x",
                                     expand=1)
        tk.Button(self.top,
                  text='Determine all distribution days',
                  command=self.determineAllDistributionDays,
                  bg='red',
                  fg='yellow').pack(side="bottom",
                                    fill="x",
                                    expand=1)
        self.returnDateTextBox = tk.Text(self.top, height=2, width = 30)
        self.returnDateTextBox.pack(side="bottom", fill="x", expand=1)
        tk.Label(self.top, text = 'Return Date (YYYY-MM-DD)').pack(side="bottom", fill="x", expand=1)
        self.endDateTextBox = tk.Text(self.top, height=2, width = 30)
        self.endDateTextBox.pack(side="bottom", fill="x", expand=1)
        tk.Label(self.top, text = 'End Date (YYYY-MM-DD)').pack(side="bottom", fill="x", expand=1)
        self.startDateTextBox = tk.Text(self.top, height=2, width = 30)
        self.startDateTextBox.pack(side="bottom", fill="x", expand=1)
        tk.Label(self.top, text = 'Start Date (YYYY-MM-DD)').pack(side="bottom", fill="x", expand=1)
        self.excelTabsDropdown = tk.OptionMenu(self.top,
                                               self.selectedExcelTab,
                                               *self.excelTabs)
        self.excelTabsDropdown.pack(side="bottom", fill="x", expand=1)
        tk.Button(self.top,
                  text='Select an Excel File',
                  command=self.selectExcelFile,
                  bg='red',
                  fg='yellow').pack(side="bottom",
                                    fill="x",
                                    expand=1)
        self.excelFileLabel = tk.Label(self.top, textvariable = self.excelFilePath)
        self.excelFileLabel.pack(side="bottom", fill="x", expand=1)
        self.excelFilePath.set('Pick an excel file')
        self.selectedExcelTab.set(self.excelTabs[0])

        self.top.mainloop()

    def determineAllDistributionDays(self):
        print(self.selectedExcelTab.get())
        currentSheet = self.excelWorkbook.get_sheet_by_name(self.selectedExcelTab.get())
        currentRow = 3

        currentStockSymbol = currentSheet['B' + str(currentRow)].value

        startDate = self.startDateTextBox.get("1.0", 'end-1c')
        endDate = self.endDateTextBox.get("1.0", 'end-1c')
        returnDate = self.returnDateTextBox.get("1.0", 'end-1c')

        while currentStockSymbol != None:
            print(currentStockSymbol)
            if ('.' not in currentStockSymbol):
                stockClient = YahooFinanceClient(currentStockSymbol)
                stockHistory = stockClient.getHistory(startDate, returnDate)
                try:
                    stockHistory.calcInvestorsData()
                    numDays = stockHistory.getNumDistDays(endDate)
                    startPrice = stockHistory.getAdjClosePrice(endDate)
                    returnPrice = stockHistory.getLastAdjClosePrice()
                except:
                    print(currentStockSymbol + 'No stockHistory')
                currentSheet['P' + str(currentRow)] = numDays
                currentSheet['V' + str(currentRow)] = startPrice
                currentSheet['W' + str(currentRow)] = returnPrice

            currentRow = currentRow + 1
            currentStockSymbol = currentSheet['B' + str(currentRow)].value
        self.excelWorkbook.save(self.excelFilePathString)
        print('done')
        print(self.excelFilePathString)

    def selectExcelFile(self):
        self.excelFilePathString = tkfd.askopenfilename(title="Select Excel File")
        self.excelFilePath.set(self.excelFilePathString)
        self.excelWorkbook = openpyxl.load_workbook(self.excelFilePathString)

        self.selectedExcelTab.set('')
        self.excelTabsDropdown['menu'].delete(0, 'end')
        self.excelTabs = self.excelWorkbook.get_sheet_names()
        for excelTab in self.excelTabs:
            self.excelTabsDropdown['menu'].add_command(label=excelTab, command=tk._setit(self.selectedExcelTab, excelTab))
        self.selectedExcelTab.set(self.excelTabs[0])

TC = TestCallback()
