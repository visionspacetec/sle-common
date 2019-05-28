from pyasn1.type import univ, namedtype, tag, constraint

from .common import ConditionalTime, Credentials, InvokeId, IntUnsignedLong,\
    SpaceLinkDataUnit, Time
from .pdu import SleScheduleStatusReportInvocation, SleStopInvocation,\
    SleAcknowledgement, SleScheduleStatusReportReturn
from .raf_structure import RafParameterName, RequestedFrameQuality, AntennaId,\
    CarrierLockStatus, DiagnosticRafGet, DiagnosticRafStart, FrameQuality,\
    FrameSyncLockStatus, LockStatus, Notification, RafGetParameter,\
    RafProductionStatus, SymbolLockStatus
from .bind import SleBindInvocation, SleBindReturn, SlePeerAbort,\
    SleUnbindInvocation, SleUnbindReturn


# Incoming PDUs

class RafStartInvocation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('invokerCredentials', Credentials()),
        namedtype.NamedType('invokeId', InvokeId()),
        namedtype.NamedType('startTime', ConditionalTime()),
        namedtype.NamedType('stopTime', ConditionalTime()),
        namedtype.NamedType('requestedFrameQuality', RequestedFrameQuality())
    )


class RafGetParameterInvocation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('invokerCredentials', Credentials()),
        namedtype.NamedType('invokeId', InvokeId()),
        namedtype.NamedType('rafParameter', RafParameterName())
    )


class RafUsertoProviderPdu(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('rafBindInvocation', SleBindInvocation().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 100))),
        namedtype.NamedType('rafBindReturn', SleBindReturn().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 101))),
        namedtype.NamedType(
            'rafUnbindInvocation', SleUnbindInvocation().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 102))),
        namedtype.NamedType('rafUnbindReturn', SleUnbindReturn().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 103))),
        namedtype.NamedType('rafStartInvocation', RafStartInvocation().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 0))),
        namedtype.NamedType('rafStopInvocation', SleStopInvocation().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 2))),
        namedtype.NamedType(
            'rafScheduleStatusReportInvocation',
            SleScheduleStatusReportInvocation().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 4))),
        namedtype.NamedType(
            'rafGetParameterInvocation', RafGetParameterInvocation().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 6))),
        namedtype.NamedType('rafPeerAbortInvocation', SlePeerAbort().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 104)))
    )


# Outgoing PDUs

class RafStartReturn(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('performerCredentials', Credentials()),
        namedtype.NamedType('invokeId', InvokeId()),
        namedtype.NamedType('result', univ.Choice(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType(
                    'positiveResult', univ.Null().subtype(
                        implicitTag=tag.Tag(
                            tag.tagClassContext, tag.tagFormatSimple, 0))),
                namedtype.NamedType(
                    'negativeResult', DiagnosticRafStart().subtype(
                        implicitTag=tag.Tag(
                            tag.tagClassContext, tag.tagFormatConstructed, 1)))
            )))
    )


class RafTransferDataInvocation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('invokerCredentials', Credentials()),
        namedtype.NamedType('earthReceiveTime', Time()),
        namedtype.NamedType('antennaId', AntennaId()),
        namedtype.NamedType('dataLinkContinuity', univ.Integer().subtype(
            subtypeSpec=constraint.ValueRangeConstraint(-1, 16777215))),
        namedtype.NamedType('deliveredFrameQuality', FrameQuality()),
        namedtype.NamedType('privateAnnotation', univ.Choice(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('null', univ.Null().subtype(
                    implicitTag=tag.Tag(
                        tag.tagClassContext, tag.tagFormatSimple, 0))),
                namedtype.NamedType('notNull', univ.OctetString().subtype(
                    subtypeSpec=constraint.ValueSizeConstraint(
                        1, 128)).subtype(
                            implicitTag=tag.Tag(
                                tag.tagClassContext, tag.tagFormatSimple, 1)))
            ))),
        namedtype.NamedType('data', SpaceLinkDataUnit())
    )


class RafSyncNotifyInvocation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('invokerCredentials', Credentials()),
        namedtype.NamedType('notification', Notification())
    )


class FrameOrNotification(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'annotatedFrame', RafTransferDataInvocation().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 0))),
        namedtype.NamedType(
            'syncNotification', RafSyncNotifyInvocation().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 1)))
    )


class RafTransferBuffer(univ.SequenceOf):
    componentType = FrameOrNotification()


class RafStatusReportInvocation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('invokerCredentials', Credentials()),
        namedtype.NamedType('errorFreeFrameNumber', IntUnsignedLong()),
        namedtype.NamedType('deliveredFrameNumber', IntUnsignedLong()),
        namedtype.NamedType('frameSyncLockStatus', FrameSyncLockStatus()),
        namedtype.NamedType('symbolSyncLockStatus', SymbolLockStatus()),
        namedtype.NamedType('subcarrierLockStatus', LockStatus()),
        namedtype.NamedType('carrierLockStatus', CarrierLockStatus()),
        namedtype.NamedType('productionStatus', RafProductionStatus())
    )


class RafGetParameterReturn(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('performerCredentials', Credentials()),
        namedtype.NamedType('invokeId', InvokeId()),
        namedtype.NamedType('result', univ.Choice(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType(
                    'positiveResult', RafGetParameter().subtype(
                        implicitTag=tag.Tag(
                            tag.tagClassContext,
                            tag.tagFormatConstructed, 0))),
                namedtype.NamedType(
                    'negativeResult', DiagnosticRafGet().subtype(
                        implicitTag=tag.Tag(
                            tag.tagClassContext, tag.tagFormatConstructed, 1)))
            )))
    )


class RafProvidertoUserPdu(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('rafBindInvocation', SleBindInvocation().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 100))),
        namedtype.NamedType('rafBindReturn', SleBindReturn().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 101))),
        namedtype.NamedType(
            'rafUnbindInvocation', SleUnbindInvocation().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 102))),
        namedtype.NamedType('rafUnbindReturn', SleUnbindReturn().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 103))),
        namedtype.NamedType('rafStartReturn', RafStartReturn().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 1))),
        namedtype.NamedType('rafStopReturn', SleAcknowledgement().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 3))),
        namedtype.NamedType('rafTransferBuffer', RafTransferBuffer().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 8))),
        namedtype.NamedType(
            'rafScheduleStatusReportReturn',
            SleScheduleStatusReportReturn().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 5))),
        namedtype.NamedType(
            'rafStatusReportInvocation', RafStatusReportInvocation().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 9))),
        namedtype.NamedType(
            'rafGetParameterReturn', RafGetParameterReturn().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 7))),
        namedtype.NamedType('rafPeerAbortInvocation', SlePeerAbort().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 104)))
    )
