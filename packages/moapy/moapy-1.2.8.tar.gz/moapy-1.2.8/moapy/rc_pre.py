from typing import Optional
from pydantic import Field, ConfigDict
from moapy.auto_convert import MBaseModel
from moapy.data_pre import Point, Stress_Strain_Component, Length, enUnitLength, Stress, enUnitStress, MaterialCurve, Area, enUnitArea, SectionRectangle
from moapy.enum_pre import enum_to_list, enUnitArea, enUnitLength, enUnitStress, enUnitThermalExpansion, enUnitAngle, enUnitTemperature, enDgnCode, enBoltName, enUnitMoment, enRebar_UNI, enUnitSystem
# ==== Concrete Material ====
class ConcreteGrade(MBaseModel):
    """
    GSD concrete class

    Args:
        design_code (str): Design code
        grade (str): Grade of the concrete
    """
    design_code: str = Field(
        default="ACI318M-19", description="Design code")
    grade: str = Field(
        default="C12", description="Grade of the concrete")

    model_config = ConfigDict(title="Concrete Grade")

class Concrete_General_Properties(MBaseModel):
    """
    GSD concrete general properties for calculation
    
    Args:
        strength (int): Grade of the concrete
        elastic_modulus (float): Elastic modulus of the concrete
        density (float): Density of the concrete
        thermal_expansion_coefficient (float): Thermal expansion coefficient of the concrete
        poisson_ratio (float): Poisson ratio of the concrete
    """
    strength: int = Field(
        gt=0, default=12, description="Grade of the concrete")
    elastic_modulus: float = Field(
        gt=0, default=30000, description="Elastic modulus of the concrete")
    density: float = Field(
        gt=0, default=2400, description="Density of the concrete")
    thermal_expansion_coefficient: float = Field(
        gt=0, default=0.00001, description="Thermal expansion coefficient of the concrete")
    poisson_ratio: float = Field(
        gt=0, default=0.2, description="Poisson ratio of the concrete")

    model_config = ConfigDict(title="Concrete General Properties")

class Concrete_Stress_ULS_Options_ACI(MBaseModel):
    """
    GSD concrete stress options for ULS
    
    Args:
        material_model (str): Material model for ULS
        factor_b1 (float): Plastic strain limit for ULS
        compressive_failure_strain (float): Failure strain limit for ULS
    """
    material_model: str = Field(
        default="Rectangle", description="Material model for ULS")
    factor_b1: float = Field(
        default=0.85, description="Plastic strain limit for ULS")
    compressive_failure_strain: float = Field(
        default=0.003, description="Failure strain limit for ULS")

    model_config = ConfigDict(title="Concrete Stress Options for ULS")

class Concrete_Stress_ULS_Options_Eurocode(MBaseModel):
    """
    GSD concrete stress options for ULS
    
    Args:
        material_model (str): Material model for ULS
        partial_factor_case (float): Partial factor case for ULS
        partial_factor (float): Partial factor for ULS
        compressive_failure_strain (float): Failure strain limit for ULS
    """
    material_model: str = Field(
        default="Rectangle", description="Material model for ULS")
    partial_factor_case: float = Field(
        default=1.0, description="Partial factor case for ULS")
    partial_factor: float = Field(
        default=1.5, description="Partial factor for ULS")
    compressive_failure_strain: float = Field(
        default=0.003, description="Failure strain limit for ULS")

    model_config = ConfigDict(title="Concrete Stress Options for ULS")

class Concrete_SLS_Options(MBaseModel):
    """
    GSD concrete stress options for SLS
    
    Args:
        material_model (str): Material model for SLS
        plastic_strain_limit (float): Plastic strain limit for SLS
        failure_compression_limit (float): Failure compression limit for SLS
        material_model_tension (str): Material model for SLS tension
        failure_tension_limit (float): Failure tension limit for SLS
    """
    material_model: str = Field(
        default="Linear", description="Material model for SLS")
    plastic_strain_limit: float = Field(
        default=0.002, description="Plastic strain limit for SLS")
    failure_compression_limit: float = Field(
        default=0.003, description="Failure compression limit for SLS")
    material_model_tension: str = Field(
        default="interpolated", description="Material model for SLS tension")
    failure_tension_limit: float = Field(
        default=0.003, description="Failure tension limit for SLS")

    model_config = ConfigDict(title="Concrete Stress Options for SLS")

