# Data Example
# Name of item, Amount of item, Total cost to attain

items = []
amounts = []
costs = []

def loadInvData() :
    #print("Loading")
    try :
        inventoryItemsDataFile = open("./inventoryItemsData.txt", "r")
    except FileNotFoundError :
        inventoryItemsDataFile = open("./inventoryItemsData.txt", "w")
        inventoryItemsDataFile.close()
        inventoryItemsDataFile = open("./inventoryItemsData.txt", "r")
    #print(inventoryDataFile.readlines())
    i=0
    for line in inventoryItemsDataFile :
        items.append(line.strip("\n")) 
        i+=1
    inventoryItemsDataFile.close()
    try :
        inventoryAmountsDataFile = open("inventoryAmountsData.txt", "r")
    except FileNotFoundError :
        inventoryAmountsDataFile = open("inventoryAmountsData.txt", "w")
        inventoryAmountsDataFile.close()
        inventoryAmountsDataFile = open("inventoryAmountsData.txt", "r")

    v=0
    for line in inventoryAmountsDataFile :
        amounts.append(int(line.strip("\n")))
    inventoryAmountsDataFile.close()
    
    try :
        inventoryCostsDataFile = open("inventoryCostsData.txt","r")
    except FileNotFoundError :
        inventoryCostsDataFile = open("inventoryCostsData.txt","w")
        inventoryCostsDataFile.close()
        inventoryCostsDataFile = open("inventoryCostsData.txt","r")
    j=0
    for line in inventoryCostsDataFile :
        costs.append(int(line.strip("\n")))
    inventoryCostsDataFile.close()


def saveInvData() :
    #print("Saving")
    inventoryItemsDataFile = open("inventoryItemsData.txt", "w")
    for i in items :
        inventoryItemsDataFile.write(i + "\n")
    #inventoryItemsDataFile.close()

    inventoryAmountsDataFile = open("inventoryAmountsData.txt", "w")
    for i in amounts :
        inventoryAmountsDataFile.write(str(i) + "\n")
    #inventoryAmountsDataFile.close()

    inventoryCostsDataFile = open("inventoryCostsData.txt", "w")
    for i in costs :
        inventoryCostsDataFile.write(str(i) + "\n")
    #inventoryCostsDataFile.close()

def adjustInv(item, amount, cost) :
    #print("Adjusting Inventory")
    if items.__contains__(item) :
        #print("Item already in list, updating inventory")
        id = items.index(item)
        #print(id)
        amounts[id] += amount
        costs[id] += cost
    else :
        items.append(item)
        amounts.append(amount)
        costs.append(cost)

        print("New Item added")

def clearInv() :
    items.clear()
    amounts.clear()
    costs.clear()
    saveInvData()

def getInvItems() :
    return items

def getInvAmounts() :
    return amounts

def appInvItems(item) :
    items.append(item)

def appInvAmounts(amount) :
    amounts.append(amount)

def remInvItems(item) :
    i = items.index(item)
    items.pop(i)

def remInvAmounts(item,amount) :
    id = items.index(item)
    amounts[id] = int(amounts[id]) - int(amount)

def remInvCosts(item,cost) :
    id = items.index(item)
    costs[id] = int(costs[id]) - int(cost)