sales = 0
purchases = 0
revenue = 0
profit = 0
cash = 0
cashArr = []

def loadFinancials() :
    try :
        financialData = open("financialData.txt", "r")
    except FileNotFoundError :
        financialData = open("financialData.txt", "w")
        num = 0
        while num < 5 :
            financialData.write("0\n")
            num += 1
        financialData.close()
        financialData = open("financialData.txt", "r")


    global sales
    global purchases
    global revenue
    global profit
    global cash

    sales = int(financialData.readline().strip("\n"))
    purchases = int(financialData.readline().strip("\n"))
    revenue = int(financialData.readline().strip("\n"))
    profit = int(financialData.readline().strip("\n"))
    cash = int(financialData.readline().strip("\n"))

    financialData.close()
    try :
        cashOverTimeData = open("cashOverTime.txt", "r")
    except FileNotFoundError :
        cashOverTimeData = open("cashOverTime.txt", "w")
        cashOverTimeData.close()
        cashOverTimeData = open("cashOverTime.txt", "r")
        
    
    for cashVal in cashOverTimeData :
        print("eye")
        print(cashArr)
        cashArr.append(int(cashVal))
    #print(cashArr)


def saveFinancials() :
    financialData = open("financialData.txt", "w")
    global sales
    global purchases
    global revenue
    global profit
    global cash
    global cashArr

    financialData.write(str(sales) + "\n")
    financialData.write(str(purchases) + "\n")
    financialData.write(str(revenue) + "\n")
    financialData.write(str(profit) + "\n")
    financialData.write(str(cash) + "\n")
    financialData.close()

    cashOverTimeData = open("cashOverTime.txt", "w")
    for cashVal in cashArr :
        cashOverTimeData.write(str(cashVal) + "\n")

def adjustFinancials(sal, purch, rev, prof, cas, app) :
    global sales
    global purchases
    global revenue
    global profit
    global cash
    global cashArr

    sales += sal
    purchases += purch
    revenue += rev
    profit += prof
    cash += cas
    if app == True :
        cashArr.append(cash)
    else : 
        pass

def clearFinancials () :
    global sales
    global purchases
    global revenue
    global profit
    global cash
    global cashArr
    
    sales = 0
    purchases = 0
    revenue = 0
    profit = 0
    cash = 0
    cashArr.clear()

    printFinancials()
    saveFinancials()

def remFromCashArr(val) :
    global cashArr
    cashArr.remove(val)
    #print("New Cash Array : " + str(cashArr))

def adjCashArr(val, index) :
    global cashArr
    #print(str(cashArr) + " Initial")
    print(index)
    cashArr[index] = cashArr[index] + int(val)
    #print(str(cashArr) + " Final")

def getFinancials() :
    global sales
    global purchases
    global revenue
    global profit
    global cash
    global cashArr

    return(sales,purchases,revenue,profit,cash,cashArr)

def printFinancials() :
    pass
    #print(sales)
    #print(purchases)
    #print(revenue)
    #print(profit)
    #print(cash)
