import logging; logging.basicConfig(level=logging.DEBUG); logger = logging.getLogger(__name__)
import struct

from pyasn1.codec.ber.encoder import encode as asn1_encode
from pyasn1.codec.der.decoder import decode as asn1_decode
import pyasn1.error


TML_SLE_FORMAT = '!ii'
TML_SLE_TYPE = 0x01000000


class SleCoding:

    def __init__(self, decode_spec):
        self.decode_spec = decode_spec

    def encode(self, pdu):
        en = asn1_encode(pdu)
        return struct.pack(
            TML_SLE_FORMAT,
            TML_SLE_TYPE,
            len(en),
        ) + en

    def decode(self, msg):
        hdr, body = msg[:8], msg[8:]

        try:
            return asn1_decode(body, asn1Spec=self.decode_spec)[0]
        except pyasn1.error.PyAsn1Error:
            logger.error('Unable to decode PDU. Skipping ...')
        except TypeError:
            logger.error('Unable to decode PDU due to type error ...')
        return None
