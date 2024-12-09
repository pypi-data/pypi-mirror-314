# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Crocube(KaitaiStruct):
    """:field dest_callsign: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    :field src_callsign: ax25_frame.ax25_header.src_callsign_raw.callsign_ror.callsign
    :field src_ssid: ax25_frame.ax25_header.src_ssid_raw.ssid
    :field dest_ssid: ax25_frame.ax25_header.dest_ssid_raw.ssid
    :field rpt_callsign: ax25_frame.ax25_header.repeater.rpt_instance[0].rpt_callsign_raw.callsign_ror.callsign
    :field ctl: ax25_frame.ax25_header.ctl
    :field pid: ax25_frame.payload.pid
    :field monitor: ax25_frame.payload.ax25_info.monitor
    :field packet_type_q: ax25_frame.payload.ax25_info.packet_type_q
    :field message: ax25_frame.payload.ax25_info.body.message
    
    :field obc_reset_cnt: ax25_frame.payload.ax25_info.body.obc_reset_cnt
    :field obc_uptime: ax25_frame.payload.ax25_info.body.obc_uptime
    :field obc_uptime_tot: ax25_frame.payload.ax25_info.body.obc_uptime_tot
    :field obc_bat: ax25_frame.payload.ax25_info.body.obc_bat
    :field obc_temp_mcu: ax25_frame.payload.ax25_info.body.obc_temp_mcu
    :field obc_freemem: ax25_frame.payload.ax25_info.body.obc_freemem
    
    :field psu_reset_cnt: ax25_frame.payload.ax25_info.body.psu_reset_cnt
    :field psu_uptime: ax25_frame.payload.ax25_info.body.psu_uptime
    :field psu_uptime_tot: ax25_frame.payload.ax25_info.body.psu_uptime_tot
    :field psu_battery: ax25_frame.payload.ax25_info.body.psu_battery
    :field psu_temp_sys: ax25_frame.payload.ax25_info.body.psu_temp_sys
    :field psu_temp_bat: ax25_frame.payload.ax25_info.body.psu_temp_bat
    :field psu_cur_in: ax25_frame.payload.ax25_info.body.psu_cur_in
    :field psu_cur_out: ax25_frame.payload.ax25_info.body.psu_cur_out
    :field psu_ch_state_num: ax25_frame.payload.ax25_info.body.psu_ch_state_num
    :field psu_ch0_state: ax25_frame.payload.ax25_info.body.psu_ch0_state
    :field psu_ch1_state: ax25_frame.payload.ax25_info.body.psu_ch1_state
    :field psu_ch2_state: ax25_frame.payload.ax25_info.body.psu_ch2_state
    :field psu_ch3_state: ax25_frame.payload.ax25_info.body.psu_ch3_state
    :field psu_ch4_state: ax25_frame.payload.ax25_info.body.psu_ch4_state
    :field psu_ch5_state: ax25_frame.payload.ax25_info.body.psu_ch5_state
    :field psu_ch6_state: ax25_frame.payload.ax25_info.body.psu_ch6_state
    :field psu_sys_state: ax25_frame.payload.ax25_info.body.psu_sys_state
    :field psu_gnd_wdt: ax25_frame.payload.ax25_info.body.psu_gnd_wdt
    
    :field mgs_temp_int_mag: ax25_frame.payload.ax25_info.body.mgs_temp_int_mag
    :field mgs_temp_int_gyr: ax25_frame.payload.ax25_info.body.mgs_temp_int_gyr
    :field mgs_int_mag_x: ax25_frame.payload.ax25_info.body.mgs_int_mag_x
    :field mgs_int_mag_y: ax25_frame.payload.ax25_info.body.mgs_int_mag_y
    :field mgs_int_mag_z: ax25_frame.payload.ax25_info.body.mgs_int_mag_z
    :field mgs_int_gyr_x: ax25_frame.payload.ax25_info.body.mgs_int_gyr_x
    :field mgs_int_gyr_y: ax25_frame.payload.ax25_info.body.mgs_int_gyr_y
    :field mgs_int_gyr_z: ax25_frame.payload.ax25_info.body.mgs_int_gyr_z
    :field mgs_temp_ext_mag: ax25_frame.payload.ax25_info.body.mgs_temp_ext_mag
    :field mgs_temp_ext_gyr: ax25_frame.payload.ax25_info.body.mgs_temp_ext_gyr
    :field mgs_ext_mag_x: ax25_frame.payload.ax25_info.body.mgs_ext_mag_x
    :field mgs_ext_mag_y: ax25_frame.payload.ax25_info.body.mgs_ext_mag_y
    :field mgs_ext_mag_z: ax25_frame.payload.ax25_info.body.mgs_ext_mag_z
    :field mgs_ext_gyr_x: ax25_frame.payload.ax25_info.body.mgs_ext_gyr_x
    :field mgs_ext_gyr_y: ax25_frame.payload.ax25_info.body.mgs_ext_gyr_y
    :field mgs_ext_gyr_z: ax25_frame.payload.ax25_info.body.mgs_ext_gyr_z
    
    :field sol_temp_zp: ax25_frame.payload.ax25_info.body.sol_temp_zp
    :field sol_temp_xp: ax25_frame.payload.ax25_info.body.sol_temp_xp
    :field sol_temp_yp: ax25_frame.payload.ax25_info.body.sol_temp_yp
    :field sol_temp_zn: ax25_frame.payload.ax25_info.body.sol_temp_zn
    :field sol_temp_xn: ax25_frame.payload.ax25_info.body.sol_temp_xn
    :field sol_temp_yn: ax25_frame.payload.ax25_info.body.sol_temp_yn
    :field sol_diode_zp: ax25_frame.payload.ax25_info.body.sol_diode_zp
    :field sol_diode_xp: ax25_frame.payload.ax25_info.body.sol_diode_xp
    :field sol_diode_yp: ax25_frame.payload.ax25_info.body.sol_diode_yp
    :field sol_diode_zn: ax25_frame.payload.ax25_info.body.sol_diode_zn
    :field sol_diode_xn: ax25_frame.payload.ax25_info.body.sol_diode_xn
    :field sol_diode_yn: ax25_frame.payload.ax25_info.body.sol_diode_yn
    
    :field atr_master_id: ax25_frame.payload.ax25_info.body.atr_master_id
    :field atr_defective_devices: ax25_frame.payload.ax25_info.body.atr_defective_devices
    :field atr_device_reset_1: ax25_frame.payload.ax25_info.body.atr_device_reset_1
    :field atr_device_reset_2: ax25_frame.payload.ax25_info.body.atr_device_reset_2
    :field atr_device_reset_3: ax25_frame.payload.ax25_info.body.atr_device_reset_3
    :field atr_device_uptime_1: ax25_frame.payload.ax25_info.body.atr_device_uptime_1
    :field atr_device_uptime_2: ax25_frame.payload.ax25_info.body.atr_device_uptime_2
    :field atr_device_uptime_3: ax25_frame.payload.ax25_info.body.atr_device_uptime_3
    :field atr_checksum: ax25_frame.payload.ax25_info.body.atr_checksum
    
    :field uhf_uptime: ax25_frame.payload.ax25_info.body.uhf_uptime
    :field uhf_uptime_tot: ax25_frame.payload.ax25_info.body.uhf_uptime_tot
    :field uhf_reset_cnt: ax25_frame.payload.ax25_info.body.uhf_reset_cnt
    :field uhf_rf_reset_cnt: ax25_frame.payload.ax25_info.body.uhf_rf_reset_cnt
    :field uhf_trx_temp: ax25_frame.payload.ax25_info.body.uhf_trx_temp
    :field uhf_rf_temp: ax25_frame.payload.ax25_info.body.uhf_rf_temp
    :field uhf_pa_temp: ax25_frame.payload.ax25_info.body.uhf_pa_temp
    :field uhf_digipeater_cnt: ax25_frame.payload.ax25_info.body.uhf_digipeater_cnt
    :field uhf_last_digipeater: ax25_frame.payload.ax25_info.body.uhf_last_digipeater
    :field uhf_rx_cnt: ax25_frame.payload.ax25_info.body.uhf_rx_cnt
    :field uhf_tx_cnt: ax25_frame.payload.ax25_info.body.uhf_tx_cnt
    :field uhf_act_rssi_raw: ax25_frame.payload.ax25_info.body.uhf_act_rssi_raw
    :field uhf_dcd_rssi_raw: ax25_frame.payload.ax25_info.body.uhf_dcd_rssi_raw
    
    :field vhf_uptime: ax25_frame.payload.ax25_info.body.vhf_uptime
    :field vhf_uptime_tot: ax25_frame.payload.ax25_info.body.vhf_uptime_tot
    :field vhf_reset_cnt: ax25_frame.payload.ax25_info.body.vhf_reset_cnt
    :field vhf_rf_reset_cnt: ax25_frame.payload.ax25_info.body.vhf_rf_reset_cnt
    :field vhf_trx_temp: ax25_frame.payload.ax25_info.body.vhf_trx_temp
    :field vhf_rf_temp: ax25_frame.payload.ax25_info.body.vhf_rf_temp
    :field vhf_pa_temp: ax25_frame.payload.ax25_info.body.vhf_pa_temp
    :field vhf_digipeater_cnt: ax25_frame.payload.ax25_info.body.vhf_digipeater_cnt
    :field vhf_last_digipeater: ax25_frame.payload.ax25_info.body.vhf_last_digipeater
    :field vhf_rx_cnt: ax25_frame.payload.ax25_info.body.vhf_rx_cnt
    :field vhf_tx_cnt: ax25_frame.payload.ax25_info.body.vhf_tx_cnt
    :field vhf_act_rssi_raw: ax25_frame.payload.ax25_info.body.vhf_act_rssi_raw
    :field vhf_dcd_rssi_raw: ax25_frame.payload.ax25_info.body.vhf_dcd_rssi_raw
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.ax25_frame = Crocube.Ax25Frame(self._io, self, self._root)

    class Psu(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.psu_pass_packet_type = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.psu_rst_cnt_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.psu_uptime_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.psu_uptime_tot_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.psu_bat_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.psu_temp_sys_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.psu_temp_bat_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.psu_cur_in_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.psu_cur_out_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.psu_ch_state_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.psu_sys_state_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.psu_gnd_wdt_str = (self._io.read_bytes_full()).decode(u"utf8")

        @property
        def psu_ch3_state(self):
            if hasattr(self, '_m_psu_ch3_state'):
                return self._m_psu_ch3_state

            self._m_psu_ch3_state = ((self.psu_ch_state_num >> 3) & 1)
            return getattr(self, '_m_psu_ch3_state', None)

        @property
        def psu_reset_cnt(self):
            if hasattr(self, '_m_psu_reset_cnt'):
                return self._m_psu_reset_cnt

            self._m_psu_reset_cnt = int(self.psu_rst_cnt_str)
            return getattr(self, '_m_psu_reset_cnt', None)

        @property
        def psu_uptime_tot(self):
            if hasattr(self, '_m_psu_uptime_tot'):
                return self._m_psu_uptime_tot

            self._m_psu_uptime_tot = int(self.psu_uptime_tot_str)
            return getattr(self, '_m_psu_uptime_tot', None)

        @property
        def psu_temp_bat(self):
            if hasattr(self, '_m_psu_temp_bat'):
                return self._m_psu_temp_bat

            self._m_psu_temp_bat = int(self.psu_temp_bat_str)
            return getattr(self, '_m_psu_temp_bat', None)

        @property
        def psu_ch5_state(self):
            if hasattr(self, '_m_psu_ch5_state'):
                return self._m_psu_ch5_state

            self._m_psu_ch5_state = ((self.psu_ch_state_num >> 5) & 1)
            return getattr(self, '_m_psu_ch5_state', None)

        @property
        def psu_ch0_state(self):
            if hasattr(self, '_m_psu_ch0_state'):
                return self._m_psu_ch0_state

            self._m_psu_ch0_state = ((self.psu_ch_state_num >> 0) & 1)
            return getattr(self, '_m_psu_ch0_state', None)

        @property
        def psu_gnd_wdt(self):
            if hasattr(self, '_m_psu_gnd_wdt'):
                return self._m_psu_gnd_wdt

            self._m_psu_gnd_wdt = int(self.psu_gnd_wdt_str)
            return getattr(self, '_m_psu_gnd_wdt', None)

        @property
        def psu_uptime(self):
            if hasattr(self, '_m_psu_uptime'):
                return self._m_psu_uptime

            self._m_psu_uptime = int(self.psu_uptime_str)
            return getattr(self, '_m_psu_uptime', None)

        @property
        def psu_sys_state(self):
            if hasattr(self, '_m_psu_sys_state'):
                return self._m_psu_sys_state

            self._m_psu_sys_state = int(self.psu_sys_state_str)
            return getattr(self, '_m_psu_sys_state', None)

        @property
        def psu_ch_state_num(self):
            if hasattr(self, '_m_psu_ch_state_num'):
                return self._m_psu_ch_state_num

            self._m_psu_ch_state_num = int(self.psu_ch_state_str, 16)
            return getattr(self, '_m_psu_ch_state_num', None)

        @property
        def psu_ch6_state(self):
            if hasattr(self, '_m_psu_ch6_state'):
                return self._m_psu_ch6_state

            self._m_psu_ch6_state = ((self.psu_ch_state_num >> 6) & 1)
            return getattr(self, '_m_psu_ch6_state', None)

        @property
        def psu_cur_out(self):
            if hasattr(self, '_m_psu_cur_out'):
                return self._m_psu_cur_out

            self._m_psu_cur_out = int(self.psu_cur_out_str)
            return getattr(self, '_m_psu_cur_out', None)

        @property
        def psu_ch2_state(self):
            if hasattr(self, '_m_psu_ch2_state'):
                return self._m_psu_ch2_state

            self._m_psu_ch2_state = ((self.psu_ch_state_num >> 2) & 1)
            return getattr(self, '_m_psu_ch2_state', None)

        @property
        def psu_temp_sys(self):
            if hasattr(self, '_m_psu_temp_sys'):
                return self._m_psu_temp_sys

            self._m_psu_temp_sys = int(self.psu_temp_sys_str)
            return getattr(self, '_m_psu_temp_sys', None)

        @property
        def psu_cur_in(self):
            if hasattr(self, '_m_psu_cur_in'):
                return self._m_psu_cur_in

            self._m_psu_cur_in = int(self.psu_cur_in_str)
            return getattr(self, '_m_psu_cur_in', None)

        @property
        def psu_ch1_state(self):
            if hasattr(self, '_m_psu_ch1_state'):
                return self._m_psu_ch1_state

            self._m_psu_ch1_state = ((self.psu_ch_state_num >> 1) & 1)
            return getattr(self, '_m_psu_ch1_state', None)

        @property
        def psu_ch4_state(self):
            if hasattr(self, '_m_psu_ch4_state'):
                return self._m_psu_ch4_state

            self._m_psu_ch4_state = ((self.psu_ch_state_num >> 4) & 1)
            return getattr(self, '_m_psu_ch4_state', None)

        @property
        def psu_battery(self):
            if hasattr(self, '_m_psu_battery'):
                return self._m_psu_battery

            self._m_psu_battery = int(self.psu_bat_str)
            return getattr(self, '_m_psu_battery', None)


    class Ax25Frame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_header = Crocube.Ax25Header(self._io, self, self._root)
            _on = (self.ax25_header.ctl & 19)
            if _on == 0:
                self.payload = Crocube.IFrame(self._io, self, self._root)
            elif _on == 3:
                self.payload = Crocube.UiFrame(self._io, self, self._root)
            elif _on == 19:
                self.payload = Crocube.UiFrame(self._io, self, self._root)
            elif _on == 16:
                self.payload = Crocube.IFrame(self._io, self, self._root)
            elif _on == 18:
                self.payload = Crocube.IFrame(self._io, self, self._root)
            elif _on == 2:
                self.payload = Crocube.IFrame(self._io, self, self._root)


    class Mgs(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.mgs_pass_packet_type = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.mgs_temp_int_mag_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.mgs_temp_int_gyr_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.mgs_int_mag_x_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.mgs_int_mag_y_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.mgs_int_mag_z_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.mgs_int_gyr_x_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.mgs_int_gyr_y_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.mgs_int_gyr_z_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.mgs_temp_ext_mag_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.mgs_temp_ext_gyr_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.mgs_ext_mag_x_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.mgs_ext_mag_y_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.mgs_ext_mag_z_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.mgs_ext_gyr_x_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.mgs_ext_gyr_y_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.mgs_ext_gyr_z_str = (self._io.read_bytes_full()).decode(u"utf8")

        @property
        def mgs_int_gyr_y(self):
            if hasattr(self, '_m_mgs_int_gyr_y'):
                return self._m_mgs_int_gyr_y

            self._m_mgs_int_gyr_y = int(self.mgs_int_gyr_y_str)
            return getattr(self, '_m_mgs_int_gyr_y', None)

        @property
        def mgs_ext_mag_x(self):
            if hasattr(self, '_m_mgs_ext_mag_x'):
                return self._m_mgs_ext_mag_x

            self._m_mgs_ext_mag_x = int(self.mgs_ext_mag_x_str)
            return getattr(self, '_m_mgs_ext_mag_x', None)

        @property
        def mgs_ext_gyr_z(self):
            if hasattr(self, '_m_mgs_ext_gyr_z'):
                return self._m_mgs_ext_gyr_z

            self._m_mgs_ext_gyr_z = int(self.mgs_ext_gyr_z_str)
            return getattr(self, '_m_mgs_ext_gyr_z', None)

        @property
        def mgs_ext_mag_z(self):
            if hasattr(self, '_m_mgs_ext_mag_z'):
                return self._m_mgs_ext_mag_z

            self._m_mgs_ext_mag_z = int(self.mgs_ext_mag_z_str)
            return getattr(self, '_m_mgs_ext_mag_z', None)

        @property
        def mgs_int_gyr_x(self):
            if hasattr(self, '_m_mgs_int_gyr_x'):
                return self._m_mgs_int_gyr_x

            self._m_mgs_int_gyr_x = int(self.mgs_int_gyr_x_str)
            return getattr(self, '_m_mgs_int_gyr_x', None)

        @property
        def mgs_temp_ext_gyr(self):
            if hasattr(self, '_m_mgs_temp_ext_gyr'):
                return self._m_mgs_temp_ext_gyr

            self._m_mgs_temp_ext_gyr = int(self.mgs_temp_ext_gyr_str)
            return getattr(self, '_m_mgs_temp_ext_gyr', None)

        @property
        def mgs_int_mag_y(self):
            if hasattr(self, '_m_mgs_int_mag_y'):
                return self._m_mgs_int_mag_y

            self._m_mgs_int_mag_y = int(self.mgs_int_mag_y_str)
            return getattr(self, '_m_mgs_int_mag_y', None)

        @property
        def mgs_ext_gyr_x(self):
            if hasattr(self, '_m_mgs_ext_gyr_x'):
                return self._m_mgs_ext_gyr_x

            self._m_mgs_ext_gyr_x = int(self.mgs_ext_gyr_x_str)
            return getattr(self, '_m_mgs_ext_gyr_x', None)

        @property
        def mgs_temp_ext_mag(self):
            if hasattr(self, '_m_mgs_temp_ext_mag'):
                return self._m_mgs_temp_ext_mag

            self._m_mgs_temp_ext_mag = int(self.mgs_temp_ext_mag_str)
            return getattr(self, '_m_mgs_temp_ext_mag', None)

        @property
        def mgs_ext_gyr_y(self):
            if hasattr(self, '_m_mgs_ext_gyr_y'):
                return self._m_mgs_ext_gyr_y

            self._m_mgs_ext_gyr_y = int(self.mgs_ext_gyr_y_str)
            return getattr(self, '_m_mgs_ext_gyr_y', None)

        @property
        def mgs_temp_int_gyr(self):
            if hasattr(self, '_m_mgs_temp_int_gyr'):
                return self._m_mgs_temp_int_gyr

            self._m_mgs_temp_int_gyr = int(self.mgs_temp_int_gyr_str)
            return getattr(self, '_m_mgs_temp_int_gyr', None)

        @property
        def mgs_temp_int_mag(self):
            if hasattr(self, '_m_mgs_temp_int_mag'):
                return self._m_mgs_temp_int_mag

            self._m_mgs_temp_int_mag = int(self.mgs_temp_int_mag_str)
            return getattr(self, '_m_mgs_temp_int_mag', None)

        @property
        def mgs_int_mag_z(self):
            if hasattr(self, '_m_mgs_int_mag_z'):
                return self._m_mgs_int_mag_z

            self._m_mgs_int_mag_z = int(self.mgs_int_mag_z_str)
            return getattr(self, '_m_mgs_int_mag_z', None)

        @property
        def mgs_int_mag_x(self):
            if hasattr(self, '_m_mgs_int_mag_x'):
                return self._m_mgs_int_mag_x

            self._m_mgs_int_mag_x = int(self.mgs_int_mag_x_str)
            return getattr(self, '_m_mgs_int_mag_x', None)

        @property
        def mgs_ext_mag_y(self):
            if hasattr(self, '_m_mgs_ext_mag_y'):
                return self._m_mgs_ext_mag_y

            self._m_mgs_ext_mag_y = int(self.mgs_ext_mag_y_str)
            return getattr(self, '_m_mgs_ext_mag_y', None)

        @property
        def mgs_int_gyr_z(self):
            if hasattr(self, '_m_mgs_int_gyr_z'):
                return self._m_mgs_int_gyr_z

            self._m_mgs_int_gyr_z = int(self.mgs_int_gyr_z_str)
            return getattr(self, '_m_mgs_int_gyr_z', None)


    class Ax25Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dest_callsign_raw = Crocube.CallsignRaw(self._io, self, self._root)
            self.dest_ssid_raw = Crocube.SsidMask(self._io, self, self._root)
            self.src_callsign_raw = Crocube.CallsignRaw(self._io, self, self._root)
            self.src_ssid_raw = Crocube.SsidMask(self._io, self, self._root)
            if (self.src_ssid_raw.ssid_mask & 1) == 0:
                self.repeater = Crocube.Repeater(self._io, self, self._root)

            self.ctl = self._io.read_u1()


    class UiFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self._raw_ax25_info = self._io.read_bytes_full()
            _io__raw_ax25_info = KaitaiStream(BytesIO(self._raw_ax25_info))
            self.ax25_info = Crocube.Tlm(_io__raw_ax25_info, self, self._root)


    class Callsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")
            if not  ((self.callsign == u"9A0CC ") or (self.callsign == u"CQ    ")) :
                raise kaitaistruct.ValidationNotAnyOfError(self.callsign, self._io, u"/types/callsign/seq/0")


    class Uhf(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.uhf_packet_id_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.uhf_uptime_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.uhf_uptime_tot_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.uhf_reset_cnt_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.uhf_rf_reset_cnt_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.uhf_trx_temp_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.uhf_rf_temp_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.uhf_pa_temp_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.uhf_digipeater_cnt_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.uhf_last_digipeater_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.uhf_rx_cnt_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.uhf_tx_cnt_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.uhf_act_rssi_raw_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.uhf_dcd_rssi_raw_str = (self._io.read_bytes_term(0, False, True, True)).decode(u"utf8")

        @property
        def uhf_rf_reset_cnt(self):
            if hasattr(self, '_m_uhf_rf_reset_cnt'):
                return self._m_uhf_rf_reset_cnt

            self._m_uhf_rf_reset_cnt = int(self.uhf_rf_reset_cnt_str)
            return getattr(self, '_m_uhf_rf_reset_cnt', None)

        @property
        def uhf_act_rssi_raw(self):
            if hasattr(self, '_m_uhf_act_rssi_raw'):
                return self._m_uhf_act_rssi_raw

            self._m_uhf_act_rssi_raw = int(self.uhf_act_rssi_raw_str)
            return getattr(self, '_m_uhf_act_rssi_raw', None)

        @property
        def uhf_last_digipeater(self):
            if hasattr(self, '_m_uhf_last_digipeater'):
                return self._m_uhf_last_digipeater

            self._m_uhf_last_digipeater = self.uhf_last_digipeater_str
            return getattr(self, '_m_uhf_last_digipeater', None)

        @property
        def uhf_pa_temp(self):
            if hasattr(self, '_m_uhf_pa_temp'):
                return self._m_uhf_pa_temp

            self._m_uhf_pa_temp = int(self.uhf_pa_temp_str)
            return getattr(self, '_m_uhf_pa_temp', None)

        @property
        def uhf_uptime_tot(self):
            if hasattr(self, '_m_uhf_uptime_tot'):
                return self._m_uhf_uptime_tot

            self._m_uhf_uptime_tot = int(self.uhf_uptime_tot_str)
            return getattr(self, '_m_uhf_uptime_tot', None)

        @property
        def uhf_tx_cnt(self):
            if hasattr(self, '_m_uhf_tx_cnt'):
                return self._m_uhf_tx_cnt

            self._m_uhf_tx_cnt = int(self.uhf_tx_cnt_str)
            return getattr(self, '_m_uhf_tx_cnt', None)

        @property
        def uhf_rf_temp(self):
            if hasattr(self, '_m_uhf_rf_temp'):
                return self._m_uhf_rf_temp

            self._m_uhf_rf_temp = int(self.uhf_rf_temp_str)
            return getattr(self, '_m_uhf_rf_temp', None)

        @property
        def uhf_dcd_rssi_raw(self):
            if hasattr(self, '_m_uhf_dcd_rssi_raw'):
                return self._m_uhf_dcd_rssi_raw

            self._m_uhf_dcd_rssi_raw = int(self.uhf_dcd_rssi_raw_str)
            return getattr(self, '_m_uhf_dcd_rssi_raw', None)

        @property
        def uhf_uptime(self):
            if hasattr(self, '_m_uhf_uptime'):
                return self._m_uhf_uptime

            self._m_uhf_uptime = int(self.uhf_uptime_str)
            return getattr(self, '_m_uhf_uptime', None)

        @property
        def uhf_rx_cnt(self):
            if hasattr(self, '_m_uhf_rx_cnt'):
                return self._m_uhf_rx_cnt

            self._m_uhf_rx_cnt = int(self.uhf_rx_cnt_str)
            return getattr(self, '_m_uhf_rx_cnt', None)

        @property
        def uhf_reset_cnt(self):
            if hasattr(self, '_m_uhf_reset_cnt'):
                return self._m_uhf_reset_cnt

            self._m_uhf_reset_cnt = int(self.uhf_reset_cnt_str)
            return getattr(self, '_m_uhf_reset_cnt', None)

        @property
        def uhf_digipeater_cnt(self):
            if hasattr(self, '_m_uhf_digipeater_cnt'):
                return self._m_uhf_digipeater_cnt

            self._m_uhf_digipeater_cnt = int(self.uhf_digipeater_cnt_str)
            return getattr(self, '_m_uhf_digipeater_cnt', None)

        @property
        def uhf_trx_temp(self):
            if hasattr(self, '_m_uhf_trx_temp'):
                return self._m_uhf_trx_temp

            self._m_uhf_trx_temp = int(self.uhf_trx_temp_str)
            return getattr(self, '_m_uhf_trx_temp', None)


    class IFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self._raw_ax25_info = self._io.read_bytes_full()
            _io__raw_ax25_info = KaitaiStream(BytesIO(self._raw_ax25_info))
            self.ax25_info = Crocube.Tlm(_io__raw_ax25_info, self, self._root)


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


    class Vhf(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.vhf_packet_id_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.vhf_uptime_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.vhf_uptime_tot_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.vhf_reset_cnt_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.vhf_rf_reset_cnt_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.vhf_trx_temp_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.vhf_rf_temp_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.vhf_pa_temp_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.vhf_digipeater_cnt_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.vhf_last_digipeater_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.vhf_rx_cnt_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.vhf_tx_cnt_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.vhf_act_rssi_raw_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.vhf_dcd_rssi_raw_str = (self._io.read_bytes_term(0, False, True, True)).decode(u"utf8")

        @property
        def vhf_digipeater_cnt(self):
            if hasattr(self, '_m_vhf_digipeater_cnt'):
                return self._m_vhf_digipeater_cnt

            self._m_vhf_digipeater_cnt = int(self.vhf_digipeater_cnt_str)
            return getattr(self, '_m_vhf_digipeater_cnt', None)

        @property
        def vhf_tx_cnt(self):
            if hasattr(self, '_m_vhf_tx_cnt'):
                return self._m_vhf_tx_cnt

            self._m_vhf_tx_cnt = int(self.vhf_tx_cnt_str)
            return getattr(self, '_m_vhf_tx_cnt', None)

        @property
        def vhf_rx_cnt(self):
            if hasattr(self, '_m_vhf_rx_cnt'):
                return self._m_vhf_rx_cnt

            self._m_vhf_rx_cnt = int(self.vhf_rx_cnt_str)
            return getattr(self, '_m_vhf_rx_cnt', None)

        @property
        def vhf_last_digipeater(self):
            if hasattr(self, '_m_vhf_last_digipeater'):
                return self._m_vhf_last_digipeater

            self._m_vhf_last_digipeater = self.vhf_last_digipeater_str
            return getattr(self, '_m_vhf_last_digipeater', None)

        @property
        def vhf_pa_temp(self):
            if hasattr(self, '_m_vhf_pa_temp'):
                return self._m_vhf_pa_temp

            self._m_vhf_pa_temp = int(self.vhf_pa_temp_str)
            return getattr(self, '_m_vhf_pa_temp', None)

        @property
        def vhf_uptime(self):
            if hasattr(self, '_m_vhf_uptime'):
                return self._m_vhf_uptime

            self._m_vhf_uptime = int(self.vhf_uptime_str)
            return getattr(self, '_m_vhf_uptime', None)

        @property
        def vhf_rf_temp(self):
            if hasattr(self, '_m_vhf_rf_temp'):
                return self._m_vhf_rf_temp

            self._m_vhf_rf_temp = int(self.vhf_rf_temp_str)
            return getattr(self, '_m_vhf_rf_temp', None)

        @property
        def vhf_uptime_tot(self):
            if hasattr(self, '_m_vhf_uptime_tot'):
                return self._m_vhf_uptime_tot

            self._m_vhf_uptime_tot = int(self.vhf_uptime_tot_str)
            return getattr(self, '_m_vhf_uptime_tot', None)

        @property
        def vhf_trx_temp(self):
            if hasattr(self, '_m_vhf_trx_temp'):
                return self._m_vhf_trx_temp

            self._m_vhf_trx_temp = int(self.vhf_trx_temp_str)
            return getattr(self, '_m_vhf_trx_temp', None)

        @property
        def vhf_rf_reset_cnt(self):
            if hasattr(self, '_m_vhf_rf_reset_cnt'):
                return self._m_vhf_rf_reset_cnt

            self._m_vhf_rf_reset_cnt = int(self.vhf_rf_reset_cnt_str)
            return getattr(self, '_m_vhf_rf_reset_cnt', None)

        @property
        def vhf_dcd_rssi_raw(self):
            if hasattr(self, '_m_vhf_dcd_rssi_raw'):
                return self._m_vhf_dcd_rssi_raw

            self._m_vhf_dcd_rssi_raw = int(self.vhf_dcd_rssi_raw_str)
            return getattr(self, '_m_vhf_dcd_rssi_raw', None)

        @property
        def vhf_reset_cnt(self):
            if hasattr(self, '_m_vhf_reset_cnt'):
                return self._m_vhf_reset_cnt

            self._m_vhf_reset_cnt = int(self.vhf_reset_cnt_str)
            return getattr(self, '_m_vhf_reset_cnt', None)

        @property
        def vhf_act_rssi_raw(self):
            if hasattr(self, '_m_vhf_act_rssi_raw'):
                return self._m_vhf_act_rssi_raw

            self._m_vhf_act_rssi_raw = int(self.vhf_act_rssi_raw_str)
            return getattr(self, '_m_vhf_act_rssi_raw', None)


    class Repeaters(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rpt_callsign_raw = Crocube.CallsignRaw(self._io, self, self._root)
            self.rpt_ssid_raw = Crocube.SsidMask(self._io, self, self._root)


    class Repeater(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rpt_instance = []
            i = 0
            while True:
                _ = Crocube.Repeaters(self._io, self, self._root)
                self.rpt_instance.append(_)
                if (_.rpt_ssid_raw.ssid_mask & 1) == 1:
                    break
                i += 1


    class Msg(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.message = (self._io.read_bytes_full()).decode(u"utf8")


    class Obc(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.obc_pass_packet_type = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.obc_rst_cnt_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.obc_uptime_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.obc_uptime_tot_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.obc_bat_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.obc_temp_mcu_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.obc_freemem_str = (self._io.read_bytes_full()).decode(u"utf8")

        @property
        def obc_uptime(self):
            if hasattr(self, '_m_obc_uptime'):
                return self._m_obc_uptime

            self._m_obc_uptime = int(self.obc_uptime_str)
            return getattr(self, '_m_obc_uptime', None)

        @property
        def obc_freemem(self):
            if hasattr(self, '_m_obc_freemem'):
                return self._m_obc_freemem

            self._m_obc_freemem = int(self.obc_freemem_str)
            return getattr(self, '_m_obc_freemem', None)

        @property
        def obc_bat(self):
            if hasattr(self, '_m_obc_bat'):
                return self._m_obc_bat

            self._m_obc_bat = int(self.obc_bat_str)
            return getattr(self, '_m_obc_bat', None)

        @property
        def obc_uptime_tot(self):
            if hasattr(self, '_m_obc_uptime_tot'):
                return self._m_obc_uptime_tot

            self._m_obc_uptime_tot = int(self.obc_uptime_tot_str)
            return getattr(self, '_m_obc_uptime_tot', None)

        @property
        def obc_reset_cnt(self):
            if hasattr(self, '_m_obc_reset_cnt'):
                return self._m_obc_reset_cnt

            self._m_obc_reset_cnt = int(self.obc_rst_cnt_str)
            return getattr(self, '_m_obc_reset_cnt', None)

        @property
        def obc_temp_mcu(self):
            if hasattr(self, '_m_obc_temp_mcu'):
                return self._m_obc_temp_mcu

            self._m_obc_temp_mcu = int(self.obc_temp_mcu_str)
            return getattr(self, '_m_obc_temp_mcu', None)


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
            self.callsign_ror = Crocube.Callsign(_io__raw_callsign_ror, self, self._root)


    class Atr(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.atr_pass_packet_type = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.atr_master_id_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.atr_defective_devices_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.atr_device_reset_1_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.atr_device_reset_2_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.atr_device_reset_3_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.atr_device_uptime_1_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.atr_device_uptime_2_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.atr_device_uptime_3_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.atr_checksum_str = (self._io.read_bytes_full()).decode(u"utf8")

        @property
        def atr_device_reset_2(self):
            if hasattr(self, '_m_atr_device_reset_2'):
                return self._m_atr_device_reset_2

            self._m_atr_device_reset_2 = int(self.atr_device_reset_2_str)
            return getattr(self, '_m_atr_device_reset_2', None)

        @property
        def atr_device_reset_1(self):
            if hasattr(self, '_m_atr_device_reset_1'):
                return self._m_atr_device_reset_1

            self._m_atr_device_reset_1 = int(self.atr_device_reset_1_str)
            return getattr(self, '_m_atr_device_reset_1', None)

        @property
        def atr_master_id(self):
            if hasattr(self, '_m_atr_master_id'):
                return self._m_atr_master_id

            self._m_atr_master_id = int(self.atr_master_id_str)
            return getattr(self, '_m_atr_master_id', None)

        @property
        def atr_checksum(self):
            if hasattr(self, '_m_atr_checksum'):
                return self._m_atr_checksum

            self._m_atr_checksum = int(self.atr_checksum_str)
            return getattr(self, '_m_atr_checksum', None)

        @property
        def atr_device_uptime_3(self):
            if hasattr(self, '_m_atr_device_uptime_3'):
                return self._m_atr_device_uptime_3

            self._m_atr_device_uptime_3 = int(self.atr_device_uptime_3_str)
            return getattr(self, '_m_atr_device_uptime_3', None)

        @property
        def atr_device_reset_3(self):
            if hasattr(self, '_m_atr_device_reset_3'):
                return self._m_atr_device_reset_3

            self._m_atr_device_reset_3 = int(self.atr_device_reset_3_str)
            return getattr(self, '_m_atr_device_reset_3', None)

        @property
        def atr_defective_devices(self):
            if hasattr(self, '_m_atr_defective_devices'):
                return self._m_atr_defective_devices

            self._m_atr_defective_devices = int(self.atr_defective_devices_str)
            return getattr(self, '_m_atr_defective_devices', None)

        @property
        def atr_device_uptime_2(self):
            if hasattr(self, '_m_atr_device_uptime_2'):
                return self._m_atr_device_uptime_2

            self._m_atr_device_uptime_2 = int(self.atr_device_uptime_2_str)
            return getattr(self, '_m_atr_device_uptime_2', None)

        @property
        def atr_device_uptime_1(self):
            if hasattr(self, '_m_atr_device_uptime_1'):
                return self._m_atr_device_uptime_1

            self._m_atr_device_uptime_1 = int(self.atr_device_uptime_1_str)
            return getattr(self, '_m_atr_device_uptime_1', None)


    class Tlm(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            _on = self.packet_type_q
            if _on == 77:
                self.body = Crocube.Mgs(self._io, self, self._root)
            elif _on == 85:
                self.body = Crocube.Uhf(self._io, self, self._root)
            elif _on == 86:
                self.body = Crocube.Vhf(self._io, self, self._root)
            elif _on == 83:
                self.body = Crocube.Sol(self._io, self, self._root)
            elif _on == 65:
                self.body = Crocube.Atr(self._io, self, self._root)
            elif _on == 79:
                self.body = Crocube.Obc(self._io, self, self._root)
            elif _on == 80:
                self.body = Crocube.Psu(self._io, self, self._root)
            else:
                self.body = Crocube.Msg(self._io, self, self._root)

        @property
        def monitor(self):
            if hasattr(self, '_m_monitor'):
                return self._m_monitor

            _pos = self._io.pos()
            self._io.seek(0)
            self._m_monitor = (self._io.read_bytes_full()).decode(u"ASCII")
            self._io.seek(_pos)
            return getattr(self, '_m_monitor', None)

        @property
        def packet_type_q(self):
            if hasattr(self, '_m_packet_type_q'):
                return self._m_packet_type_q

            _pos = self._io.pos()
            self._io.seek(0)
            self._m_packet_type_q = self._io.read_u1()
            self._io.seek(_pos)
            return getattr(self, '_m_packet_type_q', None)


    class Sol(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sol_pass_packet_type = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sol_temp_zp_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sol_temp_xp_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sol_temp_yp_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sol_temp_zn_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sol_temp_xn_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sol_temp_yn_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sol_diode_zp_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sol_diode_xp_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sol_diode_yp_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sol_diode_zn_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sol_diode_xn_str = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sol_diode_yn_str = (self._io.read_bytes_full()).decode(u"utf8")

        @property
        def sol_temp_zp(self):
            if hasattr(self, '_m_sol_temp_zp'):
                return self._m_sol_temp_zp

            self._m_sol_temp_zp = int(self.sol_temp_zp_str)
            return getattr(self, '_m_sol_temp_zp', None)

        @property
        def sol_diode_zn(self):
            if hasattr(self, '_m_sol_diode_zn'):
                return self._m_sol_diode_zn

            self._m_sol_diode_zn = int(self.sol_diode_zn_str)
            return getattr(self, '_m_sol_diode_zn', None)

        @property
        def sol_diode_xp(self):
            if hasattr(self, '_m_sol_diode_xp'):
                return self._m_sol_diode_xp

            self._m_sol_diode_xp = int(self.sol_diode_xp_str)
            return getattr(self, '_m_sol_diode_xp', None)

        @property
        def sol_temp_zn(self):
            if hasattr(self, '_m_sol_temp_zn'):
                return self._m_sol_temp_zn

            self._m_sol_temp_zn = int(self.sol_temp_zn_str)
            return getattr(self, '_m_sol_temp_zn', None)

        @property
        def sol_diode_yn(self):
            if hasattr(self, '_m_sol_diode_yn'):
                return self._m_sol_diode_yn

            self._m_sol_diode_yn = int(self.sol_diode_yn_str)
            return getattr(self, '_m_sol_diode_yn', None)

        @property
        def sol_temp_yn(self):
            if hasattr(self, '_m_sol_temp_yn'):
                return self._m_sol_temp_yn

            self._m_sol_temp_yn = int(self.sol_temp_yn_str)
            return getattr(self, '_m_sol_temp_yn', None)

        @property
        def sol_diode_zp(self):
            if hasattr(self, '_m_sol_diode_zp'):
                return self._m_sol_diode_zp

            self._m_sol_diode_zp = int(self.sol_diode_zp_str)
            return getattr(self, '_m_sol_diode_zp', None)

        @property
        def sol_temp_xn(self):
            if hasattr(self, '_m_sol_temp_xn'):
                return self._m_sol_temp_xn

            self._m_sol_temp_xn = int(self.sol_temp_xn_str)
            return getattr(self, '_m_sol_temp_xn', None)

        @property
        def sol_diode_xn(self):
            if hasattr(self, '_m_sol_diode_xn'):
                return self._m_sol_diode_xn

            self._m_sol_diode_xn = int(self.sol_diode_xn_str)
            return getattr(self, '_m_sol_diode_xn', None)

        @property
        def sol_diode_yp(self):
            if hasattr(self, '_m_sol_diode_yp'):
                return self._m_sol_diode_yp

            self._m_sol_diode_yp = int(self.sol_diode_yp_str)
            return getattr(self, '_m_sol_diode_yp', None)

        @property
        def sol_temp_xp(self):
            if hasattr(self, '_m_sol_temp_xp'):
                return self._m_sol_temp_xp

            self._m_sol_temp_xp = int(self.sol_temp_xp_str)
            return getattr(self, '_m_sol_temp_xp', None)

        @property
        def sol_temp_yp(self):
            if hasattr(self, '_m_sol_temp_yp'):
                return self._m_sol_temp_yp

            self._m_sol_temp_yp = int(self.sol_temp_yp_str)
            return getattr(self, '_m_sol_temp_yp', None)