# ==== Rebar & Tendon Materials ====
class RebarGrade(MBaseModel):
    """
    GSD rebar grade class
    
    Args:
        design_code (str): Design code
        grade (str): Grade of the rebar
    """
    design_code: str = Field(
        default="ACI318M-19", description="Design code")
    grade: str = Field(
        default="Grade 420", description="Grade of the rebar")

    model_config = ConfigDict(title="Rebar Grade")

class TendonGrade(MBaseModel):
    """
    GSD Tendon grade class
    
    Args:
        design_code (str): Design code
        grade (str): Grade of the tendon
    """
    design_code: str = Field(
        default="ACI318M-19", description="Design code")
    grade: str = Field(default="Grade 420", description="Grade of the tendon")

    model_config = ConfigDict(title="Tendon Grade")

class RebarProp(MBaseModel):
    """
    GSD rebar prop

    Args:
        area (float): Area of the rebar
    """
    area: Area = Field(default=Area(value=287.0, unit=enUnitArea.MM2), description="Area of the rebar")

    model_config = ConfigDict(title="Rebar Properties")

class TendonProp(MBaseModel):
    """
    GSD Tendon prop

    Args:
        area (float): Area of the tendon
        prestress (float): Prestress of the tendon
    """
    area: Area = Field(default=Area(value=287.0, unit=enUnitArea.MM2), description="Area of the tendon")
    prestress: Stress = Field(default=Stress(value=0.0, unit=enUnitStress.MPa), description="Prestress of the tendon")

    model_config = ConfigDict(title="Tendon Properties")

class Rebar_General_Properties(MBaseModel):
    """
    GSD rebar general properties for calculation
    
    Args:
        strength (int): Grade of the rebar
        elastic_modulus (float): Elastic modulus of the rebar
        density (float): Density of the rebar
        thermal_expansion_coefficient (float): Thermal expansion coefficient of the rebar
        poisson_ratio (float): Poisson ratio of the rebar
    """
    strength: int = Field(
        default=420, description="Grade of the rebar")
    elastic_modulus: float = Field(
        default=200000, description="Elastic modulus of the rebar")
    density: float = Field(
        default=7850, description="Density of the rebar")
    thermal_expansion_coefficient: float = Field(
        default=0.00001, description="Thermal expansion coefficient of the rebar")
    poisson_ratio: float = Field(
        default=0.3, description="Poisson ratio of the rebar")

    model_config = ConfigDict(title="Rebar General Properties")

class Rebar_Stress_ULS_Options_ACI(MBaseModel):
    """
    GSD rebar stress options for ULS
    
    Args:
        material_model (str): Material model for ULS
        failure_strain (float): Failure strain limit for ULS
    """
    material_model: str = Field(
        default="Elastic-Plastic", description="Material model for ULS")
    failure_strain: float = Field(
        default=0.7, description="Failure strain limit for ULS")

    model_config = ConfigDict(title="Rebar Stress Options for ULS")

class Rebar_Stress_SLS_Options(MBaseModel):
    """
    GSD rebar stress options for SLS
    
    Args:
        material_model (str): Material model for SLS
        failure_strain (float): Failure strain limit for SLS
    """
    material_model: str = Field(
        default="Elastic-Plastic", description="Material model for SLS")
    failure_strain: float = Field(
        default=0.7, metadata={"default" : 0.7, "description": "Failure strain limit for SLS"})

    model_config = ConfigDict(title="Rebar Stress Options for SLS")

class MaterialRebar(MaterialCurve):
    """
    GSD rebar class
    
    Args:
        grade (RebarGrade): Grade of the rebar
        curve_uls (list[Stress_Strain_Component]): Stress strain curve for ULS
        curve_sls (list[Stress_Strain_Component]): Stress strain curve for SLS
    """
    curve_uls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.0025, stress=500.0), Stress_Strain_Component(strain=0.05, stress=500.0)], description="Stress strain curve")
    curve_sls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.0025, stress=500.0), Stress_Strain_Component(strain=0.05, stress=500.0)], description="Stress strain curve")

    model_config = ConfigDict(title="Material Rebar")

