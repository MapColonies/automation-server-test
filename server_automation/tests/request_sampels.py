# pylint: disable=line-too-long, raise-missing-from, trailing-comma-tuple
"""This module provide generation of several request json files for testing purpose"""
import json
import enum
from server_automation.configuration import config


class BoxSize(enum.Enum):
    """ Size of bbox """
    Sanity = 1,
    Small = 10,
    Medium = 50,
    Big = 150


class ZoomLevels(enum.Enum):
    """
    Types of zoom levels
    """
    default = 18
    med = 15


_lod_req = {
    "fileName": "unknown_name",
    "sizeEst": 30,
    "tilesEst": 51,
    "maxZoom": 18,
    "directoryName": "test_dir",
    "exportedLayers": [
        {
            "exportType": "raster",
            "sourceLayer": config.SOURCE_LAYER,
            "url": config.BEST_LAYER_URL,
        }
    ],
    "bbox": [
        35.32951416015625,
        32.13432373046876,
        35.35697998046875,
        32.16178955078126
    ]
}

_et_req_1 = {
    "fileName": "r_regular",
    "sizeEst": 2,
    "tilesEst": 51,
    "maxZoom": 18,
    "directoryName": "e_tests",
    "exportedLayers": [
        {
            "exportType": "raster",
            "sourceLayer": config.SOURCE_LAYER,
            "url": config.BEST_LAYER_URL,
            # "url": "http://10.28.11.125/blue_m_flat2d-v001/wms?SERVICE=WMS&LAYERS=[blue_m_flat2d-v001]:1002&TILED=true"
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
    "maxZoom": 18,
    "directoryName": "e_tests",
    "exportedLayers": [
        {
            "exportType": "raster",
            "sourceLayer": config.SOURCE_LAYER,
            "url": config.BEST_LAYER_URL,
            # "url": "http://10.28.11.125/blue_m_flat2d-v001/wms?SERVICE=WMS&LAYERS=[blue_m_flat2d-v001]:1002&TILED=true"
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
    "maxZoom": 18,
    "directoryName": "size_limit_test",
    "exportedLayers": [
        {
            "exportType": "raster",
            "sourceLayer": config.SOURCE_LAYER,
            "url": config.BEST_LAYER_URL,
            # "url": "http://10.28.11.125/blue_m_flat2d-v001/wms?SERVICE=WMS&LAYERS=[blue_m_flat2d-v001]:1002&TILED=true"
        }
    ],
    "bbox": [
    ]
}

_box_sanity_size = [35.220349, 31.778416, 35.221412, 31.779315]
_box_10_10 = [34.937897, 31.854815, 35.044155, 31.944588]
_box_50_50 = [34.47921, 31.16345, 35.02029, 31.61596]
_box_150_150 = [34.321289, 30.491284, 35.911560, 31.844899]

request_index = {'et_req_1': _et_req_1, 'et_req_2': _et_req_2, 'lod_req': _lod_req}


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


def get_lod_req(size):
    """ provide valid zoom level according enum provided - ZoomLevels """
    if size == ZoomLevels.default:
        _lod_req['maxZoom'] = ZoomLevels.default.value
    elif size == ZoomLevels.med:
        _lod_req['maxZoom'] = ZoomLevels.med.value
    else:
        raise Exception("should provide valid max level value")
    return json.dumps(_lod_req)


def get_request_by_box_size(size):
    """this method generate different export request according size [big,med,small]"""
    if size == BoxSize.Big:
        _et_req_3["bbox"] = _box_150_150
    elif size == BoxSize.Medium:
        _et_req_3["bbox"] = _box_50_50
        _et_req_3["maxZoom"] = 5
    elif size == BoxSize.Small:
        _et_req_3["bbox"] = _box_10_10
    elif size == BoxSize.Sanity:
        return json.dumps(_et_req_2)
    else:
        raise Exception("should provide valid box size parameters for request")
    return json.dumps(_et_req_3)
