import fitz
import os
import mysql.connector
from os import system, name
from pathlib import Path
from datetime import datetime
from re import sub
from decimal import Decimal


pdfList = os.listdir(os.getcwd())
matches = []
yrMonth = []
listFile = []
for fileName in pdfList:
    chkPDF = fileName.find('pdf')
    if chkPDF > 0:
        #print(fileName)
        yrMonth.append(fileName.replace('.pdf', '')[-5:])
        listFile.append(fileName)
        doc = fitz.open(fileName)
        page = doc[5]


        blocks = page.get_text("blocks")
        blocks.sort(key=lambda block: block[1])
        pageLine = []
 
        for b in blocks:
            pageLine.append(b[4].replace('\n', ''))
            if b[4].replace('\n', '').find('Total Principal Funds Available') > -1:
                for match in pageLine:
                    if "Total Principal Funds Available" in match:
                        matches.append(match) 
                pass



        #print(totFund)

        pass
    pass
pass

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


conn_str = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="cs2006amc1"
)

sqlCursor = conn_str.cursor()


ind = 0
date = ''
for i in matches:
  
    print("File Name:", "", listFile[ind])
    date = str(yrMonth[ind][-4:])
    date_time_obj = datetime.strptime(date, '%y%m')
    print("Date:", "", date_time_obj, "\n")


    sqlSelQuery = """SELECT SUM(ScheduledPrincipal) AS "Scheduled Principal", SUM(Curtailments) AS "Curtailments", SUM(Prepayment) AS "Prepayment in FUll", (SUM(LiquidationPrincipal) - SUM(PrincipalLosses)) FROM cs2006amc1.enhanceloanleveldata WHERE DistributionDate LIKE %s"""
    sqlCursor.execute(sqlSelQuery, ("%" + date + "%", ))

    queryResult = sqlCursor.fetchall()
    for x in queryResult:

        scheduledPrincipal = x[0]
        curtailments = x[1]
        prepayment = x[2]
        principalLosses = x[3]

        totFundDB = "{:0,.2f}".format(scheduledPrincipal + curtailments + prepayment + principalLosses)
        totFundPDF = "{:0,.2f}".format(Decimal(sub(r'[^\d.]', '', i)))



        print("----- Enhanced Loan Level Data -----")
        print("\n")
        print("Scheduled Principal:", "", "{:0,.2f}".format(scheduledPrincipal))
        print("Curtailments:", "", "{:0,.2f}".format(curtailments))
        print("Prepayment:", "", "{:0,.2f}".format(prepayment))
        print("Principal Losses:", "", "{:0,.2f}".format(principalLosses))

        print("\n")
               
        print("Total Principal Funds Available:", (totFundDB))

        print("\n")

        print("----- Certificate Holders Statement -----")

        print("\n")

        print("Total Principal Funds Available:", (totFundPDF))

    print("\n")
    if totFundDB == totFundPDF:
        print("Values Matched")
        pass
    else:
        print("Values Mismatched")
        pass
    print("\n")
    input('Press Enter for Next')
    clear()
    ind = ind + 1

input('End of List')



    