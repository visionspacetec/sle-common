import datetime as dt
import random
import struct
import hashlib

from pyasn1.codec.ber.encoder import encode as asn1_encode
from pyasn1.codec.der.encoder import encode as asn1_der_encode
from pyasn1.codec.der.decoder import decode as asn1_decode

from slecommon.datatypes.security import HashInput, Isp1Credentials


def make_credentials(initiator_id, password):
    """Makes credentials for the initiator"""
    now = dt.datetime.utcnow()
    random_number = random.randint(0, 2147483647)
    return _generate_encoded_credentials(
        now, random_number, initiator_id, password)


def _generate_encoded_credentials(
        current_time, random_number, username, password):
    """Generates encoded ISP1 credentials"""
    hash_input = HashInput()
    days = (current_time - dt.datetime(1958, 1, 1)).days
    millisecs = 1000 * (
        current_time - current_time.replace(
            hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    microsecs = int(round(millisecs % 1 * 1000))
    millisecs = int(millisecs)
    credential_time = struct.pack('!HIH', days, millisecs, microsecs)
    hash_input['time'] = credential_time
    hash_input['randomNumber'] = random_number
    hash_input['userName'] = username
    hash_input['passWord'] = bytes.fromhex(password)
    der_encoded_hash_input = asn1_der_encode(hash_input)

    # TODO: check if SHA1 or SHA256 to be used
    the_protected = bytearray.fromhex(
        hashlib.sha1(der_encoded_hash_input).hexdigest())

    isp1_creds = Isp1Credentials()
    isp1_creds['time'] = credential_time
    isp1_creds['randomNumber'] = random_number
    isp1_creds['theProtected'] = the_protected

    return asn1_encode(isp1_creds)


def check_return_credentials(
        responder_performer_credentials,
        responder_id, responder_password,
        initiator_id, initiator_password):
    decoded_credentials = asn1_decode(
        responder_performer_credentials.asOctets(),
        asn1Spec=Isp1Credentials())[0]
    days, ms, us = struct.unpack(
        '!HIH', bytearray(decoded_credentials['time'].asNumbers()))
    time_delta = dt.timedelta(days=days, milliseconds=ms, microseconds=us)
    cred_time = time_delta + dt.datetime(1958, 1, 1)
    random_number = int(decoded_credentials['randomNumber'])
    performer_credentials = _generate_encoded_credentials(
        cred_time, random_number, responder_id, responder_password)
    return performer_credentials == responder_performer_credentials.asOctets()


def check_invoke_credentials(
        initiator_invoker_credentials,
        initiator_id, initiator_password):
    decoded_credentials = asn1_decode(initiator_invoker_credentials.asOctets(),
                                      asn1Spec=Isp1Credentials())[0]
    days, ms, us = struct.unpack('!HIH', bytearray(decoded_credentials['time'].asNumbers()))
    time_delta = dt.timedelta(days=days, milliseconds=ms, microseconds=us)
    cred_time = time_delta + dt.datetime(1958, 1, 1)
    random_number = int(decoded_credentials['randomNumber'])
    invoker_credentials = _generate_encoded_credentials(
        cred_time, random_number, initiator_id, initiator_password)
    return invoker_credentials == initiator_invoker_credentials.asOctets()
