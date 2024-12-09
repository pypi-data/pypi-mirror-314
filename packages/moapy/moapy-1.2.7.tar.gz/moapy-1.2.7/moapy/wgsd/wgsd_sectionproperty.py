from pydantic import Field, ConfigDict
from typing import List, Tuple, Annotated, Union
from sectionproperties.analysis.section import Section
from sectionproperties.pre.geometry import Polygon, Geometry
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.enum_pre import enUnitArea, enUnitInertia, enUnitLength, enUnitVolume, enUnitSystem
from moapy.data_post import SectionProperty
from moapy.mdreporter import ReportUtil
from moapy.data_pre import (
    Point, Points, OuterPolygon, SectionShapeL, SectionShapeC, SectionShapeT, SectionShapeH, SectionRectangle, SectionShapeBox, SectionShapePipe,
    Area, Length, Inertia, Volume, UnitPropertyMixin
)

InputSectionProperty = Annotated[
    Union[
        SectionShapeL,
        SectionShapeC,
        SectionShapeH,
        SectionRectangle,
        SectionShapeT,
        SectionShapeBox,
        SectionShapePipe,
    ],
    Field(default=SectionShapeH(), title="Section Input", discriminator="section_type"),
]

class SectionPropertyInput(MBaseModel):
    input: InputSectionProperty

