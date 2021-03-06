"""
@author: fangyh09
"""

import numpy as np

# KEYPOINT_NUM = 10
# WIDTH_RATIO = 0.2
# HEIGHT_RATIO = 0.3
# PERSON_NUM = 10
filter_configs = {
    "c1": [10, 10, 0.2, 0.3],
    "c2": [10, 13, 0.2, 0.3],
    "c3": [5, 10, 0.2, 0.3],
    "c4": [5, 8, 0.2, 0.3],
    "c5": [8, 10, 0.05, 0.1],
    "c6": [8, 8, 0.1, 0.15],
    "c7": [8, 8, 0.3, 0.6]
}

mode = "c7"
PERSON_NUM = filter_configs[mode][0]
KEYPOINT_NUM = filter_configs[mode][1]
WIDTH_RATIO = filter_configs[mode][2]
HEIGHT_RATIO = filter_configs[mode][3]

def ok(feed_dict):
    """
    :param
        feed_dict: <Class dict>
         {'width': width,
          'height': height,
          'vis': vis <Class dict/list/numpy>
          'x': x <Class list/numpy>
          'y': y <Class list/numpy>}

        Example:
          vis={'11': 1, '10': 1, '13': 1, '12': 1, '15': 1, '14': 1, '1': 1,
          '0': 1, '3': 0, '2': 1, '5': 1, '4': 1, '7': 1, '6': 0, '9': 0, '8': 0}
    :return: <Class boolean>
    """
    # unpack
    width = feed_dict['width']
    height = feed_dict['height']
    vis = feed_dict['vis']
    x = feed_dict['x']
    y = feed_dict['y']

    # transform
    if vis is not None and type(vis) is dict:
        vis = np.array(vis.values())
    x = np.array(x)
    y = np.array(y)
    # protocol 1
    if vis is not None:
        keypoint_num = np.sum(vis > 0)
        if keypoint_num < KEYPOINT_NUM:
            return False
    # protocol 2
    assert (vis is not None)
    minx = np.min(x[vis])
    maxx = np.max(x[vis])
    miny = np.min(y[vis])
    maxy = np.max(y[vis])
    bbox_width = maxx - minx
    bbox_height = maxy - miny
    if bbox_width < WIDTH_RATIO * width:
        return False
    if bbox_height < HEIGHT_RATIO * height:
        return False
    return True
