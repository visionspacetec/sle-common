from pyasn1.type import univ, namedtype, namedval, tag, constraint, char

from .common import ConditionalTime, DeliveryMode, Diagnostics, Duration,\
    IntPosShort, IntPosLong, IntUnsignedLong, IntUnsignedShort, ParameterName,\
    SpaceLinkDataUnit, Time
from .pdu import ReportingCycle


class BufferSize(IntUnsignedLong):
    pass


class VcId(univ.Integer):
    subtypeSpec = constraint.ValueRangeConstraint(0, 63)


class GvcId(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('spacecraftId', univ.Integer().subtype(
            subtypeSpec=constraint.ValueRangeConstraint(0, 1023))),
        namedtype.NamedType('versionNumber', univ.Integer().subtype(
            subtypeSpec=constraint.ValueRangeConstraint(0, 3))),
        namedtype.NamedType('vcId', univ.Choice(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('masterChannel', univ.Null().subtype(
                    implicitTag=tag.Tag(
                        tag.tagClassContext, tag.tagFormatSimple, 0))),
                namedtype.NamedType('virtualChannel', VcId().subtype(
                    implicitTag=tag.Tag(
                        tag.tagClassContext, tag.tagFormatSimple, 1)))
            ))
        )
    )


class ClcwGvcId(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('congigured', GvcId().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 0))),
        namedtype.NamedType('notConfigured', univ.Null().subtype(
            implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
    )


class ClcwPhysicalChannel(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('configured', char.VisibleString().subtype(
            subtypeSpec=constraint.ValueSizeConstraint(1, 32)).subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('notConfigured', univ.Null().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 1)))
    )


class CltuData(SpaceLinkDataUnit):
    pass


class CltuDeliveryMode(DeliveryMode):
    pass


class CltuIdentification(IntUnsignedLong):
    pass


class EventInvocationId(IntUnsignedLong):
    pass


class CltuStatus(univ.Integer):
    namedValues = namedval.NamedValues(
        ('radiated', 0),
        ('expired', 1),
        ('interrupted', 2),
        ('productionStarted', 4),
        ('productionNotStarted', 5),
    )


class ModulationFrequency(IntPosLong):
    pass


class ModulationIndex(IntPosShort):
    pass


class SubcarrierDivisor(IntPosShort):
    pass


class TimeoutPeriod(univ.Integer):
    subtypeSpec = constraint.ValueRangeConstraint(1, 600)


class CurrentReportingCycle(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('periodicReportingOff', univ.Null().subtype(
            implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('periodicReportingOn', ReportingCycle().subtype(
            implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
    )


class CltuGetParameter(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('parAcquisitionSequenceLength', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', IntUnsignedShort())
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 0))),

        namedtype.NamedType('parBitLockRequired', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', univ.Integer().subtype(
                    namedValues=namedval.NamedValues(
                        ('yes', 0),
                        ('no', 1)
                    )))
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 1))),

        namedtype.NamedType('parClcwGlobalVcId', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', ClcwGvcId())
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 2))),

        namedtype.NamedType('parClcwPhysicalChannel', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', ClcwPhysicalChannel())
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 3))),

        namedtype.NamedType('parDeliveryMode', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', CltuDeliveryMode())
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 4))),

        namedtype.NamedType('parCltuIdentification', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', CltuIdentification())
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 5))),

        namedtype.NamedType('parEventInvocationIdentification', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', CltuIdentification())
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 6))),

        namedtype.NamedType('parMaximumCltuLength', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', EventInvocationId())
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 7))),

        namedtype.NamedType('parMinimumDelayTime', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', Duration())
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 8))),

        namedtype.NamedType('parMinReportingCycle', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', IntPosShort())
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 19))),

        namedtype.NamedType('parModulationFrequency', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', ModulationFrequency())
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 9))),

        namedtype.NamedType('parModulationIndex', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', ModulationIndex())
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 10))),

        namedtype.NamedType('parNotificationMode', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', univ.Integer().subtype(
                    namedValues=namedval.NamedValues(
                        ('deffered', 0),
                        ('immediate', 1)
                    )))
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 11))),

        namedtype.NamedType('parPlop1IdleSequenceLength', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', IntUnsignedShort())
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 12))),

        namedtype.NamedType('parPlopInEffect', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', univ.Integer().subtype(
                    namedValues=namedval.NamedValues(
                        ('plop1', 0),
                        ('plop2', 1)
                    )))
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 13))),

        namedtype.NamedType('parProtocolAbortMode', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', univ.Integer().subtype(
                    namedValues=namedval.NamedValues(
                        ('abort', 0),
                        ('continue', 1)
                    )))
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 14))),

        namedtype.NamedType('parReportingCycle', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', CurrentReportingCycle())
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 15))),

        namedtype.NamedType('parReturnTimeout', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', TimeoutPeriod())
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 16))),

        namedtype.NamedType('parRfAvailableRequired', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', univ.Integer().subtype(
                    namedValues=namedval.NamedValues(
                        ('yes', 0),
                        ('no', 1)
                    )))
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 17))),

        namedtype.NamedType('parSubcarrierToBitRateRatio', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('parameterName', ParameterName()),
                namedtype.NamedType('parameterValue', SubcarrierDivisor())
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 18)))
        )


