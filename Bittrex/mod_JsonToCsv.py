import json
import csv

def JTC( wd , symbol , fileName , option ):

    filePath = wd + "\\" + symbol + "\\" + fileName + ".txt"
    fileObject = open( filePath, "r" )
    jsonFileContent = fileObject.read()

    try:
        parsed_json = json.loads(jsonFileContent)
    except Exception as e:
        print(repr(e))

    #
    if option == "Get Ticker - bid":
        dictInfo = parsed_json["bidRate"]
        fileName = option
        exportOption = 1
    if option == "Get Ticker - ask":
        dictInfo = parsed_json["askRate"]
        fileName = option
        exportOption = 1

    #
    if option == "Get Orderbook - bid":
        dictInfo = parsed_json["bid"]
        fileName = option
        exportOption = 2
    if option == "Get Orderbook - ask":
        dictInfo = parsed_json["ask"]
        fileName = option
        exportOption = 2

    print(dictInfo)

    csv_file = open( wd + "\\" + symbol + "\\" + fileName + ".csv", 'w', newline='')
    csv_writer = csv.writer(csv_file)

    if exportOption == 1:
        csv_writer.writerow([dictInfo])

    if exportOption == 2:
        csv_writer.writerow( dictInfo[0].keys() ) # header
        for row in dictInfo:
            csv_writer.writerow(row.values())

#
