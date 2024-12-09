import moapy.designers_guide.resource.content_component as content_comp
import moapy.designers_guide.resource.report_form as report_form

import re
import sympy
import numpy as np
from sympy.parsing.latex import parse_latex
from scipy.interpolate import interp1d, RegularGridInterpolator

from moapy.designers_guide.utils import cache_result

__symbol_mappings = {}
__all__ = ["pre_process_before_calc", "get_function_tree_by_components", "get_report_bundles", "make_report_json"]

def replace_min_max(sympy_expr):
    """sympy_expr에서 min과 max를 SymPy의 Min과 Max로 변환합니다."""
    if sympy_expr.has(sympy.Function('min')):
        sympy_expr = sympy_expr.subs({
            sympy.Function('min'): sympy.Min,
        })
    if sympy_expr.has(sympy.Function('max')):
        sympy_expr = sympy_expr.subs({
            sympy.Function('max'): sympy.Max
        })

    return sympy_expr

# @cache_result # TODO : 중간 계산식 문제로 임시 비활성화
def custom_parse_latex(latex_str: str) -> str:
    def preprocess_log(latex_str):
        processed = []
        i = 0
        while i < len(latex_str):
            if latex_str[i:i + 4] == r"\log":  # \log 발견
                processed.append(r"\log")  # 기본적으로 추가
                i += 4

                if i < len(latex_str) and latex_str[i] == "_": # 밑이 있다면 그대로 추가                    
                    processed.append("_")
                    i += 1
                    if i < len(latex_str) and latex_str[i] == "{":  # 밑의 시작
                        processed.append("{")
                        i += 1
                        brace_level = 1
                        while i < len(latex_str) and brace_level > 0:
                            processed.append(latex_str[i])
                            if latex_str[i] == "{":
                                brace_level += 1
                            elif latex_str[i] == "}":
                                brace_level -= 1
                            i += 1
                else: # 밑이 없는 경우 log_{10}으로 치환
                    processed.append(r"_{10}")
            else:
                processed.append(latex_str[i])
                i += 1

        return "".join(processed)
    
    preprocessed_latex = preprocess_log(latex_str) # parse_latex 이전에 log(x) 형식 전처리
    sympy_expr: sympy.Equality = parse_latex(preprocessed_latex)
    
    sympy_expr = replace_min_max(sympy_expr)

    return sympy_expr

# Func Desc. Insert spaces around operators in LaTeX
def insert_spaces(latex_expr):
    operators = content_comp.binary_operators + content_comp.relation_operators + content_comp.function_operators

    for op in operators:
        latex_expr = re.sub(f'({op})([^ ])', r'\1 \2', latex_expr)
        latex_expr = re.sub(f'([^ ])({op})', r'\1 \2', latex_expr)
    return re.sub(r'\s+', ' ', latex_expr).strip()

def is_latex_equation(expr):
    operators = content_comp.binary_operators + content_comp.relation_operators + content_comp.function_operators

    for op in operators:
        if re.search(op, expr):
            return True
    return False

# Func Desc. Make simple symbols and map
def get_symbol_mappings():
    global __symbol_mappings
    if __symbol_mappings != {}:
        return __symbol_mappings
    
    comp_list = content_comp.component_list
    __symbol_mappings = {(item['latex_symbol'], item['id']): f'S_{{{i + 1}}}' for i, item in enumerate(comp_list)}
    __symbol_mappings = dict(sorted(__symbol_mappings.items(), key=lambda item: len(item[0][0]), reverse=True))
    return __symbol_mappings

# Func Desc. Replace LaTeX symbols
def pre_process_before_calc():
    get_symbol_mappings()
    content_comp.component_list = replace_symbols_in_equations(content_comp.component_list)

def replace_latex_to_simple(latex_str, symbol_mappings, required_comps = None):
    symbol_mappings = get_symbol_mappings()
    lhs = latex_str.split('=')[0].strip()
    simple_str = latex_str

    for sym_id, simple_symbol in symbol_mappings.items():
        sym = sym_id[0]
        id = sym_id[1]
        if sym != lhs and required_comps != None and id not in required_comps: 
            continue
        simple_str = re.sub(rf'(?<!\w){re.escape(sym)}(?!\w)', simple_symbol, simple_str)
    return simple_str

