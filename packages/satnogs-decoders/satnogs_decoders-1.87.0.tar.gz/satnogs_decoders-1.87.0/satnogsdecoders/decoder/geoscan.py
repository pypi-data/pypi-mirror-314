# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Geoscan(KaitaiStruct):
    """:field callsign: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    :field ssid_mask: ax25_frame.ax25_header.dest_ssid_raw.ssid_mask
    :field ssid: ax25_frame.ax25_header.dest_ssid_raw.ssid
    :field src_callsign_raw_callsign: ax25_frame.ax25_header.src_callsign_raw.callsign_ror.callsign
    :field src_ssid_raw_ssid_mask: ax25_frame.ax25_header.src_ssid_raw.ssid_mask
    :field src_ssid_raw_ssid: ax25_frame.ax25_header.src_ssid_raw.ssid
    :field ctl: ax25_frame.ax25_header.ctl
    :field pid: ax25_frame.ax25_header.pid
    :field beacon_id: ax25_frame.payload.beacon_id
    :field eps_timestamp: ax25_frame.payload.eps_timestamp
    :field eps_mode: ax25_frame.payload.eps_mode
    :field eps_switch_count: ax25_frame.payload.eps_switch_count
    :field eps_consumption_current: ax25_frame.payload.eps_consumption_current
    :field eps_system_current: ax25_frame.payload.eps_system_current
    :field eps_cell_voltage_half: ax25_frame.payload.eps_cell_voltage_half
    :field eps_cell_voltage_full: ax25_frame.payload.eps_cell_voltage_full
    :field eps_systems_status: ax25_frame.payload.eps_systems_status
    :field eps_temperature_cell1: ax25_frame.payload.eps_temperature_cell1
    :field eps_temperature_cell2: ax25_frame.payload.eps_temperature_cell2
    :field eps_boot_count: ax25_frame.payload.eps_boot_count
    :field eps_heater_mode: ax25_frame.payload.eps_heater_mode
    :field eps_reserved: ax25_frame.payload.eps_reserved
    :field obc_boot_count: ax25_frame.payload.obc_boot_count
    :field obc_active_status: ax25_frame.payload.obc_active_status
    :field obc_temperature_pos_x: ax25_frame.payload.obc_temperature_pos_x
    :field obc_temperature_neg_x: ax25_frame.payload.obc_temperature_neg_x
    :field obc_temperature_pos_y: ax25_frame.payload.obc_temperature_pos_y
    :field obc_temperature_neg_y: ax25_frame.payload.obc_temperature_neg_y
    :field gnss_sat_number: ax25_frame.payload.gnss_sat_number
    :field adcs_mode: ax25_frame.payload.adcs_mode
    :field adcs_reserved: ax25_frame.payload.adcs_reserved
    :field cam_photos_number: ax25_frame.payload.cam_photos_number
    :field cam_mode: ax25_frame.payload.cam_mode
    :field cam_reserved: ax25_frame.payload.cam_reserved
    :field comm_type: ax25_frame.payload.comm_type
    :field comm_bus_voltage: ax25_frame.payload.comm_bus_voltage
    :field comm_boot_count: ax25_frame.payload.comm_boot_count
    :field comm_rssi: ax25_frame.payload.comm_rssi
    :field comm_rssi_minimal: ax25_frame.payload.comm_rssi_minimal
    :field comm_received_valid_packets: ax25_frame.payload.comm_received_valid_packets
    :field comm_received_invalid_packets: ax25_frame.payload.comm_received_invalid_packets
    :field comm_sent_packets: ax25_frame.payload.comm_sent_packets
    :field comm_status: ax25_frame.payload.comm_status
    :field comm_mode: ax25_frame.payload.comm_mode
    :field comm_temperature: ax25_frame.payload.comm_temperature
    :field comm_qso_received: ax25_frame.payload.comm_qso_received
    :field comm_reserved: ax25_frame.payload.comm_reserved
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.ax25_frame = Geoscan.Ax25Frame(self._io, self, self._root)

    class Ax25Frame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_header = Geoscan.Ax25Header(self._io, self, self._root)
            self.payload = Geoscan.GeoscanBeaconTlm(self._io, self, self._root)


    class Ax25Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dest_callsign_raw = Geoscan.CallsignRaw(self._io, self, self._root)
            self.dest_ssid_raw = Geoscan.SsidMask(self._io, self, self._root)
            self.src_callsign_raw = Geoscan.CallsignRaw(self._io, self, self._root)
            self.src_ssid_raw = Geoscan.SsidMask(self._io, self, self._root)
            self.ctl = self._io.read_u1()
            self.pid = self._io.read_u1()


    class Callsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


    class SsidMask(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ssid_mask = self._io.read_u1()

        @property
        def ssid(self):
            if hasattr(self, '_m_ssid'):
                return self._m_ssid

            self._m_ssid = ((self.ssid_mask & 15) >> 1)
            return getattr(self, '_m_ssid', None)


    class GeoscanBeaconTlm(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.beacon_id = self._io.read_u1()
            self.eps_timestamp = self._io.read_u4le()
            self.eps_mode = self._io.read_u1()
            self.eps_switch_count = self._io.read_u1()
            self.eps_consumption_current = self._io.read_u2le()
            self.eps_solar_cells_current = self._io.read_u2le()
            self.eps_cell_voltage_half = self._io.read_u2le()
            self.eps_cell_voltage_full = self._io.read_u2le()
            self.eps_systems_status = self._io.read_u2le()
            self.eps_temperature_cell1 = self._io.read_s1()
            self.eps_temperature_cell2 = self._io.read_s1()
            self.eps_boot_count = self._io.read_u2le()
            self.eps_heater_mode = self._io.read_u1()
            self.eps_reserved = self._io.read_u2le()
            self.obc_boot_count = self._io.read_u2le()
            self.obc_active_status = self._io.read_u1()
            self.obc_temperature_pos_x = self._io.read_s1()
            self.obc_temperature_neg_x = self._io.read_s1()
            self.obc_temperature_pos_y = self._io.read_s1()
            self.obc_temperature_neg_y = self._io.read_s1()
            self.gnss_sat_number = self._io.read_u1()
            self.adcs_mode = self._io.read_u1()
            self.adcs_reserved = self._io.read_u1()
            self.cam_photos_number = self._io.read_u1()
            self.cam_mode = self._io.read_u1()
            self.cam_reserved = self._io.read_u4le()
            self.comm_type = self._io.read_u1()
            self.comm_bus_voltage = self._io.read_u2le()
            self.comm_boot_count = self._io.read_u2le()
            self.comm_rssi = self._io.read_s1()
            self.comm_rssi_minimal = self._io.read_s1()
            self.comm_received_valid_packets = self._io.read_u1()
            self.comm_received_invalid_packets = self._io.read_u1()
            self.comm_sent_packets = self._io.read_u1()
            self.comm_status = self._io.read_u1()
            self.comm_mode = self._io.read_u1()
            self.comm_temperature = self._io.read_s1()
            self.comm_qso_received = self._io.read_u1()
            self.comm_reserved = self._io.read_u2le()


    class CallsignRaw(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw__raw_callsign_ror = self._io.read_bytes(6)
            self._raw_callsign_ror = KaitaiStream.process_rotate_left(self._raw__raw_callsign_ror, 8 - (1), 1)
            _io__raw_callsign_ror = KaitaiStream(BytesIO(self._raw_callsign_ror))
            self.callsign_ror = Geoscan.Callsign(_io__raw_callsign_ror, self, self._root)



