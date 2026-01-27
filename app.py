import random
import requests
import ssl
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

## API credentials (recommend setting these via environment variables)
WIGLE_API_NAME = os.environ.get("WIGLE_API_NAME", "")
WIGLE_API_TOKEN = os.environ.get("WIGLE_API_TOKEN", "")
OPENCELLID_API_KEY = os.environ.get("OPENCELLID_API_KEY", "")
SHODAN_API_KEY = os.environ.get("SHODAN_API_KEY", "")


# Dummy data for testing
DUMMY_DATA = [
    {
        "lat": 51.505,
        "lon": -0.09,
        "ssid": "TestWiFi",
        "bssid": "00:14:22:01:23:45",
        "vendor": "Generic",
        "signal": -65,
        "accuracy": 50,
        "timestamp": "2025-04-11T10:00:00Z",
        "type": "router"
    },
    {
        "lat": 51.506,
        "lon": -0.088,
        "cell_id": "123456789",
        "vendor": "N/A",
        "signal": -70,
        "accuracy": 100,
        "timestamp": "2025-04-11T10:01:00Z",
        "type": "cell_tower"
    },
    {
        "lat": 51.504,
        "lon": -0.091,
        "ip": "192.168.1.100",
        "vendor": "CameraCorp",
        "type": "camera"
    }
]

@app.route('/map-w')
def wifi_map():
    return render_template('wifi-search.html')

def classify_device(name, original_type):
    if not name:
        return original_type
    name_upper = name.upper()
    if any(k in name_upper for k in ["CAR", "FORD", "TOYOTA", "BMW", "TESLA", "SYNC", "MAZDA", "HONDA", "UCONNECT", "HYUNDAI", "LEXUS", "NISSAN"]):
        return "car"
    if any(k in name_upper for k in ["TV", "BRAVIA", "VIZIO", "SAMSUNG", "LG", "ROKU", "FIRE", "SMARTVIEW", "KDL-"]):
        return "tv"
    if any(k in name_upper for k in ["HEADPHONE", "EARBUD", "BOSE", "SONY", "BEATS", "AUDIO", "AIRPOD", "JBL", "SENNHEISER"]):
        return "headphone"
    if any(k in name_upper for k in ["DASHCAM", "DASH CAM", "DVR", "70MAI", "VIOFO", "GARMIN DASH"]):
        return "dashcam"
    if any(k in name_upper for k in ["CAM", "SURVEILLANCE", "SECURITY", "NEST", "RING", "ARLO", "HIKVISION", "DAHUA", "REOLINK"]):
        return "camera"
    if any(k in name_upper for k in ["WATCH", "FITBIT", "GARMIN", "WHOOP"]):
        return "iot"
    return original_type

