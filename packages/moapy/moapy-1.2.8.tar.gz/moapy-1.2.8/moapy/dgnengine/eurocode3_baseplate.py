import ctypes
import json
import base64
from pydantic import Field
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.data_post import ResultBytes
from moapy.data_pre import SectionForce, Stress, Force, Moment
from moapy.steel_pre import AnchorBolt, BasePlate, SteelMaterial, SteelSection, SteelConnectMember_EC, SteelPlateMember_EC, ConnectType, SteelBolt_EC, Welding_EC, SteelMember_EC, SteelSection_EN10365, SteelMaterial_EC, BoltMaterial_EC, SteelBolt, BoltMaterial
from moapy.enum_pre import enum_to_list, en_H_EN10365, enSteelMaterial_EN10025, enBoltMaterialEC, enUnitStress
from moapy.dgnengine.base import call_func, load_dll, read_file_as_binary

@auto_schema(
    title="Eurocode 3 Base Plate Design",
    description=( 
        "The Eurocode 3 (EN 1993-1-8) standard for base plate design ensures the stability and safety of steel structures "
        "by analyzing and verifying key design factors for the connection between the base plate and anchor bolts. "
        "This design process involves assessing the performance of the base plate under various load conditions to ensure "
        "that the loads are securely transferred to the supporting foundation.\n\n"
        
        "- Verification of Bearing and Shear Capacities: Evaluates whether the load is safely transferred through the plate "
        "and bolts, assessing bearing strength based on the material and thickness of the plate.\n"
        
        "- Design for Compression and Shear Forces: Calculates the resistance to applied vertical and horizontal loads to "
        "maintain structural stability.\n"
        
        "- Check for Bolt Group Effects and Slip Resistance: Assesses the effects of bolt groups and slip resistance under "
        "concentrated loads to ensure compliance with design requirements.\n"
        
        "- Consideration of Ductility and Stability: Ensures that the base plate provides the necessary flexibility and "
        "stability to distribute loads safely.\n\n"
        
        "This functionality provides detailed design results and recommendations for each connection scenario, offering "
        "structural engineers reliable guidance in making design decisions."
    )
)
def report_ec3_baseplate(baseplate: BasePlate = BasePlate(matl=SteelMaterial.create_default(code="EN10025", enum_list=enum_to_list(enSteelMaterial_EN10025))),
                         sect: SteelSection = SteelSection.create_default(name="HD 260x54.1", enum_list=enum_to_list(en_H_EN10365)),
                         force: SectionForce = SectionForce(Fz=Force(value=3.0, unit="kN"), Mx=Moment(value=1.0, unit="kN.m")), My=Moment(value=0.0, unit="kN.m"), Vx=Force(value=2.0, unit="kN"), Vy=Force(value=0.0, unit="kN"),
                         anchor: AnchorBolt = AnchorBolt(steelbolt=SteelBolt(matl=BoltMaterial.create_default(name=enBoltMaterialEC.Class48, enum_list=enum_to_list(enBoltMaterialEC))))) -> ResultBytes:
    dll = load_dll()
    json_data_list = [sect.json(), sect.json(), force.json(), baseplate.json(), anchor.json()]
    file_path = call_func(dll, 'Report_EC3_BasePlate', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_ec3_baseplate(baseplate: BasePlate = BasePlate(matl=SteelMaterial.create_default(code="EN10025", enum_list=enum_to_list(enSteelMaterial_EN10025))),
                       sect: SteelSection = SteelSection.create_default(name="HD 260x54.1", enum_list=enum_to_list(en_H_EN10365)),
                       force: SectionForce = SectionForce(Fz=Force(value=3.0, unit="kN"), Mx=Moment(value=1.0, unit="kN.m")), My=Moment(value=0.0, unit="kN.m"), Vx=Force(value=2.0, unit="kN"), Vy=Force(value=0.0, unit="kN"),
                       anchor: AnchorBolt = AnchorBolt(steelbolt=SteelBolt(matl=BoltMaterial.create_default(name=enBoltMaterialEC.Class48, enum_list=enum_to_list(enBoltMaterialEC))))) -> dict:
    dll = load_dll()
    json_data_list = [sect.json(), force.json(), baseplate.json(), anchor.json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_EC3_BasePlate', json_data_list)
    dict = json.loads(jsondata)
    print(dict)


if __name__ == "__main__":
    data = {
        "input": {
            "fck": {
            "value": 24,
            "unit": "MPa"
            },
            "baseplate": {
            "matl": {
                "code": "EN10025",
                "name": "S235"
            },
            "thk": {
                "unit": "mm",
                "value": 6
            },
            "width": {
                "unit": "mm",
                "value": 390
            },
            "height": {
                "unit": "mm",
                "value": 400
            }
            },
            "sect": {
            "shape": "H",
            "name": "HD 260x114"
            },
            "force": {
            "Fz": {
                "unit": "kN",
                "value": 3
            },
            "Mx": {
                "unit": "kN.m",
                "value": 1
            },
            "My": {
                "unit": "kN.m",
                "value": 0
            },
            "Vx": {
                "unit": "kN",
                "value": 0
            },
            "Vy": {
                "unit": "kN",
                "value": 0
            }
            },
            "anchor": {
            "type": "Cast-In-Place",
            "steelbolt": {
                "matl": {
                "name": "4.8"
                },
                "name": "M16"
            },
            "length": 25,
            "posX": {
                "unit": "mm",
                "value": 50
            },
            "posY": {
                "unit": "mm",
                "value": 50
            },
            "numX": 2,
            "numY": 2
            }
        }
    }
    res = report_ec3_baseplate(**data)
    print(res)