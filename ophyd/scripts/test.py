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
    prefix = 'ADSIM:'
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
    print(os.getenv('EPICS_CA_ADDR_LIST'))
    print(os.getenv('EPICS_CA_AUTO_ADDR_LIST'))

    os.environ["EPICS_CA_ADDR_LIST"] = ''
    os.environ["EPICS_CA_AUTO_ADDR_LIST"] = ''

    #set_cl('caproto')
    #set_cl('pyepics')
    ad_prefix = get_ad_prefix()

    #print(caget('XF:31IDA-OP{Tbl-Ax:X1}Mtr'))

    class MyDetector(SingleTrigger, SimDetector):
        tiff1 = Cpt(TIFFPlugin, 'TIFF1:')

    det = MyDetector(ad_prefix, name='test')
    print(det.tiff1.plugin_type)

    det.wait_for_connection()

    det.cam.acquire_time.put(0.5)
    det.cam.acquire_period.put(0.5)
    det.cam.num_images.put(1)
    det.cam.image_mode.put(det.cam.ImageMode.SINGLE)
    det.stage()
    st = det.trigger()
    wait(st, timeout=5)
    det.unstage()

except:
    print(f'Exception: {sys.exc_info()}')







