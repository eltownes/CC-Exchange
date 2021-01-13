import json
import csv

def PJ( wd , symbol , fileName ):

    filePath = wd + "\\" + symbol + "\\" + fileName + ".txt"
    fileObject = open( filePath, "r" )
    jsonFileContent = fileObject.read()

    try:
        parsed_json = json.loads(jsonFileContent)
    except Exception as e:
        print(repr(e))

    csv_file = open( wd + "\\" + symbol + "\\" + fileName + ".csv", 'w', newline='')
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow( parsed_json[0].keys() ) # header

    for row in parsed_json:
        csv_writer.writerow(curr.values())
