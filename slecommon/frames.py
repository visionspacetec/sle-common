import logging; logging.basicConfig(level=logging.DEBUG); logger = logging.getLogger(__name__)
from bitstring import BitArray

idle_space_packet = BitArray('0x07ffc00000390000000000000000000000000000000000000000000000000000000000000000000000'
                             '0000000000000000000000000000000000000000000000')


class TelemetryTransferFrame(dict):

    def __init__(self, data=None, frame_error_control_field=False):
        super().__init__()
        self._data = []
        self.has_fecf = frame_error_control_field
        self.is_idle = False
        self.has_no_pkts = False
        if data:
            self.decode(data)
            self._data = data
            self.length = int(len(data[2:])/2)

    def decode(self, data):
        """Decode data as a TM Transfer Frame"""
        hdr = BitArray(data[:14])
        self['version'] = hdr[0:2].uint
        self['spacecraft_id'] = hdr[2:12].uint
        self['virtual_channel_id'] = hdr[12:15].uint
        self['ocf_flag'] = hdr[15]
        self['master_chan_frame_count'] = hdr[16:24].uint
        self['virtual_chan_frame_count'] = hdr[24:32].uint
        self['sec_header_flag'] = hdr[32]
        self['sync_flag'] = hdr[33]
        self['pkt_order_flag'] = hdr[34]
        self['seg_len_id'] = hdr[35:37].uint
        self['first_hdr_ptr'] = hdr[37:48].uint

        if self['ocf_flag']:
            if self.has_fecf:
                self['ocf'] = BitArray('0x' + data[-12:-4])
            else:
                self['ocf'] = BitArray('0x' + data[-8:])

        if self.has_fecf:
            self['fecf'] = BitArray('0x' + data[-4:])

        # idle frame received
        if self['first_hdr_ptr'] == int('11111111110', 2):
            self.is_idle = True
            return

        if self['first_hdr_ptr'] == int('11111111111', 2):
            self.has_no_pkts = True
            return

        if self['sec_header_flag']:
            raise NotImplementedError

    def encode(self):
        try:
            tm_frame = BitArray()
            tm_frame.append(format(self['version'], '#04b'))
            tm_frame.append(format(self['spacecraft_id'], '#012b'))
            tm_frame.append(format(self['virtual_channel_id'], '#05b'))
            tm_frame.append(format(self['ocf_flag'], '#03b'))
            tm_frame.append(format(self['master_chan_frame_count'], '#010b'))
            tm_frame.append(format(self['virtual_chan_frame_count'], '#010b'))
            tm_frame.append(format(self['sec_header_flag'], '#03b'))
            tm_frame.append(format(self['sync_flag'], '#03b'))
            tm_frame.append(format(self['pkt_order_flag'], '#03b'))
            tm_frame.append(format(self['seg_len_id'], '#04b'))
            tm_frame.append(format(self['first_hdr_ptr'], '#013b'))

            if self['sec_header_flag']:
                raise NotImplementedError
            offset = tm_frame.length
            if self['ocf_flag']:
                offset += 32
            if self.has_fecf:
                offset += 16
            if self.has_no_pkts is True:
                tm_frame.append(format(0, '#0{}b'.format((self.length * 8 - offset) + 2)))
            elif self.is_idle is True:

                tm_frame.append(idle_space_packet)
                offset += idle_space_packet.length
                tm_frame.append(format(0, '#0{}b'.format((self.length * 8 - offset) + 2)))
            else:
                raise NotImplementedError
            if self['ocf_flag']:
                tm_frame.append(self['ocf'])
            if self.has_fecf:
                self['fecf'] = format(self._calculate_fecf(bytearray.fromhex(tm_frame.hex)), '#018b')
                tm_frame.append(self['fecf'])
            return tm_frame.hex
        except Exception as e:
            print(e)

    def _calculate_fecf(self, byte_array):
        shift_register = 0x0000FFFF
        polynomial = 0x00001021
        array_size = len(byte_array)
        index = 0
        while index < array_size:
            next_byte = byte_array[index]
            bit_number = 7
            while bit_number >= 0:
                mask = (1 << bit_number)
                if (next_byte & mask) > 0:
                    h = 0x00010000
                else:
                    h = 0
                shift_register <<= 1
                if (h ^ (shift_register & 0x00010000)) > 0:
                    shift_register ^= polynomial
                bit_number -= 1
            index += 1
        return shift_register & 0x0000FFFF
