"""
CISCO SAMPLE CODE LICENSE
                                  Version 1.1
                Copyright (c) 2020 Cisco and/or its affiliates

   These terms govern this Cisco Systems, Inc. ("Cisco"), example or demo
   source code and its associated documentation (together, the "Sample
   Code"). By downloading, copying, modifying, compiling, or redistributing
   the Sample Code, you accept and agree to be bound by the following terms
   and conditions (the "License"). If you are accepting the License on
   behalf of an entity, you represent that you have the authority to do so
   (either you or the entity, "you"). Sample Code is not supported by Cisco
   TAC and is not tested for quality or performance. This is your only
   license to the Sample Code and all rights not expressly granted are
   reserved.

   1. LICENSE GRANT: Subject to the terms and conditions of this License,
      Cisco hereby grants to you a perpetual, worldwide, non-exclusive, non-
      transferable, non-sublicensable, royalty-free license to copy and
      modify the Sample Code in source code form, and compile and
      redistribute the Sample Code in binary/object code or other executable
      forms, in whole or in part, solely for use with Cisco products and
      services. For interpreted languages like Java and Python, the
      executable form of the software may include source code and
      compilation is not required.

   2. CONDITIONS: You shall not use the Sample Code independent of, or to
      replicate or compete with, a Cisco product or service. Cisco products
      and services are licensed under their own separate terms and you shall
      not use the Sample Code in any way that violates or is inconsistent
      with those terms (for more information, please visit:
      www.cisco.com/go/terms).

   3. OWNERSHIP: Cisco retains sole and exclusive ownership of the Sample
      Code, including all intellectual property rights therein, except with
      respect to any third-party material that may be used in or by the
      Sample Code. Any such third-party material is licensed under its own
      separate terms (such as an open source license) and all use must be in
      full accordance with the applicable license. This License does not
      grant you permission to use any trade names, trademarks, service
      marks, or product names of Cisco. If you provide any feedback to Cisco
      regarding the Sample Code, you agree that Cisco, its partners, and its
      customers shall be free to use and incorporate such feedback into the
      Sample Code, and Cisco products and services, for any purpose, and
      without restriction, payment, or additional consideration of any kind.
      If you initiate or participate in any litigation against Cisco, its
      partners, or its customers (including cross-claims and counter-claims)
      alleging that the Sample Code and/or its use infringe any patent,
      copyright, or other intellectual property right, then all rights
      granted to you under this License shall terminate immediately without
      notice.

   4. LIMITATION OF LIABILITY: CISCO SHALL HAVE NO LIABILITY IN CONNECTION
      WITH OR RELATING TO THIS LICENSE OR USE OF THE SAMPLE CODE, FOR
      DAMAGES OF ANY KIND, INCLUDING BUT NOT LIMITED TO DIRECT, INCIDENTAL,
      AND CONSEQUENTIAL DAMAGES, OR FOR ANY LOSS OF USE, DATA, INFORMATION,
      PROFITS, BUSINESS, OR GOODWILL, HOWEVER CAUSED, EVEN IF ADVISED OF THE
      POSSIBILITY OF SUCH DAMAGES.

   5. DISCLAIMER OF WARRANTY: SAMPLE CODE IS INTENDED FOR EXAMPLE PURPOSES
      ONLY AND IS PROVIDED BY CISCO "AS IS" WITH ALL FAULTS AND WITHOUT
      WARRANTY OR SUPPORT OF ANY KIND. TO THE MAXIMUM EXTENT PERMITTED BY
      LAW, ALL EXPRESS AND IMPLIED CONDITIONS, REPRESENTATIONS, AND
      WARRANTIES INCLUDING, WITHOUT LIMITATION, ANY IMPLIED WARRANTY OR
      CONDITION OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-
      INFRINGEMENT, SATISFACTORY QUALITY, NON-INTERFERENCE, AND ACCURACY,
      ARE HEREBY EXCLUDED AND EXPRESSLY DISCLAIMED BY CISCO. CISCO DOES NOT
      WARRANT THAT THE SAMPLE CODE IS SUITABLE FOR PRODUCTION OR COMMERCIAL
      USE, WILL OPERATE PROPERLY, IS ACCURATE OR COMPLETE, OR IS WITHOUT
      ERROR OR DEFECT.

   6. GENERAL: This License shall be governed by and interpreted in
      accordance with the laws of the State of California, excluding its
      conflict of laws provisions. You agree to comply with all applicable
      United States export laws, rules, and regulations. If any provision of
      this License is judged illegal, invalid, or otherwise unenforceable,
      that provision shall be severed and the rest of the License shall
      remain in full force and effect. No failure by Cisco to enforce any of
      its rights related to the Sample Code or to a breach of this License
      in a particular situation will act as a waiver of such rights. In the
      event of any inconsistencies with any other terms, this License shall
      take precedence.
"""

