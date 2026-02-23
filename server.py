from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def f_dataref(name):
  r0 = requests.get("http://localhost:8086/api/v2/datarefs").json()
  for e in r0["data"]:
    if (e.get("name") == name):
      return e.get("id")

@app.route('/hello', methods=['GET'])
def hello():
  return "hello"

@app.route('/flt-rwy/<apt>/<rwy>', methods=['GET'])
def fltch(apt, rwy):
  dt = {
    "runway_start": {
      "airport_id": apt,
      "runway": rwy
    },
    "aircraft": {
      "path": "Aircraft/Laminar Research/Cessna 172 SP/Cessna_172SP.acf",
      "livery": "default"
    }
  }
  r = requests.post('http://localhost:8086/api/v3/flight', json=dt)
  print("Flight set response " + str(r.status_code))
  print("Flight set response JSON " + str(r.json()))
  return "done"

@app.route('/flt-air/<lat>/<lon>/<m>/<ms>/<hdg>', methods=['GET'])
def fltair(lat, lon, m, ms, hdg):
  dt = {
    "lle_air_start": {
      "latitude": float(lat),
      "longitude": float(lon),
      "elevation_in_meters": float(m),
      "heading_true": float(hdg),
      "speed_in_meters_per_second": float(ms)
    },
    "aircraft": {
      "path": "Aircraft/Laminar Research/Cessna 172 SP/Cessna_172SP.acf",
      "livery": "default"
    }
  }
  r = requests.post('http://localhost:8086/api/v3/flight', json=dt)
  print("Flight in air rsp " + str(r.status_code))
  print("Flight in air JSON " + str(r.json()))
  return "done"

@app.route('/dr/<path:dataref>', methods=['GET'])
def rollrat(dataref):
  drnum = f_dataref(dataref)
  drval = requests.get(f"http://localhost:8086/api/v2/datarefs/{drnum}/value").json()
  return jsonify({"data": drval})

@app.route('/set/<val>/<path:dr>', methods=['GET'])
def setdr(val, dr):
  try:
    val = int(val)
  except ValueError:
    val = float(val)
  drnum = f_dataref(dr)
  url = "http://localhost:8086/api/v2/datarefs/" + str(drnum) + "/value"
  prms = { "data": val }
  requests.patch(url, json=prms)
  return "done"

@app.route('/sim-pause', methods=['GET'])
def sim_pause():
  r = requests.get('http://localhost:8086/api/v2/commands').json()
  for e in r["data"]:
    if (e.get("name") == "sim/operation/pause_toggle"):
      dt = { "duration": 0 }
      r1 = requests.post('http://localhost:8086/api/v2/command/' + str(e.get("id")) + '/activate', json=dt)
      print("Pause returned code " + str(r1.status_code))
      print("Pause returned " + str(r1.json()))
      break
  return "it has been done"

@app.route('/time/<doy>/<wch>/<tme>', methods=['GET'])
def tmeset(doy, wch, tme):
  tme = float(tme)
  doy = int(doy)
  if (wch == "L"):
    dt = {
      "data": {
        "local_time": {
          "day_of_year": doy,
          "time_in_24_hours": tme
        }
      }
    }
    rL = requests.patch('http://localhost:8086/api/v3/flight', json=dt)
    print("Timeset code " + str(rL.status_code))
    print("Timeset JSON " + str(rL.json()))
  elif (wch == "Z"):
    dt = {
      "data": {
        "gmt_time": {
          "day_of_year": doy,
          "time_in_24_hours": tme
        }
      }
    }
    rZ = requests.patch('http://localhost:8086/api/v3/flight', json=dt)
    print("TimesetZ code " + str(rZ.status_code))
    print("TimesetZ JSON " + str(rZ.json()))
  return "done"

app.run(host='0.0.0.0', port=6741)