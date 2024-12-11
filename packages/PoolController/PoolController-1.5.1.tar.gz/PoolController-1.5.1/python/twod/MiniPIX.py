import PyTango
# import time, os

from sardana import DataAccess
# from sardana import State, DataAccess
from sardana.pool.controller import TwoDController
# from sardana.pool.controller import Type, Access, Description, DefaultValue
from sardana.pool.controller import Type, Access, Description
# from sardana.pool import PoolUtil

ReadOnly = DataAccess.ReadOnly
ReadWrite = DataAccess.ReadWrite


class MiniPIXCtrl(TwoDController):
    "This class is the Tango Sardana Two D controller for the MiniPIX"

    axis_attributes = {
        'FrameTime': {Type: 'PyTango.DevDouble', Access: ReadWrite},
        'SaveFileName': {Type: 'PyTango.DevString', Access: ReadWrite},
        'SaveFilePath': {Type: 'PyTango.DevString', Access: ReadWrite},
        'FrameCounter': {Type: 'PyTango.DevLong', Access: ReadWrite},
        'FrameNumbers': {Type: 'PyTango.DevLong', Access: ReadWrite},
        'EnergyThreshold': {Type: 'PyTango.DevFloat', Access: ReadWrite},
        'TangoDevice': {Type: 'PyTango.DevString', Access: ReadOnly}
    }

    ctrl_properties = {
        'RootDeviceName': {
            Type: str,
            Description: 'The root name of the MiniPIX Tango devices'},
        'TangoHost': {
            Type: str,
            Description: 'The tango host where searching the devices'},
    }

    MaxDevice = 97

    def __init__(self, inst, props, *args, **kwargs):
        self.TangoHost = None
        TwoDController.__init__(self, inst, props, *args, **kwargs)

        if self.TangoHost is None:
            self.db = PyTango.Database()
        else:
            self.node = self.TangoHost
            self.port = 10000
            if self.TangoHost.find(':'):
                lst = self.TangoHost.split(':')
                self.node = lst[0]
                self.port = int(lst[1])
            self.db = PyTango.Database(self.node, self.port)
        name_dev_ask = self.RootDeviceName + "*"
        self.devices = self.db.get_device_exported(name_dev_ask)
        self.max_device = 0
        self.tango_device = []
        self.proxy = []
        self.device_available = []
        for name in self.devices.value_string:
            self.tango_device.append(name)
            self.proxy.append(None)
            self.device_available.append(0)
            self.max_device = self.max_device + 1
        self.started = False
        self.dft_FrameTime = 0
        self.FrameTime = []
        self.dft_SaveFileName = ""
        self.SaveFileName = []
        self.dft_SaveFilePath = ""
        self.SaveFilePath = []
        self.dft_FrameCounter = 0
        self.FrameCounter = []
        self.dft_FrameNumbers = 0
        self.FrameNumbers = []
        self.dft_EnergyThreshold = 0
        self.EnergyThreshold = []

    def AddDevice(self, ind):
        TwoDController.AddDevice(self, ind)
        if ind > self.max_device:
            print("False index")
            return
        proxy_name = self.tango_device[ind - 1]
        if self.TangoHost is None:
            proxy_name = self.tango_device[ind - 1]
        else:
            proxy_name = str(self.node) + (":%s/" % self.port) \
                + str(self.tango_device[ind - 1])
        self.proxy[ind - 1] = PyTango.DeviceProxy(proxy_name)
        self.device_available[ind - 1] = 1
        self.FrameTime.append(self.dft_FrameTime)
        self.SaveFileName.append(self.dft_SaveFileName)
        self.SaveFilePath.append(self.dft_SaveFilePath)
        self.FrameCounter.append(self.dft_FrameCounter)
        self.FrameNumbers.append(self.dft_FrameNumbers)
        self.EnergyThreshold.append(self.dft_EnergyThreshold)

    def DeleteDevice(self, ind):
        TwoDController.DeleteDevice(self, ind)
        self.proxy[ind - 1] = None
        self.device_available[ind - 1] = 0

    def StateOne(self, ind):
        if self.device_available[ind - 1] == 1:
            sta = self.proxy[ind - 1].command_inout("State")
            if sta == PyTango.DevState.ON:
                tup = (sta, "Camera ready")
            elif sta == PyTango.DevState.RUNNING:
                sta = PyTango.DevState.MOVING
                tup = (sta, "Camera taking images")
            elif sta == PyTango.DevState.MOVING:
                sta = PyTango.DevState.MOVING
                tup = (sta, "Camera taking images")
            elif sta == PyTango.DevState.FAULT:
                tup = (sta, "Camera in FAULT state")
            elif sta == PyTango.DevState.DISABLE:
                sta = PyTango.DevState.FAULT
                tup = (sta, "Camera disabled")
            elif sta == PyTango.DevState.UNKNOWN:
                sta = PyTango.DevState.FAULT
                tup = (sta, "State is unknown")
            return tup

    def PreReadAll(self):
        pass

    def PreReadOne(self, ind):
        pass

    def ReadAll(self):
        pass

    def ReadOne(self, ind):
        # The MiniPIX return an Image in type encoded
        tmp_value = [(-1,), (-1,)]
        if self.device_available[ind - 1] == 1:
            return tmp_value

    def PreStartAll(self):
        pass

    def StartOne(self, ind, position=None):
        self.proxy[ind - 1].command_inout("StartAcq")

    def AbortOne(self, ind):
        try:
            self.proxy[ind - 1].command_inout("StopAcq")
        except Exception:
            print("Not able to stop miniPIX if in ON state")

    def LoadOne(self, ind, value, repetitions, latency_time):
        # Frame Time is in ms
        self.proxy[ind - 1].write_attribute("FrameTime", value)

    def GetAxisExtraPar(self, ind, name):
        if self.device_available[ind - 1]:
            if name == "FrameTime":
                return self.proxy[ind - 1].read_attribute("FrameTime").value
            elif name == "SaveFileName":
                return self.proxy[ind - 1].read_attribute("SaveFileName").value
            elif name == "SaveFilePath":
                return self.proxy[ind - 1].read_attribute("SaveFilePath").value
            elif name == "FrameCounter":
                return self.proxy[ind - 1].read_attribute(
                    "FrameCounter").value
            elif name == "FrameNumbers":
                return self.proxy[ind - 1].read_attribute(
                    "FrameNumbers").value
            elif name == "EnergyThreshold":
                return self.proxy[ind - 1].read_attribute(
                    "EnergyThreshold").value
            elif name == "TangoDevice":
                tango_device = self.node + ":" + str(self.port) + "/" + \
                    self.proxy[ind - 1].name()
                return tango_device

    def SetAxisExtraPar(self, ind, name, value):
        if self.device_available[ind - 1]:
            if name == "FrameTime":
                self.proxy[ind - 1].write_attribute("FrameTime", value)
            elif name == "SaveFileName":
                self.proxy[ind - 1].write_attribute("SaveFileName", value)
            elif name == "SaveFilePath":
                self.proxy[ind - 1].write_attribute("SaveFilePath", value)
            elif name == "FrameCounter":
                self.proxy[ind - 1].write_attribute("FrameCounter", value)
            elif name == "FrameNumbers":
                self.proxy[ind - 1].write_attribute("FrameNumbers", value)
            elif name == "EnergyThreshold":
                self.proxy[ind - 1].write_attribute("EnergyThreshold", value)

    def SendToCtrl(self, in_data):
        #        print "Received value =", in_data
        return "Nothing sent"

    def __del__(self):
        print("PYTHON -> MiniPIXCtrl dying")


if __name__ == "__main__":
    obj = TwoDController('test')