# Func Desc. Replace LaTeX symbols with simple symbols in Component list
def replace_symbols_in_equations(comp_list):
    symbol_mappings = get_symbol_mappings()
    for comp in (m for m in comp_list if "latex_equation" in m):
        required_symbols = comp['required'] if 'required' in comp else None
        preprocessed_eq = comp['latex_equation']
        preprocessed_eq = replace_latex_to_simple(preprocessed_eq, symbol_mappings, required_symbols)
        comp['preprocessed_equation'] = preprocessed_eq
        comp['sympy_expr'] = custom_parse_latex(preprocessed_eq)
    return comp_list

class TreeNode:
    def __init__(self, symbol, operation=None, children=None):
        self.symbol = symbol  # 노드의 심볼 (변수 또는 함수명)
        self.operation = operation  # 노드의 연산자 또는 함수 정의
        self.children = children if children is not None else []  # 자식 노드 리스트

    def add_child(self, child_node):
        self.children.append(child_node)

def replace_log_to_ln(equation):
    stack = []
    replaced_equation = []

    i = 0
    while i < len(equation):
        if equation[i:i+4] == "log(":
            stack.append(len(replaced_equation))
            replaced_equation.append("ln(")
            i += 4
        elif len(stack) > 0 and equation[i:i+4] == ", E)":
            replaced_equation.append(")")
            stack.pop()
            i += 4
        else:
            replaced_equation.append(equation[i])
            i += 1

    return ''.join(replaced_equation)

def get_child_components_from_required(comp):
    if 'required' in comp:
        return comp['required']
    return []

def get_calc_tree(target_comp_id):
    target_comp = content_comp.find_by_id(target_comp_id)
    if target_comp is None:
        return None
    
    target_symbol = target_comp['latex_symbol']
    tree_node = TreeNode(target_symbol, target_comp)
    
    child_comps = set(get_child_components_from_required(target_comp))
    for child in child_comps:
        child_comp = get_calc_tree(child)
        if child_comp is not None:
            tree_node.add_child(child_comp)
        else:
            tree_node.add_child(TreeNode(target_symbol, target_comp))
        
    return tree_node

def get_function_tree_by_components(target_comps_id):
    params_tree = []
    for target_comp_id in target_comps_id:
        content_tree = get_calc_tree(target_comp_id)
        if content_tree is not None:
            params_tree.append(content_tree)
    return params_tree

def is_calcuated_symbol(stack_reports, symbol):
    return any(report.symbol == symbol for report in stack_reports)

def unique_merge_report(stack_reports, sub_reports): 
    symbols_stack = {report.symbol for report in stack_reports}
    symbols_sub = {report.symbol for report in sub_reports}
    duplicates = symbols_stack & symbols_sub
    unique_sub_reports = [report for report in sub_reports if report.symbol not in duplicates]
    return unique_sub_reports

def sympy_post_replace_symbols(expr):
    if r'pi' in str(expr): # pi
        pi = sympy.symbols(r'pi')
        expr = expr.subs(pi, sympy.pi.evalf())
    return expr

def sympy_post_processing(expr): # 단순 계산이 안되는 연산식 처리
    expr_rhs_str = str(expr.rhs)
    res_value = sympy.parse_expr(expr_rhs_str)
    expr = sympy.Eq(expr.lhs, res_value)
    # rhs_value = 0
    # min_match = re.search(r'min\(([\d\.]+),\s*([\d\.]+)\)', expr_rhs_str)
    # max_match = re.search(r'max\(([\d\.]+),\s*([\d\.]+)\)', expr_rhs_str)
    # if min_match:
    #     rhs_value = sympy.Min(*map(float, min_match.groups()))
    # elif max_match:
    #     rhs_value = sympy.Max(*map(float, max_match.groups()))
    # else:
    #     return None
    # expr_rhs_str = expr_rhs_str.replace(min_match.group(), str(rhs_value))
    # expr_rhs_simbol = sympy.parse_expr(expr_rhs_str)
    # expr = sympy.Eq(expr.lhs, expr_rhs_simbol)
    # recursion_expr = sympy_post_processing(expr)
    # if recursion_expr is not None:
    #     expr = recursion_expr
    return expr

