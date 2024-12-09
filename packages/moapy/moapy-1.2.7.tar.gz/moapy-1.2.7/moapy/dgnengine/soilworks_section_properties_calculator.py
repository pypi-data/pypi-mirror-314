import re
from enum import Enum
import pandas as pd
from pydantic import Field, ConfigDict
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.enum_pre import enum_to_list
from moapy.designers_guide.resource.report_form import ReportForm
from moapy.designers_guide.func_general import DG_Result_Reports

class KS18Grades(Enum):
    SS275 = "SS275"
    SM275 = "SM275"
    SM355 = "SM355"
    SHP275 = "SHP275"
    SHP355 = "SHP355"

class HSectionData:
    data = [
            ["H 100x50x5/7", "H", 0.1, 0.05, 0.005, 0.007, 0.001185, 1.8e-06, 1.48e-07, 4.1795e-05],
            ["H 100x100x6/8", "H", 0.1, 0.1, 0.006, 0.008, 0.00219, 3.83e-06, 1.34e-06, 8.4184e-05],
            ["H 125x125x6.5/9", "H", 0.125, 0.125, 0.0065, 0.009, 0.003031, 8.47e-06, 2.93e-06, 0.000149105],
            ["H 150x75x5/7", "H", 0.15, 0.075, 0.005, 0.007, 0.001785, 6.66e-06, 4.95e-07, 9.8195e-05],
            ["H 148x100x6/9", "H", 0.148, 0.1, 0.006, 0.009, 0.002684, 1.02e-05, 1.51e-06, 0.00015045],
            ["H 150x150x7/10", "H", 0.15, 0.15, 0.007, 0.01, 0.004014, 1.64e-05, 5.63e-06, 0.000239575],
            ["H 198x99x4.5/7", "H", 0.198, 0.099, 0.0045, 0.007, 0.002318, 1.58e-05, 1.14e-06, 0.000170451],
            ["H 200x100x5.5/8", "H", 0.2, 0.1, 0.0055, 0.008, 0.002716, 1.84e-05, 1.34e-06, 0.000200152],
            ["H 194x150x6/9", "H", 0.194, 0.15, 0.006, 0.009, 0.003901, 2.69e-05, 5.07e-06, 0.000296214],
            ["H 200x200x8/12", "H", 0.2, 0.2, 0.008, 0.012, 0.006353, 4.72e-05, 1.6e-05, 0.000513152],
            ["H 200x204x12/12", "H", 0.2, 0.204, 0.012, 0.012, 0.007153, 4.98e-05, 1.7e-05, 0.000553152],
            ["H 208x202x10/16", "H", 0.208, 0.202, 0.01, 0.016, 0.008369, 6.53e-05, 2.2e-05, 0.000697984],
            ["H 248x124x5/8", "H", 0.248, 0.124, 0.005, 0.008, 0.003268, 3.54e-05, 2.55e-06, 0.00030536],
            ["H 250x125x6/9", "H", 0.25, 0.125, 0.006, 0.009, 0.003766, 4.05e-05, 2.94e-06, 0.000351861],
            ["H 244x175x7/11", "H", 0.244, 0.175, 0.007, 0.011, 0.005624, 6.12e-05, 9.84e-06, 0.000534772],
            ["H 244x252x11/11", "H", 0.244, 0.252, 0.011, 0.011, 0.008206, 8.79e-05, 2.94e-05, 0.000781407],
            ["H 248x249x8/13", "H", 0.248, 0.249, 0.008, 0.013, 0.00847, 9.93e-05, 3.35e-05, 0.000859263],
            ["H 250x250x9/14", "H", 0.25, 0.25, 0.009, 0.014, 0.009218, 1.08e-04, 3.65e-05, 0.000936889],
            ["H 250x255x14/14", "H", 0.25, 0.255, 0.014, 0.014, 0.01047, 1.15e-04, 3.88e-05, 0.001015014],
            ["H 298x149x5.5/8", "H", 0.298, 0.149, 0.0055, 0.008, 0.00408, 6.32e-05, 4.42e-06, 0.000455026],
            ["H 300x150x6.5/9", "H", 0.3, 0.15, 0.0065, 0.009, 0.004678, 7.21e-05, 5.08e-06, 0.000522077],
            ["H 294x200x8/12", "H", 0.294, 0.2, 0.008, 0.012, 0.007238, 0.000113, 1.6e-05, 0.0008226],
            ["H 298x201x9/14", "H", 0.298, 0.201, 0.009, 0.014, 0.008336, 0.000133, 1.9e-05, 0.000963201],
            ["H 294x302x12/12", "H", 0.294, 0.302, 0.012, 0.012, 0.01077, 0.000169, 5.52e-05, 0.001240668],
            ["H 298x299x9/14", "H", 0.298, 0.299, 0.009, 0.014, 0.01108, 0.000188, 6.24e-05, 0.001352849],
            ["H 300x300x10/15", "H", 0.3, 0.3, 0.01, 0.015, 0.01198, 0.000204, 6.75e-05, 0.00146475],
            ["H 300x305x15/15", "H", 0.3, 0.305, 0.015, 0.015, 0.01348, 0.000215, 7.1e-05, 0.00157725],
            ["H 304x301x11/17", "H", 0.304, 0.301, 0.011, 0.017, 0.01348, 0.000234, 7.73e-05, 0.001669054],
            ["H 310x305x15/20", "H", 0.31, 0.305, 0.015, 0.02, 0.01653, 0.0002815, 9.46e-05, 0.002042375],
            ["H 310x310x20/20", "H", 0.31, 0.31, 0.02, 0.02, 0.01808, 0.0002939, 9.94e-05, 0.0021625],
            ["H 346x174x6/9", "H", 0.346, 0.174, 0.006, 0.009, 0.005268, 0.000111, 7.92e-06, 0.000689118],
            ["H 350x175x7/11", "H", 0.35, 0.175, 0.007, 0.011, 0.006314, 0.000136, 9.84e-06, 0.000840847],
            ["H 354x176x8/13", "H", 0.354, 0.176, 0.008, 0.013, 0.007368, 0.000161, 1.18e-05, 0.000995376],
            ["H 336x249x8/12", "H", 0.336, 0.249, 0.008, 0.012, 0.008815, 0.000185, 3.09e-05, 0.0011628],
            ["H 340x250x9/14", "H", 0.34, 0.25, 0.009, 0.014, 0.01015, 0.000217, 3.65e-05, 0.001360024],
            ["H 338x351x13/13", "H", 0.338, 0.351, 0.013, 0.013, 0.01353, 0.000282, 9.38e-05, 0.001799343],
            ["H 344x348x10/16", "H", 0.344, 0.348, 0.01, 0.016, 0.0146, 0.000333, 0.000112, 0.002069664],
            ["H 344x354x16/16", "H", 0.344, 0.354, 0.016, 0.016, 0.01666, 0.000353, 0.000118, 0.002247168],
            ["H 350x350x12/19", "H", 0.35, 0.35, 0.012, 0.019, 0.01739, 0.000403, 0.000136, 0.002493182],
            ["H 350x357x19/19", "H", 0.35, 0.357, 0.019, 0.019, 0.01914, 0.000428, 0.000144, 0.002707557],
            ["H 396x199x7/11", "H", 0.396, 0.199, 0.007, 0.011, 0.007216, 0.0002, 1.45e-05, 0.001087548],
            ["H 400x200x8/13", "H", 0.4, 0.2, 0.008, 0.013, 0.008412, 0.000237, 1.74e-05, 0.001285952],
            ["H 404x201x9/15", "H", 0.404, 0.201, 0.009, 0.015, 0.009616, 0.000275, 2.03e-05, 0.001487556],
            ["H 386x299x9/14", "H", 0.386, 0.299, 0.009, 0.014, 0.01201, 0.000337, 6.24e-05, 0.001845561],
            ["H 390x300x10/16", "H", 0.39, 0.3, 0.01, 0.016, 0.0136, 0.000387, 7.21e-05, 0.00211561],
            ["H 388x402x15/15", "H", 0.388, 0.402, 0.015, 0.015, 0.01785, 0.00049, 0.000163, 0.002729805],
            ["H 394x398x11/18", "H", 0.394, 0.398, 0.011, 0.018, 0.01868, 0.000561, 0.000189, 0.003046115],
            ["H 394x405x18/18", "H", 0.394, 0.405, 0.018, 0.018, 0.02144, 0.000597, 0.0002, 0.003317778],
            ["H 400x300x39/24", "H", 0.4, 0.3, 0.039, 0.024, 0.02854, 0.000662, 0.00011, 0.003915264],
            ["H 400x400x13/21", "H", 0.4, 0.4, 0.013, 0.021, 0.02187, 0.000666, 0.000224, 0.003600133],
            ["H 400x408x21/21", "H", 0.4, 0.408, 0.021, 0.021, 0.02507, 0.000709, 0.000238, 0.003920133],
            ["H 406x403x16/24", "H", 0.406, 0.403, 0.016, 0.024, 0.02549, 0.00078, 0.000262, 0.00420736],
            ["H 414x405x18/28", "H", 0.414, 0.405, 0.018, 0.028, 0.02954, 0.000928, 0.00031, 0.004953978],
            ["H 428x407x20/35", "H", 0.428, 0.407, 0.02, 0.035, 0.03607, 0.00119, 0.000394, 0.006239105],
            ["H 458x417x30/50", "H", 0.458, 0.417, 0.03, 0.05, 0.05286, 0.001877, 0.000605, 0.00946803],
            ["H 498x432x45/70", "H", 0.498, 0.432, 0.045, 0.07, 0.07701, 0.00298, 0.00094, 0.014384565],
            ["H 446x199x8/12", "H", 0.446, 0.199, 0.008, 0.012, 0.00843, 0.000287, 1.58e-05, 0.00139256],
            ["H 450x200x9/14", "H", 0.45, 0.2, 0.009, 0.014, 0.009676, 0.000335, 1.87e-05, 0.001621489],
            ["H 434x299x10/15", "H", 0.434, 0.299, 0.01, 0.015, 0.0135, 0.000468, 6.69e-05, 0.002287255],
            ["H 440x300x11/18", "H", 0.44, 0.3, 0.011, 0.018, 0.01574, 0.000561, 8.11e-05, 0.002727644],
            ["H 496x199x9/14", "H", 0.496, 0.199, 0.009, 0.014, 0.01013, 0.000419, 1.84e-05, 0.001835656],
            ["H 500x200x10/16", "H", 0.5, 0.2, 0.01, 0.016, 0.01142, 0.000478, 2.14e-05, 0.00209636],
            ["H 506x201x11/19", "H", 0.506, 0.201, 0.011, 0.019, 0.01313, 0.000565, 2.58e-05, 0.002462169],
            ["H 482x300x11/15", "H", 0.482, 0.3, 0.011, 0.015, 0.01455, 0.000604, 6.76e-05, 0.002663336],
            ["H 488x300x11/18", "H", 0.488, 0.3, 0.011, 0.018, 0.01635, 0.00071, 8.11e-05, 0.003099836],
            ["H 596x199x10/15", "H", 0.596, 0.199, 0.01, 0.015, 0.01205, 0.000687, 1.98e-05, 0.002535175],
            ["H 600x200x11/17", "H", 0.6, 0.2, 0.011, 0.017, 0.01344, 0.000776, 2.28e-05, 0.002863179],
            ["H 606x201x12/20", "H", 0.606, 0.201, 0.012, 0.02, 0.01525, 0.000904, 2.72e-05, 0.003316788],
            ["H 612x202x13/23", "H", 0.612, 0.202, 0.013, 0.023, 0.01707, 0.00103, 3.18e-05, 0.003777651],
            ["H 582x300x12/17", "H", 0.582, 0.3, 0.012, 0.017, 0.01745, 0.00103, 7.67e-05, 0.003782412],
            ["H 588x300x12/20", "H", 0.588, 0.3, 0.012, 0.02, 0.01925, 0.00118, 9.02e-05, 0.004308912],
            ["H 594x302x14/23", "H", 0.594, 0.302, 0.014, 0.023, 0.02224, 0.00137, 0.000106, 0.00501723],
            ["H 692x300x13/20", "H", 0.692, 0.3, 0.013, 0.02, 0.02115, 0.00172, 9.02e-05, 0.005413588],
            ["H 700x300x13/24", "H", 0.7, 0.3, 0.013, 0.024, 0.02355, 0.00201, 0.000108, 0.006248788],
            ["H 708x302x15/28", "H", 0.708, 0.302, 0.015, 0.028, 0.02736, 0.00237, 0.000129, 0.00734422],
            ["H 792x300x14/22", "H", 0.792, 0.3, 0.014, 0.022, 0.02434, 0.00254, 9.93e-05, 0.007040264],
            ["H 800x300x14/26", "H", 0.8, 0.3, 0.014, 0.026, 0.02674, 0.00292, 0.000117, 0.007995464],
            ["H 808x302x16/30", "H", 0.808, 0.302, 0.016, 0.03, 0.03076, 0.00339, 0.000138, 0.009286696],
            ["H 890x299x15/23", "H", 0.89, 0.299, 0.015, 0.023, 0.02668, 0.00339, 0.000103, 0.008633619],
            ["H 900x300x16/28", "H", 0.9, 0.3, 0.016, 0.028, 0.03058, 0.00404, 0.000126, 0.010174144],
            ["H 912x302x18/34", "H", 0.912, 0.302, 0.018, 0.034, 0.03601, 0.00491, 0.000157, 0.012220816],
            ["H 918x303x19/37", "H", 0.918, 0.303, 0.019, 0.037, 0.03874, 0.00535, 0.000172, 0.013260487]
        ]
    # Column names
    columns = ["Section", "Shape", "H", "B", "tw", "tf", "Area", "Iy", "Iz", "Zp"]

    @classmethod
    def to_dataframe(cls):
        # Creating the dataframe
        return pd.DataFrame(cls.data, columns=cls.columns)

    @classmethod
    def get_section_enum(cls):
        df = cls.to_dataframe()
        # Define the HSection enum directly using class syntax
        enum_dict = {section: section for section in df['Section']}
        HSection = Enum('HSection', enum_dict)
        return HSection