class CltuLastOk(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('noCltuOk', univ.Null().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('cltuOk', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType(
                    'cltuIdentification', CltuIdentification()),
                namedtype.NamedType('radiationStopTime', Time())
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 1)))
    )


class CltuLastProcessed(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('noCltuProcessed', univ.Null().subtype(
            implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('cltuProcessed', univ.Sequence(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType(
                    'cltuIdentification', CltuIdentification()),
                namedtype.NamedType('radiationStartTime', ConditionalTime()),
                namedtype.NamedType('cltuStatus', CltuStatus())
            )).subtype(implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 1)))
    )


class CltuNotification(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('cltuRadiated', univ.Null().subtype(
            implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('slduExpired', univ.Null().subtype(
            implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
        namedtype.NamedType('productionInterrupted', univ.Null().subtype(
            implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),
        namedtype.NamedType('productionHalted', univ.Null().subtype(
            implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
        namedtype.NamedType('productionOperational', univ.Null().subtype(
            implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))),
        namedtype.NamedType('bufferEmpty', univ.Null().subtype(
            implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5))),
        namedtype.NamedType('actionListCompleted', EventInvocationId().subtype(
            implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 6))),
        namedtype.NamedType(
            'actionListNotCompleted', EventInvocationId().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 7))),
        namedtype.NamedType(
            'eventConditionEvFalse', EventInvocationId().subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 8)))
    )


class CltuParameterName(univ.Integer):
    namedValues = namedval.NamedValues(
        ('acquisitionSequenceLength', 201),
        ('bitLockRequired', 3),
        ('clcwGlobalVcId', 202),
        ('clcwPhysicalChannel', 203),
        ('deliveryMode', 6),
        ('expectedEventInvocationIdentification', 9),
        ('expectedSlduIdentification', 10),
        ('maximumSlduLength', 21),
        ('minimumDelayTime', 204),
        ('minReportingCycle', 301),
        ('modulationFrequency', 22),
        ('modulationIndex', 23),
        ('notificationMode', 205),
        ('plop1IdleSequenceLength', 206),
        ('plopInEffect', 25),
        ('protocolAbortMode', 207),
        ('reportingCycle', 26),
        ('returnTimeoutPeriod', 29),
        ('rfAvailableRequired', 31),
        ('subcarrierToBitRateRatio', 34),
    )


class DiagnosticCltuGetParameter(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('common', Diagnostics().subtype(
            implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('specific', univ.Integer(
            namedValues=namedval.NamedValues(('unknownParameter', 0))).subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 1)))
    )


class DiagnosticCltuStart(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('common', Diagnostics().subtype(
            implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('specific', univ.Integer(
            namedValues=namedval.NamedValues(
                ('outOfService', 0),
                ('unableToComply', 1),
                ('productionTimeExpired', 2),
                ('invalidCltuId', 3))).subtype(implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 1)))
    )


class DiagnosticCltuThrowEvent(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('common', Diagnostics().subtype(
            implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('specific', univ.Integer(
            namedValues=namedval.NamedValues(
                ('operationNotSupported', 0),
                ('eventInvocIdOutOfSequence', 1),
                ('noSuchEvent', 2))).subtype(implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 1)))
    )


class DiagnosticCltuTransferData(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('common', Diagnostics().subtype(
            implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('specific', univ.Integer(
            namedValues=namedval.NamedValues(
                ('unableToProcess', 0),
                ('unableToStore', 1),
                ('outOfSequence', 2),
                ('inconsistentTimeRange', 3),
                ('invalidTime', 4),
                ('lateSldu', 5),
                ('invalidDelayTime', 6),
                ('cltuError', 7))).subtype(implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 1)))
    )


class NumberOfCltusProcessed(IntUnsignedLong):
    pass


class NumberOfCltusRadiated(IntUnsignedLong):
    pass


class NumberOfCltusReceived(IntUnsignedLong):
    pass


class ProductionStatus(univ.Integer):
    namedValues = namedval.NamedValues(
        ('operational', 0),
        ('configured', 1),
        ('interrupted', 2),
        ('halted', 3)
    )


class UplinkStatus(univ.Integer):
    namedValues = namedval.NamedValues(
        ('uplinkStatusNotAvailable', 0),
        ('noRfAvailable', 1),
        ('noBitLock', 2),
        ('nominal', 3)
    )
