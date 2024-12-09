import ctypes
import os
from pydantic import Field, ConfigDict
from moapy.auto_convert import auto_schema, MBaseModel

class InFy(MBaseModel):
    matlcode: str = Field(default='KS18(S)', description="Material code")
    matlname: str = Field(default='SS275', description="Material name")
    thick: float = Field(default=5.0, description="Thickness")

    model_config = ConfigDict(
        title="Fy Input Data",
        description="Fy Input Data"
    )

class OutFy(MBaseModel):
    fy: float = Field(default=0.0, description="Fy Value")

    model_config = ConfigDict(
        title="Fy Output Data",
        description="Fy Output Data"
    )

@auto_schema(title="Fy Calculation", description="Fy Calculation")
def call_getfy(inp: InFy) -> OutFy:
    # 현재 스크립트의 디렉토리 경로를 가져옴
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # DLL 파일의 정확한 경로를 설정
    dll_path = os.path.join(script_dir, 'dll', 'dgn_api.dll')

    # DLL 파일 로드
    dll = ctypes.CDLL(dll_path)
    # 구조체 인스턴스 생성
    sMatlCode = ctypes.create_string_buffer(inp.matlcode.encode('utf-8'), 50)  # 50은 예시 크기
    sMatlName = ctypes.create_string_buffer(inp.matlname.encode('utf-8'), 50)  # 50은 예시 크기
    sSectName = ctypes.create_string_buffer(b'Test', 50)  # 50은 예시 크기
    dThickness = ctypes.c_double(inp.thick)  # 예제 두께 값

    # DLL 함수 프로토타입 정의
    dll.GetFy.argtypes = [ctypes.c_void_p,
                          ctypes.c_void_p,
                          ctypes.c_void_p,
                          ctypes.c_double]
    dll.GetFy.restype = ctypes.c_double

    # 함수 호출
    result = dll.GetFy(ctypes.byref(sMatlCode),
                       ctypes.byref(sMatlName),
                       ctypes.byref(sSectName),
                       dThickness)

    return result
