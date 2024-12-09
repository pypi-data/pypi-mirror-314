import ctypes
import json
import base64
from pydantic import Field
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.data_post import ResultBytes
from moapy.steel_pre import SteelConnectMember, SteelMember, SteelSection, SteelMaterial, SteelPlateMember_EC, ConnectType, SteelBolt_EC, Welding_EC, SteelBoltConnectionForce
from moapy.dgnengine.base import call_func, load_dll, read_file_as_binary
from moapy.enum_pre import enum_to_list, en_H_EN10365, enSteelMaterial_EN10025
    
@auto_schema(
    title="Eurocode 3 Steel Bolt Connection Design",
    description=(
        "This functionality performs the design and verification of steel bolt connections "
        "in accordance with Eurocode 3 (EN 1993-1-8). The design process considers key "
        "parameters such as bolt properties, connection geometry, and applied loads, "
        "including the following analyses:\n\n"
        "- Verification of bearing and shear capacities\n"
        "- Design for tensile and shear forces\n"
        "- Check for bolt group effects and slip resistance\n"
        "- Consideration of connection ductility and stability\n\n"
        "The functionality provides detailed design results, including assessments and "
        "recommendations for each connection scenario."
    )
)
def report_ec3_bolt_connection(conn: SteelConnectMember = SteelConnectMember(
                                   supporting=SteelMember(
                                       sect=SteelSection.create_default(name="HD 260x54.1", enum_list=enum_to_list(en_H_EN10365), description="EN 10365 is a European standard that defines specifications for cross sections of structural steel. The standard supports the accurate design of steel sections used in a variety of structures, including requirements for the shape, dimensions, tolerances, and mechanical properties of steel. EN 10365 is primarily concerned with the design of beams, plates, tubes, and other structural elements."),
                                       matl=SteelMaterial.create_default(code="EN10025", enum_list=enum_to_list(enSteelMaterial_EN10025), description="EN 10025 is the standard for steel materials used in Europe and specifies the technical requirements for steel, primarily for structural purposes. The standard defines mechanical properties, chemical composition, manufacturing methods, and inspection methods for different types of steel. EN 10025 is divided into several parts, each of which covers requirements for a specific steel type.")
                                   ),
                                   supported=SteelMember(
                                       sect=SteelSection.create_default(name="HD 260x54.1", enum_list=enum_to_list(en_H_EN10365), description="EN 10365 is a European standard that defines specifications for cross sections of structural steel. The standard supports the accurate design of steel sections used in a variety of structures, including requirements for the shape, dimensions, tolerances, and mechanical properties of steel. EN 10365 is primarily concerned with the design of beams, plates, tubes, and other structural elements."),
                                       matl=SteelMaterial.create_default(code="EN10025", enum_list=enum_to_list(enSteelMaterial_EN10025), description="EN 10025 is the standard for steel materials used in Europe and specifies the technical requirements for steel, primarily for structural purposes. The standard defines mechanical properties, chemical composition, manufacturing methods, and inspection methods for different types of steel. EN 10025 is divided into several parts, each of which covers requirements for a specific steel type.")
                                   )),
                               plate: SteelPlateMember_EC = SteelPlateMember_EC(),
                               connect_type: ConnectType = ConnectType(),
                               bolt: SteelBolt_EC = SteelBolt_EC(),
                               weld: Welding_EC = Welding_EC(),
                               force: SteelBoltConnectionForce = SteelBoltConnectionForce()) -> ResultBytes:
    dll = load_dll()
    json_data_list = [conn.supporting.json(), conn.supported.json(), plate.json(), connect_type.json(), bolt.json(), weld.json(), force.json()]
    file_path = call_func(dll, 'Report_EC3_BoltConnection', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_ec3_bolt_connection(conn: SteelConnectMember = SteelConnectMember(
                                 supporting=SteelMember(
                                     sect=SteelSection.create_default(name="HD 260x54.1", enum_list=enum_to_list(en_H_EN10365), description="EN 10365 is a European standard that defines specifications for cross sections of structural steel. The standard supports the accurate design of steel sections used in a variety of structures, including requirements for the shape, dimensions, tolerances, and mechanical properties of steel. EN 10365 is primarily concerned with the design of beams, plates, tubes, and other structural elements."),
                                     matl=SteelMaterial.create_default(code="EN10025", enum_list=enum_to_list(enSteelMaterial_EN10025), description="EN 10025 is the standard for steel materials used in Europe and specifies the technical requirements for steel, primarily for structural purposes. The standard defines mechanical properties, chemical composition, manufacturing methods, and inspection methods for different types of steel. EN 10025 is divided into several parts, each of which covers requirements for a specific steel type.")
                                 ),
                                 supported=SteelMember(
                                     sect=SteelSection.create_default(name="HD 260x54.1", enum_list=enum_to_list(en_H_EN10365), description="EN 10365 is a European standard that defines specifications for cross sections of structural steel. The standard supports the accurate design of steel sections used in a variety of structures, including requirements for the shape, dimensions, tolerances, and mechanical properties of steel. EN 10365 is primarily concerned with the design of beams, plates, tubes, and other structural elements."),
                                     matl=SteelMaterial.create_default(code="EN10025", enum_list=enum_to_list(enSteelMaterial_EN10025), description="EN 10025 is the standard for steel materials used in Europe and specifies the technical requirements for steel, primarily for structural purposes. The standard defines mechanical properties, chemical composition, manufacturing methods, and inspection methods for different types of steel. EN 10025 is divided into several parts, each of which covers requirements for a specific steel type.")
                                 )),
                             plate: SteelPlateMember_EC = SteelPlateMember_EC(),
                             connect_type: ConnectType = ConnectType(),
                             bolt: SteelBolt_EC = SteelBolt_EC(),
                             weld: Welding_EC = Welding_EC(),
                             force: SteelBoltConnectionForce = SteelBoltConnectionForce()) -> dict:
    dll = load_dll()
    json_data_list = [conn.supporting.json(), conn.supported.json(), plate.json(), connect_type.json(), bolt.json(), weld.json(), force.json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_EC3_BoltConnection', json_data_list)
    dict = json.loads(jsondata)
    print(dict)


# if __name__ == "__main__":
    # res = report_ec3_bolt_connection(InputEC3BoltConnection())
    # print(res)