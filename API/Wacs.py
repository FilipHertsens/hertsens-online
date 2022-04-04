import requests
import json

apikey = 'Bg8mf4V59bcSGlb+WftHuQ=='

def GetAllAssetsBase():
    response = requests.get(
        'https://api.wacs.online/api/v1/Assets/GetAll',
        params={'key': apikey},
    )
    json_response = response.json()
    return json_response

def GetChecklist():
    response = requests.get(
        'https://api.wacs.online/api/v1/checklist',
        params={'key': apikey},
    )
    json_response = response.json()
    return json_response



def GetAllTodo():
    response = requests.get(
        'https://api.wacs.online/api/v1/Todo/GetAllTodos',
        params={'key': apikey},
    )
    json_response = response.json()
    return json_response


def GetPlanorders():
    response = requests.get(
        'https://api.wacs.online/api/v1/Planning/GetOrders',
        params={'key': apikey},
    )
    if response.status_code == 200:
        json_response = response.json()
        with open('planorders.json', 'w') as outfile:
            json.dump(json_response, outfile)
        return {"response": "alle planorders ontvangen", "code": response.status_code}
    else:
        return {"response": "Request for alle planorders mislukt", "code": response.status_code}


def GetKeuringdata():
    response = requests.get(
        'https://api.wacs.online/api/v1/Todo/GetVehicleDates',
        params={'key': apikey},
    )
    json_response = response.json()
    return json_response


def GetAssetmodified(x):
    response = requests.get(
        'https://api.wacs.online/api/v1/Assets/GetAllLastModified',
        params={'key': apikey, 'seconds': x},
    )
    if response.status_code == 200:
        json_response = response.json()
        with open('assetmodified.txt', 'w') as outfile:
            json.dump(json_response, outfile)
        return {"response": "lijst asset modified ontvangen", "code": response.status_code}
    else:
        return {"response": "Request for all modified assets mislukt", "code": response.status_code}

def GetAssetDetails(x):
    response = requests.get(
        'https://api.wacs.online/api/v1/Assets/GetByID',
        params={'key': apikey, 'id': x},
    )
    json_response = response.json()
    return json_response




def UpdateKmById(AssetId, Km):
    response = requests.post(
        'https://api.wacs.online/api/v1/Assets/UpdateMileageById',
        params={'key': apikey, 'id': AssetId, 'mileage': Km})
    print(response)

    if response.status_code > 199 < 300:
        return {"response": "Request add todo is gelukt", "code": response.status_code}

    else:
        return {"response": response, "code": 'error'}


if __name__ == '__main__':
    pass