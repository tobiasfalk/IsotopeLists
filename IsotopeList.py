import requests
import csv
import time
from urllib.request import urlretrieve
import json

intensityCutOff = 10 # in %
apiTimeout = 5

def createJsonOutput(fileName ,isotopeList, radType = ["bm", "bp", "g", "e", "x"]):
    isotopeData = {}

    for isotope in isotopeList:
        print("Isotope:")
        print(isotope[0])
        print("energies:")
        print(isotope[1])
        
        energieList = []
        
        for energie in isotope[1]:
            if energie[0] in radType:
                energieList.append(float(energie[1]))
            
        print(energieList)
        
        isotopeData.update({isotope[0] : energieList})
        
        print(isotopeData)
        
        print("--------------------------------------------------------------------------------------------------------------------------------------------------")

    with open(fileName + '.json', 'w') as f:
        json.dump(isotopeData, f)

def formateIsotopeName(str):
    n = 0
    numbersList = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    numberStr = ""
    letterStr = ""
    while(str[n] in numbersList):
        numberStr = numberStr + str[n]
        n = n + 1
    return str[n:] + "-" + numberStr
        

def requestsGet(url):
    print(url)
    resp = False
    
    while True:
        try:
            response = requests.get(url, timeout=apiTimeout)
            print(response)
            resp = True
        except:
            print("An exception occurred") 
        
        if resp:
            break
    return response

def requestsGetPar(url, query_parameters):
    print(url)
    
    resp = False
    
    while True:
        try:
            response = requests.get(url, params=query_parameters, timeout=apiTimeout)
            print(response)
            resp = True
        except:
            print("An exception occurred") 
        
        if resp:
            break
    return response

def filter(fileName, nuclides, rad_types):
    
    # print(fileName)
    
    resultList = []
    
    with open(fileName) as csvfile:
        energyLevels = csv.reader(csvfile, delimiter= ",")
        header = next(energyLevels)
        if header != "0":
            for row in energyLevels:
                if len(row) > 0 and len(row[0]) > 0 and len(row[2]) > 0: #  and 
                    if float(row[2]) > intensityCutOff:
                        resultList.append([rad_types, row[0], row[2]])
                    
    return resultList

def getNuDAT(nuclides, rad_types):
    nudat_api_url = "http://www-nds.iaea.org/relnsd/v1/data?fields=decay_rads&nuclides=" + nuclides + "&rad_types=" + rad_types
                
    # print(nudat_api_url)
    
    query_parameters = {"downloadformat": "csv"}
    nudat_response = requestsGetPar(nudat_api_url, query_parameters)#requests.get(nudat_api_url, params=query_parameters, timeout=20)
    
    fileName = nuclides + "_" + rad_types + ".csv"
    
    with open(fileName, mode="wb") as file:
        file.write(nudat_response.content)

    # print(nudat_response)
    time.sleep(.1)
    
    return filter(fileName, nuclides, rad_types)

def getNuDATall(nuclides):
    
    resultList = []
    
    bm = getNuDAT(nuclides, "bm")
    bp = getNuDAT(nuclides, "bp")
    g = getNuDAT(nuclides, "g")
    # e = getNuDAT(nuclides, "e"))
    x = getNuDAT(nuclides, "x")
    
    if len(bm) > 0:
        resultList = resultList + bm
    if len(bp) > 0:
        resultList = resultList + bp
    if len(g) > 0:
        resultList = resultList + g
    # if len(e) > 0:
    #    resultList = resultList + e
    if len(x) > 0:
        resultList = resultList + x
        
            
    return [formateIsotopeName(nuclides), resultList]
    
    
    
