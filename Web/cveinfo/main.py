from flask import Flask, request, jsonify, render_template, send_file
import json
from typing import ClassVar
import requests

app = Flask(__name__)

def getCVSSbyCVE(cveid: str):
    """
    Get cvss info by CVE-ID.
    Params:
    @ cveid - cve-id to get cvss.
    """
    try:
        json_response = json.loads(requests.get(f'http://services.nvd.nist.gov/rest/json/cve/1.0/{str(cveid)}').text)
            
        json_impacts = json_response['result']['CVE_Items'][0]['impact']
    
        if 'baseMetricV3' in json_impacts:
            cvss = str(json_impacts['baseMetricV3']['cvssV3']['baseScore'])

        elif 'baseMetricV2' in json_impacts:
            cvss = str(json_impacts['baseMetricV2']['cvssV2']['baseScore'])
    except:
        cvss = 0
    return cvss 

@app.route('/', methods=['GET'])
def index():   
    return render_template("index.html")

@app.route('/get_cvss/', methods=['GET'])
#CVE-2021-42013
def getcvss():   
    if request.args.get('cveid'):
        cveid = request.args.get('cveid')
        CVE = cveid
        if(cveid[0:3].lower() == 'cve'):
            cveid = cveid.replace("__import__","")
            cveid = cveid.replace("|","")
            cveid = cveid.replace('system',"")
            try:
                cvss = getCVSSbyCVE(cveid).strip('CVE-')
            except:
                cvss = cveid
            cvss = eval(cvss)
            return jsonify({"CVE":CVE, "CVSS":str(cvss)})
        else:
            return "error"
    else:   
        return "error"

@app.route('/download', methods=['GET', 'POST'])
def download():
    path = "./main.py"
    return send_file(path, as_attachment=True)


app.run(host='0.0.0.0', debug=False)