
import xml.etree.ElementTree as xml
import csv
import json

# function to parse CSV into a more useable format
def parse_CSV(path):
    with open(path) as csvfile:
        hostValues = {
            "aggregate": {
                "name": "AGGREGATE",
                "total": 0,
                "entries": 0,
                "minimum": float('inf'),
                "maximum": float('-inf')
            }
        }
        lines = csv.reader(csvfile)
        i = 0
        for row in lines:        
            j = 0     
            for value in row: 
                if i == 0:
                    if j == 0:
                        j += 1
                        continue
                        
                    colName = value.split('#')[1]

                    hostValues[j] = {
                        "name": colName,
                        "total": 0,
                        "entries": 0,
                        "minimum": float('inf'),
                        "maximum": float('-inf')
                    }
                else: 
                    if j == 0:
                        j += 1
                        continue

                    value = float(value) if value else None

                    # skip calculations if there is no value
                    if value == None:
                        continue

                    # calculations per column
                    hostValues[j]["total"] += value
                    hostValues[j]["entries"] += 1
                    if hostValues[j]["minimum"] > value:
                        hostValues[j]["minimum"] = value 
                    if hostValues[j]["maximum"] < value:
                        hostValues[j]["maximum"] = value 

                    # calculations for the whole dataset
                    hostValues["aggregate"]["total"] += value
                    hostValues["aggregate"]["entries"] += 1
                    if hostValues["aggregate"]["minimum"] > value:
                        hostValues["aggregate"]["minimum"] = value 
                    if hostValues["aggregate"]["maximum"] < value:
                        hostValues["aggregate"]["maximum"] = value 
                
                j += 1
            
            j = 0
            i += 1

        return hostValues

# function to output data in desired format
def print_output(path):
    dataset = parse_CSV(path)
    for keyname in dataset:
        current = dataset[keyname]

        average = round(current["total"] / current["entries"], 2)

        print(f'{current["name"]} data:')
        print(f'Average value: {average:.2f}')
        print(f'Maximum value: {current["maximum"]:.2f}')
        print(f'Minimum value: {current["minimum"]:.2f}')
        print('----------------------------------------')

def output_to_json(path, writepath):
    dataset = parse_CSV(path)

    dumpdata = {}

    for keyname in dataset:
        current = dataset[keyname]

        average = round(current["total"] / current["entries"], 2)

        dumpdata[current["name"]] = {
            "average": average,
            "maximum": current["maximum"],
            "minimum": current["minimum"]
        }

    json_object = json.dumps(dumpdata, indent=4)

    with open(writepath, 'w') as outfile:
        outfile.write(json_object)

def output_to_xml(path, writepath): 
    dataset = parse_CSV(path)

    root = xml.Element('data')

    for keyname in dataset:
        current = dataset[keyname]

        col = xml.Element(current["name"])

        average = round(current["total"] / current["entries"], 2)

        colAverage = xml.SubElement(col, 'average')
        colAverage.text = str(average)

        colMax = xml.SubElement(col, 'maximum')
        colMax.text = str(current["maximum"])

        colMin = xml.SubElement(col, 'minimum')
        colMin.text = str(current["minimum"])

        root.append(col)

    xmlTree = xml.ElementTree(root)

    xml.indent(xmlTree, space=" ", level=0)

    with open(writepath, "wb") as outfile:
        xmlTree.write(outfile) 

        


filepath = './python/data.csv'
jsonpath = './python/data.json'
xmlpath = './python/data.xml'

print_output(filepath)
output_to_json(filepath, jsonpath)
output_to_xml(filepath, xmlpath)