def replace_frac_to_division(latex_expr):
    def replace_frac(match):
        # Extract the numerator and denominator contents
        numerator, denominator = match.groups()
        # Process nested fractions recursively
        numerator = replace_frac_to_division(numerator)
        denominator = replace_frac_to_division(denominator)
        return f"({numerator})/({denominator})"
    # Keep replacing until there are no more \frac expressions
    while r'\frac' in latex_expr:
        latex_expr = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', replace_frac, latex_expr)
    return latex_expr

def validate_criteria(criteria_str, symbol_result, required_symbols, used_symbols):
    symbol_mappings = get_symbol_mappings()
    criteria = replace_latex_to_simple(criteria_str, symbol_mappings, required_symbols)
    for sym, disp_sym, res in symbol_result:
        if sym in criteria:
            criteria = criteria.replace(sym, str(res))
            used_symbols.add(disp_sym)

    def replace_latex_for_criteria(expr):
        # Replace logical operators
        expr = expr.replace(r'\land', 'and').replace(r'\lor', 'or')
        expr = expr.replace(r'\leq', '<=').replace(r'\geq', '>=')
        expr = expr.replace(r'\lt', '<').replace(r'\gt', '>')
        expr = expr.replace(r'\lt', '<').replace(r'\gt', '>')
        # Replace fractions (\frac{a}{b} -> (a)/(b))
        expr = replace_frac_to_division(expr)
        return expr
    
    criteria_expr = replace_latex_for_criteria(criteria)
    try: # Attempt to evaluate as a mathematical expression
        is_found = sympy.sympify(criteria_expr)
    except Exception as e: # Fallback to string comparison
        criteria_expr = re.sub(r'(?<![<>!])=(?![=<>])', '==', criteria_expr)
        splited_cr = [part.strip() for part in re.split(r'==', criteria_expr)]
        if len(splited_cr) == 2:
            is_found = splited_cr[0] == splited_cr[1]
        else:
            print(f"Error during evaluation: {e} and is not valid for string comparison.")
            is_found = False

    return bool(is_found)

def format_log(base_expr, inner_expr, is_natural):
    log_func = r'\ln' if is_natural else r'\log' # 자연로그 여부에 따라 함수명을 결정
    if inner_expr.is_Mul and inner_expr.args[0] == -1: # 음수 표현이 포함된 경우 '-' 기호만 추가
        return f'{log_func}\\left(-{convert_latex_formula(inner_expr.args[1])}\\right)'
    if not is_natural: # 밑이 있는 로그인 경우
        return f'{log_func}_{{{convert_latex_formula(base_expr)}}}\\left({convert_latex_formula(inner_expr)}\\right)'
    return f'{log_func}\\left({convert_latex_formula(inner_expr)}\\right)' # 기본 로그 출력

