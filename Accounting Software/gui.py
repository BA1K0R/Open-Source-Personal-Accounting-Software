import tkinter as tk
from tkinter import *
import customtkinter

from PIL import ImageTk, Image

from financials import getFinancials
from financials import clearFinancials
from financials import adjustFinancials
from financials import saveFinancials
from financials import remFromCashArr
from financials import adjCashArr

from inventory import adjustInv
from inventory import saveInvData
from inventory import clearInv
from inventory import getInvAmounts
from inventory import getInvItems
from inventory import remInvAmounts
from inventory import remInvCosts
from inventory import remInvItems

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure

cashGraphTextColor = "White"
cashGraphLineColor = "Green"

matplotlib.rcParams["text.color"] = cashGraphTextColor
matplotlib.rcParams["axes.labelcolor"] = cashGraphTextColor
matplotlib.rcParams["xtick.color"] = cashGraphTextColor
matplotlib.rcParams["ytick.color"] = cashGraphTextColor
matplotlib.rcParams["axes.edgecolor"] = cashGraphTextColor

version = "1.2.2"
numTrans = 1
itemNum = 0
numDeleted = 0
transactions = []
transNumArray = [0]
cashValsArray = [0]
firstRun = True

def clearTransactions() :
    transactionDataFile = open("transactionData.txt", "w")

def saveTransactions() :
    #print("Saving")
    transactionDataFile = open("transactionData.txt","w")
    for trans in transactions :
        #print(trans)
        transactionDataFile.write(trans + "\n")

def updateCashSubPlot(plot,canvas) :
    print("In updateCashSubPlot")
    print(transNumArray, cashValsArray)
    try :
        plot.clear()
        plot.plot(transNumArray,cashValsArray,color=cashGraphLineColor)
        plot.set_facecolor("#2b2b2b")
        canvas.draw()
    except ValueError :
        pass

