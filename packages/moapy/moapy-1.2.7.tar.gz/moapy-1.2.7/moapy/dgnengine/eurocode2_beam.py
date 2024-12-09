import ctypes
import json
import base64
from pydantic import Field
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.data_pre import UnitLoads, SectionRectangle, SectionForce, Moment, enUnitMoment, enUnitLength, Length
from moapy.rc_pre import SlabMember_EC, GirderLength, BeamRebarPattern, MaterialNative
from moapy.dgnengine.base import load_dll, call_func, read_file_as_binary
from moapy.data_post import ResultBytes
from moapy.enum_pre import enUnitSystem

@auto_schema(
    title="Eurocode 2 Beam Design",
    description="Eurocode 2 provides a comprehensive review of reinforced concrete (RC) beam design with a focus on strength assessment, available in Excel format."
)
def report_ec2_beam(matl: MaterialNative = MaterialNative.create_default(enUnitSystem.SI),
                    sect: SectionRectangle = SectionRectangle.create_default(enUnitSystem.SI),
                    rebar: BeamRebarPattern = BeamRebarPattern.create_default(enUnitSystem.SI),
                    force: SectionForce = SectionForce.create_default(enUnitSystem.SI)) -> ResultBytes:
    dll = load_dll()
    json_data_list = [matl.json(), sect.json(), rebar.json(), force.json()]
    file_path = call_func(dll, 'Report_EC2_Beam', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_ec2_beam(matl: MaterialNative = MaterialNative.create_default(enUnitSystem.SI),
                  sect: SectionRectangle = SectionRectangle.create_default(enUnitSystem.SI),
                  rebar: BeamRebarPattern = BeamRebarPattern.create_default(enUnitSystem.SI),
                  force: SectionForce = SectionForce.create_default(enUnitSystem.SI)) -> dict:
    dll = load_dll()
    json_data_list = [matl.json(), sect.json(), rebar.json(), force.json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_EC2_Beam', json_data_list)
    dict = json.loads(jsondata)
    print(dict)


# if __name__ == "__main__":
    # res = report_ec2_beam(InputEC2Beam())
    # print(res)