class MaterialTendon(MaterialCurve):
    """
    GSD tendon class
    
    Args:
        grade (TendonGrade): Grade of the tendon
        curve_uls (list[Stress_Strain_Component]): Stress strain curve for ULS
        curve_sls (list[Stress_Strain_Component]): Stress strain curve for SLS
    """
    curve_uls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.00725, stress=1450.0), Stress_Strain_Component(strain=0.05, stress=1750.0)], description="Stress strain curve")
    curve_sls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.00725, stress=1450.0), Stress_Strain_Component(strain=0.05, stress=1750.0)], description="Stress strain curve")

    model_config = ConfigDict(title="Material Tendon")

class MaterialConcrete(MaterialCurve):
    """
    GSD material for Concrete class
    
    Args:
        curve_uls (list[Stress_Strain_Component]): Stress strain curve concrete ULS
        curve_sls (list[Stress_Strain_Component]): Stress strain curve
    """
    curve_uls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.0006, stress=0.0), Stress_Strain_Component(strain=0.0006, stress=34.0), Stress_Strain_Component(strain=0.003, stress=34.0)], description="Stress strain curve concrete ULS")
    curve_sls: list[Stress_Strain_Component] = Field(default=[Stress_Strain_Component(strain=0.0, stress=0.0), Stress_Strain_Component(strain=0.001, stress=32.8)], description="Stress strain curve")

    model_config = ConfigDict(title="Material Concrete")

class Material(MBaseModel):
    """
    GSD concrete class

    Args:
        concrete (MaterialConcrete): Concrete properties
        rebar (MaterialRebar): Rebar properties
        tendon (MaterialTendon): Tendon properties
    """
    concrete: MaterialConcrete = Field(default=MaterialConcrete(), description="Concrete properties")
    rebar: Optional[MaterialRebar] = Field(default=MaterialRebar(), description="Rebar properties")
    tendon: Optional[MaterialTendon] = Field(default=MaterialTendon(), description="Tendon properties")

    def __post_init__(self):
        if self.rebar is None and self.tendon is None:
            raise ValueError("Either rebar or tendon must be provided.")

    model_config = ConfigDict(title="Material")

class MaterialNative(MBaseModel):
    """
    Material Native Data for Concrete and Rebar Strengths
    This class represents the material properties of concrete and reinforcement bars (rebars) 
    used in structural design, including their respective strengths for design calculations.
    """
    fck: Stress = Field(
        default_factory=Stress,
        title="Concrete Compressive Strength (fck)",
        description="The characteristic strength of concrete in compression, typically measured in MPa (SI) or psi (US). This is a key parameter in the design of concrete structures."
    )

    fy: Stress = Field(
        default_factory=Stress,
        title="Rebar Yield Strength (fy)",
        description="The yield strength of the reinforcement bars (rebar) used in concrete, typically measured in MPa (SI) or psi (US). It represents the stress at which the rebar begins to plastically deform."
    )

    fys: Stress = Field(
        default_factory=Stress,
        title="Stirrup Yield Strength (fys)",
        description="The yield strength of stirrups (reinforcing steel ties used for shear reinforcement) in concrete, typically measured in MPa (SI) or psi (US)."
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        """Create default values based on unit system"""
        if unit_system == enUnitSystem.US:
            return cls(
                fck=Stress(value=3500.0, unit="psi"),  # US units (psi)
                fy=Stress(value=58000.0, unit="psi"),  # US units (psi)
                fys=Stress(value=58000.0, unit="psi"),  # US units (psi)
            )
        else:  # SI units by default
            return cls(
                fck=Stress(value=24.0, unit="MPa"),  # SI units (MPa)
                fy=Stress(value=400.0, unit="MPa"),  # SI units (MPa)
                fys=Stress(value=400.0, unit="MPa"),  # SI units (MPa)
            )

    model_config = ConfigDict(
        title="Material Strength Properties",
        json_schema_extra={
            "description": "Defines the material strength properties of concrete and reinforcement used in structural design, including compressive strength of concrete and yield strength of rebars and stirrups."
        }
    )

class ConcreteGeometry(MBaseModel):
    """
    GSD concrete geometry class
    
    Args:
        outerPolygon (list[Point]): Outer polygon of the concrete
        innerPolygon (list[Point]): Inner polygon of the concrete
    """
    outerPolygon: list[Point] = Field(default=[Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)), Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)), 
                                               Point(x=Length(value=400.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM)), Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=600.0, unit=enUnitLength.MM))], description="Outer polygon of the concrete")
    innerPolygon: list[Point] = Field(default=[Point(x=Length(value=80.0, unit=enUnitLength.MM), y=Length(value=80.0, unit=enUnitLength.MM)), Point(x=Length(value=320.0, unit=enUnitLength.MM), y=Length(value=80.0, unit=enUnitLength.MM)),
                                               Point(x=Length(value=320.0, unit=enUnitLength.MM), y=Length(value=520.0, unit=enUnitLength.MM)), Point(x=Length(value=80.0, unit=enUnitLength.MM), y=Length(value=520.0, unit=enUnitLength.MM))], description="Inner polygon of the concrete")

    model_config = ConfigDict(title="Concrete Geometry")

