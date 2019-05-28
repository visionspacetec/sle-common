from pyasn1.type import univ, namedtype, namedval, tag, constraint

from .common import Credentials, Diagnostics, InvokeId


class SleAcknowledgement(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('credentials', Credentials()),
        namedtype.NamedType('invokeId', InvokeId()),
        namedtype.NamedType('result', univ.Choice(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('positiveResult', univ.Null().subtype(
                    implicitTag=tag.Tag(
                        tag.tagClassContext, tag.tagFormatSimple, 0))),
                namedtype.NamedType('negativeResult', Diagnostics().subtype(
                    implicitTag=tag.Tag(
                        tag.tagClassContext, tag.tagFormatSimple, 1)))
            ))
        )
    )


class ReportingCycle(univ.Integer):
    subtypeSpec = constraint.ValueRangeConstraint(2, 600)


class ReportRequestType(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('immediately', univ.Null().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('periodically', ReportingCycle().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 1))),
        namedtype.NamedType('stop', univ.Null().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 2)))
    )


class SleScheduleStatusReportInvocation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('invokerCredentials', Credentials()),
        namedtype.NamedType('invokeId', InvokeId()),
        namedtype.NamedType('reportRequestType', ReportRequestType())
    )


class DiagnosticScheduleStatusReport(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('common', Diagnostics().subtype(
            implicitTag=tag.Tag(
                tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('specific', univ.Integer(
            namedValues=namedval.NamedValues(
                ('notSupportedInThisDeliveryMode', 0),
                ('alreadyStopped', 1),
                ('invalidReportingCycle', 2)
                )).subtype(
                    implicitTag=tag.Tag(
                        tag.tagClassContext, tag.tagFormatSimple, 1)))
    )


class SleScheduleStatusReportReturn(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('performerCredentials', Credentials()),
        namedtype.NamedType('invokeId', InvokeId()),
        namedtype.NamedType('result', univ.Choice(
            componentType=namedtype.NamedTypes(
                namedtype.NamedType('positiveResult', univ.Null().subtype(
                    implicitTag=tag.Tag(
                        tag.tagClassContext, tag.tagFormatSimple, 0))),
                namedtype.NamedType(
                    'negativeResult', DiagnosticScheduleStatusReport().subtype(
                        implicitTag=tag.Tag(
                            tag.tagClassContext,
                            tag.tagFormatConstructed, 1)))
            ))
        )
    )


class SleStopInvocation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('invokerCredentials', Credentials()),
        namedtype.NamedType('invokeId', InvokeId())
    )
