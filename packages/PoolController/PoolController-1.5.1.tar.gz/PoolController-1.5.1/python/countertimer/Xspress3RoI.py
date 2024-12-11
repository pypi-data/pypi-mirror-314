
# import time, os

import PyTango
from sardana import DataAccess
# from sardana import State
from sardana.pool.controller import CounterTimerController
from sardana.pool.controller import Type, Access, Description
# from sardana.pool.controller import DefaultValue
# from sardana.pool import PoolUtil

ReadOnly = DataAccess.ReadOnly
ReadWrite = DataAccess.ReadWrite

global last_sta


class Xspress3RoIsCtrl(CounterTimerController):
    "This class is the Tango Sardana CounterTimer controller" + \
        "for making RoIs from OneD"

    axis_attributes = {
        'TangoDevice': {Type: 'PyTango.DevString', Access: ReadOnly},
        'RoIStart': {Type: 'PyTango.DevLong', Access: ReadWrite},
        'RoIEnd': {Type: 'PyTango.DevLong', Access: ReadWrite},
        'DataChannel': {Type: 'PyTango.DevLong', Access: ReadWrite}
    }

    ctrl_properties = {
        'RootDeviceName': {
            Type: 'PyTango.DevString',
            Description: 'The root name of the MCA Tango devices'},
        'TangoHost': {
            Type: str,
            Description: 'The tango host where searching the devices'},
    }

    MaxDevice = 97

    gender = "CounterTimer"
    model = "Xspress3RoIs"
    organization = "DESY"
    state = ""
    status = ""

    def __init__(self, inst, props, *args, **kwargs):
        self.TangoHost = None
        CounterTimerController.__init__(self, inst, props, *args, **kwargs)

        if self.TangoHost is not None:
            self.node = self.TangoHost
            self.port = 10000
            if self.TangoHost.find(':'):
                lst = self.TangoHost.split(':')
                self.node = lst[0]
                self.port = int(lst[1])
        self.RoIs_start = []
        self.RoIs_end = []
        self.value = []
        self.channel = []
        proxy_name = self.RootDeviceName
        if self.TangoHost is not None:
            proxy_name = str(self.node) + \
                (":%s/" % self.port) + str(proxy_name)
        self.proxy = PyTango.DeviceProxy(proxy_name)
        global last_sta
        last_sta = PyTango.DevState.ON

    def AddDevice(self, ind):
        CounterTimerController.AddDevice(self, ind)
        self.RoIs_start.append(0)
        self.RoIs_end.append(0)
        self.value.append(0)
        self.channel.append(0)
        self.flagIsMini = 0
        if hasattr(self.proxy, 'DataCh00ROI0'):
            self.flagIsMini = True

    def DeleteDevice(self, ind):
        CounterTimerController.DeleteDevice(self, ind)
        self.proxy = None

    def StateOne(self, ind):
        global last_sta
        try:
            sta = self.proxy.command_inout("State")
            last_sta = sta
        except Exception:
            sta = last_sta
        if sta == PyTango.DevState.ON:
            tup = (sta, "Xspress3 idle")
        elif sta == PyTango.DevState.MOVING or sta == PyTango.DevState.RUNNING:
            tup = (PyTango.DevState.MOVING, "Device is acquiring data")
        else:
            tup = (sta, "")

        return tup

    def LoadOne(self, axis, value, repetitions, latency_time):
        self.proxy.ExposureTime = value

    def PreReadAll(self):
        pass

    def PreReadOne(self, ind):
        pass

    def ReadAll(self):
        pass

    def ReadOne(self, ind):
        if self.flagIsMini is False:
            attr_name = "DataCh" + str(self.channel[ind - 1])
            data = self.proxy.read_attribute(attr_name).value
            self.value[ind - 1] = 0
            for j in range(self.RoIs_start[ind - 1],
                           self.RoIs_end[ind - 1] + 1):
                self.value[ind - 1] = self.value[ind - 1] + data[j]
        else:
            attr_name = "DataCh00ROI" + str(self.channel[ind - 1])
            self.value[ind-1] = self.proxy.read_attribute(attr_name).value

        return self.value[ind - 1]

    def PreStartAll(self):
        pass

    def StartAll(self):
        try:
            sta = self.proxy.command_inout("State")
        except Exception:
            sta = PyTango.DevState.ON
        if sta == PyTango.DevState.ON:
            self.proxy.command_inout("StartAcquisition")

    def PreStartOne(self, ind, value):
        return True

    def StartOne(self, ind, value):
        pass

    def AbortOne(self, ind):
        self.proxy.command_inout("StopAcquisition")

    def GetAxisExtraPar(self, ind, name):
        if name == "TangoDevice":
            tango_device = self.node + ":" + str(self.port) + "/" \
                + self.proxy.name()
            return tango_device
        elif name == "DataLength":
            datalength = int(self.proxy.read_attribute("MCALength").value)
            return datalength
        elif name == "RoIStart":
            if self.flagIsMini is False:
                return self.RoIs_start[ind - 1]
            else:
                attr_name = "DataCh00ROI" + \
                    str(self.channel[ind - 1]) + "Start"
                return int(self.proxy.read_attribute(attr_name).value)
        elif name == "RoIEnd":
            if self.flagIsMini is False:
                return self.RoIs_end[ind - 1]
            else:
                attr_name = "DataCh00ROI" + str(self.channel[ind - 1]) + "End"
                return int(self.proxy.read_attribute(attr_name).value)
        elif name == "DataChannel":
            return self.channel[ind - 1]

    def SetAxisExtraPar(self, ind, name, value):
        if name == "DataLength":
            self.proxy.write_attribute("MCALength", value)
        elif name == "RoIStart":
            if self.flagIsMini is False:
                self.RoIs_start[ind - 1] = value
            else:
                attr_name = "DataCh00ROI" + \
                    str(self.channel[ind - 1]) + "Start"
                self.proxy.write_attribute(attr_name, value)
        elif name == "RoIEnd":
            if self.flagIsMini is False:
                self.RoIs_end[ind - 1] = value
            else:
                attr_name = "DataCh00ROI" + str(self.channel[ind - 1]) + "End"
                self.proxy.write_attribute(attr_name, value)
        elif name == "DataChannel":
            self.channel[ind - 1] = value

    def SendToCtrl(self, in_data):
        return "Nothing sent"

    def __del__(self):
        print("Xspress3RoIsCtrl dying")


if __name__ == "__main__":
    obj = CounterTimerController('test')