class RebarGeometry(MBaseModel):
    """
    GSD rebar geometry class

    Args:
        prop (RebarProp): properties of the rebar
        points (list[Point]): Rebar Points
    """
    prop: RebarProp = Field(default=RebarProp(), description="properties of the rebar")
    points: list[Point] = Field(default=[Point(x=Length(value=40.0, unit=enUnitLength.MM), y=Length(value=40.0, unit=enUnitLength.MM)), Point(x=Length(value=360.0, unit=enUnitLength.MM), y=Length(value=40.0, unit=enUnitLength.MM)),
                                         Point(x=Length(value=360.0, unit=enUnitLength.MM), y=Length(value=560.0, unit=enUnitLength.MM)), Point(x=Length(value=40.0, unit=enUnitLength.MM), y=Length(value=560.0, unit=enUnitLength.MM))], description="Rebar Points")

    model_config = ConfigDict(title="Rebar Geometry")

class TendonGeometry(MBaseModel):
    """
    GSD tendon geometry class
    
    Args:
        prop (TendonProp): properties of the tendon
        points (list[Point]): Tendon Points
    """
    prop: TendonProp = Field(default=TendonProp(), description="properties of the tendon")
    points: list[Point] = Field(default=[], description="Tendon Points")

    model_config = ConfigDict(title="Tendon Geometry")

class Geometry(MBaseModel):
    """
    GSD geometry class

    Args:
        concrete (ConcreteGeometry): Concrete geometry
        rebar (RebarGeometry): Rebar geometry
        tendon (TendonGeometry): Tendon geometry
    """
    concrete: ConcreteGeometry = Field(default=ConcreteGeometry(), description="Concrete geometry")
    rebar: Optional[list[RebarGeometry]] = Field(default=[RebarGeometry()], description="Rebar geometry")
    tendon: Optional[list[TendonGeometry]] = Field(default=[TendonGeometry()], description="Tendon geometry")

    model_config = ConfigDict(title="Geometry")

class SlabMember_EC(MBaseModel):
    """
    Slab Member class for defining the concrete slab properties.

    Args:
        fck (Stress): Concrete compressive strength (fck) in MPa.
        thickness (Length): Thickness of the slab in mm.
    """
    fck: Stress = Field(default=Stress(value=24.0, unit=enUnitStress.MPa), title="Concrete Strength (fck)", description="Compressive strength of the concrete in MPa, representing its ability to resist axial load.")
    thickness: Length = Field(default=Length(value=150.0, unit=enUnitLength.MM), title="Slab Thickness", description="Thickness of the slab in millimeters, representing the depth of the concrete slab section.")

    model_config = ConfigDict(
        title="Concrete Slab Member",
        json_schema_extra={
            "description": "Defines a concrete slab member with properties such as compressive strength (fck) and thickness, essential for structural design and load-bearing capacity evaluation."
        }
    )