@app.route('/nearby')
def nearby():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    mode = request.args.get('mode', 'wifi') # 'wifi' or 'bluetooth'
    
    if not lat or not lon:
        return jsonify({"error": "Missing coordinates"}), 400

    devices = []
    
    if mode == 'bluetooth':
        # Wigle Bluetooth API call
        try:
            wigle_response = requests.get(
                'https://api.wigle.net/api/v2/bluetooth/search',
                params={'latrange1': lat-0.01, 'latrange2': lat+0.01, 'longrange1': lon-0.01, 'longrange2': lon+0.01},
                auth=(WIGLE_API_NAME, WIGLE_API_TOKEN)
            )
            if wigle_response.status_code == 200:
                for device in wigle_response.json().get('results', []):
                    name = device.get('name') or device.get('netid')
                    original_type = "bluetooth"
                    classified_type = classify_device(name, original_type)
                    
                    devices.append({
                        "lat": device.get('trilat'),
                        "lon": device.get('trilong'),
                        "ssid": name,
                        "bssid": device.get('netid'),
                        "vendor": device.get('type') or ("Bluetooth Node" if classified_type == "bluetooth" else classified_type.replace('_', ' ').title()),
                        "signal": device.get('level'),
                        "timestamp": device.get('lastupdt'),
                        "type": classified_type
                    })
            else:
                print(f"Wigle BT error: {wigle_response.status_code} - {wigle_response.text}")
        except Exception as e:
            print(f"Wigle BT exception: {str(e)}")
    else:
        # Standard WiFi/Cell/IoT Logic
        # Wigle API call
        try:
            wigle_response = requests.get(
                'https://api.wigle.net/api/v2/network/search',
                params={'latrange1': lat-0.01, 'latrange2': lat+0.01, 'longrange1': lon-0.01, 'longrange2': lon+0.01},
                auth=(WIGLE_API_NAME, WIGLE_API_TOKEN)
            )
            if wigle_response.status_code == 200:
                for network in wigle_response.json().get('results', []):
                    name = network.get('ssid')
                    original_type = "router"
                    classified_type = classify_device(name, original_type)

                    devices.append({
                        "lat": network.get('trilat'),
                        "lon": network.get('trilong'),
                        "ssid": name,
                        "bssid": network.get('netid'),
                        "vendor": network.get('vendor'),
                        "signal": network.get('level'),
                        "timestamp": network.get('lastupdt'),
                        "type": classified_type
                    })
            else:
                print(f"Wigle error: {wigle_response.status_code} - {wigle_response.text}")
        except Exception as e:
            print(f"Wigle exception: {str(e)}")

        # OpenCellID API call
        try:
            opencell_response = requests.get(
                'https://us1.unwiredlabs.com/v2/process.php',
                json={
                    "token": OPENCELLID_API_KEY,
                    "lat": lat,
                    "lon": lon,
                    "address": 0
                }
            )
            if opencell_response.status_code == 200:
                data = opencell_response.json()
                if data.get('status') == 'ok':
                    for cell in data.get('cells', []):
                        devices.append({
                            "lat": cell.get('lat'),
                            "lon": cell.get('lon'),
                            "cell_id": str(cell.get('cellid')),
                            "signal": cell.get('signal'),
                            "accuracy": cell.get('accuracy'),
                            "timestamp": cell.get('updated'),
                            "type": "cell_tower"
                        })
                else:
                    print(f"OpenCellID API error: {data.get('message', 'Unknown error')}")
            else:
                print(f"OpenCellID HTTP error: {opencell_response.status_code} - {opencell_response.text}")
        except Exception as e:
            print(f"OpenCellID exception: {str(e)}")

        # Shodan API call
        if SHODAN_API_KEY:
            try:
                shodan_response = requests.get(
                    'https://api.shodan.io/shodan/host/search',
                    params={'key': SHODAN_API_KEY, 'query': f'geo:{lat},{lon},1', 'limit': 5}
                )
                if shodan_response.status_code == 200:
                    for banner in shodan_response.json().get('matches', []):
                        ip = banner['ip_str']
                        info = banner.get('data', '')
                        classified_type = classify_device(info, "iot_device")

                        devices.append({
                            "lat": banner['location']['latitude'],
                            "lon": banner['location']['longitude'],
                            "ip": ip,
                            "info": info[:50],
                            "type": classified_type
                        })
            except Exception as e:
                print(f"Shodan exception: {str(e)}")

    # Fallback to dummy data if no results
    if not devices:
        print(f"Using dummy data fallback for {mode}")
        if mode == 'bluetooth':
            devices = [
                {"lat": lat + random.uniform(-0.002, 0.002), "lon": lon + random.uniform(-0.002, 0.002), "ssid": "Tesla Model 3", "type": "car", "vendor": "Tesla Motors"},
                {"lat": lat + random.uniform(-0.002, 0.002), "lon": lon + random.uniform(-0.002, 0.002), "ssid": "Sony WH-1000XM4", "type": "headphone", "vendor": "Sony Corp."},
                {"lat": lat + random.uniform(-0.002, 0.002), "lon": lon + random.uniform(-0.002, 0.002), "ssid": "Samsung QLED 75", "type": "tv", "vendor": "Samsung Electronics"},
                {"lat": lat + random.uniform(-0.002, 0.002), "lon": lon + random.uniform(-0.002, 0.002), "ssid": "Hidden_BT_Tracker", "type": "bluetooth", "vendor": "Unknown"}
            ]
        else:
            devices = [
                {"lat": lat + random.uniform(-0.001, 0.001), "lon": lon + random.uniform(-0.001, 0.001), "ssid": "CYBER_SURVEILLANCE_ROUTER", "type": "router", "vendor": "Cisco Systems"},
                {"lat": lat + random.uniform(-0.001, 0.001), "lon": lon + random.uniform(-0.001, 0.001), "ssid": "DASHCAM_V3", "type": "camera", "vendor": "Nextbase"},
                {"lat": lat + random.uniform(-0.001, 0.001), "lon": lon + random.uniform(-0.001, 0.001), "ssid": "5G_TOWER_B4", "type": "cell_tower", "vendor": "Ericsson"}
            ]

    return jsonify({"devices": devices})

