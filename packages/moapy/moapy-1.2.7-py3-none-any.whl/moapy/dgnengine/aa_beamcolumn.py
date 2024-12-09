import base64
from pydantic import Field
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.data_pre import SectionForce, EffectiveLengthFactor
from moapy.steel_pre import SteelSection_AISC05_US, SteelLength
from moapy.alu_pre import AluMaterial, AluMomentModificationFactor
from moapy.dgnengine.base import call_func, load_dll, read_file_as_binary
from moapy.data_post import ResultBytes
from moapy.enum_pre import enUnitSystem

@auto_schema(
    title="AA-LRFD05 Aluminum Beam Design",
    description=(
        "This functionality performs the design and verification of aluminum beam members "
        "in accordance with the AA-LRFD05 standard. The design process incorporates key "
        "parameters such as cross-sectional properties, material characteristics, and load "
        "combinations. The analyses included are:\n\n"
        "- Verification of cross-sectional strength and stability\n"
        "- Design for bending moments, shear forces, and axial forces\n"
        "- Check for local buckling and overall stability\n"
        "- Application of safety factors and load combinations\n\n"
        "The functionality provides detailed design results, including assessments and "
        "recommendations for each design scenario."
    )
)
def report_aluminum_beam_column(matl: AluMaterial = AluMaterial(), sect: SteelSection_AISC05_US = SteelSection_AISC05_US(), load: SectionForce = SectionForce.create_default(enUnitSystem.SI),
                                length: SteelLength = SteelLength.create_default(enUnitSystem.SI), eff_len: EffectiveLengthFactor = EffectiveLengthFactor(), factor: AluMomentModificationFactor = AluMomentModificationFactor()) -> ResultBytes:
    dll = load_dll()
    json_data_list = [matl.json(), sect.json(), load.json(), length.json(), eff_len.json(), factor.json()]
    file_path = call_func(dll, 'Report_Aluminum_BeamColumn', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

if __name__ == "__main__":
    data = {
        "matl": {
            "matl": "2014-T6"
        },
        "sect": {
            "name": "W40X362"
        },
        "load": {
            "Fz": {
            "value": 0,
            "unit": "kN"
            },
            "Mx": {
            "value": 0,
            "unit": "kN.m"
            },
            "My": {
            "value": 0,
            "unit": "kN.m"
            },
            "Vx": {
            "value": 0,
            "unit": "kN"
            },
            "Vy": {
            "value": 0,
            "unit": "kN"
            }
        },
        "length": {
            "l_x": {
            "value": 3000,
            "unit": "mm"
            },
            "l_y": {
            "value": 3000,
            "unit": "mm"
            },
            "l_b": {
            "value": 3000,
            "unit": "mm"
            }
        },
        "eff_len": {
            "kx": 1,
            "ky": 1
        },
        "factor": {
            "c_mx": 1,
            "c_my": 1,
            "cb": 1,
            "m": 1
        }
    }
    res = report_aluminum_beam_column(**data)
    print(res)