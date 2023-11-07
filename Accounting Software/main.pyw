from inventory import loadInvData
from inventory import saveInvData
from inventory import adjustInv
from inventory import clearInv
from inventory import getInvAmounts
from inventory import getInvItems

from financials import loadFinancials
from financials import saveFinancials
from financials import adjustFinancials
from financials import clearFinancials
from financials import getFinancials

from gui import genGUI
from gui import clearTransactions

dataTable = []
itemsDataTable = []
itemAmountsDataTable = []

def loadData() :
    loadInvData()
    loadFinancials()

def saveData() :
    saveInvData()
    saveFinancials()

def resetData() :
    clearFinancials()
    clearInv()
    clearTransactions()

def __main__ () :

    loadData()

    #insert data to dataTable so our other script isnt out of range while loading
    for item in getFinancials() :
        dataTable.append(str(item))

    for item in getInvItems() :
        itemsDataTable.append(str(item))

    for item in getInvAmounts() :
        itemAmountsDataTable.append(str(item))

    genGUI(dataTable)


__main__()


