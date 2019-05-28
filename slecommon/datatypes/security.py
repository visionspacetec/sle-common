from pyasn1.type import univ, namedtype, char, constraint

from .common import TimeCCSDS


class RandomNumber(univ.Integer):
    subtypeSpec = constraint.ValueRangeConstraint(0, 2147483647)


class HashInput(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('time', TimeCCSDS()),
        namedtype.NamedType('randomNumber', RandomNumber()),
        namedtype.NamedType('userName', char.VisibleString()),
        namedtype.NamedType('passWord', univ.OctetString())
    )


class Isp1Credentials(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('time', TimeCCSDS()),
        namedtype.NamedType('randomNumber', RandomNumber()),
        namedtype.NamedType('theProtected', univ.OctetString().subtype(
            subtypeSpec=constraint.ValueSizeConstraint(20, 32)))
    )
