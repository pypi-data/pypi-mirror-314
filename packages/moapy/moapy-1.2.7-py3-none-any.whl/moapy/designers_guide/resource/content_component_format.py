component_format = [
    {
        'id': 'G{N}_COMP_{i}', # N: 예제 번호, i: 모듈 번호
        'standard': '{standard_number}', # standard_number: 설계기준 ex) EN1991-1-5
        'reference': ['{reference_1}', '{reference_2}', ...], # reference: 기호 및 수식이 포함되는 section
        'title': '{title}', # title: content component 이름
        'description': r'{description}', # description: component에 대한 설명. 결과 Report에 표시되는 내용
        'figure_file': '{desc_figure}', # desc_figure: dropdown에 표시할 이미지 (path)
        'latex_symbol': r'{symbol}', # symbol: content component의 대표 기호 (필수 입력. 공백 허용 X)
        'latex_equation': r'{equation}', # equation: component의 결과 값을 도출 할 수 있는 수식 (필요 시에만 입력. LaTex 형식)
        'type': '{result_type}', # result_type: 결과 값의 최종 형태 (number, string, table, graph, ...)
        # 'type': 'table' - Report의 결과 값이 table 형태로 출력
        # 'type': 'graph' - Report의 결과 값은 table이지만, UI에서 그래프로 출력
        'unit': '{unit}', # unit: content component 결과 값의 단위 (불필요 시 '' 입력)
        'notation': '{notation}', # notation: component의 결과 값에 대한 표기법 (Standard, Scientific(XeY), Percentage(X%), Text)
        'decimal': '{decimal}', # decimal: component의 결과 값 소수점 자리수 (0, 1, 2, ...)
        'limits': {
            'ex_min': '{exclusive_min}', # exclusive_min: component의 결과 값의 최소 제한 값 (초과)
            'in_min': '{inclusive_min}', # inclusive_min: component의 결과 값의 최소 제한 값 (이상)
            'in_max': '{inclusive_max}', # inclusive_max: component의 결과 값의 최대 제한 값 (이하)
            'ex_max': '{exclusive_max}', # exclusive_max: component의 결과 값의 최대 제한 값 (미만)
        },
        'default': '{default_value}', # default_value: component의 기본 값 (필요 시에만 입력)
        'required': ['{required_id_1}', '{required_id_2}', ...], # required_list: equation 및 table에 필요한 component의 id
        'table': '{table_data_type}', # table_data_type: table에 입력되는 데이터 형식 (dropdown, text, formula, result)
        # 'table': 'dropdown' - 사용자에게 combo box 형태로 입력 받음
        # 'table': 'text' - 특정 조건에 따라 다른 text를 적용
        # 'table': 'formula' - 특정 조건에 따라 다른 formula를 적용
        # 'table': 'result' - Report에 표시할 결과 값에 대한 정보를 담은 table
        'const': '{const_boolean}', # const_boolean: component의 값의 상수 여부. (True: 설계기준에 의해 component의 값이 결정, False)
        'use_std': '{const_boolean}', # const_boolean: default를 가지면서 const가 아닌 경우 작성. component의 값 설계기준 반영 여부 (True, False)
    },
]

# TODO : enum, formula, text, result table 분리 여부 검토
data_table_format = [
    # 'table': 'dropdown'
    {
        'id': '{component_id}', # component_id: table을 사용할 component의 id
        'enum': [
            {
                'label': '{enum_label}', # enum_label: dropdown에 표시할 값
                'description': '{enum_description}', # enum_description: dropdown에 대한 설명
            }
        ],
    },
    # 'table': 'text' and 'fomula'
    {
        'id': '{component_id}', # component_id: table을 사용할 component의 id
        'criteria': [
            ['{criteria_A1}', '{criteria_A2}', ...], # criteria: 적용 조건
            ['{criteria_B1}', '{criteria_B2}', ...], # criteria: 적용 조건
        ],
        # apply_value: 조건 만족 시 적용되는 formula/text (formula - component['latex_equation'] 대체)
        # 조건(criteria) 1개 일 때
        'data': [
            # 1차원 배열로 작성. [column]
            r'{apply_value_A1_B1}',
            r'{apply_value_A1_B2}',
            ..., 
        ],
        # 조건(criteria) 2개 일 때
        'data': [
            # table 모습처럼 작성. [row][column]
            [
                r'{apply_value_A1_B1}', r'{apply_value_A1_B2}', ...
            ],
            [
                r'{apply_value_A2_B1}', r'{apply_value_A2_B2}', ...
            ],
        ],
    },
    # 'table': 'interpolation', 'bi-interpolation
    {
        'id': '{component_id}', # component_id: table을 사용할 component의 id
        'point': {
            r'{ref_symbol_x}' : ['{point_x1}', '{point_x2}', ...], # point: x coordinate
            r'{ref_symbol_y}' : ['{point_y1}', '{point_y2}', ...], # point: y coordinate
        },
        # apply_value: 변수 값 대응되는 지점의 값 (보간법 적용)
        # 1 dimension list
        'data': [
            # 1차원 배열로 작성. [x]
            r'{value_x1}',
            r'{value_x2}',
            ..., 
        ],
        # 2 dimension grid
        'data': [
            # table 모습처럼 작성. [x][y]
            [
                r'{value_x1_y1}', r'{value_x1_y2}', ...
            ],
            [
                r'{value_x2_y1}', r'{value_x2_y2}', ...
            ],
        ],
    },
    # 'table': 'result'
    {
        'id': '{component_id}', # component_id: table을 사용할 component의 id
        'data': [
            { # row 1
                '{colum_1}': r'{colum_value_1}', # colum_value_1: 표시할 값
                '{colum_2}': r'{colum_value_1}', # colum_value_2: 표시할 값 (수식이 들어갈 수 있음)
            },
            { # row 2
                '{colum_1}': r'{colum_value_1}', # colum_value_1: 표시할 값
                '{colum_2}': r'{colum_value_1}', # colum_value_2: 표시할 값 (수식이 들어갈 수 있음)
            },
        ],
    },
]