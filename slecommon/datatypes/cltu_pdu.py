from pyasn1.type import univ, namedtype, tag, constraint

from .common import ConditionalTime, Credentials, Duration, IntPosShort,\
    InvokeId, SlduStatusNotification, Time
from .pdu import SleScheduleStatusReportInvocation, SleStopInvocation,\
    SleAcknowledgement, SleScheduleStatusReportReturn
from .cltu_structure import CltuData, CltuIdentification, CltuParameterName,\
    EventInvocationId, BufferSize, CltuGetParameter, CltuLastProcessed,\
    CltuLastOk, CltuNotification, DiagnosticCltuGetParameter,\
    DiagnosticCltuStart, DiagnosticCltuThrowEvent, DiagnosticCltuTransferData,\
    NumberOfCltusProcessed, NumberOfCltusRadiated, NumberOfCltusReceived,\
    ProductionStatus, UplinkStatus
from .bind import SleBindInvocation, SlePeerAbort, SleUnbindInvocation,\
    SleBindReturn, SleUnbindReturn


# Incoming PDUs

class CltuStartInvocation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('invokerCredentials', Credentials()),
        namedtype.NamedType('invokeId', InvokeId()),
        namedtype.NamedType('firstCltuIdentification', CltuIdentification()),
    )


class CltuGetParameterInvocation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('invokerCredentials', Credentials()),
        namedtype.NamedType('invokeId', InvokeId()),
        namedtype.NamedType('cltuParameter', CltuParameterName())
    )


class CltuThrowEventInvocation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('invokerCredentials', Credentials()),
        namedtype.NamedType('invokeId', InvokeId()),
        namedtype.NamedType(
            'eventInvocationIdentification', EventInvocationId()),
        namedtype.NamedType('eventIdentifier', IntPosShort()),
        namedtype.NamedType('eventQualifier', univ.OctetString().subtype(
            subtypeSpec=constraint.ValueSizeConstraint(1, 1024)))
    )


class CltuTransferDataInvocation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('invokerCredentials', Credentials()),
        namedtype.NamedType('invokeId', InvokeId()),
        namedtype.NamedType('cltuIdentification', CltuIdentification()),
        namedtype.NamedType('earliestTransmissionTime', ConditionalTime()),
        namedtype.NamedType('latestTransmissionTime', ConditionalTime()),
        namedtype.NamedType('delayTime', Duration()),
        namedtype.NamedType(
            'slduRadiationNotification', SlduStatusNotification()),
        namedtype.NamedType('cltuData', CltuData())
    )


class CltuUserToProviderPdu(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'cltuBindInvocation', SleBindInvocation().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 100))),
        namedtype.NamedType(
            'cltuUnbindInvocation', SleUnbindInvocation().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 102))),
        namedtype.NamedType(
            'cltuStartInvocation', CltuStartInvocation().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 0))),
        namedtype.NamedType(
            'cltuStopInvocation', SleStopInvocation().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 2))),
        namedtype.NamedType(
            'cltuScheduleStatusReportInvocation',
            SleScheduleStatusReportInvocation().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 4))),
        namedtype.NamedType(
            'cltuGetParameterInvocation', CltuGetParameterInvocation().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 6))),
        namedtype.NamedType(
            'cltuThrowEventInvocation', CltuThrowEventInvocation().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 8))),
        namedtype.NamedType(
            'cltuTransferDataInvocation', CltuTransferDataInvocation().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 10))),
        namedtype.NamedType(
            'cltuPeerAbortInvocation', SlePeerAbort().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 104)))
    )


# Outgoing PDUs

class CltuStartReturn(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('performerCredentials', Credentials()),
        namedtype.NamedType('invokeId', InvokeId()),
        namedtype.NamedType('result', univ.Choice(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('positiveResult', univ.Sequence(
                    componentType=namedtype.NamedTypes(
                        namedtype.NamedType(
                            'startRadiationTime', Time()),
                        namedtype.NamedType(
                            'stopRadiationTime', ConditionalTime())
                    )).subtype(implicitTag=tag.Tag(
                        tag.tagClassContext, tag.tagFormatConstructed, 0))),
                namedtype.NamedType(
                    'negativeResult', DiagnosticCltuStart().subtype(
                        implicitTag=tag.Tag(
                            tag.tagClassContext, tag.tagFormatSimple, 1)))
            )))
    )


