"""
Yamjam config.
"""

import os

import YamJam

cfg = {}

try:
    config_file_path = os.environ.get('EQ_MAP_BACKEND_YAMJAM_CONF_FILE_PATH', '/tmp/path/to/file')
    cfg = YamJam.yamjam(config_file_path)
except YamJam.YAMLError:
    pass