traceNuk = [['H-3', [['bm', '5.6817', '100']]], ['Cs-135', [['bm', '75.7', '100'], ['g', '787.2', '99.7'], ['g', '846.1', '96']]], ['Fe-60', [['bm', '50.2', '100'], ['g', '6.93', '18.40876096933858'], ['x', '6.93', '18.40876096933858']]]] # []
synthNuk = [['Cs-131', [['g', '29.458', '21.059017649047863'], ['g', '29.778', '39.01262995377522'], ['g', '33.726', '11.309605499334086'], ['g', '34.03', '13.97867239717693'], ['x', '29.458', '21.059017649047863'], ['x', '29.778', '39.01262995377522'], ['x', '33.726', '11.309605499334086'], ['x', '34.03', '13.97867239717693']]], ['Cs-134', [['bm', '23.12', '27.27'], ['bm', '210.2', '70.17'], ['g', '127.502', '12.6'], ['g', '569.331', '15.373'], ['g', '604.721', '97.62'], ['g', '795.864', '85.46'], ['g', '4.749', '15.57077764788'], ['g', '30.973', '16.516202456847438'], ['x', '4.749', '15.57077764788'], ['x', '30.973', '16.516202456847438']]], ['Cs-134', [['bm', '23.12', '27.27'], ['bm', '210.2', '70.17'], ['g', '127.502', '12.6'], ['g', '569.331', '15.373'], ['g', '604.721', '97.62'], ['g', '795.864', '85.46'], ['g', '4.749', '15.57077764788'], ['g', '30.973', '16.516202456847438'], ['x', '4.749', '15.57077764788'], ['x', '30.973', '16.516202456847438']]], ['Cs-137', [['bm', '174.32', '94.7'], ['g', '661.657', '85.1']]], ['Fe-55', [['g', '5.899', '16.563801543845308'], ['x', '5.899', '16.563801543845308']]], ['Fe-59', [['bm', '80.94', '45.3'], ['bm', '149.21', '53.1'], ['g', 
'1099.245', '56.5'], ['g', '1291.59', '43.2']]]] # []
below10P = []
above10P = []

with open("elements.txt") as csvfile:
    elements = csv.reader(csvfile, delimiter= ",")
    
    types = ['trace', 'synth', '0.25%', '0.187%', '100%', '0.02%', '100.0%', '0.005%', '0.720%', '99.3%']
    
    for row in elements:
        print("--------------------------------------------------------------------------------------------------------------------------------------------------")
        print(row[0])
        print("--------------------------------------------------------------------------------------------------------------------------------------------------")

        wiki_api_url = "https://www.wikitable2json.com/api/" + row[0]# + "?table=2"
        
        # print(wiki_api_url)
        
        wiki_response = requestsGet(wiki_api_url)#requests.get(wiki_api_url)

        # print(wiki_response)
        # print(wiki_response.json())
        
        for table in wiki_response.json():
            # print("--------------------------------------------------------------------------------------------------------------------------------------------------")
            # print("table:")
            # print(table)
        
            if "Main isotopes" in table[0][0]:
            
                for tableRow in table:
                    if not ("stable" in tableRow[2]) and not ("half-life (t1/2)" in tableRow[2]) and not ("Main isotopes" in tableRow[2]):
                        print("-----------------------------------------------------------------------------")
                        print("Row:")
                        print(tableRow)
                        
                        data = getNuDATall(tableRow[0])
                        print(data)
                        
                        if len(data[1]) > 0:
                        
                            if tableRow[1] == 'trace':
                                traceNuk.append(data)
                            elif tableRow[1] == 'synth':
                                synthNuk.append(data)
                            elif "%" in tableRow[1]:
                                amountP = float(tableRow[1].replace("%", ""))
                                if amountP < 10:
                                    below10P.append(data)
                                else:
                                    above10P.append(data)
                        
                        
        print("--------------------------------------------------------------------------------------------------------------------------------------------------")   
        print("--------------------------------------------------------------------------------------------------------------------------------------------------") 
        print(traceNuk)
        print("--------------------------------------------------------------------------------------------------------------------------------------------------") 
        print(synthNuk)
        print("--------------------------------------------------------------------------------------------------------------------------------------------------") 
        print(below10P)
        print("--------------------------------------------------------------------------------------------------------------------------------------------------") 
        print(above10P)
        print("--------------------------------------------------------------------------------------------------------------------------------------------------")
        print("--------------------------------------------------------------------------------------------------------------------------------------------------") 
        
        time.sleep(.1)  # import time
    print("--------------------------------------------------------------------------------------------------------------------------------------------------")
    print("--------------------------------------------------------------------------------------------------------------------------------------------------")
    print("--------------------------------------------------------------------------------------------------------------------------------------------------")
    print("Collection Done") 
    print("--------------------------------------------------------------------------------------------------------------------------------------------------") 
    print("--------------------------------------------------------------------------------------------------------------------------------------------------")
    print("--------------------------------------------------------------------------------------------------------------------------------------------------")




createJsonOutput("all_Isotopes_NuDAT", traceNuk + synthNuk + below10P + above10P)
createJsonOutput("natural_Isotopes_NuDAT", traceNuk + below10P + above10P)
createJsonOutput("trace_Isotopes_NuDAT", traceNuk)
createJsonOutput("synth_Isotopes_NuDAT", synthNuk)
createJsonOutput("below10P_Isotopes_NuDAT", below10P)
createJsonOutput("above10P_Isotopes_NuDAT", above10P)
