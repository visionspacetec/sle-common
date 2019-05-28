from pyasn1.type import univ, namedtype, namedval, tag, constraint

from .common import Diagnostics, IntPosShort, ParameterName, Time
from .pdu import ReportingCycle


class AntennaId(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('globalForm', univ.ObjectIdentifier().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('localForm', univ.OctetString().subtype(
            subtypeSpec=constraint.ValueSizeConstraint(1, 16)).subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 1)))
    )


class CarrierLockStatus(univ.Integer):
    namedValues = namedval.NamedValues(
        ('inLock', 0),
        ('outOfLock', 1),
        ('unknown', 3)
    )


class CurrentReportingCycle(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('periodicReportingOff', univ.Null().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('periodicReportingOn', ReportingCycle().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 1)))
    )


class DiagnosticRafGet(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('common', Diagnostics().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('specific', univ.Integer(
            namedValues=namedval.NamedValues(
                ('unknownParameter', 0))).subtype(
                    implicitTag=tag.Tag(
                        tag.tagClassContext, tag.tagFormatSimple, 1)))
    )


class DiagnosticRafStart(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('common', Diagnostics().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('specific', univ.Integer(
            namedValues=namedval.NamedValues(
                ('outOfService', 0),
                ('unableToComply', 1),
                ('invalidStartTime', 2),
                ('invalidStopTime', 3),
                ('missingTimeValue', 4))).subtype(
                    implicitTag=tag.Tag(
                        tag.tagClassContext, tag.tagFormatSimple, 1)))
    )


class FrameQuality(univ.Integer):
    namedValues = namedval.NamedValues(
        ('good', 0),
        ('erred', 1),
        ('undetermined', 2)
    )


class FrameSyncLockStatus(univ.Integer):
    namedValues = namedval.NamedValues(
        ('inLock', 0),
        ('outOfLock', 1),
        ('unknown', 3)
    )


class LockStatus(univ.Integer):
    namedValues = namedval.NamedValues(
        ('inLock', 0),
        ('outOfLock', 1),
        ('notInUse', 2),
        ('unknown', 3)
    )


class SymbolLockStatus(univ.Integer):
    namedValues = namedval.NamedValues(
        ('inLock', 0),
        ('outOfLock', 1),
        ('unknown', 3)
    )


class LockStatusReport(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('time', Time()),
        namedtype.NamedType('carrierLockStatus', CarrierLockStatus()),
        namedtype.NamedType('subcarrierLockStatus', LockStatus()),
        namedtype.NamedType('symbolSyncLockStatus', SymbolLockStatus())
    )


class RafProductionStatus(univ.Integer):
    namedValues = namedval.NamedValues(
        ('running', 0),
        ('interrupted', 1),
        ('halted', 2)
    )


class Notification(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('lossFrameSync', LockStatusReport().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 0))),
        namedtype.NamedType(
            'productionStatusChange', RafProductionStatus().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 1))),
        namedtype.NamedType('excessiveDataBacklog', univ.Null().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 2))),
        namedtype.NamedType('endOfData', univ.Null().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 3)))
    )


class RafDeliveryMode(univ.Integer):
    namedValues = namedval.NamedValues(
        ('rtnTimelyOnline', 0),
        ('rtnCompleteOnline', 1),
        ('rtnOffline', 2),
    )


class RequestedFrameQuality(univ.Integer):
    namedValues = namedval.NamedValues(
        ('goodFramesOnly', 0),
        ('erredFramesOnly', 1),
        ('allFrames', 2)
    )


class PermittedFrameQualitySet(univ.SetOf):
    componentType = RequestedFrameQuality()
    #subtypeSpec = constraint.ValueSizeConstraint(0, 2)


class TimeoutPeriod(univ.Integer):
    subtypeSpec = constraint.ValueRangeConstraint(1, 600)


class RafGetParameter(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('parBufferSize', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', IntPosShort())
            )).subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 0))),

        namedtype.NamedType('parDeliveryMode', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', RafDeliveryMode())
            )).subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 1))),

        namedtype.NamedType('parLatencyLimit', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', univ.Choice(
                    componentType=namedtype.NamedTypes(
                        namedtype.NamedType('online', IntPosShort().subtype(
                            implicitTag=tag.Tag(
                                tag.tagClassContext, tag.tagFormatSimple, 0))),
                        namedtype.NamedType('offline', univ.Null().subtype(
                            implicitTag=tag.Tag(
                                tag.tagClassContext, tag.tagFormatSimple, 1)))
                    )))
            )).subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 2))),

        namedtype.NamedType('parMinReportingCycle', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', IntPosShort())
            )).subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 7))),

        namedtype.NamedType('parPermittedFrameQuality', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType(
                    'parameterValue', PermittedFrameQualitySet())
            )).subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 6))),

        namedtype.NamedType('parReportingCycle', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', CurrentReportingCycle())
            )).subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 3))),

        namedtype.NamedType('parReqFrameQuality', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', univ.Integer().subtype(
                    namedValues=namedval.NamedValues(
                        ('goodFramesOnly', 0),
                        ('erredFramesOnly', 1),
                        ('allFrames', 2)
                    )))
            )).subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 4))),

        namedtype.NamedType('parReturnTimeout', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', TimeoutPeriod())
            )).subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatConstructed, 5))),
    )


class RafParameterName(univ.Integer):
    namedValues = namedval.NamedValues(
        ('bufferSize', 4),
        ('deliveryMode', 6),
        ('latencyLimit', 15),
        ('minReportingCycle', 301),
        ('permittedFrameQuality', 302),
        ('reportingCycle', 26),
        ('requestedFrameQuality', 27),
        ('returnTimeoutPeriod', 29),
    )
