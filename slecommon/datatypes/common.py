from pyasn1.type import univ, namedtype, namedval, tag, constraint


class IntPosLong(univ.Integer):
    subtypeSpec = constraint.ValueRangeConstraint(1, 4294967295)


class IntPosShort(univ.Integer):
    subtypeSpec = constraint.ValueRangeConstraint(1, 65535)


class IntUnsignedLong(univ.Integer):
    subtypeSpec = constraint.ValueRangeConstraint(0, 4294967295)


class IntUnsignedShort(univ.Integer):
    subtypeSpec = constraint.ValueRangeConstraint(0, 65535)


class TimeCCSDS(univ.OctetString):
    # CCSDS Day Segmented Time Code (CDS)
    # 16-bit day segment, 32-bit ms of day, 16-bit-microsecs
    # subtypeSpec = constraint.ValueSizeConstraint(8, 8)
    pass


class TimeCCSDSpico(univ.OctetString):
    subtypeSpec = constraint.ValueSizeConstraint(10, 10)


class Time(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('ccsdsFormat', TimeCCSDS().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('ccsdsPicoFormat', TimeCCSDSpico().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 1)))
    )


class ConditionalTime(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('undefined', univ.Null().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('known', Time().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatConstructed, 1)))
    )


class Credentials(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('unused', univ.Null().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('used', univ.OctetString().subtype(
            subtypeSpec=constraint.ValueSizeConstraint(8, 256)).subtype(
                implicitTag=tag.Tag(
                    tag.tagClassContext, tag.tagFormatSimple, 1)))
    )


class DeliveryMode(univ.Integer):
    namedValues = namedval.NamedValues(
        ('rtnTimelyOnline', 0),
        ('rtnCompleteOnline', 1),
        ('rtnOffline', 2),
        ('fwdOnline', 3),
        ('fwdOffline', 4)
    )


class Diagnostics(univ.Integer):
    namedValues = namedval.NamedValues(
        ('duplicateInvokeId', 100),
        ('otherReason', 127)
    )


class Duration(IntUnsignedLong):
    pass


class ForwardDuStatus(univ.Integer):
    namedValues = namedval.NamedValues(
        ('radiated', 0),
        ('expired', 1),
        ('interrupted', 2),
        ('acknowledged', 3),
        ('productionStarted', 4),
        ('productionNotStarted', 5),
        ('unsupportedTransmissionMode', 6)
    )


class InvokeId(IntUnsignedShort):
    pass


class ParameterName(univ.Integer):
    namedValues = namedval.NamedValues(
        ('acquisitionSequenceLength', 201),
        ('apidList', 2),
        ('bitLockRequired', 3),
        ('blockingTimeoutPeriod', 0),
        ('blockingUsage', 1),
        ('bufferSize', 4),
        ('clcwGlobalVcId', 202),
        ('clcwPhysicalChannel', 203),
        ('copCntrFramesRepetition', 300),
        ('deliveryMode', 6),
        ('directiveInvocation', 7),
        ('directiveInvocationOnline', 108),
        ('expectedDirectiveIdentification', 8),
        ('expectedEventInvocationIdentification', 9),
        ('expectedSlduIdentification', 10),
        ('fopSlidingWindow', 11),
        ('fopState', 12),
        ('latencyLimit', 15),
        ('mapList', 16),
        ('mapMuxControl', 17),
        ('mapMuxScheme', 18),
        ('maximumFrameLength', 19),
        ('maximumPacketLength', 20),
        ('maximumSlduLength', 21),
        ('minimumDelayTime', 204),
        ('minReportingCycle', 301),
        ('modulationFrequency', 22),
        ('modulationIndex', 23),
        ('notificationMode', 205),
        ('permittedControlWordTypeSet', 101),
        ('permittedFrameQuality', 302),
        ('permittedGvcidSet', 24),
        ('permittedTcVcidSet', 102),
        ('permittedTransmissionMode', 107),
        ('permittedUpdateModeSet', 103),
        ('plop1IdleSequenceLength', 206),
        ('plopInEffect', 25),
        ('protocolAbortMode', 207),
        ('reportingCycle', 26),
        ('requestedControlWordType', 104),
        ('requestedFrameQuality', 27),
        ('requestedGvcid', 28),
        ('requestedTcVcid', 105),
        ('requestedUpdateMode', 106),
        ('returnTimeoutPeriod', 29),
        ('rfAvailable', 30),
        ('rfAvailableRequired', 31),
        ('segmentHeader', 32),
        ('sequCntrFramesRepetition', 303),
        ('subcarrierToBitRateRatio', 34),
        ('throwEventOperation', 304),
        ('timeoutType', 35),
        ('timerInitial', 36),
        ('transmissionLimit', 37),
        ('transmitterFrameSequenceNumber', 38),
        ('vcMuxControl', 39),
        ('vcMuxScheme', 40),
        ('virtualChannel', 41)
    )


class SlduStatusNotification(univ.Integer):
    namedValues = namedval.NamedValues(
        ('produceNotification', 0),
        ('doNotProduceNotification', 1)
    )


class SpaceLinkDataUnit(univ.OctetString):
    subtypeSpec = constraint.ValueSizeConstraint(1, 65536)