def convert_latex_formula(expr):
    symbol_mul = r' \times '
    if expr.is_Atom: # basic atom
        return sympy.latex(expr, mul_symbol=symbol_mul)
    
    elif expr.func == sympy.log: # Logs(로그)
        if len(expr.args) == 2: # with a base: log(a, E), log(a, b) 
            base_expr, inner_expr = expr.args[1], expr.args[0]
            return format_log(base_expr, inner_expr, is_natural=(base_expr == sympy.E))
        else: # without a base: log(a)
            return format_log(sympy.Integer(10), expr.args[0], is_natural=False)
        
    elif expr.func == sympy.Mul: # Multiple(곱셈)
        numerators = []
        denominators = []
        for arg in expr.args:
            if arg == -1: # `-1` 단독 : 기호만 추가
                numerators.append('-')
            elif arg.func == sympy.Pow and arg.args[1] == -1: # 음수 지수
                denominators.append(convert_latex_formula(arg.args[0]))
            elif arg.func == sympy.log: # log
                numerators.append(convert_latex_formula(arg))
            elif arg.is_negative:  # 음수 : 분자로 취급하되, 기호를 -로 처리
                numerators.append(f"-{convert_latex_formula(-arg)}")
            else:
                numerators.append(convert_latex_formula(arg))

        if numerators[0] == "-":  # '-' 기호가 단독으로 나온 경우 공백 제거
            expr_numerator = "-" + symbol_mul.join(num for num in numerators[1:])
        else:
            expr_numerator = symbol_mul.join(numerators)
            
        if denominators: # 분자와 분모를 구분하여 출력
            return r'\frac{' + expr_numerator + r'}{' + symbol_mul.join(denominators) + r'}'
        else:
            return expr_numerator
        
    elif expr.func == sympy.Pow: # Power(거듭제곱): b^a
        base, exp = expr.args
        if exp == -1: # x^{-1}
            return r'\frac{1}{' + convert_latex_formula(base) + r'}'
        elif isinstance(exp, sympy.Rational) and 0 < exp < 1 and exp.p == 1: # x^{1/n}
            denominator = exp.q
            if denominator == 2:  # x^(1/2): 제곱근
                return r'\sqrt{' + convert_latex_formula(base) + r'}'
            else:  # x^(1/n): 일반적인 n제곱근
                return r'\sqrt[' + str(denominator) + r']{' + convert_latex_formula(base) + r'}'
        else: # x^{y}
            return convert_latex_formula(base) + "^{" + convert_latex_formula(exp) + r'}'
        
    elif expr.is_Add: # Addition(덧셈)
        numerators = []
        for arg in expr.args:
            if arg.is_negative:  # 음수인 기호 -로 별도 처리
                numerators.append(f"-{convert_latex_formula(-arg)}")
            else:
                numerators.append(convert_latex_formula(arg))
        return numerators[0] + ' ' + ' '.join(f"+ {num}" if num[0] != '-' else num for num in numerators[1:])
    
    else: # Etc.
        return sympy.latex(expr, mul_symbol=symbol_mul)

def post_tune_latex(latex_str):
    latex_str = latex_str.replace(r'\operatorname', '').replace(r'\frac', r'\dfrac')
    latex_str = latex_str.replace('--', '+').replace('+-', '-').replace('-+', '-').replace('- -', '+').replace('- +', '-').replace('+ -', '-')
    return latex_str