import logging
from meraki.config import MERAKI_PYTHON_SDK_CALLER
import requests, time, os, meraki, json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from flask import Flask, request, render_template, redirect
import threading
from dotenv import load_dotenv

app = Flask(__name__)

MERAKI_BASE_URL = "http://api.meraki.com/api/v1/"
WEBEX_BASE_URL = "https://webexapis.com/v1/"

def getJson(filename):
    with open(filename, "r") as f:
        return json.load(f)

def writeJson(content, filename):
    with open(filename, "w") as f:
        return json.dump(content, f, indent=2)

# Landing page
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

# Make and send a snapshot
@app.route('/snapshot', methods=["GET", "POST"])
def snapshot():
    settings = getJson("settings.json")
    f = take_snapshot(settings['CAMERA_SERIAL'])
    send_snapshot(f)
    return render_template('index.html')

# Settings: start
@app.route('/settings', methods=["GET", "POST"])
def settings():
    return render_template('settings.html', stage="key", 
    selected_elements={ 
        "organization" : ""
    }, cameras = [{ 
        "name" : "test", "id" : "xyz"
    }], sensors = [{ 
        "name" : "test", "id" : "xyz" 
    }])

# Settings: API keys
@app.route('/settings2', methods=["GET", "POST"])
def settings2():
    key = request.form.get('apikey')
    botkey = request.form.get('botkey')
    email = request.form.get('email')
    webhook = request.form.get('webhook')
    settings = getJson("settings.json")
    settings["MERAKI_API_KEY"] = key
    settings["BOT_API_KEY"] = botkey
    settings["WEBEX_EMAIL"] = email
    settings["WEBHOOK"] = webhook
    writeJson(settings, "settings.json")

    return render_template('settings.html', stage="org", dropdown_content=get_dropdown_content(), selected_elements={
        "organization" : ""
    }, cameras = [{
        "name" : "test", "id" : "xyz"
    }], sensors = [{
        "name" : "test", "id" : "xyz"
    }])

# Settings: Organization and network
@app.route('/settings3', methods=["GET", "POST"])
def settings3():
    org = request.form.get('organization')
    network = request.form.get('network')
    settings = getJson("settings.json")
    settings['NETWORK'] = network
    writeJson(settings, "settings.json")

    content = get_cameras_and_sensors(network)
    
    return render_template('settings.html', stage="cam", dropdown_content=get_dropdown_content(), selected_elements={
        "organization" : org,
        "network_id" : network
    }, cameras = content[0], sensors = content[1])

# Settings: Camera and sensor
@app.route('/settings4', methods=["GET", "POST"])
def settings4():
    camera = request.form.get('camera')
    sensor = request.form.get('sensor')
    settings = getJson("settings.json")
    settings["CAMERA_SERIAL"] = camera
    settings["SENSOR_SERIAL"] = sensor
    writeJson(settings, "settings.json")
    post_webhook(settings['NETWORK'], f"{settings['WEBHOOK']}/fridge")
    return redirect('/')

# Retrieve cameras and sensors in selected network
def get_cameras_and_sensors(network):
    settings = getJson("settings.json")
    merakiAPI = meraki.DashboardAPI(api_key=settings['MERAKI_API_KEY'], suppress_logging=True)
    devices = merakiAPI.networks.getNetworkDevices(network)

    cameras = []
    sensors = []
    for device in devices:
        if "MV" in device['model']:
            cameras += [{
                "id" : device['serial'],
                "name" : device['name']
            }]
        elif "MT" in device['model']:
            sensors += [{
                "id" : device['serial'],
                "name" : device['name']
            }]
    return [cameras, sensors]

