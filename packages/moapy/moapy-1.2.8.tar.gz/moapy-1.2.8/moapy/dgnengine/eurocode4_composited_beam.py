import ctypes
import json
import base64
from dataclasses import asdict
from pydantic import Field
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.data_pre import UnitLoads
from moapy.rc_pre import SlabMember_EC, GirderLength
from moapy.steel_pre import SteelMember_EC, ShearConnector_EC
from moapy.dgnengine.base import load_dll, call_func, read_file_as_binary
from moapy.data_post import ResultBytes
from moapy.enum_pre import enUnitSystem

@auto_schema(
    title="Eurocode 4 Steel Composite Beam Design",
    description="Composite beam that resists bending moment by integrally connecting to reinforced concrete slab and steel beam supporting it by shear connector is designed. Depending on the data that  is entered by users, results of deflection checking, shear connector estimation and Heel drop vibration checking as well as design stress checking applied to each part of composite beam and is automatically calculated."
)
def report_ec4_composited_beam(steel: SteelMember_EC = SteelMember_EC(),
                               shear_conn: ShearConnector_EC = ShearConnector_EC(),
                               slab: SlabMember_EC = SlabMember_EC(),
                               leng: GirderLength = GirderLength.create_default(enUnitSystem.SI),
                               load: UnitLoads = UnitLoads.create_default(enUnitSystem.SI)) -> ResultBytes:
    dll = load_dll()
    json_data_list = [steel.json(), shear_conn.json(), slab.json(), leng.json(), load.json()]
    file_path = call_func(dll, 'Report_EC4_CompositedBeam', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_ec4_composited_beam(steel: SteelMember_EC = SteelMember_EC(),
                             shear_conn: ShearConnector_EC = ShearConnector_EC(),
                             slab: SlabMember_EC = SlabMember_EC(),
                             leng: GirderLength = GirderLength.create_default(enUnitSystem.SI),
                             load: UnitLoads = UnitLoads.create_default(enUnitSystem.SI)) -> dict:
    dll = load_dll()
    json_data_list = [steel.json(), shear_conn.json(), slab.json(), leng.json(), load.json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_EC4_CompositedBeam', json_data_list)
    dict = json.loads(jsondata)
    print(dict)

def save_result_to_json(result: ResultBytes, file_name: str) -> None:
    """ResultBytes 객체를 JSON 파일로 저장"""
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(result.dict(), f, ensure_ascii=False, indent=4)


# if __name__ == "__main__":
    # res = report_ec4_composited_beam(InputEC4CompositedBeam())
    # print(res)