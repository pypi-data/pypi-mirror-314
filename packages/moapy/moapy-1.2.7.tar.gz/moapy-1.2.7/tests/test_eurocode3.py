import sys
import pytest
import moapy.dgnengine.eurocode3_beam as eurocode3_beam
import moapy.dgnengine.eurocode3_boltconnection as eurocode3_boltconnection
import moapy.dgnengine.eurocode4_composited_beam as eurocode4_composited_beam
from moapy.data_pre import (
    SectionForce, UnitLoads, EffectiveLengthFactor, Force, Moment, Length, enUnitForce, enUnitLength, enUnitMoment
)

from moapy.steel_pre import (
    SteelMaterial_EC, SteelSection_EN10365, SteelConnectMember_EC, SteelPlateMember_EC, ConnectType,
    SteelBolt_EC, Welding_EC, SteelMember_EC, ShearConnector_EC, SteelLength_EC, SteelMomentModificationFactor_EC, SteelBoltConnectionForce,
)
from moapy.rc_pre import GirderLength, SlabMember_EC

@pytest.mark.skipif(sys.platform.startswith('linux'), reason="Skip test on Linux")
def test_calc_EC3_beamcolumn():
    return eurocode3_beam.calc_ec3_beam_column(SteelMaterial_EC(code="ASTM09", name="A36"), SteelSection_EN10365(name="IPE 400"),
                                         SectionForce(Fz=Force(value=1000.0, unit=enUnitForce.kN), Mx=Moment(value=500.0, unit=enUnitMoment.kNm), My=Moment(value=200.0, unit=enUnitMoment.kNm),
                                                      Vx=Force(value=300.0, unit=enUnitForce.kN), Vy=Force(value=400.0, unit=enUnitForce.kN)),
                                         SteelLength_EC(Lb=Length(value=3000.0, unit=enUnitLength.MM)),
                                         EffectiveLengthFactor(Lx=Length(value=3000.0, unit=enUnitLength.MM), Ly=Length(value=3000.0, unit=enUnitLength.MM)),
                                         SteelMomentModificationFactor_EC(c1=1.0, c_mx=1.0, c_my=1.0, c_mlt=1.0))

@pytest.mark.skipif(sys.platform.startswith('linux'), reason="Skip test on Linux")
def test_report_EC3_beamcolumn():
    return eurocode3_beam.report_ec3_beam_column(SteelMaterial_EC(), SteelSection_EN10365(), SectionForce(), SteelLength_EC(), EffectiveLengthFactor(), SteelMomentModificationFactor_EC())

@pytest.mark.skipif(sys.platform.startswith('linux'), reason="Skip test on Linux")
def test_calc_boltconnection():
    return eurocode3_boltconnection.calc_ec3_bolt_connection(SteelConnectMember_EC(), SteelPlateMember_EC(), ConnectType(), SteelBolt_EC(), Welding_EC(), SteelBoltConnectionForce())

@pytest.mark.skipif(sys.platform.startswith('linux'), reason="Skip test on Linux")
def test_report_boltconnection():
    return eurocode3_boltconnection.report_ec3_bolt_connection(SteelConnectMember_EC(), SteelPlateMember_EC(), ConnectType(), SteelBolt_EC(), Welding_EC(), SteelBoltConnectionForce())

@pytest.mark.skipif(sys.platform.startswith('linux'), reason="Skip test on Linux")
def test_calc_composited_beam():
    return eurocode4_composited_beam.calc_ec4_composited_beam(SteelMember_EC(), ShearConnector_EC(), SlabMember_EC(), GirderLength(), UnitLoads())

@pytest.mark.skipif(sys.platform.startswith('linux'), reason="Skip test on Linux")
def test_report_composited_beam():
    return eurocode4_composited_beam.report_ec4_composited_beam(SteelMember_EC(), ShearConnector_EC(), SlabMember_EC(), GirderLength(), UnitLoads())


if __name__ == "__main__":
    test_calc_EC3_beamcolumn()
    test_report_EC3_beamcolumn()
    test_calc_boltconnection()
    test_report_boltconnection()
    test_calc_composited_beam()
    test_report_composited_beam()