@app.route('/api/geo/towers')
def get_towers():
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        
        if not lat or not lon:
            lat = 51.505
            lon = -0.09

        # Calculate Bounding Box (approx 5-10km radius)
        # 1 deg lat ~= 111km. 0.05 ~= 5.5km
        min_lat = lat - 0.05
        max_lat = lat + 0.05
        min_lon = lon - 0.05
        max_lon = lon + 0.05
        bbox = f"{min_lat},{min_lon},{max_lat},{max_lon}"

        # Using OpenCellID 'getInArea' API
        # Note: 'pk' tokens are typically UnwiredLabs, but user requested opencellid.org.
        # If the key is cross-compatible or this is the intended endpoint:
        response = requests.get(
            'http://opencellid.org/cell/getInArea',
            params={
                "key": OPENCELLID_API_KEY,
                "BBOX": bbox,
                "format": "json"
            }
        )
        
        if response.status_code == 200:
            # API might return JSON if format=json is supported and valid
            try:
                data = response.json()
            except:
                # Fallback if text/csv
                return jsonify({"error": "API returned non-JSON", "details": response.text[:100]})

            towers = []
            # OpenCellID usually returns { "cells": [ ... ] } or just a list?
            # Adjusting parsing based on common OpenCellID formatting
            cells = data.get('cells', []) if isinstance(data, dict) else data
            
            if isinstance(cells, list):
                for cell in cells:
                    towers.append({
                        "id": str(cell.get('cellid', 'Unknown')),
                        "lat": float(cell.get('lat')),
                        "lon": float(cell.get('lon')),
                        "lac": cell.get('lac', 0),
                        "mcc": cell.get('mcc', 0),
                        "mnc": cell.get('mnc', 0),
                        "signal": cell.get('signal', 0), # Often not present in static DB
                        "radio": cell.get('radio', 'gsm')
                    })
            
            return jsonify(towers)
            
        else:
            return jsonify({"error": f"Upstream API error: {response.status_code}", "details": response.text[:100]}), 502

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/geo/celltower')
def get_celltower_click():
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        
        if not lat or not lon:
            return jsonify({"error": "Missing coordinates"}), 400

        # Small BBOX for specific location (approx 2km radius)
        # BBOX format for OpenCellID ajax: min_lon,min_lat,max_lon,max_lat
        min_lat = lat - 0.01
        max_lat = lat + 0.01
        min_lon = lon - 0.01
        max_lon = lon + 0.01
        bbox = f"{min_lon},{min_lat},{max_lon},{max_lat}"

        # Using the endpoint provided by user
        # This appears to be an internal/public web endpoint
        response = requests.get(
            'https://www.opencellid.org/ajax/getCells.php',
            params={
                "bbox": bbox
                # API Key might not be needed for this specific AJAX endpoint, 
                # or it uses cookies/referer. We try without first as per user URL.
            }
        )
        
        if response.status_code == 200:
            try:
                data = response.json()
            except:
                return jsonify({"error": "API returned non-JSON", "details": response.text[:100]})

            towers = []
            
            # The AJAX endpoint returns GeoJSON: { "type": "FeatureCollection", "features": [ ... ] }
            features = data.get('features', []) if isinstance(data, dict) else []
            
            for feature in features:
                props = feature.get('properties', {})
                geom = feature.get('geometry', {})
                coords = geom.get('coordinates', [0, 0]) # [lon, lat]
                
                # Note: 'cellid' might be missing in this public aggregate view
                # Mapping: mcc=mcc, net=mnc, area=lac/tac
                towers.append({
                    "id": str(props.get('cellid', props.get('unit', 'Unknown'))),
                    "lat": float(coords[1]),
                    "lon": float(coords[0]),
                    "lac": props.get('area', 0),
                    "mcc": props.get('mcc', 0),
                    "mnc": props.get('net', 0),
                    "signal": props.get('samples', 0), # Using samples as proxy for 'strength/reliability'
                    "radio": props.get('radio', 'gsm')
                })
            
            return jsonify(towers)
        else:
            return jsonify({"error": f"Upstream API error: {response.status_code}", "details": response.text[:100]}), 502

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route('/searchzz')
def search():
    search_type = request.args.get('type')
    query = request.args.get('query')
    if not search_type or not query:
        return jsonify({"error": "Missing search parameters"}), 400

    devices = []

    if search_type == 'location':
        try:
            lat, lon = map(float, query.split(','))
            # Wigle API call
            try:
                wigle_response = requests.get(
                    'https://api.wigle.net/api/v2/network/search',
                    params={'latrange1': lat-0.01, 'latrange2': lat+0.01, 'longrange1': lon-0.01, 'longrange2': lon+0.01},
                    auth=(WIGLE_API_NAME, WIGLE_API_TOKEN)
                )
                if wigle_response.status_code == 200:
                    for network in wigle_response.json().get('results', []):
                        devices.append({
                            "lat": network.get('trilat'),
                            "lon": network.get('trilong'),
                            "ssid": network.get('ssid'),
                            "bssid": network.get('netid'),
                            "vendor": network.get('vendor'),
                            "signal": network.get('level'),
                            "timestamp": network.get('lastupdt'),
                            "type": "router"
                        })
                else:
                    print(f"Wigle location error: {wigle_response.status_code} - {wigle_response.text}")
            except Exception as e:
                print(f"Wigle location exception: {str(e)}")

            # OpenCellID API call
            try:
                opencell_response = requests.get(
                    'https://us1.unwiredlabs.com/v2/process.php',
                    json={
                        "token": OPENCELLID_API_KEY,
                        "lat": lat,
                        "lon": lon,
                        "address": 0
                    }
                )
                if opencell_response.status_code == 200:
                    data = opencell_response.json()
                    if data.get('status') == 'ok':
                        for cell in data.get('cells', []):
                            devices.append({
                                "lat": cell.get('lat'),
                                "lon": cell.get('lon'),
                                "cell_id": str(cell.get('cellid')),
                                "signal": cell.get('signal'),
                                "accuracy": cell.get('accuracy'),
                                "timestamp": cell.get('updated'),
                                "type": "cell_tower"
                            })
                    else:
                        print(f"OpenCellID location error: {data.get('message', 'Unknown error')}")
                else:
                    print(f"OpenCellID location HTTP error: {opencell_response.status_code} - {opencell_response.text}")
            except Exception as e:
                print(f"OpenCellID location exception: {str(e)}")
        except:
            return jsonify({"error": "Invalid location format"})

    elif search_type == 'bssid':
        try:
            wigle_response = requests.get(
                'https://api.wigle.net/api/v2/network/search',
                params={'netid': query},
                auth=(WIGLE_API_NAME, WIGLE_API_TOKEN)
            )
            if wigle_response.status_code == 200:
                for network in wigle_response.json().get('results', []):
                    devices.append({
                        "lat": network.get('trilat'),
                        "lon": network.get('trilong'),
                        "ssid": network.get('ssid'),
                        "bssid": network.get('netid'),
                        "vendor": network.get('vendor'),
                        "signal": network.get('level'),
                        "timestamp": network.get('lastupdt'),
                        "type": "router"
                    })
            else:
                print(f"Wigle BSSID error: {wigle_response.status_code} - {wigle_response.text}")
        except Exception as e:
            print(f"Wigle BSSID exception: {str(e)}")

    elif search_type == 'ssid':
        try:
            wigle_response = requests.get(
                'https://api.wigle.net/api/v2/network/search',
                params={'ssid': query},
                auth=(WIGLE_API_NAME, WIGLE_API_TOKEN)
            )
            if wigle_response.status_code == 200:
                for network in wigle_response.json().get('results', []):
                    devices.append({
                        "lat": network.get('trilat'),
                        "lon": network.get('trilong'),
                        "ssid": network.get('ssid'),
                        "bssid": network.get('netid'),
                        "vendor": network.get('vendor'),
                        "signal": network.get('level'),
                        "timestamp": network.get('lastupdt'),
                        "type": "router"
                    })
            else:
                print(f"Wigle SSID error: {wigle_response.status_code} - {wigle_response.text}")
        except Exception as e:
            print(f"Wigle SSID exception: {str(e)}")

    elif search_type == 'network':
        if SHODAN_API_KEY:
            try:
                shodan_response = requests.get(
                    'https://api.shodan.io/shodan/host/search',
                    params={'key': SHODAN_API_KEY, 'query': query}
                )
                if shodan_response.status_code == 200:
                    for host in shodan_response.json().get('matches', []):
                        devices.append({
                            "lat": host.get('location', {}).get('latitude'),
                            "lon": host.get('location', {}).get('longitude'),
                            "ip": host.get('ip_str'),
                            "vendor": host.get('org'),
                            "type": host.get('product', 'iot')
                        })
                else:
                    print(f"Shodan search error: {shodan_response.status_code} - {shodan_response.text}")
            except Exception as e:
                print(f"Shodan search exception: {str(e)}")
        else:
            print("Shodan search skipped: No API key provided")

    # Fallback to dummy data if no results
    if not devices and search_type in ['location', 'ssid', 'bssid', 'network']:
        devices = [d for d in DUMMY_DATA if (
            (search_type == 'location' and abs(d['lat'] - lat) < 0.1 and abs(d['lon'] - lon) < 0.1) or
            (search_type == 'ssid' and d.get('ssid', '').lower() == query.lower()) or
            (search_type == 'bssid' and d.get('bssid', '').lower() == query.lower()) or
            (search_type == 'network' and d.get('ip', '') == query)
        )]
        print("Using dummy data for search")

    return jsonify({"devices": devices})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

    
