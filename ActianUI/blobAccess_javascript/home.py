#!/usr/bin/env python
from flask import Flask, jsonify, make_response, Response, json
import base64
import imageio
import sys
import os

app = Flask(__name__)

#@app.route('/api/targetMatches')
#def get_targetData():
#    Data = targetTb.select_all()
#    Data_dict = {'results': Data}
#    jsonDict = jsonify(Data_dict)
#    finalResponse = make_response(jsonDict)
#    finalResponse.headers['Access-Control-Allow-Origin'] = '*'
#    return(finalResponse)

#encode:  string=>encoded_bytes
#decode:  bytes_encode => string 

@app.route('/api/imgBytes')
def get_imageByte():
    im = open('../../../foo2.jpg', 'rb')
    imData = im.read()
    print(type(imData))
    #print('making string')
    #encoded = base64.b64encode(imData)
    #print(type(encoded))
    data = []
    data.append('welcome to Kavons api')
    #data.append(encoded)
    data.append(imData)
    #apiFriendly = str(imData) 
    imDict = {'results': data}

    # ========================
    # this is one method of returning the dictionary
    #return Response(json.dumps(imDict), mimetype='application/json')
    # ========================
    
    # =====================
    jsonDict = jsonify(imDict)
    finalResponse = make_response(jsonDict)
    finalResponse.headers['Access-Control-Allow-Origin'] = '*'
    return(finalResponse)
    # ========================
    


if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0')
    app.run(debug=True)
