import requests
import xlsxwriter
import sys
import threading
import time

param = sys.argv[2]
paramType = sys.argv[1]
stillData = True
fullData = []
index=0
threads = []
lock = []

def writeExcel(data, param):
    name = param + '.xlsx'
    workbook = xlsxwriter.Workbook(name)
    worksheet = workbook.add_worksheet()
    worksheet.write(0,0, 'chartcode')
    worksheet.write(0,1, 'formatName')
    worksheet.write(0,2, 'artistname')
    worksheet.write(0,3, 'artistname_sort')
    worksheet.write(0,4, 'artistslug')
    worksheet.write(0,5, 'charttitle')
    worksheet.write(0,6, 'charttitle_sort')
    worksheet.write(0,7, 'chartweeks')
    worksheet.write(0,8, 'date')
    worksheet.write(0,9, 'rank')
    worksheet.write(0,10, 'peakdate')
    worksheet.write(0,11, 'peakpos')
    worksheet.write(0,12, 'label')
    worksheet.write(0,13, 'label_sort')
    worksheet.write(0,14, 'chartUrl')
    worksheet.write(0,15, 'artistUrl')
    row = 1
    for data in data:
        col = 0
        for key in data:
            worksheet.write(row,col, data[key])
            col += 1
        row += 1

    workbook.close()

def getUrl(index, paramType, param):
    url = "https://www.billboard.com/fe-ajax/charts/search?page=" + str(index) + "&"+ paramType + "=" + param
    return url

def getData(index, paramType, param):
    url = getUrl(index, paramType, param)
    response = requests.get(url)
    return response

def getData2(index, paramType, param):
    url = getUrl(index, paramType, param)
    response = requests.get(url)
    json = response.json()['results']
    if(type(json) is dict):
        for x in json:
            if(param in json[x][paramType].lower()):
                fullData.append(json[x])
    elif (type(json) is list):
        for x in json:
            if(param in x[paramType].lower()):
                fullData.append(x)
    lock.append("Thread %s is done" % index)


for i in range(400):
    t = threading.Thread(target=getData2, args=(i, paramType, param))
    threads.append(t)
    t.start()
    # t.join()

while(len(lock) != len(threads)):
    time.sleep(1)
    print("threads still executing: " + str(len(threads) - len(lock)))
print(len(fullData))
writeExcel(fullData, param)