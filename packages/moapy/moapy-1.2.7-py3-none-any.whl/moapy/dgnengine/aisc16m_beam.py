import ctypes
import base64
import json
from pydantic import Field
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.data_pre import SectionForce, EffectiveLengthFactor, enUnitSystem
from moapy.data_post import ResultBytes
from moapy.steel_pre import SteelMaterial, SteelLength, SteelMomentModificationFactorLTB, SteelSection
from moapy.enum_pre import en_H_AISC10_US, en_H_AISC10_SI, enum_to_list, enSteelMaterial_ASTM
from moapy.dgnengine.base import call_func, load_dll, read_file_as_binary

@auto_schema(
    title="AISC16(SI) Beam Design",
    description="Steel column that is subjected to axial force, biaxial bending moment and shear force and steel beam that is subjected to the bending moment are designed. Automatic design or code check for load resistance capacity of cross-sections like H-beam depending on the form of member is conducted."
)
def report_aisc16si_beam_column(matl: SteelMaterial = SteelMaterial.create_default(code="ASTM09(S)", enum_list=enum_to_list(enSteelMaterial_ASTM)),
                                sect: SteelSection = SteelSection.create_default(name="HP410X151", enum_list=enum_to_list(en_H_AISC10_SI)),
                                length: SteelLength = SteelLength.create_default(enUnitSystem.SI),
                                eff_len: EffectiveLengthFactor = EffectiveLengthFactor(),
                                factor: SteelMomentModificationFactorLTB = SteelMomentModificationFactorLTB(),
                                load: SectionForce = SectionForce.create_default(enUnitSystem.SI)) -> ResultBytes:
    dll = load_dll()
    json_data_list = [matl.json(), sect.json(), load.json(), length.json(), eff_len.json(), factor.json()]
    file_path = call_func(dll, 'Report_AISC16SI_BeamColumn', json_data_list)
    if file_path is None:
        return ResultBytes(type="md", result="Error: Failed to generate report.")
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

def calc_aisc16si_beam_column(matl: SteelMaterial = SteelMaterial.create_default(code="ASTM09(S)", enum_list=enum_to_list(enSteelMaterial_ASTM)),
                              sect: SteelSection = SteelSection.create_default(name="HP410X151", enum_list=enum_to_list(en_H_AISC10_SI)),
                              length: SteelLength = SteelLength.create_default(enUnitSystem.SI),
                              eff_len: EffectiveLengthFactor = EffectiveLengthFactor(),
                              factor: SteelMomentModificationFactorLTB = SteelMomentModificationFactorLTB(),
                              load: SectionForce = SectionForce.create_default(enUnitSystem.SI)) -> dict:
    dll = load_dll()
    json_data_list = [matl.json(), sect.json(), load.json(), length.json(), eff_len.json(), factor.json(), ctypes.c_void_p(0), ctypes.c_void_p(0)]
    jsondata = call_func(dll, 'Calc_AISC16SI_BeamColumn', json_data_list)
    dict = json.loads(jsondata)
    print(dict)