# print(HSection['H 100x50x5/7'])
# print(HSection['H 100x50x5/7'].value)




# print(df)

# if abc == KS18Grade.SS275:

# 입력구조체
class InputData(MBaseModel):

    Section: str = Field(default="H 918x303x19/37", title="data_title", description="section 단면 선택",
                     enum=enum_to_list(HSectionData.get_section_enum())
                     )
    Grade: str = Field(default="SS275", title="data_title", description="data_description",
                     enum=enum_to_list(KS18Grades)
                     )

    model_config = ConfigDict(
        title="LEM Pile input Parameter Calculator",
        description="SoilWorks LEM Pile/Nail input Parameter Calculator "
    )

class OutputData(MBaseModel):
    result: str = Field(default="TGC", title="data_title", description="data_description")

    model_config = ConfigDict(
        title="TGC 2024 Output Data test",
        description="It provide output test data description",
        result_table=[
            ["Properties", "Value"],
            ["selected_section",""
             "selected_grade",
             "plastic_moment (kNm)",
             "flexural_rigidity (kNm²)",
             "tension_force (kN)",
             "fy_value (kPa)",
             "E_steel (kN/m²)",
             "zp_value (m³)",
             "iy_value (m⁴)",
             "tensile_strength (kPa)"],
        ]
    )

