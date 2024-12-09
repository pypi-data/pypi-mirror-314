import ctypes
import json
import base64
from pydantic import Field
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.data_pre import SectionRectangle, SectionForce, Moment, enUnitMoment, BucklingLength, MemberForce, EffectiveLengthFactor, Length, Force, OuterPolygon
from moapy.rc_pre import BeamRebarPattern, MaterialNative, ColumnRebarPattern, GeneralRebarPattern, EquivalentAreaGeneralSect
from moapy.enum_pre import enUnitSystem, enUnitLength
from moapy.dgnengine.base import load_dll, call_func, read_file_as_binary
from moapy.data_post import ResultBytes


@auto_schema(
    title="Eurocode 2 Column Design",
    description="Eurocode 2 provides a comprehensive review of reinforced concrete (RC) column design with a focus on strength assessment, available in Excel format."
)
def report_ec2_column(matl: MaterialNative = MaterialNative.create_default(enUnitSystem.SI),
                      sect: SectionRectangle = SectionRectangle.create_default(enUnitSystem.SI),
                      rebar: ColumnRebarPattern = ColumnRebarPattern.create_default(enUnitSystem.SI),
                      force: MemberForce = MemberForce.create_default(enUnitSystem.SI),
                      length: BucklingLength = BucklingLength.create_default(enUnitSystem.SI),
                      eff_len: EffectiveLengthFactor = EffectiveLengthFactor()) -> ResultBytes:
    dll = load_dll()
    json_data_list = [matl.json(), sect.json(), rebar.json(), force.json(), length.json(), eff_len.json()]
    file_path = call_func(dll, 'Report_EC2_Column', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_ec2_column(matl: MaterialNative = MaterialNative.create_default(enUnitSystem.SI),
                    sect: SectionRectangle = SectionRectangle.create_default(enUnitSystem.SI),
                    rebar: ColumnRebarPattern = ColumnRebarPattern.create_default(enUnitSystem.SI),
                    force: MemberForce = MemberForce.create_default(enUnitSystem.SI),
                    length: BucklingLength = BucklingLength.create_default(enUnitSystem.SI),
                    eff_len: EffectiveLengthFactor = EffectiveLengthFactor()) -> dict:
    dll = load_dll()
    json_data_list = [matl.json(), sect.json(), rebar.json(), force.json(), length.json(), eff_len.json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_EC2_Column', json_data_list)
    dict = json.loads(jsondata)
    print(dict)


@auto_schema(
    title="Eurocode 2 General Column Design",
    description="Eurocode 2 provides a comprehensive review of reinforced concrete (RC) General column design with a focus on strength assessment, available in Excel format."
)
def report_ec2_generalcolumn(matl: MaterialNative = MaterialNative.create_default(enUnitSystem.SI),
                             sect: OuterPolygon = OuterPolygon(),
                             eff_area: EquivalentAreaGeneralSect = EquivalentAreaGeneralSect(b=Length(value=300, unit=enUnitLength.MM), h=Length(value=300, unit=enUnitLength.MM)),
                             rebar: GeneralRebarPattern = GeneralRebarPattern(),
                             force: MemberForce = MemberForce.create_default(enUnitSystem.SI),
                             length: BucklingLength = BucklingLength.create_default(enUnitSystem.SI),
                             eff_len: EffectiveLengthFactor = EffectiveLengthFactor()) -> ResultBytes:
    dll = load_dll()
    json_data_list = [matl.json(), sect.json(), eff_area.json(), rebar.json(), force.json(), length.json(), eff_len.json()]
    file_path = call_func(dll, 'Report_EC2_GeneralColumn', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_ec2_generalcolumn(matl: MaterialNative = MaterialNative.create_default(enUnitSystem.SI),
                           sect: OuterPolygon = OuterPolygon(),
                           eff_area: EquivalentAreaGeneralSect = EquivalentAreaGeneralSect(),
                           rebar: GeneralRebarPattern = GeneralRebarPattern(),
                           force: MemberForce = MemberForce.create_default(enUnitSystem.SI),
                           length: BucklingLength = BucklingLength.create_default(enUnitSystem.SI),
                           eff_len: EffectiveLengthFactor = EffectiveLengthFactor()) -> dict:
    dll = load_dll()
    json_data_list = [matl.json(), sect.json(), eff_area.json(), rebar.json(), force.json(), length.json(), eff_len.json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_EC2_GeneralColumn', json_data_list)
    dict = json.loads(jsondata)
    print(dict)


# if __name__ == "__main__":
    # res = report_ec2_generalcolumn(InputEC2GenColumn())
    # print(res)