# Webhook for fridge open/close
@app.route('/fridge', methods=["GET", "POST"])
def on_open_fridge():
    payload = request.get_json()
    print("Got webhook : " + json.dumps(payload))
    t = threading.Thread(target=fridge_opening_thread, args=(payload,))
    t.start()
    return "ok"

# Thread fired at webhook trigger
def fridge_opening_thread(payload):
    # Check if door opened
    settings = getJson("settings.json")
    try:
        if payload['alertData']['triggerData'][0]['trigger']['type'] == 'door' and payload['deviceSerial'] == settings["SENSOR_SERIAL"]:
            if payload['alertData']['triggerData'][0]['trigger']['sensorValue'] == 1.0: 
                # Send message to Webex space
                m = MultipartEncoder({'toPersonEmail': settings['WEBEX_EMAIL'],
                                'text': 'The fridge was opened. A snapshot will be sent later.',})
                resp = requests.post(f'{WEBEX_BASE_URL}messages', data=m,
                                headers={'Authorization': f"Bearer {settings['BOT_API_KEY']}",
                                'Content-Type': m.content_type})
                print(resp.text)

                # Send snapshot to Webex space
                f = take_snapshot(settings['CAMERA_SERIAL'])
                send_snapshot(f)
    except Exception as exc:
        print(exc)

    return "ok"

# Post webhook for sensor
def post_webhook(networkId, webhook):
    settings = getJson("settings.json")
    WEBHOOK_NAME = "Meraki Sensor Snapshot Trigger"
    
    url = f"{MERAKI_BASE_URL}networks/{networkId}/webhooks/httpServers"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": settings['MERAKI_API_KEY']
    }

    # Check if webhook already exists
    webhooks = requests.get(url, headers=headers).json()
    for w in webhooks:
        if w['url'] == webhook:
            return
    
    # Post webhook
    body = """
    {
        "name": """ + WEBHOOK_NAME + """,
        "url": """ + webhook + """,
        "sharedSecret": "shh",
        "payloadTemplate": {
            "payloadTemplateId": "wpt_00001"
        }
    }
    """

    resp = requests.request("POST", url, data=body, headers=headers)
    resp.raise_for_status()

# Trigger MV snapshot, returns filename
def take_snapshot(serial):
    settings = getJson("settings.json")
    dashboard = meraki.DashboardAPI(settings['MERAKI_API_KEY'])

    try:    
        response = dashboard.camera.generateDeviceCameraSnapshot(
            serial
        )
        print(response)
    except Exception as exc:
        # Return last snapshot
        return "snapshot.png"

    # Save the snapshot
    url = response['url']
    resp = requests.get(url, verify=False)
    with open("snapshot.png", "wb") as f:
        while resp.status_code != 200:
            time.sleep(2)
            resp = requests.get(url, verify=False)
            print(resp.status_code)
        f.write(resp.content)
        f.close()
    
    return "snapshot.png"

# Send snapshot to Webex Teams space
def send_snapshot(filename):
    print("sending message...")
    settings = getJson("settings.json")
    m = MultipartEncoder({'toPersonEmail':settings['WEBEX_EMAIL'],
                      'text': 'You look gorgeous today!',
                      'files': (filename, open(filename, 'rb'),
                      'image/png')})

    resp = requests.post(f'{WEBEX_BASE_URL}messages', data=m,
                    headers={'Authorization': f"Bearer {settings['BOT_API_KEY']}",
                    'Content-Type': m.content_type})
    
    print(resp.text)

# Get list of organizations and networks
def get_dropdown_content():
    settings = getJson("settings.json")
    merakiAPI = meraki.DashboardAPI(api_key=settings['MERAKI_API_KEY'], suppress_logging=True)
    orgs = merakiAPI.organizations.getOrganizations()
    dropdown_content = []
    for org in orgs:
        temp1 = {}
        temp1['orgaid'] = org['id']
        temp1['organame'] = org['name']
        networks = merakiAPI.organizations.getOrganizationNetworks(org['id'])
        temp1['networks'] = []
        for network in networks:
            temp2 = {}
            temp2['networkid'] = network['id']
            temp2['networkname'] = network['name']
            temp1['networks'].append(temp2)
        dropdown_content.append(temp1)  
    return dropdown_content

if __name__ == "__main__":
    app.run(port=6161)