# def calc(inp: InputData) -> OutputData:
#     # Creating an instance of the class and displaying the dataframe
#     h_section_data = HSectionData()
#     df = HSectionData().to_dataframe()
#     # out = OutputData(result="calculated ")
#
#     return out


# # Creating the enum without an instance
# HSection = HSectionData.get_section_enum()
#
# # df = pd.DataFrame(data)
#
# h_section_data = HSectionData()
# df = HSectionData().to_dataframe()
#
# # # 사용자가 선택한 섹션 정보를 입력
# user_input = InputData(Section="H 918x303x19/37", Grade="SS275")
#
# # 데이터프레임에서 사용자가 선택한 섹션 정보를 찾기
# selected_section = InputData.Section
# filtered_df = df[df["Section"] == selected_section]

# 섹션 속성 및 강종의 항복강도와 인장강도를 계산하는 함수
@auto_schema(title="soilworks section properties calculator", description="desc.")
def calculate_properties(inp: InputData) -> DG_Result_Reports:

    # 탄성계수 (E_steel) 설정 (예: 200 GPa = 200,000,000 kN/m²)
    E_steel = 200000000

    # 강종의 항복강도와 인장강도 계산
    match = re.search(r'\d+', inp.Grade)
    fy_value = int(match.group()) * 1000
    if fy_value == 275000:
        tensile_strength = 410000
    elif fy_value == 355000:
        tensile_strength = 490000
    else:
        tensile_strength = None

    # 데이터 프레임 만들기
    df = HSectionData().to_dataframe()

    # 섹션 속성 계산
    filtered_df = df[df['Section'] == inp.Section]
    if filtered_df.empty:
        raise ValueError(f"섹션 '{inp.Section}'에 해당하는 데이터가 없습니다.")

    iy_value = filtered_df['Iy'].values[0]
    zp_value = filtered_df['Zp'].values[0]
    area_value = filtered_df['Area'].values[0]

    plastic_moment = fy_value * zp_value
    flexural_rigidity = E_steel * iy_value
    tension_force = 0.6 * tensile_strength * area_value

    result = ReportForm(title="Soilworks Section Properties Results", description="blablablabla", result_table=[
        ["Properties", "Value"],
        ["Selected_section", inp.Section],
        ["Selected_grade", inp.Grade],
        ["Plastic_moment (kNm)", plastic_moment],
        ["Flexural_rigidity (kNm²)", flexural_rigidity],
        ["Tension_Force (kN)", tension_force],
        ["fy (MPa)", fy_value],
        ["E (kN/m²)", E_steel],
        ["Zp (m³)", zp_value],
        ["Iy (m⁴)", iy_value],
        ["Tensile_strength (kPa)", tensile_strength]
    ])
    results = {
        "result": [
            [
                result.to_dict()
            ]
        ]
    }
    return DG_Result_Reports(res_report=results)
#
# # 최종 결과를 출력하는 함수
# def print_results(selected_section, selected_grade, plastic_moment, flexural_rigidity, tension_force, fy_value, E_steel,
#                   zp_value, iy_value, tensile_strength):
#     print("\n선택한 단면의 최종 정보:")
#     print(f"선택한 단면: {selected_section}")
#     print(f"선택한 강종: {selected_grade}")
#     print(f"소성모멘트 (Mp): {plastic_moment} kNm")
#     print(f"휨강성 (E * Iy): {flexural_rigidity} kNm²")
#     print(f"인장력 (0.6 * Fu * Ag): {tension_force} kN")
#     print(f"항복강도 (fy): {fy_value} kPa")
#     print(f"탄성계수 (E): {E_steel} kN/m²")
#     print(f"소성단면계수 (Zp): {zp_value} m³")
#     print(f"단면2차 모멘트 (Iy): {iy_value} m⁴")
#     print(f"인장강도 (Fu): {tensile_strength} kPa")

if __name__ == "__main__":
    res = calculate_properties(**{"inp":{"Section":"H 918x303x19/37","Grade":"SS275"}})
    print(res)
