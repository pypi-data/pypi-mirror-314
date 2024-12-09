import moapy.designers_guide.content_calculator as calc_logic
from moapy.auto_convert import MBaseModel
from pydantic import Field

class DG_Result_Reports(MBaseModel):
    res_report: dict = Field(default_factory=dict)

def execute_calc_content(target_components: list, req_input: dict) -> DG_Result_Reports:
    symbol_to_value = []
    for id, val in req_input.items():
        symbol_to_value.append({"component": id, "value": val})

    calc_logic.pre_process_before_calc()
    content_trees = calc_logic.get_function_tree_by_components(target_components)
    report_bundles = calc_logic.get_report_bundles(content_trees, symbol_to_value)
    report_json = calc_logic.make_report_json(report_bundles)

    return DG_Result_Reports(res_report=report_json)