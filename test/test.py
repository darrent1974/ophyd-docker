import datetime
import logging
import os
import shutil
import time
from unittest.mock import Mock
import sys

import numpy as np
import pytest
from io import StringIO
from pathlib import PurePath, Path

from ophyd import (set_cl, EpicsMotor, Signal, EpicsSignal, EpicsSignalRO,
                   Component as Cpt)
from ophyd.utils.epics_pvs import (AlarmSeverity, AlarmStatus)                   

from ophyd.utils.paths import make_dir_tree
from ophyd import (SimDetector, SingleTrigger, Component, Device,
                   DynamicDeviceComponent, Kind, wait)
from ophyd.areadetector.plugins import (ImagePlugin, StatsPlugin,
                                        ColorConvPlugin, ProcessPlugin,
                                        OverlayPlugin, ROIPlugin,
                                        TransformPlugin, NetCDFPlugin,
                                        TIFFPlugin, JPEGPlugin, HDF5Plugin,
                                        KafkaPlugin
                                        # FilePlugin
                                        )
from ophyd.areadetector.base import NDDerivedSignal
from ophyd.areadetector.filestore_mixins import (
    FileStoreTIFF, FileStoreIterativeWrite,
    FileStoreHDF5)

# we do not have nexus installed on our test IOC
# from ophyd.areadetector.plugins import NexusPlugin
from ophyd.areadetector.plugins import PluginBase
from ophyd.areadetector.util import stub_templates
#from ophyd.device import (Component as Cpt, )
from ophyd.signal import Signal
import uuid

def get_ad_prefix():
    # prefixes = ['13SIM1:', 'XF:31IDA-BI{Cam:Tbl}']
    prefix = '13SIM1:'
    test_pv = prefix + 'TIFF1:PluginType_RBV'
    try:
        sig = EpicsSignalRO(test_pv)
        sig.wait_for_connection(timeout=2)
    except TimeoutError:
        raise TimeoutError('No areaDetector IOC running')
    else:
        print('areaDetector detected with prefix:', prefix)
        return prefix
    finally:
        sig.destroy()

try:
    os.environ["EPICS_CA_ADDR_LIST"] = ''
    os.environ["EPICS_CA_AUTO_ADDR_LIST"] = ''

    #set_cl('caproto')
    #set_cl('pyepics')
    ad_prefix = get_ad_prefix()

    class MyDetector(SingleTrigger, SimDetector):
        image1 = Cpt(ImagePlugin, ImagePlugin._default_suffix)
        #kafka1 = Cpt(KafkaPlugin, KafkaPlugin._default_suffix)

    det = MyDetector(ad_prefix, name='test')
    #kafka_plugin = det.kafka1

    print(det.image1.plugin_type)
    #print(kafka_plugin.plugin_type)
    #print(kafka_plugin.port_name.get())
    
    det.wait_for_connection()

    #kafka_plugin.kafka_broker_address.put('localhost:1234')

    det.cam.acquire_time.put(0.01)
    det.cam.acquire_period.put(0.01)
    det.cam.num_images.put(1)
    det.cam.image_mode.put(det.cam.ImageMode.SINGLE)
    det.stage()
    st = det.trigger()
    wait(st, timeout=5)
    det.unstage()

except:
    print(f'Exception: {sys.exc_info()}')







