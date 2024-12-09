import ctypes
import json
import base64
from pydantic import Field
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.data_post import ResultBytes
from moapy.data_pre import SectionForce, Stress, Force, Moment, Length
from moapy.steel_pre import AnchorBolt, BasePlate, SteelMaterial, SteelSection, SteelConnectMember_EC, SteelPlateMember_EC, ConnectType, SteelBolt_EC, Welding_EC, SteelMember_EC, SteelSection_EN10365, SteelMaterial_EC, BoltMaterial_EC, SteelBolt, BoltMaterial
from moapy.enum_pre import enum_to_list, en_H_AISC10_US, enSteelMaterial_ASTM, enBoltMaterialASTM, enUnitStress, enUnitForce, enUnitMoment, enUnitSystem, enUnitLength, en_H_AISC10_SI
from moapy.dgnengine.base import call_func, load_dll, read_file_as_binary

@auto_schema(
    title="AISC-LRFD16(US) Base Plate Design",
    description=(
        "The AISC-LRFD16(US) standard outlines the requirements for designing base plates that connect steel columns "
        "to foundations, emphasizing both safety and efficiency. The design process incorporates key considerations "
        "such as material properties, load conditions, and connection integrity. The analyses included are:\n\n"
        "- Verification of bearing and shear capacities based on material, thickness, and concrete contact\n"
        "- Design for axial, shear, and bending forces to maintain structural integrity\n"
        "- Analysis of bolt group effects and anchor design, ensuring resistance without excessive deformation\n"
        "- Incorporation of ductility and stability to accommodate misalignments and differential movements\n"
        "- Concrete bearing and punching checks to prevent failure or excessive cracking\n\n"
        "The AISC approach integrates these factors into a unified design methodology, providing engineers with reliable "
        "tools and recommendations for designing safe and effective base plate connections."
    )
)
def report_aisc16_baseplate(baseplate: BasePlate = BasePlate.create_default(unit_system=enUnitSystem.US), sect: SteelSection = SteelSection.create_default(name="HP18X181", enum_list=enum_to_list(en_H_AISC10_US)),
                            force: SectionForce = SectionForce.create_default(unit_system=enUnitSystem.US), anchor: AnchorBolt = AnchorBolt.create_default(unit_system=enUnitSystem.US)) -> ResultBytes:
    dll = load_dll()
    json_data_list = [sect.json(), sect.json(), force.json(), baseplate.json(), anchor.json()]
    file_path = call_func(dll, 'Report_AISC16_BasePlate', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_aisc16_baseplate(baseplate: BasePlate = BasePlate.create_default(unit_system=enUnitSystem.US), sect: SteelSection = SteelSection.create_default(name="HP18X181", enum_list=enum_to_list(en_H_AISC10_US)),
                          force: SectionForce = SectionForce.create_default(unit_system=enUnitSystem.US), anchor: AnchorBolt = AnchorBolt.create_default(unit_system=enUnitSystem.US)) -> dict:
    dll = load_dll()
    json_data_list = [sect.json(), force.json(), baseplate.json(), anchor.json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_AISC16_BasePlate', json_data_list)
    dict = json.loads(jsondata)
    print(dict)

# if __name__ == "__main__":
    # res = report_aisc16_baseplate(InputAISC16BasePlate())
    # print(res)