class CltuGetParameterReturn(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('performerCredentials', Credentials()),
        namedtype.NamedType('invokeId', InvokeId()),
        namedtype.NamedType('result', univ.Choice(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType(
                    'positiveResult', CltuGetParameter().subtype(
                        implicitTag=tag.Tag(
                            tag.tagClassContext, tag.tagFormatSimple, 0))),
                namedtype.NamedType(
                    'negativeResult', DiagnosticCltuGetParameter().subtype(
                        implicitTag=tag.Tag(
                            tag.tagClassContext, tag.tagFormatSimple, 1)))
                )))
    )


class CltuThrowEventReturn(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('performerCredentials', Credentials()),
        namedtype.NamedType('invokeId', InvokeId()),
        namedtype.NamedType(
            'eventInvocationIdentification', EventInvocationId()),
        namedtype.NamedType('result', univ.Choice(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType(
                    'positiveResult', univ.Null().subtype(
                        implicitTag=tag.Tag(
                            tag.tagClassContext, tag.tagFormatSimple, 0))),
                namedtype.NamedType(
                    'negativeResult', DiagnosticCltuThrowEvent().subtype(
                        implicitTag=tag.Tag(
                            tag.tagClassContext, tag.tagFormatSimple, 1)))
            )))
    )


class CltuTransferDataReturn(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('performerCredentials', Credentials()),
        namedtype.NamedType('invokeId', InvokeId()),
        namedtype.NamedType('cltuIdentification', CltuIdentification()),
        namedtype.NamedType('cltuBufferAvailable', BufferSize()),
        namedtype.NamedType('result', univ.Choice(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType(
                    'positiveResult', univ.Null().subtype(
                        implicitTag=tag.Tag(
                            tag.tagClassContext, tag.tagFormatSimple, 0))),
                namedtype.NamedType(
                    'negativeResult', DiagnosticCltuTransferData().subtype(
                        implicitTag=tag.Tag(
                            tag.tagClassContext, tag.tagFormatSimple, 1)))
            )))
    )


class CltuAsyncNotifyInvocation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('invokerCredentials', Credentials()),
        namedtype.NamedType('cltuNotification', CltuNotification()),
        namedtype.NamedType('cltuLastProcessed', CltuLastProcessed()),
        namedtype.NamedType('cltuLastOk', CltuLastOk()),
        namedtype.NamedType('productionStatus', ProductionStatus()),
        namedtype.NamedType('uplinkStatus', UplinkStatus())
    )


class CltuStatusReportInvocation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('invokerCredentials', Credentials()),
        namedtype.NamedType('cltuLastProcessed', CltuLastProcessed()),
        namedtype.NamedType('cltuLastOk', CltuLastOk()),
        namedtype.NamedType('cltuProductionStatus', ProductionStatus()),
        namedtype.NamedType('uplinkStatus', UplinkStatus()),
        namedtype.NamedType('numberOfCltusReceived', NumberOfCltusReceived()),
        namedtype.NamedType(
            'numberOfCltusProcessed', NumberOfCltusProcessed()),
        namedtype.NamedType('numberOfCltusRadiated', NumberOfCltusRadiated()),
        namedtype.NamedType('cltuBufferAvailable', BufferSize())
    )


class CltuProviderToUserPdu(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'cltuBindReturn', SleBindReturn().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 101))),
        namedtype.NamedType(
            'cltuUnbindReturn', SleUnbindReturn().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 103))),
        namedtype.NamedType(
            'cltuStartReturn', CltuStartReturn().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 1))),
        namedtype.NamedType(
            'cltuStopReturn', SleAcknowledgement().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 3))),
        namedtype.NamedType(
            'cltuScheduleStatusReportReturn',
            SleScheduleStatusReportReturn().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 5))),
        namedtype.NamedType(
            'cltuGetParameterReturn', CltuGetParameterReturn().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 7))),
        namedtype.NamedType(
            'cltuThrowEventReturn', CltuThrowEventReturn().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 9))),
        namedtype.NamedType(
            'cltuTransferDataReturn', CltuTransferDataReturn().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 11))),
        namedtype.NamedType(
            'cltuAsyncNotifyInvocation', CltuAsyncNotifyInvocation().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 12))),
        namedtype.NamedType(
            'cltuStatusReportInvocation', CltuStatusReportInvocation().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 13))),
        namedtype.NamedType(
            'cltuPeerAbortInvocation', SlePeerAbort().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 104)))
    )
