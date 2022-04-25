import API.BAlertClientTpms as BAlertClient
import urllib
import xml.etree.ElementTree as ET
import xmltodict
from pprint import pprint
import datetime


# usage of the API below
server = "api.balert.net"  # address of server hosting the API
port = 8080
api_key = "hertsens"  # supplied API key for this application
secret_api_key = "6sd5g4df6g4S6DFG6GH465D4FG"  # supplied secret for API key, this will not be transmitted in any way in cleartext!

user = "Hertsens"  # user of which the devices will be queried
password = "b.Alert"  # password of user for which the devices will be queried, this will not be transmitted in any way in cleartext!

balertClient = BAlertClient.BAlertClient(server, api_key, secret_api_key, port=port)

def Get_vehicle_by_Name():
    # filtering = "$filter=" + urllib.parse.quote(f"vehicle/name eq '{name}'")
    tireData = balertClient.getVehicles(user, password)
    tireData2 = xmltodict.parse(tireData)
    if tireData2['rsp']['@stat'] == 'ok':
        return True, tireData2['rsp']['vehicle']
    else:
        return False,'fail to get tiredata'

def Get_tires_by_Name(name):
    filtering = "$filter=" + urllib.parse.quote(f"vehicle/name eq '{name}'")
    tireData = balertClient.getTires(user, password, filtering)
    tireData2 = xmltodict.parse(tireData)
    if tireData2['rsp']['@stat'] == 'ok':
        if 'vehicle' in tireData2['rsp']:
            return True, tireData2['rsp']['vehicle']

    return False,'fail to get tiredata'

def Get_tires_by_Id(id):
    filtering = "$filter=" + urllib.parse.quote(f"vehicle/id eq {id}")
    tireData = balertClient.getTires(user, password, filtering)
    tireData2 = xmltodict.parse(tireData)
    if tireData2['rsp']['@stat'] == 'ok':
        if 'vehicle' in tireData2['rsp']:
            return True, tireData2['rsp']['vehicle']
    return False,'fail to get tiredata'

def Get_tire_name(typeid,tire):
    global tire_names

    positie = tire['@position_on_vehicle'].split('.')
    axel = str(int(positie[0])-1)
    LR = '1'
    IO = '1'
    if int(positie[1]) > 2:
        LR = '0'
    if positie[1] in ['4','1']:
        IO = '0'
    list_tire_typs = ([x for x in tire_names if x["@vehicle_type_id"] == typeid and x['@position_row'] == axel and
                       x['@position_left_right'] == LR and x['@position_inside_outside'] == IO and
                       x['@language'] == 'dutch'])
    return list_tire_typs[0]['@name']

def Add_tireNames(xml):
    global vehicle
    typeid = next(x for x in vehicle[1] if x["@name"] == xml['@name'])['@vehicle_type_id']
    for tire in xml['tire']:
        tire['@position_name'] = Get_tire_name(typeid, tire)
    return xml

def Add_vehicle_alerts(xml):
    last_connection = datetime.datetime.strptime(xml['@time_stamp'], '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.utcnow()
    xml['@alerts'] = []
    if now + datetime.timedelta(hours=-1) > last_connection:
        if now + datetime.timedelta(days=-1) > last_connection:
            xml['@alerts'].append(['connection', 'red'])
        else:
            xml['@alerts'].append(['connection', 'orange'])
    return xml

def Add_tire_alerts(xml):
    for tire in xml['tire']:
        tire['@alerts'] = []
        last_connection = datetime.datetime.strptime(tire['@time_stamp'], '%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.utcnow()
        if float(tire['@fill_level']) < 0.91:
            error = ['tire','orange']
            if float(tire['@fill_level']) < 0.7:
                error = ['tire','red']
            tire['@alerts'].append(error)
        if int(tire['@internal_temperature']) > 119:
            tire['@alerts'].append(['temp','red'])
        if now + datetime.timedelta(hours=-1) > last_connection:
            if now + datetime.timedelta(days=-1) > last_connection:
                tire['@alerts'].append(['connection', 'red'])
            else:
                tire['@alerts'].append(['connection','orange'])
    return xml

def get_vehicles():
    vehicle = Get_vehicle_by_Name()
    return vehicle

def get_tire_names():
    tire_names = xmltodict.parse(balertClient.getTirePositionNames(user, password))
    if tire_names['rsp']['@stat'] == 'ok':
        return tire_names['rsp']['tire_position_name']
    else:
        return []


def get_all_data(name=None, id=None):
    data = []
    if name:
        tires = Get_tires_by_Name(name)
    else:
        tires = Get_tires_by_Id(id)
    if tires[0]:
        data = Add_vehicle_alerts(tires[1])
        data = Add_tireNames(data)
        data = Add_tire_alerts(data)
        return data
    return []

vehicle = get_vehicles()
tire_names = get_tire_names()