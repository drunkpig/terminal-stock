# -*- coding: utf-8 -*- 

import string
import time
import os
import platform
from terminalColor import bcolors
import requests

mystock = {}

stocks = ''

url = "https://hq.sinajs.cn/list="


def readData():
    f = open('my_stock.dat', 'r')
    stockList = f.read().split('\n')
    global stocks, mystock, mystockCode
    for item in stockList:
        if item != '':
            itemList = item.split()
            stocks += itemList[0] + ','
            mystock[itemList[0]] = (itemList[1], itemList[2]) if len(itemList) == 3 else None
    stocks = stocks[:-1]
    f.close()


def getTime():
    return time.strftime('%Y-%m-%d %A %p %X', time.localtime(time.time()))


def highOrLow(a, b):
    return bcolors.RED if a >= b else bcolors.GREEN


def printStock():
    ctx = requests.get(url + stocks, headers={"Referer": "https://finance.sina.com.cn"})
    ctx.encoding = "gb2312"
    data = ctx.text
    # print type(data)
    line = data.split('\n')

    print(bcolors.WHITE+"CODE      NM         Close      Open        Hi         Low       Now        %         Lost           Lost%       $$" + bcolors.ENDC)
    for stock in line:
        stockInfo = stock.split(',')
        if stockInfo[0]:
            temp = stockInfo[0].split('_')[2].replace('"', '').split('=')
            code = temp[0]
            name = temp[1]
            todayBeginPrice = string.atof(stockInfo[1])
            yersterdayEndPrice = string.atof(stockInfo[2])
            currentPrice = string.atof(stockInfo[3])
            todayMaxPrice = string.atof(stockInfo[4])
            todayMinPrice = string.atof(stockInfo[5])
            per = u'停牌  ' if '%.2f' % todayBeginPrice == '0.00' else ('%+.2f' % (
                    (currentPrice / yersterdayEndPrice - 1) * 100)) + '%'
            # 红涨绿跌
            todayBeginPriceColor = highOrLow(todayBeginPrice, yersterdayEndPrice)
            currentPriceColor = highOrLow(currentPrice, yersterdayEndPrice)
            todayMaxPriceColor = highOrLow(todayMaxPrice, yersterdayEndPrice)
            todayMinPriceColor = highOrLow(todayMinPrice, yersterdayEndPrice)

            stockCost = 0
            stockQuantity = 0
            floatMoney = 0
            stockRatio = 0
            floatMoneyColor = bcolors.WHITE
            if (code in mystock) and (mystock[code] != None):
                stockQuantity = int(mystock[code][0])
                stockCost = string.atof(mystock[code][1])
                if '%.2f' % todayBeginPrice != '0.00':
                    floatMoney = (currentPrice - stockCost) * stockQuantity
                    stockRatio = ('%+.2f' % ((currentPrice / stockCost - 1) * 100)) + '%'
                    floatMoneyColor = highOrLow(currentPrice, stockCost)
                else:
                    floatMoney = (yersterdayEndPrice - stockCost) * stockQuantity
                    stockRatio = ('%+.2f' % ((yersterdayEndPrice / stockCost - 1) * 100)) + '%'
                    floatMoneyColor = highOrLow(yersterdayEndPrice, stockCost)

                print(
                    '%s%s%s %s%4s%s %s%10.2f%s %s%10.2f%s %s%10.2f%s %s%10.2f%s %s%10.2f   %s%s    %s%10.2f     %10s%s   %s%10.2f%s' %
                    (bcolors.WHITE, code, bcolors.ENDC,
                     bcolors.WHITE, name, bcolors.ENDC,
                     bcolors.WHITE, yersterdayEndPrice, bcolors.ENDC,
                     todayBeginPriceColor, todayBeginPrice, bcolors.ENDC,
                     todayMaxPriceColor, todayMaxPrice, bcolors.ENDC,
                     todayBeginPriceColor, todayMinPrice, bcolors.ENDC,
                     currentPriceColor, currentPrice, per, bcolors.ENDC,
                     floatMoneyColor, floatMoney, stockRatio, bcolors.ENDC,
                     bcolors.WHITE, stockCost * stockQuantity, bcolors.ENDC)
                )

            else:
                print(
                    '%s%s%s %s%4s%s %s%10.2f%s %s%10.2f%s %s%10.2f%s %s%10.2f%s %s%10.2f   %s%s' %
                    (bcolors.WHITE, code, bcolors.ENDC,
                     bcolors.WHITE, name, bcolors.ENDC,
                     bcolors.WHITE, yersterdayEndPrice, bcolors.ENDC,
                     todayBeginPriceColor, todayBeginPrice, bcolors.ENDC,
                     todayMaxPriceColor, todayMaxPrice, bcolors.ENDC,
                     todayBeginPriceColor, todayMinPrice, bcolors.ENDC,
                     currentPriceColor, currentPrice, per, bcolors.ENDC)
                )


if __name__ == '__main__':
    readData()
    sysstr = platform.system()
    clear_screen_cmd = "clear"

    if sysstr == 'Darwin' or sysstr == "Linux":
        clear_screen_cmd = "clear"
    elif sysstr == 'Windows':
        clear_screen_cmd = "cls"

    while True:
        os.system(clear_screen_cmd)
        print(bcolors.YELLOW+getTime()+bcolors.ENDC)
        try:
            printStock()
        except:
            pass

        time.sleep(5)