def genGUI(dataTable) :

    def resetData() :
        global itemNum
        global numTrans
        global transNumArray
        global cashValsArray
        clearFinancials()
        clearInv()
        clearTransactions()
        for child in inventoryFrame.winfo_children() :
            child.destroy()
        for child in transactionHistoryScrollableFrame.winfo_children() :
            child.destroy()
        transNumArray = [0]
        cashValsArray = [0]
        itemNum= 0
        numTrans = 1
        loadItemsInInv()
        loadTransactions()
        updateFincancialDataTable()
        cashSubplot.clear()
        cashSubplot.plot(transNumArray,cashValsArray,color=cashGraphLineColor)
        cashSubplot.set_facecolor("#2b2b2b")
        cashGraphCanvas.draw()
        


    def hideDashboard() :
        salesFrame.place_forget()
        purchasesFrame.place_forget()
        revenueFrame.place_forget()
        profitFrame.place_forget()
        cashBalanceFrame.place_forget()
        transactionHistoryFrame.place_forget()
        placeHolderFrame1.place_forget()
        placeHolderFrame2.place_forget()
        dashboardTitleFrame.place_forget()

    def showDashboard() :
        salesFrame.place(relwidth=0.19,relheight=.16,relx=0.1,rely=0.15)
        purchasesFrame.place(relwidth=0.19,relheight=.16,relx=0.31,rely=0.15)
        revenueFrame.place(relwidth=0.19,relheight=.16,relx=0.52,rely=0.15)
        profitFrame.place(relwidth=0.19,relheight=.16,relx=0.73,rely=0.15)
        cashBalanceFrame.place(relwidth=.4,relheight=.3,relx=.1,rely=.36)
        transactionHistoryFrame.place(relwidth=.4,relheight=.59,relx=.52,rely=.36)
        placeHolderFrame1.place(relwidth=.19,relheight=.27,relx=.1,rely=.68)
        placeHolderFrame2.place(relwidth=.19,relheight=.27,relx=.31,rely=.68)
        dashboardTitleFrame.place(relwidth=.1,relheight=.05,relx=.1,rely=0.05)

    def showSettings() :
        settingsTitleFrame.place(relwidth=.1,relheight=.05,relx=.1,rely=0.05)   
        settingsFrame.place(relwidth=0.5,relheight=0.8,relx=0.1,rely=0.15)
        clearDataButton.place(relwidth=0.2,relheight=0.05,relx=0.05,rely=0.05)
     

    def hideSettings() :
        settingsTitleFrame.place_forget()
        settingsFrame.place_forget()
        clearDataButton.place_forget()
        confirmClearFrame.place_forget()

    def showInventory() :
        inventoryTitleFrame.place(relwidth=.1,relheight=.05,relx=.1,rely=0.05)   
        inventoryFrame.place(relwidth=0.8,relheight=0.7,relx=0.1,rely=0.25)
        inventoryTitlesFrame.place(relwidth=0.5,relheight=0.05,relx=0.1,rely=0.15)
        inventoryItemLable.place(relheight=1,x=0,rely=0.05)
        inventoryAmountLable.place(relheight=1,x=200,rely=0.05)
    
    def hideInventory() :
        inventoryTitleFrame.place_forget()
        inventoryFrame.place_forget()
        inventoryTitlesFrame.place_forget()

    def settingsButtonPush() :
        #print("Settings Popup! Kablowie!")
        hideDashboard()
        hideInventory()
        showSettings()

    def dashboardButtonPush() :
        hideSettings()
        hideInventory()
        showDashboard()

    def inventoryButtonPush() :
        hideDashboard()
        hideSettings()
        showInventory()

    def clearDataButtonPush() :
        confirmClearFrame.place(relwidth=.2,relheight=.2,relx=.4,rely=.4)
        clearDataWarningLabel.place(relwidth=0.8, relheight=0.4, relx=0.1, rely = 0.05)
        clearDataNoButton.place(relwidth=0.35, relheight=0.4, relx=0.1, rely=0.5)
        clearDataYesButton.place(relwidth=0.35, relheight=0.4, relx=0.6, rely=0.5)

    def clearDataNoButtonPush() :
        confirmClearFrame.place_forget()
    
    def clearDataYesButtonPush() :
        #print("Data Deleted Successfully")
        resetData()
        clearDataSuccessPopupFrame.place(relwidth=.2,relheight=.2,relx=.4,rely=.4)
        clearDataSuccessPopupLabel.place(relwidth=0.8,relheight=0.4,relx=0.1,rely=0.05)
        clearDataSuccessPopupButton.place(relwidth=0.35, relheight=0.4, relx=0.325, rely=0.5)
        confirmClearFrame.place_forget()

    def clearDataSuccessPopupButtonPush() :
        clearDataSuccessPopupFrame.place_forget()

    def updateFincancialDataTable() :
        dataTable.clear()
        for item in getFinancials() :
            dataTable.append(str(item))
        
       # print(dataTable)
        salesNumLabel.configure(text=dataTable[0])
        purchasesNumLabel.configure(text=dataTable[1])
        revenueNumLabel.configure(text=dataTable[2])
        profitNumLabel.configure(text=dataTable[3])
        cashBalanceNumLabel.configure(text="$" + dataTable[4])

    
    
    window = customtkinter.CTk()
    window.geometry("1280x800")
    window.title("Acc Build " + version)


    def addTransaction() :
        global numTrans
        global itemNum
        if transTypeEntry.get() != "P/S" :
            createTransaction(transTypeEntry.get(),transItemEntry.get(),transAmountEntry.get(),transPriceEntry.get(),transactionHistoryScrollableFrame,numTrans)
            transactions.append(transTypeEntry.get() + " " + transItemEntry.get() + " " + transAmountEntry.get() + " " + transPriceEntry.get())
            
            if transTypeEntry.get() == "Purchase" : 
                adjustInv(transItemEntry.get(), int(transAmountEntry.get()), int(transPriceEntry.get()))
                adjustFinancials(0, 1, 0, -int(transPriceEntry.get()), -int(transPriceEntry.get()), True)
            elif transTypeEntry.get() == "Sale" : 
                adjustInv(transItemEntry.get(), -int(transAmountEntry.get()), -int(transPriceEntry.get()))
                adjustFinancials(1, 0, int(transPriceEntry.get()), int(transPriceEntry.get()), int(transPriceEntry.get()), True)
            saveTransactions()
            saveFinancials()
            saveInvData()
            updateFincancialDataTable()

            #Delete all entries in inventory and remake them to update data
            for child in inventoryFrame.winfo_children() :
                child.destroy()
            itemNum= 0
            loadItemsInInv()

            transNumArray.append(numTrans)
            print("In add transaction")
            print(cashValsArray)
            cashValsArray.append(getFinancials()[5][numTrans-1])
            print("AAAAA")
            print(getFinancials()[5][numTrans-1])
            print(cashValsArray)
            #print(transNumArray)
            #print(cashValsArray)
            numTrans += 1
            
            updateCashSubPlot(cashSubplot,cashGraphCanvas)
        else :
            pass

    def loadTransactions() :
        global firstRun
        print("Start of load Transactions")
        print(cashValsArray)
        global numTrans
        try :
            transactionDataFile = open("transactionData.txt", "r")
        except FileNotFoundError :
            transactionDataFile = open("transactionData.txt", "w")
            transactionDataFile.close()
            transactionDataFile = open("transactionData.txt", "r")
        #print(transactionDataFile.readlines())
        i = 1
        for line in transactionDataFile :
            text = line.split()
            createTransaction(text[0],text[1],text[2],text[3],transactionHistoryScrollableFrame,numTrans)
            transactions.append(str(text[0]) + " " + str(text[1]) + " " + str(text[2]) + " " + str(text[3]))
            transNumArray.append(i)
            print("BBBB")
            print(getFinancials()[5])
            #print(i)

            cashValsArray.append(getFinancials()[5][i - 1])
            print(getFinancials()[5])

            i+=1
            numTrans+=1
            print(transNumArray)
            updateCashSubPlot(cashSubplot,cashGraphCanvas)
            #print(transactions)
        print("End of load Transactions")
        print(cashValsArray)
        transactionDataFile.close()

    def createTransaction(transType, item, amount, price, frame, transID) :
        genFrame = customtkinter.CTkFrame(frame,width=400,height=50,fg_color="#333333")
        genFrame.pack(anchor=W,pady=1, fill=X)

        generatedText = str(transType) + " " + str(item) + " " + str(amount) + " " + str(price)
        transactionElement = customtkinter.CTkLabel(genFrame, text=generatedText)
        transactionElement.pack(anchor=W,pady=0.05)#(relwidth=0.8, relheight=1, relx=-.3, rely=0.05)

        #Create Delete Button
        delButton = customtkinter.CTkButton(genFrame,fg_color="Red",hover_color="Dark Red",text="Del",command=lambda: deleteTransaction(transType,item,amount,price,genFrame,transID))
        delButton.place(relwidth=0.1,relheight=1,relx=0.85)

    def deleteTransaction(transType,transItemName,transAmount,transPrice,transFrame,transID) :
        global numTrans
        global numDeleted
        global itemNum
        transFrame.destroy()

        transNumArray.remove(int(numTrans-1))
        

        transactions.remove(transType + " " + transItemName + " " + transAmount + " " + transPrice)
        if transType == "Purchase" :
            adjustInv(transItemName, int(transAmount) * -1, int(transPrice) * -1)
            adjustFinancials(0, -1, 0, int(transPrice), int(transPrice), False)
            adjCashArr(transPrice,numTrans-2)
        elif transType == "Sale" : 
            adjustInv(transItemName, int(transAmount), int(transPrice))
            adjustFinancials(1, 0, -int(transPrice), -int(transPrice), -int(transPrice), False)
            adjCashArr(int(transPrice) * -1,numTrans-2)
        else :
            pass
        
        remFromCashArr(getFinancials()[5][numTrans-2])
        if transType == "Purchase" :
            cashValsArray.pop(-2)
            cashValsArray[-1] += int(transPrice)
        else :
            cashValsArray.pop(-2)
            cashValsArray[-1] -= int(transPrice)
        #print(getFinancials()[5])
        #print(cashValsArray)
        #print(transNumArray, cashValsArray)

        saveTransactions()
        saveFinancials()
        saveInvData()
        updateFincancialDataTable()

        #Delete all entries in inventory and remake them to update data
        for child in inventoryFrame.winfo_children() :
            child.destroy()
        itemNum= 0
        

        #print(transNumArray)
        #print(cashValsArray)
        numTrans -= 1

        #remInvAmounts(transItemName,transAmount)
        #remInvCosts(transItemName,transPrice)
        #remInvItems(transItemName)

        loadItemsInInv()
        updateCashSubPlot(cashSubplot,cashGraphCanvas)
        numDeleted += 1

    def loadItemsInInv() :
        for item in getInvItems() :
            #print(itemNum)
            createItemInInv(item, getInvAmounts()[itemNum], inventoryFrame)


    #Sales Frames
    salesFrame = customtkinter.CTkFrame(window)
    salesFrame.place(relwidth=0.19,relheight=.16,relx=0.1,rely=0.15)

    salesLabel = customtkinter.CTkLabel(salesFrame,text="Number of Sales")
    salesLabel.place(relx=.05,rely=.05)
    salesNumLabel = customtkinter.CTkLabel(salesFrame,text=dataTable[0])
    salesNumLabel.place(relx=.05,rely=.3)

    #Purchase Frames
    purchasesFrame = customtkinter.CTkFrame(window)
    purchasesFrame.place(relwidth=0.19,relheight=.16,relx=0.31,rely=0.15)

    purchasesLabel = customtkinter.CTkLabel(purchasesFrame,text="Number of Purchases")
    purchasesLabel.place(relx=.05,rely=.05)
    purchasesNumLabel = customtkinter.CTkLabel(purchasesFrame,text=dataTable[1])
    purchasesNumLabel.place(relx=.05,rely=.3)

    #Revenue Frames
    revenueFrame = customtkinter.CTkFrame(window)
    revenueFrame.place(relwidth=0.19,relheight=.16,relx=0.52,rely=0.15)

    revenueLabel = customtkinter.CTkLabel(revenueFrame,text="Revenue")
    revenueLabel.place(relx=.05,rely=.05)
    revenueNumLabel = customtkinter.CTkLabel(revenueFrame,text=dataTable[2])
    revenueNumLabel.place(relx=.05,rely=.3)

    #Profit Frames
    profitFrame = customtkinter.CTkFrame(window)
    profitFrame.place(relwidth=0.19,relheight=.16,relx=0.73,rely=0.15)

    profitLabel = customtkinter.CTkLabel(profitFrame,text="Profit")
    profitLabel.place(relx=.05,rely=.05)
    profitNumLabel = customtkinter.CTkLabel(profitFrame,text=dataTable[3])
    profitNumLabel.place(relx=.05,rely=.3)

    #Transaction Frames
    transactionHistoryFrame = customtkinter.CTkFrame(window)
    transactionHistoryFrame.place(relwidth=.4,relheight=.59,relx=.52,rely=.36)
    transactionHistoryLabel = customtkinter.CTkLabel(transactionHistoryFrame,text="Transaction History")
    transactionHistoryLabel.place(relx=0.05,rely=0.05)

    transactionHistoryScrollableFrame = customtkinter.CTkScrollableFrame(transactionHistoryFrame)
    transactionHistoryScrollableFrame.place(relwidth=0.9,relheight=0.75,relx=.05,rely=.2)


    addTransactionButton = customtkinter.CTkButton(transactionHistoryFrame,text="+",command=addTransaction)
    addTransactionButton.place(relwidth=.1,relx=0.05,rely=0.1)

    transTypeEntry = customtkinter.CTkOptionMenu(transactionHistoryFrame,
                                                values=["P/S","Purchase", "Sale"])
    transTypeEntry.place(relwidth=0.15,relx=0.16,rely=0.1)

    transItemEntry = customtkinter.CTkEntry(transactionHistoryFrame)
    transItemEntry.place(relwidth=0.15,relx=0.32,rely=0.1)
    transItemEntry.insert(0,"Item")

    transAmountEntry = customtkinter.CTkEntry(transactionHistoryFrame)
    transAmountEntry.place(relwidth=0.15,relx=0.48,rely=0.1)
    transAmountEntry.insert(0,"Amount")

    transPriceEntry = customtkinter.CTkEntry(transactionHistoryFrame)
    transPriceEntry.place(relwidth=0.15,relx=0.64,rely=0.1)
    transPriceEntry.insert(0,"Price")

    #Cash Balance Area
    cashBalanceFrame = customtkinter.CTkFrame(window)
    cashBalanceFrame.place(relwidth=.4,relheight=.3,relx=.1,rely=.36)
    cashBalanceLabel = customtkinter.CTkLabel(cashBalanceFrame,text="Cash Balance")
    cashBalanceLabel.place(relx=0.05,rely=0.05)
    cashBalanceNumLabel = customtkinter.CTkLabel(cashBalanceFrame,text="$" + dataTable[4])
    cashBalanceNumLabel.place(relx=.8,rely=0.05)

    cashGraphFigure = Figure(figsize=(11, 11), dpi=100)
    cashGraphFigure.set_facecolor("#2b2b2b")
    cashSubplot = cashGraphFigure.add_subplot(111)
    print("startup Values")
    print(transNumArray, cashValsArray)
    cashSubplot.plot(transNumArray,cashValsArray,color=cashGraphLineColor)
    cashSubplot.set_facecolor("#2b2b2b")
    
    cashGraphCanvas = FigureCanvasTkAgg(cashGraphFigure, cashBalanceFrame)
    cashGraphCanvas._tkcanvas.place(relwidth=0.79,relheight=0.8,relx=0.105,rely=0.15)

    #PlaceHolders
    placeHolderFrame1 = customtkinter.CTkFrame(window)
    placeHolderFrame1.place(relwidth=.19,relheight=.27,relx=.1,rely=.68)
    placeHolderFrame2 = customtkinter.CTkFrame(window)
    placeHolderFrame2.place(relwidth=.19,relheight=.27,relx=.31,rely=.68)

    #SideBar
    sideBarFrame = customtkinter.CTkFrame(window)
    sideBarFrame.place(relwidth=.07,relheight=1)

    #Dashboard Title
    dashboardTitleFrame = customtkinter.CTkFrame(window)
    dashboardTitleFrame.place(relwidth=.1,relheight=.05,relx=.1,rely=0.05)

    dashBoardTitle = customtkinter.CTkLabel(dashboardTitleFrame,text="Dashboard",font=("SegoeUI",13,"bold"))
    dashBoardTitle.place(relwidth=.6,relheight=.7,relx=0.2,rely=0.15)

    #Dashboard Button
    dashboardButton = customtkinter.CTkButton(master=window, command=dashboardButtonPush, text="Dashboard")
    dashboardButton.place(relwidth=0.05,relheight=0.05, relx = 0.01, rely=0.5)  

    #Settings Button
    settingsButton = customtkinter.CTkButton(master=window, command=settingsButtonPush, text="Settings")
    settingsButton.place(relwidth=0.05,relheight=0.05, relx = 0.01, rely=0.6)
    
    #Settings Title Frame
    settingsTitleFrame = customtkinter.CTkFrame(window)

    #Settings Title
    settingsTitle = customtkinter.CTkLabel(settingsTitleFrame,text="Settings",font=("SegoeUI",13,"bold"))
    settingsTitle.place(relwidth=.6,relheight=.7,relx=0.2,rely=0.15)

    #Settings Frame
    settingsFrame = customtkinter.CTkFrame(window)

    clearDataButton = customtkinter.CTkButton(settingsFrame, text="Clear All Data", command=clearDataButtonPush)

    confirmClearFrame = customtkinter.CTkFrame(window, fg_color="black")
    clearDataWarningLabel = customtkinter.CTkLabel(confirmClearFrame, text="Are you sure \nyou want to clear \nall data? This will \nreset all data.")
    clearDataNoButton = customtkinter.CTkButton(confirmClearFrame, text="No", fg_color="green", hover_color="dark green", command=clearDataNoButtonPush)
    clearDataYesButton = customtkinter.CTkButton(confirmClearFrame, text="Yes", fg_color="red", hover_color="dark red", command=clearDataYesButtonPush)
    clearDataSuccessPopupFrame = customtkinter.CTkFrame(window,fg_color="black")
    clearDataSuccessPopupLabel = customtkinter.CTkLabel(clearDataSuccessPopupFrame,text="Data Cleared Successfully",fg_color="black")
    clearDataSuccessPopupButton = customtkinter.CTkButton(clearDataSuccessPopupFrame, text="Ok",command=clearDataSuccessPopupButtonPush)

    #Inventory Gui
    inventoryButton = customtkinter.CTkButton(window,text="Inventory",command=inventoryButtonPush)
    inventoryButton.place(relwidth=0.05,relheight=0.05,relx=0.01,rely=0.4)

    #Inventory Title
    inventoryTitleFrame = customtkinter.CTkFrame(window)
    inventoryTitle = customtkinter.CTkLabel(inventoryTitleFrame,text="Inventory",font=("SegoeUI",13,"bold"))
    inventoryTitle.place(relwidth=.6,relheight=.7,relx=0.2,rely=0.15)


    inventoryFrame = customtkinter.CTkScrollableFrame(window)
    inventoryTitlesFrame = customtkinter.CTkFrame(window)
    inventoryItemLable = customtkinter.CTkLabel(inventoryTitlesFrame,text="Item Name",width=100)
    inventoryAmountLable = customtkinter.CTkLabel(inventoryTitlesFrame,text="Amount in Inventory",width=100)

    loadTransactions()
    loadItemsInInv()
    window.mainloop()



def createItemInInv(item, amount, frame) :
    global itemNum
    #print(itemNum)
    itemElement = customtkinter.CTkLabel(frame,text=item)
    itemElement.pack(anchor=W,padx=20,pady=0.02*itemNum)
    amountElement = customtkinter.CTkLabel(frame,text=amount)
    amountElement.pack(anchor=W,padx=200,pady=0.02*itemNum)
    itemNum += 1



    saveTransactions()