def get_report(node, comp_to_value):
    symbol_mappings = get_symbol_mappings()
    params_report = []
    symbol_result = []
    for chlid in node.children:
        if is_calcuated_symbol(params_report, chlid.symbol):
            continue
        sub_reports = get_report(chlid, comp_to_value)
        if sub_reports is None:
            continue
        for sub_report in sub_reports:
            symbol_result.append(tuple([symbol_mappings[(f"{sub_report.symbol}", f"{sub_report.id}")], sub_report.symbol, sub_report.result]))
        unique_sub_reports = unique_merge_report(params_report, sub_reports)
        params_report.extend(unique_sub_reports)

    for comp_val in comp_to_value:
        simple_symbol = symbol_mappings[next(((sym, id) for (sym, id) in symbol_mappings if id == comp_val['component']), (None, None))]
        if next((item for item in symbol_result if item[0] == simple_symbol), None):
            continue
        required = node.operation.get('required', [])
        if required == []:
            continue
        req_id = next((req_param for req_param in required if req_param == comp_val['component']), None)
        if req_id:
            sym = content_comp.find_by_id(req_id)['latex_symbol']
            symbol_result.append(tuple([symbol_mappings[(sym, req_id)], sym, comp_val['value']]))
    symbol_result = set(frozenset(symbol_result))

    current_comp_id = node.operation['id']
    current_comp = content_comp.find_by_id(current_comp_id)
    
    current_report = report_form.ReportForm()
    current_report.id = current_comp_id
    current_report.is_used = False
    current_report.standard = current_comp['standard']
    current_report.reference = current_comp['reference']
    current_report.title = current_comp['title']
    current_report.description = current_comp['description']
    current_report.figure_path = f"{content_comp.get_figure_server_url()}/{current_comp['figure_file']}" if (current_comp.get('figure_file', None) != None) else None
    current_report.descript_table = content_comp.convert_enum_table_to_detail(current_comp)
    current_report.symbol = current_comp['latex_symbol']
    current_report.formula = []
    current_report.unit = current_comp.get('unit', '')
    current_report.notation = current_comp['notation']
    current_report.decimal = current_comp.get('decimal', 0)
    current_report.ref_std = current_comp.get('use_std', False)
    current_report.limits = current_comp.get('limits', {})
    current_report.result_table = []
    if 'default' in current_comp:
        current_report.result = current_comp['default']

    required_symbols = current_comp['required'] if 'required' in current_comp else None

    input_value = next((item for item in comp_to_value if item['component'] == current_comp_id), None)
    if input_value:
            current_report.result = input_value['value']
    
    used_symbols = set()
    if 'table' in current_comp:
        table_type = current_comp['table']
        if table_type == 'dropdown': # 'table' : 'dropdown'
            table_enum = content_comp.get_table_enum_by_component(current_comp)
            for te in table_enum if table_enum else []:
                if te['label'] == input_value['value']:
                    current_report.result = te['label']
        if table_type == 'text' or table_type == 'formula': # 'table' : 'text' or 'formula'
            ref_table = content_comp.get_table_by_component(current_comp)
            if 'criteria' not in ref_table or 'data' not in ref_table:
                # TODO : Error Handling
                print("Error : criteria or data is not in table_data")
            
            criteria_table = ref_table.get('criteria', [])
            num_criteria = len(criteria_table)
            matched_cr = []
            for group_cr in range(num_criteria):
                for idx_cr, cr_expr in enumerate(criteria_table[group_cr]):
                    if validate_criteria(cr_expr, symbol_result, required_symbols, used_symbols):
                        matched_cr.append(idx_cr)
                        break

            if matched_cr != [] and len(matched_cr) == num_criteria:
                if num_criteria == 1:
                    table_data = ref_table['data'][matched_cr[0]]
                elif num_criteria == 2:
                    table_data = ref_table['data'][matched_cr[0]][matched_cr[1]]

                if table_type == 'text':
                    current_report.result = table_data
                elif table_type == 'formula':
                    node.operation['sympy_expr'] = custom_parse_latex(replace_latex_to_simple(table_data, symbol_mappings, required_symbols))

        if table_type == 'result': # 'table' : 'result'
            table_data = content_comp.get_table_data_by_component(current_comp)
            for i, td in enumerate(table_data) if table_data else []:
                if i == 0:
                    header_list = []
                    for key, value in td.items():
                        header_list.append(key)
                    current_report.result_table.append(tuple(header_list))
                row_list = []
                for key, value in td.items():
                    res_value = ""
                    if is_latex_equation(str(value)):
                        calc_expr = insert_spaces(value)
                        expr_parts = re.split(r'\\text\{([^}]*)\}', str(calc_expr))
                        for i, part in enumerate(expr_parts):
                            if i % 2 == 0:
                                part_expr = custom_parse_latex(replace_latex_to_simple(part, symbol_mappings, required_symbols))
                                for sym, disp_sym, res in symbol_result:
                                    x = sympy.symbols(f"{sym}")
                                    if part_expr.has(x):
                                        part_expr = part_expr.subs(x, res)
                                        used_symbols.add(disp_sym)
                                res_value += f"{str(part_expr.evalf())} "
                            else:
                                res_value += f"{part} "
                    else:
                        res_value = str(value)
                    row_list.append(res_value)
                current_report.result_table.append(row_list)
        if table_type == 'interpolation' or table_type == 'bi-interpolation':
            table_itrpl = content_comp.get_table_by_component(current_comp)
            point_data = table_itrpl.get('point', {})
            dimension = len(point_data)
            if dimension == 1:
                x_symbol = list(point_data.keys())[0]
                x_value = next((item[2] for item in symbol_result if item[1] == x_symbol), None)
                if x_value != None:
                    x_point = np.array(point_data[x_symbol])
                    z_value = np.array(table_itrpl['data'])
                    if x_value < x_point.min(): x_value = x_point.min()
                    elif x_value > x_point.max(): x_value = x_point.max()
                    f_linear = interp1d(x_point, z_value, kind='linear')
                    current_report.result = f_linear(float(x_value)).item()
                used_symbols.add(x_symbol)
            elif dimension == 2:
                x_symbol = list(point_data.keys())[0]
                y_symbol = list(point_data.keys())[1]

                x_value = next((item[2] for item in symbol_result if item[1] == x_symbol), None)
                y_value = next((item[2] for item in symbol_result if item[1] == y_symbol), None)
                if x_value != None and y_value != None:
                    x_point = np.array(point_data[x_symbol])
                    y_point = np.array(point_data[y_symbol])
                    z_value = np.array(table_itrpl['data'])
                    if x_value < x_point.min(): x_value = x_point.min()
                    elif x_value > x_point.max(): x_value = x_point.max()
                    if y_value < y_point.min(): y_value = y_point.min()
                    elif y_value > y_point.max(): y_value = y_point.max()
                    xy_point = (float(x_value), float(y_value))

                    interp_func = RegularGridInterpolator((x_point, y_point), z_value)
                    current_report.result = interp_func(xy_point).item()
                used_symbols.add(x_symbol)
                used_symbols.add(y_symbol)
            else:
                # TODO : Error Handling
                print("Error : point data is not in table of interpolation")
    
    if 'sympy_expr' in current_comp: # fomula
        expr = node.operation['sympy_expr']
        org_formula = convert_latex_formula(expr.rhs)
        mid_formula = org_formula
        for sym, disp_sym, res in symbol_result:
            x = sympy.symbols(f"{sym}")
            if expr.has(x):
                expr = expr.subs(x, res)
                used_symbols.add(disp_sym)
            org_formula = org_formula.replace(sym, disp_sym)
            mid_formula = mid_formula.replace(sym, str(res))
        expr = sympy_post_replace_symbols(expr)

        org_formula = post_tune_latex(org_formula)
        mid_formula = post_tune_latex(mid_formula)
        
        current_report.result = expr.evalf().rhs
        if org_formula != current_report.result:
            current_report.formula.append(org_formula)
        if org_formula != mid_formula:
            current_report.formula.append(mid_formula)

        if 'min' in str(expr) or 'max' in str(expr):
            expr = sympy_post_processing(expr)
            current_report.result = expr.evalf().rhs
    
    if used_symbols:
        set_is_used_by_symbol(params_report, used_symbols)

    params_report.append(current_report)
    
    return params_report

def set_is_used_by_symbol(params_report, used_symbols):
    for report in params_report:
        if report.symbol in used_symbols:
            report.is_used = True

def get_report_bundles(content_trees, symbol_to_value):
    report_bundles = []
    for content_tree in content_trees:
        report_bundles.append(get_report(content_tree, symbol_to_value))
    
    report_bundles = get_unique_report_bundles(report_bundles)
    return report_bundles

def get_unique_report_bundles(report_bundles):
    processed_symbols = []
    report_bundle_unique = []
    for report_bundle in report_bundles:
        report_unique = []
        for report in report_bundle:
            if report.symbol in processed_symbols:
                continue
            if report != report_bundle[-1] and report.is_used == False:
                continue
            report_unique.append(report)
            processed_symbols.append(report.symbol)
        report_bundle_unique.append(report_unique)
    return report_bundle_unique

def make_report_json(report_bundles):
    report_bundle_json = []
    for report_bundle in report_bundles:
        report_json = []
        for report in report_bundle:
            report_json.append(report.to_dict())
        report_bundle_json.append(report_json)
    return {"result": report_bundle_json}