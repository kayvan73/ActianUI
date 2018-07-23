#!/usr/bin/env python3
from flask import Flask, jsonify, make_response
import sys
import os
sys.path.insert(0, '../dataCollection/py3_data')
#import targetTable_py2_access as targetTb
import targetTable_py3_access as targetTb



app = Flask(__name__)

@app.route('/api/targetMatches')
def get_targetData():
    Data = targetTb.select_all()
    Data_dict = {'results': Data}
    jsonDict = jsonify(Data_dict)
    finalResponse = make_response(jsonDict)
    finalResponse.headers['Access-Control-Allow-Origin'] = '*'
    return(finalResponse)


#def get_imageFromPsql():
#   imageArray = btrieve2.select_all_targetImages()
#   nonBytes = []
#   for i in range(len(imageArray)):
#      nonBytes.append(imageArray[i][2].decode('UTF-8'))
#   print(nonBytes)
#   return (nonBytes)


#@app.route('/api/allData')
#def get_targetData():
#    allData = btrieve2.select_all_targetData()
#    allData_dict = {'results': allData}
#    jsonDict = jsonify(allData_dict)
#    finalResponse = make_response(jsonDict)
#    finalResponse.headers['Access-Control-Allow-Origin'] = '*'
#    return(finalResponse)
#
	
#@app.route('/api/images')
#def imageReturn():
#   imageLocations = get_imageFromPsql()
#   imageDict = {'result': imageLocations}
#   #for i in range(len(imageLocations)):
#   #   imageDict[str[i]] = imageLocations[i]
#   return (jsonify(imageDict))
#       
#
#@app.route('/api/coordinates')
#def hello():
#    coordArray = btrieve2.select_all_targetGPS()
#    coordsDict = {'results': coordArray}
#    return(jsonify(coordsDict))

if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0')
    app.run(debug=True)
