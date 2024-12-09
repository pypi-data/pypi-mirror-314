from dataclasses import dataclass, field

@dataclass
class ReportForm:
    id: str = ''  # NOTE: Do not print to JSON
    is_used = False # NOTE : Do not print to json. just for the calculate logic
    standard: str = ''
    reference: str = ''
    title: str = ''
    description: str = ''
    figure_path: str = ''
    descript_table: list = field(default_factory=list)
    symbol: str = ''
    formula: list = field(default_factory=list)
    result: float = 0.0
    result_table: list = field(default_factory=list)
    ref_std: bool = False
    unit: str = ''
    notation: str = 'standard'
    decimal: int = 0  # Default integer value
    limits: dict = field(default_factory=dict)
    
    def to_dict(self):
        return {
            'standard': self.standard,
            'reference': self.reference if isinstance(self.reference, list) else [self.reference],
            'title': self.title,
            'description': self.description,
            'figure_path': self.figure_path,
            'descript_table': self.descript_table,
            'symbol': self.symbol,
            'formula': self.formula if isinstance(self.formula, list) else [self.formula],
            'result': str(self.result),
            'result_table': self.result_table if isinstance(self.result_table, list) else [self.result_table],
            # 'ref_std': self.ref_std,
            'unit': self.unit,
            'notation': self.notation,
            'decimal': self.decimal,
            # 'limits': self.limits if isinstance(self.limits, dict) else [self.limits],
        }
    
    def __repr__(self) -> str:
        full_formula = ""
        full_formula += f"{self.symbol}"
        for curr_formula in self.formula if self.formula else []:
            full_formula += " = " + f"{curr_formula}"
        full_formula += " = " + f"{self.result}" + f" {self.unit}"
                
        return (
            f"[{self.standard} {self.reference}] "
            f"{self.title}\n"
            f"{self.description}\n"
            f"{full_formula}"
        )