class SectionCentroid(MBaseModel):
    """
    Section Centroid
    """
    elasticx: Length = Field(default=0.0, description="x-dir. Elastic Centroid")
    elasticy: Length = Field(default=0.0, description="y-dir. Elastic Centroid")
    shearx: Length = Field(default=0.0, description="x-dir. Shear Centroid")
    sheary: Length = Field(default=0.0, description="y-dir. Shear Centroid")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(elasticx=Length(unit=enUnitLength.IN), elasticy=Length(unit=enUnitLength.IN), shearx=Length(unit=enUnitLength.IN), sheary=Length(unit=enUnitLength.IN))
        else:
            return cls(elasticx=Length(unit=enUnitLength.MM), elasticy=Length(unit=enUnitLength.MM), shearx=Length(unit=enUnitLength.MM), sheary=Length(unit=enUnitLength.MM))

    def update_property(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                attr = getattr(self, key)
                if isinstance(value, (int, float)):  # 값만 전달된 경우
                    attr.update_value(value)
                elif isinstance(value, UnitPropertyMixin):  # 전체 객체 전달된 경우
                    setattr(self, key, value)

    model_config = ConfigDict(title="Section Centroid")

class SectionPropertyResult(MBaseModel):
    """
    Section Property Result
    """
    section_property: SectionProperty = Field(default_factory=SectionProperty, description="Section Property")
    section_centroid: SectionCentroid = Field(default_factory=SectionCentroid, description="Section Centroid")

    model_config = ConfigDict(title="Section Property Result")

    def dict(self, **kwargs):
        base_dict = super().dict(**kwargs)
        result = {}

        # Handle section_property field with nested descriptions
        if hasattr(self.section_property, "dict"):
            result["section_property"] = self.section_property.dict(**kwargs)

        # Handle section_centroid field with nested descriptions
        if hasattr(self.section_centroid, "dict"):
            result["section_centroid"] = self.section_centroid.dict(**kwargs)

        # Merge the base dictionary with the detailed field outputs
        return {**base_dict, **result}

@auto_schema(title="Input Polygon", description="Input Polygon")
def input_polygon(points: Points) -> OuterPolygon:
    return OuterPolygon(outerPolygon=points.points)

def convert_points_to_tuple(points: list[Point]) -> Tuple[Tuple[float, float], ...]:
    return tuple((point.x.value, point.y.value) for point in points)

@auto_schema(title="Calculate Section Property", description="Calculate Section Property")
def calc_sectprop(polygon: OuterPolygon) -> SectionProperty:
    polygon = Polygon(convert_points_to_tuple(polygon.points))
    geom = Geometry(polygon)
    geom.create_mesh(mesh_sizes=100.0)
    section = Section(geom)
    section.calculate_geometric_properties()
    section.calculate_warping_properties()
    section.calculate_plastic_properties()
    res = section.calculate_stress(n=0.0, vx=1.0, vy=1.0)
    qyb = max(res.material_groups[0].stress_result.sig_zy_vy) * section.get_ic()[0]
    qzb = max(res.material_groups[0].stress_result.sig_zx_vx) * section.get_ic()[1]
    cx = section.get_c()[0]
    cy = section.get_c()[1]
    return SectionProperty(area=Area(value=section.get_area()), asy=Area(value=section.get_as()[0]), asz=Area(value=section.get_as()[1]), ixx=Inertia(value=section.get_j()), iyy=Inertia(value=section.get_ic()[0]), izz=Inertia(value=section.get_ic()[1]),
                           cyp=Length(value=polygon.bounds[2] - cx), cym=Length(value=cx - polygon.bounds[0]),
                           czp=Length(value=polygon.bounds[3] - cy), czm=Length(value=cy - polygon.bounds[1]),
                           syp=Volume(value=section.get_z()[0]), sym=Volume(value=section.get_z()[1]), szp=Volume(value=section.get_z()[2]), szm=Volume(value=section.get_z()[3]),
                           ipyy=Inertia(value=section.get_ip()[0]), ipzz=Inertia(value=section.get_ip()[1]), zy=Volume(value=section.get_s()[0]), zz=Volume(value=section.get_s()[1]), ry=Length(value=section.get_rc()[0]), rz=Length(value=section.get_rc()[1]),
                           qyb=Area(value=qyb), qzb=Area(value=qzb), periO=Length(value=section.get_perimeter())
                           )


@auto_schema(title="Typical Section Property", description="Typical Section Property")
def calc_sectionproperties_typical(sect: SectionPropertyInput) -> SectionPropertyResult:
    points = sect.input.do_convert_point()
    unitsystem = sect.input.get_unitsystem()
    periInner = 0.0
    if len(points) == 2:
        polygon = Polygon(points[0])
        outer = Geometry(geom=polygon)
        inpolygon = Polygon(points[1])
        inner = Geometry(geom=inpolygon).align_center(align_to=outer)
        geom = outer - inner
        periInner = inpolygon.length
    else:
        polygon = Polygon(points)
        geom = Geometry(polygon)

    geom.create_mesh(mesh_sizes=100)
    section = Section(geom)
    section.calculate_geometric_properties()
    section.calculate_warping_properties()
    section.calculate_plastic_properties()
    x_c, y_c = section.get_c()
    x_s, y_s = section.get_sc()
    cyp = polygon.bounds[2] - x_c
    cym = x_c - polygon.bounds[0]
    czp = polygon.bounds[3] - y_c
    czm = y_c - polygon.bounds[1]
    qyb, qzb = sect.input.calculate_qb_values(cym, czm)
    section_property = SectionProperty.create_default(unitsystem)
    section_property.update_property(area=section.get_area(), asy=section.get_as()[0], asz=section.get_as()[1], ixx=section.get_j(), iyy=section.get_ic()[0], izz=section.get_ic()[1],
                                     cyp=cyp, cym=cym,
                                     czp=czp, czm=czm,
                                     syp=section.get_z()[0], sym=section.get_z()[1], szp=section.get_z()[2], szm=section.get_z()[3],
                                     ipyy=section.get_ip()[0], ipzz=section.get_ip()[1], zy=section.get_s()[0], zz=section.get_s()[1], ry=section.get_rc()[0], rz=section.get_rc()[1],
                                     qyb=qyb, qzb=qzb, periO=section.get_perimeter(), periI=periInner)
    section_centroid = SectionCentroid.create_default(unitsystem)
    section_centroid.update_property(elasticx=x_c, elasticy=y_c, shearx=x_s, sheary=y_s)
    return SectionPropertyResult(section_property=section_property, section_centroid=section_centroid)

@auto_schema(title="Report Section Property", description="Report Section Property")
def report_sectprop(sectprop: SectionProperty) -> str:
    rpt = ReportUtil("sectprop.md", "*Section Properties*")
    rpt.add_line_fvu("A_{rea}", sectprop.area.value, sectprop.area.unit)
    rpt.add_line_fvu("A_{sy}", sectprop.asy.value, sectprop.asy.unit)
    rpt.add_line_fvu("A_{sz}", sectprop.asz.value, sectprop.asz.unit)
    rpt.add_line_fvu("I_{xx}", sectprop.ixx.value, sectprop.ixx.unit)
    rpt.add_line_fvu("I_{yy}", sectprop.iyy.value, sectprop.iyy.unit) 
    rpt.add_line_fvu("I_{zz}", sectprop.izz.value, sectprop.izz.unit)
    rpt.add_line_fvu("C_y", sectprop.cyp.value, sectprop.cyp.unit)
    rpt.add_line_fvu("C_z", sectprop.czp.value, sectprop.czp.unit)
    rpt.add_line_fvu("S_{yp}", sectprop.syp.value, sectprop.syp.unit)
    rpt.add_line_fvu("S_{ym}", sectprop.sym.value, sectprop.sym.unit)
    rpt.add_line_fvu("S_{zp}", sectprop.szp.value, sectprop.szp.unit)
    rpt.add_line_fvu("S_{zm}", sectprop.szm.value, sectprop.szm.unit)
    rpt.add_line_fvu("I_{pyy}", sectprop.ipyy.value, sectprop.ipyy.unit)
    rpt.add_line_fvu("I_{pzz}", sectprop.ipzz.value, sectprop.ipzz.unit)
    rpt.add_line_fvu("Z_y", sectprop.zy.value, sectprop.zy.unit)
    rpt.add_line_fvu("Z_z", sectprop.zz.value, sectprop.zz.unit)
    rpt.add_line_fvu("r_y", sectprop.ry.value, sectprop.ry.unit)
    rpt.add_line_fvu("r_z", sectprop.rz.value, sectprop.rz.unit)
    return rpt.get_md_text()


if __name__ == "__main__":
    data = {
        "sect" : {
        "input": {
            "sectionType": "Angle",
            "b": {
            "value": 300,
            "unit": "mm"
            },
            "h": {
            "value": 500,
            "unit": "mm"
            },
            "tw": {
            "value": 50,
            "unit": "mm"
            },
            "tf": {
            "value": 30,
            "unit": "mm"
            },
        }
        }
    }
    res = calc_sectionproperties_typical(**data)
    print(res.dict())
    print(res.section_property.qyb.value, res.section_property.qzb.value)