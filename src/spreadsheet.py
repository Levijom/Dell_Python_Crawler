###########################################################
# QuoteCrawler v2.0 - Spreadsheet.py                      #
# Copyright (C) Joao A. Haddad - Sep-Dec/2020             #
# Usage: python QuoteCrawler SOURCE.TXT DESTINATION.XLSX  #
###########################################################

import xlsxwriter


class Spreadsheet:
    workBook = xlsxwriter.workbook.Workbook
    workSheet = xlsxwriter.worksheet.Worksheet
    comparisonSheet = xlsxwriter.worksheet.Worksheet
    intelSheet = xlsxwriter.worksheet.Worksheet
    formats = {}

    def MakeCell(self, row, column):
        # "This prints a passed string into this function"
        return chr(ord("A") + column) + str(row + 1)

    def __init__(self, destFile: str, numberQuotes: int):
        self.workBook = xlsxwriter.Workbook(destFile)  # Create Excel File

        self.formats["standard_format"] = self.workBook.add_format()
        self.formats["money_format"] = self.workBook.add_format(
            {"num_format": "$#,##0"}
        )
        self.formats["percentage_format"] = self.workBook.add_format(
            {"num_format": "0.00%"}
        )
        self.formats["modifier_format"] = self.workBook.add_format(
            {"num_format": "0.00"}
        )
        self.formats["number_format"] = self.workBook.add_format({"num_format": "0"})
        self.formats["processor_format"] = self.workBook.add_format({"bold": 0})
        self.formats["processor_format"].set_bg_color("#FFFF00")  # yellow
        self.formats["memory_format"] = self.workBook.add_format({"bold": 0})
        self.formats["memory_format"].set_bg_color("#CCFFFF")  # lightblue
        self.formats["bold"] = self.workBook.add_format({"bold": 1})

        self.workSheet = self.workBook.add_worksheet("Main")  # Create Main Sheet
        self.workSheet.write("A1", "Quote #", self.formats["bold"])
        self.workSheet.set_column(0, 0, 15)  # Width of column A set to 14.
        self.workSheet.write("B1", "Config ID", self.formats["bold"])
        self.workSheet.set_column(1, 1, 10)  # Width of column B set to 10.
        self.workSheet.write("C1", "List Price", self.formats["bold"])
        self.workSheet.write("D1", "Sale Price", self.formats["bold"])
        self.workSheet.write("E1", "Freight Price", self.formats["bold"])
        self.workSheet.write("F1", "DOL%", self.formats["bold"])
        self.workSheet.write("G1", "Modifier", self.formats["bold"])
        self.workSheet.write("H1", "Quote Name", self.formats["bold"])
        self.workSheet.write("I1", "Shipping Adress", self.formats["bold"])

        self.comparisonSheet = self.workBook.add_worksheet(
            "Comparison"
        )  # ComparisonSheet
        self.comparisonSheet.set_column(0, numberQuotes, 50)

        self.intelSheet = self.workBook.add_worksheet("Intel Processors")
        self.intelSheet.write("A1", "Quote #", self.formats["bold"])
        self.intelSheet.set_column(0, 0, 16)  # Width of column A set to 16.
        self.intelSheet.write("B1", "Proc quantity", self.formats["bold"])
        self.intelSheet.write("C1", "Intel Processor", self.formats["bold"])
        self.intelSheet.set_column(2, 2, 50)  # Width of column B set to 50.

    def WritetoExcel(self, list, customerReady: bool):
        intelSheetRow = 1
        for index, item in enumerate(list):
            if item["Completed"] == False:
                self.workSheet.write(
                    index + 1, 0, item["FullQuoteNumber"]
                )  # Quote Number
                continue
            quoteNumberWithVersion = (
                item["quotenumber"] + "." + item["quotenumberversion"]
            )

            self.workSheet.write(index + 1, 0, quoteNumberWithVersion)  # Quote Number
            self.workSheet.write(index + 1, 1, item["solutionnumber"])  # Config ID
            self.workSheet.write_number(
                index + 1,
                2,
                item["TotalListPrice"],
                self.formats["money_format"],
            )  # List Price
            self.workSheet.write_number(
                index + 1,
                3,
                item["TotalSellingPrice"],
                self.formats["money_format"],
            )  # Sale Price
            self.workSheet.write_number(
                index + 1,
                4,
                item["TotalShippingPrice"],
                self.formats["money_format"],
            )  # Freight Price
            self.workSheet.write_number(
                index + 1,
                5,
                item["TotalDiscount"],
                self.formats["percentage_format"],
            )  # DOL%
            self.workSheet.write_number(
                index + 1,
                6,
                item["OverallModifier"],
                self.formats["modifier_format"],
            )  # Modifier
            self.workSheet.write(index + 1, 7, item["quoteName"])  # Quote Name
            self.workSheet.write(index + 1, 8, item["shippingAdress"])  # Quote Name

            quotesheet = self.workBook.add_worksheet(
                quoteNumberWithVersion
            )  # Create one Sheet per quote
            self.workSheet.write_url(
                self.MakeCell(index + 1, 0),
                "internal:" + quoteNumberWithVersion + "!A1",
            )  # adds the URL to the right tab

            #        quotesheet.write('A1', 'RETURN TO MAIN',bold)
            quotesheet.write_url(
                "C1",
                "internal:Main!" + self.MakeCell(index + 1, 0),
                string="RETURN TO MAIN",
            )  # return button
            quotesheet.write(
                "D1", "Quote #" + quoteNumberWithVersion, self.formats["bold"]
            )
            quotesheet.write("A2", "ID", self.formats["bold"])
            quotesheet.set_column(0, 0, 3.5)  # ID with width of 3.5
            if customerReady == False:
                quotesheet.write("B2", "UnitListPrice", self.formats["bold"])
                quotesheet.write("C2", "UnitSalePrice", self.formats["bold"])
                quotesheet.write("D2", "Quantity", self.formats["bold"])
                quotesheet.write("E2", "DOL%", self.formats["bold"])
                quotesheet.write("F2", "Modifier", self.formats["bold"])
                quotesheet.write("G2", "Configuration", self.formats["bold"])
                quotesheet.set_column(6, 6, 30)
                quotesheet.set_column(7, 7, 50)
            else:
                quotesheet.write("B2", "Quantity", self.formats["bold"])
                quotesheet.set_column(2, 2, 30)
                quotesheet.set_column(3, 3, 50)

            self.comparisonSheet.write(
                0, index, quoteNumberWithVersion, self.formats["bold"]
            )  # Quote Number

            ###################################################################
            #### PART 2 - Go recursively through all subitems in the quote ####
            ###################################################################
            quoteSheetRow = 2
            comparisonSheetRow = 1
            for index2, subitems in enumerate(item["SubItems"]):
                #
                quotesheet.write_number(quoteSheetRow, 0, index2)
                if customerReady == False:  # Adds internal information
                    quotesheet.write_number(
                        quoteSheetRow,
                        1,
                        subitems["ListPrice"],
                        self.formats["money_format"],
                    )  # List Price
                    quotesheet.write_number(
                        quoteSheetRow,
                        2,
                        subitems["SellingPrice"],
                        self.formats["money_format"],
                    )  # Selling Price
                    quotesheet.write_number(
                        quoteSheetRow,
                        3,
                        subitems["quantity"],
                        self.formats["number_format"],
                    )  # Quantity
                    quotesheet.write_number(
                        quoteSheetRow,
                        4,
                        subitems["DOL"],
                        self.formats["percentage_format"],
                    )  # DOL%
                    quotesheet.write_number(
                        quoteSheetRow,
                        5,
                        subitems["Modifier"],
                        self.formats["modifier_format"],
                    )  # Modifier
                else:
                    quotesheet.write_number(
                        quoteSheetRow,
                        1,
                        subitems["quantity"],
                        self.formats["number_format"],
                    )  # Quantity

                aux = True
                for line in subitems["configuration"].splitlines():
                    try:   # Checking to remove the Integer for Supply Chain / Lead Time
                        i = int(line)
                        continue
                    except:
                        i = 1
                    if customerReady == False:
                        columnToWrite = 6 if aux else 7
                    else:
                        columnToWrite = 2 if aux else 3

                    quotesheet.write(quoteSheetRow, columnToWrite, line)
                    if not aux:
                        formattouse = self.formats["standard_format"]
                        if "Xeon" in line:
                            formattouse = self.formats["processor_format"]
                            self.intelSheet.write(
                                intelSheetRow,
                                0,
                                quoteNumberWithVersion,
                                self.formats["bold"],
                            )  # also write on the Intel Sheet
                            self.intelSheet.write_number(
                                intelSheetRow,
                                1,
                                subitems["quantity"],
                                self.formats["number_format"],
                            )
                            self.intelSheet.write(intelSheetRow, 2, line)
                            intelSheetRow += 1
                        if (
                            "RDIMM" in line
                            or "rNDC" in line
                            or "SSD" in line
                            or "NVM" in line
                            or "15K" in line
                        ):
                            formattouse = self.formats["memory_format"]
                        self.comparisonSheet.write(
                            comparisonSheetRow, index, line, formattouse
                        )
                        quoteSheetRow += 1
                        comparisonSheetRow += 1
                    aux = not aux

        self.workBook.close()