class GirderLength(MBaseModel):
    """
    Girder Length class to define the span and spacing of girders in a structure.

    Args:
        span (Length): Span length of the girder.
        spacing (Length): Spacing between the girders.
    """
    span: Length = Field(default=Length(value=10.0, unit=enUnitLength.M), title="Span Length", description="The distance between two supports of the girder. This is a critical measurement in determining the load-carrying capacity of the girder.")
    spacing: Length = Field(default=Length(value=3.0, unit=enUnitLength.M), title="Spacing", description="The distance between adjacent girders. Proper spacing ensures optimal load distribution and stability of the structure.")

    model_config = ConfigDict(
        title="Girder Length and Spacing",
        json_schema_extra={
            "description": "Defines the span length and spacing between girders in a structure, crucial for ensuring proper load distribution and structural stability."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        """Create default values based on unit system"""
        if unit_system == enUnitSystem.US:
            return cls(span=Length(value=30, unit=enUnitLength.FT), spacing=Length(value=8, unit=enUnitLength.FT))
        else:
            return cls(span=Length(value=10, unit=enUnitLength.M), spacing=Length(value=3, unit=enUnitLength.M))

class NeutralAxisDepth(MBaseModel):
    """
    Neutral Axis Depth
    """
    depth: Length = Field(default=Length(value=0.0, unit=enUnitLength.MM), title="Neutral Axis Depth", description="Neutral Axis Depth")

    model_config = ConfigDict(title="Neutral Axis Depth", description="Neutral Axis Depth")

class RebarNumberNameCover(MBaseModel):
    """
    Rebar Number and Cover Information
    This class defines the details for a specific rebar used in the concrete structure, 
    including the number of rebars, their designation (name), and the concrete cover 
    distance from the centroid of the reinforcement to the nearest surface of the concrete.
    """
    number: int = Field(
        default=2,
        title="Number of Rebars",
        description="The number of reinforcement bars (rebars) used in the given location. This specifies how many rebars are placed together in the beam or column section."
    )

    name: str = Field(
        default="P26",
        title="Rebar Name",
        description="The name or designation of the rebar. This typically refers to the type or size of the rebar, such as 'P26' or 'D16'.",
        enum=enum_to_list(enRebar_UNI)
    )

    cover: Length = Field(
        default_factory=Length,
        title="Concrete Cover",
        description="The distance from the centroid of the rebar to the nearest surface of the concrete. This cover ensures adequate protection for the rebar and prevents corrosion."
    )

    model_config = ConfigDict(
        title="Rebar Number and Cover",
        json_schema_extra={
            "description": "Defines the number, name, and concrete cover for reinforcement bars (rebars) used in concrete structures. The concrete cover ensures the durability and protection of the rebars from environmental factors."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        """Create default values based on unit system"""
        if unit_system == enUnitSystem.US:
            return cls(cover=Length(value=1.5, unit=enUnitLength.IN))  # US units (inches)
        else:  # SI units by default
            return cls(cover=Length(value=40, unit=enUnitLength.MM))  # SI units (millimeters)


class RebarNumberRowNameCover(MBaseModel):
    """
    Rebar Number, Row, and Concrete Cover Information
    This class defines the details for a specific rebar, including the number of rebars, 
    their designation (name), the number of rows of rebars, and the concrete cover distance 
    from the centroid of the reinforcement to the nearest surface of the concrete.
    """

    number: int = Field(
        default=4,
        title="Number of Rebars",
        description="The total number of reinforcement bars (rebars) used in the given location. This specifies how many rebars are placed together in a beam or column section."
    )

    row: int = Field(
        default=2,
        title="Number of Rows",
        description="The number of rows of rebars in the given location. This specifies how the rebars are distributed vertically in the section."
    )

    name: str = Field(
        default="P26",
        title="Rebar Name",
        description="The name or designation of the rebar. This typically refers to the type or size of the rebar, such as 'P26' or 'D16'.",
        enum=enum_to_list(enRebar_UNI)
    )

    cover: Length = Field(
        default_factory=Length,
        title="Concrete Cover",
        description="The distance from the centroid of the rebar to the nearest surface of the concrete. This cover ensures adequate protection for the rebar and prevents corrosion."
    )

    model_config = ConfigDict(
        title="Rebar Number, Row, and Cover",
        json_schema_extra={
            "description": "Defines the number of rebars, the number of rows of rebars, and the concrete cover for reinforcement bars (rebars) used in concrete structures. The concrete cover ensures the durability and protection of the rebars from environmental factors."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        """Create default values based on unit system"""
        if unit_system == enUnitSystem.US:
            return cls(cover=Length(value=2, unit=enUnitLength.IN))  # US units (inches)
        else:  # SI units by default
            return cls(cover=Length(value=60, unit=enUnitLength.MM))  # SI units (millimeters)

class RebarNumberNameSpace(MBaseModel):
    """
    Rebar Number, Name, and Spacing Information
    This class defines the details for a specific rebar, including the number of rebars, 
    their designation (name), and the spacing between the rebars.
    """

    number: int = Field(
        default=2,
        title="Number of Legs",
        description="The number of legs for the reinforcement bar. This specifies how many individual legs (bars) are used for the rebar."
    )

    name: str = Field(
        default="P10",
        title="Rebar Name",
        description="The name or designation of the rebar. This typically refers to the type or size of the rebar, such as 'P10' or 'D12'.",
        enum=enum_to_list(enRebar_UNI)
    )

    space: Length = Field(
        default_factory=Length,
        title="Rebar Spacing",
        description="The distance between adjacent rebars. This specifies the spacing between each reinforcement bar to ensure proper load transfer and concrete bonding."
    )

    model_config = ConfigDict(
        title="Rebar Number and Spacing",
        json_schema_extra={
            "description": "Defines the number of legs of rebars and the spacing between them for reinforcement in concrete structures. Proper spacing ensures load transfer efficiency and concrete bonding around the rebar."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        """Create default values based on unit system"""
        if unit_system == enUnitSystem.US:
            return cls(space=Length(value=10, unit=enUnitLength.IN))  # US units (inches)
        else:  # SI units by default
            return cls(space=Length(value=100, unit=enUnitLength.MM))  # SI units (millimeters)

class RebarPointName(MBaseModel):
    """
    Rebar Point Name
    """
    point: Point = Field(default=Point(x=Length(value=0.0, unit=enUnitLength.MM), y=Length(value=0.0, unit=enUnitLength.MM)), title="Point", description="Rebar Point")
    name: str = Field(default="P26", title="Name", description="Rebar Name", enum=enum_to_list(enRebar_UNI))

    model_config = ConfigDict(title="Rebar Point Name", description="Rebar Point Name")

class BeamRebarPattern(MBaseModel): 
    """
    Beam Rebar Pattern
    This class represents the reinforcement pattern of a beam, including the top and bottom reinforcement bars (rebars) and stirrups (shear reinforcement). 
    The pattern specifies the number, type, and spacing of rebars based on the unit system.
    """

    top: list[RebarNumberNameCover] = Field(
        default_factory=list,
        title="Top Reinforcement Bars",
        description="List of top reinforcement bars (rebars) for the beam. Includes details such as rebar number, type, and cover distance from the beam surface."
    )

    bot: list[RebarNumberNameCover] = Field(
        default_factory=list,
        title="Bottom Reinforcement Bars",
        description="List of bottom reinforcement bars (rebars) for the beam. Includes details such as rebar number, type, and cover distance from the beam surface."
    )

    stirrup: RebarNumberNameSpace = Field(
        default_factory=RebarNumberNameSpace,
        title="Stirrup Reinforcement",
        description="Details of the stirrup reinforcement for the beam, including the rebar type, spacing, and other parameters for shear reinforcement."
    )

    model_config = ConfigDict(
        title="Beam Rebar Pattern",
        json_schema_extra={
            "description": "Defines the rebar pattern for a beam, including top and bottom reinforcement bars (rebars) and stirrup reinforcements. The pattern is determined based on the unit system (SI or US) and includes specifications like number, size, type, and spacing of rebars."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        """Create default values based on unit system"""
        if unit_system == enUnitSystem.US:
            return cls(
                top=[RebarNumberNameCover.create_default(enUnitSystem.US)],
                bot=[RebarNumberNameCover.create_default(enUnitSystem.US)],
                stirrup=RebarNumberNameSpace.create_default(enUnitSystem.US)
            )
        else:  # SI units by default
            return cls(
                top=[RebarNumberNameCover.create_default(enUnitSystem.SI)],
                bot=[RebarNumberNameCover.create_default(enUnitSystem.SI)],
                stirrup=RebarNumberNameSpace.create_default(enUnitSystem.SI)
            )

class ColumnRebarPattern(MBaseModel):
    """
    Defines the rebar pattern for a column, including main reinforcement bars, end stirrups, and mid stirrups.
    
    Attributes:
        main (list[RebarNumberRowNameCover]): Main reinforcement bars for the column.
        end_stirrup (RebarNumberNameSpace): End stirrup reinforcement for the column.
        mid_stirrup (RebarNumberNameSpace): Middle stirrup reinforcement for the column.
    """
    main: list[RebarNumberRowNameCover] = Field(
        default_factory=list,
        title="Main Rebar",
        description="Main reinforcement bars for the column, including specifications such as number, size, and cover."
    )
    end_stirrup: RebarNumberNameSpace = Field(
        default_factory=RebarNumberNameSpace,
        title="End Stirrup",
        description="End stirrup reinforcement for the column, typically used for confinement at the ends."
    )
    mid_stirrup: RebarNumberNameSpace = Field(
        default_factory=RebarNumberNameSpace,
        title="Middle Stirrup",
        description="Middle stirrup reinforcement for the column, used for confinement in the midsection."
    )

    model_config = ConfigDict(
        title="Column Rebar Pattern",
        json_schema_extra={
            "description": "Defines the rebar pattern for a column, including main reinforcement bars, end stirrups, and mid stirrups."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        """Create default values based on unit system"""
        if unit_system == enUnitSystem.US:
            return cls(
                main=[RebarNumberRowNameCover.create_default(enUnitSystem.US)],
                end_stirrup=RebarNumberNameSpace.create_default(enUnitSystem.US),
                mid_stirrup=RebarNumberNameSpace.create_default(enUnitSystem.US)
            )
        else:  # SI units by default
            return cls(
                main=[RebarNumberRowNameCover.create_default(enUnitSystem.SI)],
                end_stirrup=RebarNumberNameSpace.create_default(enUnitSystem.SI),
                mid_stirrup=RebarNumberNameSpace.create_default(enUnitSystem.SI)
            )

class GeneralRebarPattern(MBaseModel):
    """
    Defines the general rebar pattern, including main reinforcement points, cover, and stirrup reinforcement.

    Attributes:
        main (list[RebarPointName]): Main rebar points, defined by their positions (x, y) in the cross-section.
        cover (Length): Cover distance, representing the distance from the reinforcement to the outer surface of the concrete.
        stirrup (RebarNumberNameSpace): Stirrup rebar reinforcement, used to provide confinement to the main reinforcement bars.
    """
    main: list[RebarPointName] = Field(
        default=[
            RebarPointName(point=Point(x=Length(value=40), y=Length(value=40))),
            RebarPointName(point=Point(x=Length(value=360), y=Length(value=40))),
            RebarPointName(point=Point(x=Length(value=40), y=Length(value=560))),
            RebarPointName(point=Point(x=Length(value=360), y=Length(value=560)))
        ],
        title="Main Rebar",
        description="Main reinforcement bars defined by their positions (x, y) in the section, used for load-bearing in the structural design."
    )
    cover: Length = Field(
        default=Length(value=22.0, unit=enUnitLength.MM),
        title="Cover",
        description="Distance from the centroid of reinforcement to the nearest surface of the concrete, providing protection against corrosion."
    )
    stirrup: RebarNumberNameSpace = Field(
        default=RebarNumberNameSpace(),
        title="Stirrup",
        description="Stirrup rebar reinforcement, used to provide confinement and shear strength in the structural member."
    )

    model_config = ConfigDict(
        title="General Rebar Pattern",
        json_schema_extra={
            "description": "Defines the general rebar pattern, including main reinforcement points, cover, and stirrup reinforcement for a structural element."
        }
    )

class EquivalentAreaGeneralSect(MBaseModel):
    """
    Defines the equivalent area for a general section, representing the effective width and depth for structural analysis.

    Attributes:
        b (Length): Effective width of the section, used in the calculation of section properties.
        d (Length): Effective depth of the section, used in the calculation of section properties.
    """
    b: Length = Field(
        default_factory=Length,
        title="Effective Width",
        description="The effective width of the section, which is used to determine section properties such as moment of inertia and bending capacity."
    )
    d: Length = Field(
        default_factory=Length,
        title="Effective Depth",
        description="The effective depth of the section, which is used to determine section properties such as bending capacity and shear strength."
    )

    model_config = ConfigDict(
        title="Equivalent Area for General Section",
        json_schema_extra={
            "description": "Defines the equivalent area for a general section, including effective width and depth for structural analysis."
        }
    )
