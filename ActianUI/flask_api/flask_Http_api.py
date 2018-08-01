#!/usr/bin/env python3
from flask import Flask, jsonify, make_response
import sys
import os


#I have the below code so that no matter where i run this file 
#it will be able to import the correct files form the correct places
curdir = os.getcwd()
print('the cwd is: ' + curdir)
if (curdir == '/home/pi/Desktop/ActianUI/ActianUI/flask_api'):
    print('we at flask_api/')
    sys.path.insert(1, '../flightAnalysis/targetMatches_psql/')
    import store_TargetMatches as targetTb
    assert(os.getcwd() == curdir)
    sys.path.insert(1, '../flightAnalysis/fullReport_psql/')
    import videoTable_py3_access as videoTb
    assert(os.getcwd() == curdir)
elif (curdir == '/home/pi/Desktop/ActianUI/ActianUI'):
    print('we at home folder')
    sys.path.insert(1, './flightAnalysis/targetMatches_psql/')
    import store_TargetMatches as targetTb
    assert(os.getcwd() == curdir)
    sys.path.insert(1, './flightAnalysis/fullReport_psql/')
    import videoTable_py3_access as videoTb
    assert(os.getcwd() == curdir)
print(os.getcwd())



app = Flask(__name__)

@app.route('/api/Matches')
def get_matches():
    TableData = targetTb.select_all()
    assert(type(TableData) == dict)

    # ===========================================
    # this is where i tack on the encoded videos to the jSON dict i am returning
    # ===========================================
    TableData['encodedVideo'] = []  #initalizing a new element in the dict called encoded video that i will populate in loop
    for i in range(len(TableData['encodedImages'])):
        vids = videoTb.select_range(TableData['fixedRecords'][i][6], TableData['fixedRecords'][i][7])
        TableData['encodedVideo'].append(vids)
        
    jsonDict = jsonify(TableData)
    finalResponse = make_response(jsonDict)
    finalResponse.headers['Access-Control-Allow-Origin'] = '*'
    return(finalResponse)



@app.route('/api/fixedRecords')
def get_fixedRecords():
    records = targetTb.select_fixedRecords()
    recordDict = {'results': records}
    jsonDict = jsonify(recordDict)
    finalResponse = make_response(jsonDict)
    finalResponse.headers['Access-Control-Allow-Origin'] = '*'
    return(finalResponse)



@app.route('/api/imageData')
def get_imageData():
    TableData = targetTb.select_all()
    assert(type(TableData) == dict)
    jsonDict = jsonify(TableData)
    finalResponse = make_response(jsonDict)
    finalResponse.headers['Access-Control-Allow-Origin'] = '*'
    return(finalResponse)

#
#@app.route('/api/targetVideo')
#def get_VideoData():
#    vidBlobs = videoTb.get_videos()
#    vidDict = {'results': vidBlobs}
#    jsonDict = jsonify(vidDict)
#    finalResponse = make_response(jsonDict)
#    finalResponse.headers['Access-Control-Allow-Origin'] = '*'
#    return(finalResponse)


if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0')
    app.run(debug=True)
