import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import numpy as np

def findOptimalAllocation(startDate, endDate, symbols):
    bestSharpeRatio = 0;
    bestAllocations = [0.0, 0.0, 0.0, 0.0]

    totalTrys = 0
    totalLegalAllocations = 0
    totalIlleagalAllocations = 0

    for x1 in range(0,11):
        for x2 in range(0,11):
            for x3 in range(0,11):
                for x4 in range(0,11):
                    allocations = [x1 * 0.1, x2 * 0.1, x3 * 0.1, x4 * 0.1]
                    totalTrys += 1
                    if isLegalAllocations(allocations):
                        totalLegalAllocations += 1
                        sharpeRatio, standardDeviation, averageDailyReturn, totalReturn =  calculatePortfolio(startDate, endDate, symbols, allocations)
                        if sharpeRatio > 1.416:
                            print "Try: {}; SharpeRatio: {}; Allocations: {}".format(totalTrys, sharpeRatio, allocations)
                        if (sharpeRatio > bestSharpeRatio):
                            bestSharpeRatio = sharpeRatio
                            bestAllocations = allocations
                    else:
                        totalIlleagalAllocations += 1

    print "Total Trys: {}".format(totalTrys)
    print "Total Legal Trys: {}".format(totalLegalAllocations)
    print "Total Illeagal Trys: {}".format(totalIlleagalAllocations)

    sharpeRatio, standardDeviation, averageDailyReturn, totalReturn = calculatePortfolio(startDate, endDate, symbols, bestAllocations)

    return sharpeRatio, standardDeviation, averageDailyReturn, totalReturn, bestAllocations

def isLegalAllocations(weightVector):
    if np.sum(weightVector) == 1.0:
        return True
    else:
        return False

def calculatePortfolio(startDate, endDate, symbols, allocations):
    stockDataDictionary = getStockData(startDate, endDate, symbols)
    closePrices = stockDataDictionary['close'].values

    tsu.returnize0(closePrices)
    sumDailyreturns = np.sum(closePrices * allocations, axis=1)

    sharpeRatio = tsu.get_sharpe_ratio(sumDailyreturns)
    standardDeviation = np.std(sumDailyreturns)
    averageDailyReturn = np.average(sumDailyreturns)
    totalReturn = np.prod(sumDailyreturns + 1)

    return sharpeRatio, standardDeviation, averageDailyReturn, totalReturn

def getStockData(startDate, endDate, symbols):
    readTime = dt.timedelta(hours = 16)
    tradingDays = du.getNYSEdays(startDate, endDate, readTime)

    dataObject = da.DataAccess('Yahoo', cachestalltime = 1)
    dataKeys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    dataFrame = dataObject.get_data(tradingDays, symbols, dataKeys)
    stockDataDictionary = dict(zip(dataKeys, dataFrame))

    return stockDataDictionary

startDate = dt.datetime(2010, 1, 1)
endDate = dt.datetime(2010, 12, 31)
symbols = ['BRCM', 'TXN', 'IBM', 'HNZ']
allocations = [0.1, 0.1, 0.0, 0.8]

sharpeRatio, standardDeviation, averageDailyReturn, totalReturn, bestAllocations = findOptimalAllocation(startDate, endDate, symbols)
# sharpeRatio, standardDeviation, averageDailyReturn, totalReturn = calculatePortfolio(startDate, endDate, symbols, allocations)

print
print "Start Date: {}".format(startDate)
print "End Date: {}".format(endDate)
print "Symbols: {}".format(symbols)
print "Best Allocations: {}".format(bestAllocations)
print "Sharpe Ratio: {}".format(sharpeRatio)
print "Standard Deviation: {}".format(standardDeviation)
print "Average Daily Return: {}".format(averageDailyReturn)
print "Total Return: {}".format(totalReturn)
