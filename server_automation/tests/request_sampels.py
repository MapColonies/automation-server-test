import json
import enum


class box_size(enum.Enum):
    Big = 150,
    Medium = 50,
    Small = 10,
    Sanity = 1


_et_req_1 = {
    "fileName": "r_regular",
    "sizeEst": 2,
    "tilesEst": 51,
    "directoryName": "e_tests",
    "exportedLayers": [
        {
            "exportType": "raster",
            "url": "http://10.28.11.125/blue_m_flat2d-v001/wms?SERVICE=WMS&LAYERS=[blue_m_flat2d-v001]:1002&TILED=true"
        }
    ],
    "bbox": [
        34.97348584069924,
        31.807417142121864,
        34.97845515081091,
        31.811133321857543
    ]
}

_et_req_2 = {
    "fileName": "r_short",
    "sizeEst": 30,
    "tilesEst": 10,
    "directoryName": "e_tests",
    "exportedLayers": [
        {
            "exportType": "raster",
            "url": "http://10.28.11.125/blue_m_flat2d-v001/wms?SERVICE=WMS&LAYERS=[blue_m_flat2d-v001]:1002&TILED=true"
        }
    ],
    "bbox": [
        34.864467174986935,
        32.02514200985454,
        34.865206880136384,
        32.02579011373897
    ]
}


_et_req_3 = {
    "fileName": "dynamic_box",
    "sizeEst": 30,
    "tilesEst": 10,
    "directoryName": "size_limit_test",
    "exportedLayers": [
        {
            "exportType": "raster",
            "url": "http://10.28.11.125/blue_m_flat2d-v001/wms?SERVICE=WMS&LAYERS=[blue_m_flat2d-v001]:1002&TILED=true"
        }
    ],
    "bbox": [
            ]
}

_box_sanity_size = [35.220349, 31.778416, 35.221412, 31.779315]
_box_10_10 = [34.937897, 31.854815, 35.044155, 31.944588]
_box_50_50 = [34.894638, 31.670915, 35.215130, 31.947210]
_box_150_150 = [34.321289, 30.491284, 35.911560, 31.844899]

request_index = {'et_req_1': _et_req_1, 'et_req_2': _et_req_2}


def show_requests():
    """ Show all exist requests sample for export-trigger request api"""
    for req in request_index:
        print("\n" + req)
        print(json.dumps(request_index[req], indent=4))


def get_request_sample(req_name):
    """
  Return json request by name
  :param req_name:
  :return:
  """

    try:
        req = request_index[req_name]
        return json.dumps(req)

    except KeyError:
        raise KeyError('Request name not exist')

    except Exception:
        raise Exception('Unknown error')


def get_request_by_box_size(size):
    if size==box_size.Big:
        _et_req_3["bbox"] = _box_150_150
    elif size==box_size.Medium:
        _et_req_3["bbox"] = _box_50_50
    elif size==box_size.Small:
        _et_req_3["bbox"] = _box_10_10
    elif size==box_size.Sanity:
        return json.dumps(_et_req_2)
    else:
        raise Exception("should provide valide box size parameters for request")
    return json.dumps(_et_req_3)