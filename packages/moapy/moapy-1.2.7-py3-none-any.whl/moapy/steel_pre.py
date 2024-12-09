from pydantic import Field, ConfigDict
from typing import List
from moapy.auto_convert import MBaseModel
from moapy.enum_pre import enum_to_list, enConnectionType, enUnitLength, en_H_EN10365, enSteelMaterial_EN10025, en_H_AISC05_US, enBoltName, enBoltMaterialEC, enSteelMaterial_ASTM, en_H_AISC10_US, en_H_AISC10_SI, enUnitSystem, enAnchorType, enBoltMaterialASTM, enUnitStress
from moapy.data_pre import Length, BucklingLength, Stress, Percentage

# ==    == Steel DB ====
class SteelLength(BucklingLength):
    """
    Steel DB Length
    """
    l_b: Length = Field(default_factory=Length, title="Lb", description="Lateral unbraced length")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        instance = super().create_default(unit_system)
        if unit_system == enUnitSystem.US:
            instance.l_b = Length(value=15, unit=enUnitLength.IN)
        else:
            instance.l_b = Length(value=3000, unit=enUnitLength.MM)

        return instance

    model_config = ConfigDict(
        title="Member Length",
        json_schema_extra={
            "description": "Buckling length is the length at which a structural member, such as a column or plate, can resist the phenomenon of buckling. Buckling is the sudden deformation of a long member under compressive load along its own center of gravity, which has a significant impact on the safety of a structure. Buckling length is an important factor in analyzing and preventing this phenomenon."
        }
    )

class SteelLength_EC(SteelLength):
    """
    Steel DB Length
    """
    l_t: Length = Field(default_factory=Length, title="Lt", description="Torsional Buckling Length")

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        instance = super().create_default(unit_system)
        instance.l_t = Length(value=3000, unit=enUnitLength.MM)
        return instance

    model_config = ConfigDict(
        title="Member Length",
        json_schema_extra={
            "description": "Buckling length is the length at which a structural member, such as a column or plate, can resist the phenomenon of buckling. Buckling is the sudden deformation of a long member under compressive load along its own center of gravity, which has a significant impact on the safety of a structure. Buckling length is an important factor in analyzing and preventing this phenomenon."
        }
    )

class SteelMomentModificationFactorLTB(MBaseModel):
    """
    Steel DB Moment Modification Factor
    """
    c_b: float = Field(default=1.0, title="Cb", description="Cb Modification Factor")

    model_config = ConfigDict(
        title="Steel Moment Modification Factor",
        json_schema_extra={
            "description": "It is calculated based on the moment distribution, using Mmax(the maximum moment within the unbraced length) and specific moments at certain points (Ma, Mb, Mc)"
        }
    )

class SteelMomentModificationFactor(MBaseModel):
    """
    Steel DB Moment Modification Factor
    """
    c_mx: float = Field(default=1.0, title="Cmx", description="Cmx Modification Factor")
    c_my: float = Field(default=1.0, title="Cmy", description="Cmy Modification Factor")

    model_config = ConfigDict(
        title="Steel Moment Modification Factor",
        json_schema_extra={
            "description": "A coefficient used in structural design to adjust the moments in a structure based on specific conditions or types of support. It is often applied to improve the assessment of loads and moments on columns, beams, or other structural elements. moment modification factor plays an important role in adjusting the moments to reflect the behavior and loading conditions of the structure."
        }
    )

class SteelMomentModificationFactor_EC(SteelMomentModificationFactor):
    """
    Steel DB Moment Modification Factor
    """
    c1: float = Field(default=1.0, title="C1", description="ratio between the critical bending moment and the critical constant bending moment for a member with hinged supports")
    c_mlt: float = Field(default=1.0, title="Cmlt", description="equivalent uniform moment factor for LTB")

    model_config = ConfigDict(
        title="Steel Moment Modification Factor",
        json_schema_extra={
            "description": "A coefficient used in structural design to adjust the moments in a structure based on specific conditions or types of support. It is often applied to improve the assessment of loads and moments on columns, beams, or other structural elements. moment modification factor plays an important role in adjusting the moments to reflect the behavior and loading conditions of the structure."
        }
    )

class SteelSection(MBaseModel):
    """
    Steel DB Section
    """
    shape: str = Field(
        default='H',
        title="Section Shape",
        description="Structural steel section profile type (e.g., H-shape, I-beam, Channel, Angle). This parameter defines the fundamental cross-sectional geometry of the steel member.",
        readOnly=True
    )

    name: str = Field(
        default=None,
        title="Section Designation",
        description="Standardized designation of the steel section based on industry specifications. This identifier corresponds to specific dimensional and structural properties in the steel section database.",
        enum=[]
    )

    model_config = ConfigDict(
        title="Steel Section Database Parameters",
        json_schema_extra={
            "description": "Database specifications for structural steel sections including section shape and standardized member designations. This configuration provides essential cross-sectional properties for structural steel design and analysis."
        }
    )

    @classmethod
    def create_default(cls, name: str, enum_list: List[str], description: str = ""):
        """
        Creates an instance of SteelSection with a specific enum list and dynamic description for the name field.
        """
        section = cls()
        # Dynamically set the enum for the name field
        section.__fields__['name'].json_schema_extra['enum'] = enum_list
        # Set default name if enum_list is provided
        section.name = name
        # Change description dynamically
        if description:
            cls.model_config["description"] = description
        return section

class SteelSection_AISC05_US(SteelSection):
    """
    Steel Section Specification (AISC 2005 US)
    """
    shape: str = Field(
        default='H', 
        description="Defines the shape of the structural steel section. In this case, 'H' represents an H-beam, commonly used in construction for its high load-bearing capacity.",
        readOnly=True,
        title="Section Shape"
    )
    name: str = Field(
        default='W40X362', 
        description="Select the specific steel section from the available list of shapes. The 'W40X362' is a typical designation for a wide-flange section, specifying its nominal depth and weight.",
        title="Section Name", 
        enum=enum_to_list(en_H_AISC05_US)
    )

    model_config = ConfigDict(
        title="Steel Section (AISC 2005 US)",
        json_schema_extra={
            "description": "This model provides a detailed specification for steel sections based on the AISC 2005 standards. Currently, only 'H' (wide-flange) sections are supported, and users can select from a predefined list of available sections."
        }
    )

class SteelSection_AISC10_US(SteelSection):
    """
    Steel DB Section
    """
    shape: str = Field(default='H', description="Shape of member section", readOnly=True)
    name: str = Field(default='W40X183', description="Please select a section.", enum=enum_to_list(en_H_AISC10_US))

    model_config = ConfigDict(
        title="Steel DB Section",
        json_schema_extra={
            "description": "Currently, only H-sections are supported."
        }
    )

class SteelSection_AISC10_SI(SteelSection):
    """
    Steel DB Section
    """
    shape: str = Field(default='H', description="Shape of member section", readOnly=True)
    name: str = Field(default="W360X72", description="Please select a section.", enum=enum_to_list(en_H_AISC10_SI))

    model_config = ConfigDict(
        title="Steel DB Section",
        json_schema_extra={
            "description": "Currently, only H-sections are supported."
        }
    )

class SteelSection_EN10365(SteelSection):
    """
    Steel DB Section wit
    """
    shape: str = Field(default='H', description="Shape of member section", readOnly=True)
    name: str = Field(default='HD 260x54.1', description="Use DB stored in EN10365", enum=enum_to_list(en_H_EN10365))

    model_config = ConfigDict(
        title="Steel DB Section",
        json_schema_extra={
            "description": "EN 10365 is a European standard that defines specifications for cross sections of structural steel. The standard supports the accurate design of steel sections used in a variety of structures, including requirements for the shape, dimensions, tolerances, and mechanical properties of steel. EN 10365 is primarily concerned with the design of beams, plates, tubes, and other structural elements."
        }
    )

class SteelMaterial(MBaseModel):
    """
    Steel Material for structural design.
    
    This model represents a steel material used in structural applications. It includes 
    information about the material code, its name, and the available material options 
    from a predefined list. This information is crucial for steel material selection 
    and ensuring that the correct material is used in structural design calculations.
    """
    # Material code for the steel, usually assigned based on industry standards
    code: str = Field(default_factory=str, description="Unique code for the material as defined in the material database. This is used to identify the specific steel material.", readOnly=True)

    # Name of the steel material, selected from a predefined list of available materials
    name: str = Field(default_factory=str, description="Name of the steel material. The material name is selected from a list of available materials.", enum=[])

    @classmethod
    def create_default(cls, code: str, enum_list: List[str], description: str = "Steel DB Material"):
        """
        Create a SteelMaterial instance with customizable values including description.
        
        This method allows for the creation of a SteelMaterial instance by specifying 
        the material code, a list of available material names (enum list), and an optional 
        description to provide additional context for the material.
        """
        material = cls()
        # Dynamically set the description for the material
        material.model_config["description"] = description
        # Dynamically set the enum options for the 'name' field
        material.__fields__['name'].json_schema_extra['enum'] = enum_list
        material.code = code
        material.name = enum_list[0] if enum_list else None
        return material

    model_config = ConfigDict(
        title="Steel Material",
        json_schema_extra={
            "description": "A steel material used in structural design, with customizable options for material code and name. The material properties are selected from a predefined list."
        }
    )

class SteelMaterial_EC(SteelMaterial):
    """
    Steel DB Material
    """
    code: str = Field(default='EN10025', description="Material code", readOnly=True)
    name: str = Field(default=enSteelMaterial_EN10025.S275, description="Material of steel member", enum=enum_to_list(enSteelMaterial_EN10025))

    model_config = ConfigDict(
        title="Steel DB Material",
        json_schema_extra={
            "description": "EN 10025 is the standard for steel materials used in Europe and specifies the technical requirements for steel, primarily for structural purposes. The standard defines mechanical properties, chemical composition, manufacturing methods, and inspection methods for different types of steel. EN 10025 is divided into several parts, each of which covers requirements for a specific steel type."
        }
    )

class BoltMaterial(MBaseModel):
    """
    Bolt Material
    """
    # Material name, representing the type or grade of the bolt material
    name: str = Field(
        default_factory=str,
        title="Bolt Material Type",
        description="The type or grade of the material used for the bolt. This determines the bolt's mechanical properties, such as strength, ductility, and corrosion resistance.",
        enum=[]
    )

    @classmethod
    def create_default(cls, name: str, enum_list: List[str]):
        """
        Creates a default instance of BoltMaterial with a dynamic material name and enum list.
        """
        material = cls()
        material.__fields__['name'].json_schema_extra['enum'] = enum_list
        material.name = name
        return material

    model_config = ConfigDict(
        title="Bolt Material Specifications",
        json_schema_extra={
            "description": "This model defines the properties of the bolt material, including its type and mechanical characteristics. The material type affects the bolt's strength, durability, and suitability for specific applications."
        }
    )

class BoltMaterial_EC(BoltMaterial):
    """
    Bolt Material
    """
    name: str = Field(default='4.8', description="Bolt Material Name", enum=enum_to_list(enBoltMaterialEC))

    model_config = ConfigDict(
        title="Bolt Material",
        json_schema_extra={
            "description": "Bolt Material"
        }
    )

class SteelMember(MBaseModel):
    """
    Steel Member class representing a structural steel member, consisting of a section and material. 

    Args:
        sect (SteelSection): The cross-sectional shape and properties of the steel member.
        matl (SteelMaterial): The material properties of the steel member, including strength and durability.
    """
    sect: SteelSection = Field(default_factory=SteelSection, title="Section", description="The cross-sectional shape and properties of the steel member.")
    matl: SteelMaterial = Field(default_factory=SteelMaterial, title="Material", description="The material properties, including strength, durability, and composition, of the steel member.")

    model_config = ConfigDict(
        title="Steel Member",
        json_schema_extra={
            "description": "A steel member consists of both the section (cross-sectional shape) and material (material properties). Proper selection of the section and material is critical for ensuring the strength, stability, and durability of the structure. This contributes to the design of a safe and efficient steel structure."
        }
    )

class SteelMember_EC(SteelMember):
    """
    Steel Member class for defining the properties of steel members used in structural design.

    Args:
        sect (SteelSection_EN10365): Section shape of the steel member.
        matl (SteelMaterial_EC): Material used for the steel member.
    """
    sect: SteelSection_EN10365 = Field(default=SteelSection_EN10365(), title="Section Shape", description="Shape of the steel member section, defining its geometric properties.")
    matl: SteelMaterial_EC = Field(default=SteelMaterial_EC(), title="Material", description="Material of the steel member, specifying its composition and mechanical properties.")

    model_config = ConfigDict(
        title="Steel Member",
        json_schema_extra={
            "description": "Steel sections and material inputs are fundamental elements of structural design, each requiring proper selection based on their characteristics and requirements. Proper selection of the section shape and material maximizes the strength, stability, and durability of the structure and ensures the safe and efficient design of the steel member."
        }
    )

class SteelConnectMember(MBaseModel):
    """
    Steel Connect Member class representing the relationship between supporting and supported members in a connection.
    
    Args:
        supporting (SteelMember): The supporting member that provides resistance to forces.
        supported (SteelMember): The supported member that receives the load from the supporting member.
    """
    supporting: SteelMember = Field(default_factory=SteelMember, title="Supporting Member", description="The member that supports and resists forces.")
    supported: SteelMember = Field(default_factory=SteelMember, title="Supported Member", description="The member that is supported and carries the load from the supporting member.")

    model_config = ConfigDict(
        title="Steel Connect Member",
        json_schema_extra={
            "description": "Defines the connection between two steel members: one acting as the supporting member, and the other as the supported member. This connection is crucial in bolted joints, contributing to load transfer and ensuring the stability and safety of the structure."
        }
    )

class SteelConnectMember_EC(SteelConnectMember):
    """
    Steel Connect Member
    """
    supporting: SteelMember_EC = Field(default_factory=SteelMember_EC, title="Supporting member", description="Supporting Member")
    supported: SteelMember_EC = Field(default_factory=SteelMember_EC, title="Supported member", description="Supported Member")

    model_config = ConfigDict(
        title="Steel Connect Member",
        json_schema_extra={
            "description": "Supporting and supported sections play complementary roles in bolted connections and make important contributions to the load bearing and transfer of the structure. The correct design and analysis of these two sections is essential to ensure the stability and durability of the structure."
        }
    )

class SteelBoltConnectionForce(MBaseModel):
    """
    Steel Bolt Connection Force class for defining the percentage of the member strength used in the steel bolt connection.

    Args:
        percent (float): The percentage of member strength considered for the steel bolt connection.
    """
    percent: Percentage = Field(default=30.0, title="Strength Design Percentage", description="The strength design percentage for the steel bolt connection. By default, shear is assumed to be 30% of the member strength, as it generally does not cause issues. If a higher percentage is required, adjust the value accordingly.")

    model_config = ConfigDict(
        title="Steel Bolt Connection Force",
        json_schema_extra={
            "description": "Defines the percentage of member strength assumed for the steel bolt connection, typically 30% for shear. This value can be adjusted based on design requirements."
        }
    )

class SteelBolt(MBaseModel):
    """
    Steel Bolt
    """
    # Bolt name with enum of sizes
    name: str = Field(
        default_factory=str,
        title="Bolt Size",
        description="The size or type of the steel bolt, represented by its designation (e.g., M16). This defines the dimensions and thread specifications of the bolt.",
        enum=enum_to_list(enBoltName)
    )

    # Bolt material, describing the type of material the bolt is made from
    matl: BoltMaterial = Field(
        default_factory=BoltMaterial,
        title="Bolt Material",
        description="The material from which the steel bolt is manufactured (e.g., carbon steel, stainless steel). This affects the bolt's strength, durability, and corrosion resistance."
    )

    model_config = ConfigDict(
        title="Steel Bolt Specifications",
        json_schema_extra={
            "description": "This model defines the properties of a steel bolt, including its size and material. Steel bolts are essential components in fastening structures, and their properties affect the overall strength and stability of the connection."
        }
    )

class AnchorBolt(MBaseModel):
    """
    Anchor Bolt

    This class represents anchor bolts used to secure structures to concrete foundations. 
    Anchor bolts are designed to withstand applied forces and loads, providing stability and support to the structure. 
    Anchor bolts come in various sizes, materials, and configurations to meet different structural requirements.
    """
    type: str = Field(
        default=enAnchorType.CIP,
        title="Anchor Bolt Installation Type",
        description="Type of anchor bolt installation method. Options include Cast-in-Place (CIP) or Post-Installed types, defining how the anchor bolt is embedded into the foundation.",
        enum=enum_to_list(enAnchorType)
    )

    steelbolt: SteelBolt = Field(
        default_factory=SteelBolt,
        title="Steel Bolt",
        description="Steel bolt used in the anchor bolt assembly. It defines the material and mechanical properties of the bolt that ensures its strength and load-bearing capacity."
    )

    length: float = Field(
        default=25.0,
        title="Anchor Bolt Length",
        description="The length of the anchor bolt, typically specified as the total length including both the embedded length in the foundation and the exposed portion. Length is critical for proper installation and load transfer."
    )

    pos_x: Length = Field(
        default_factory=Length,
        title="Position X",
        description="The horizontal position of the anchor bolt along the X-axis. This defines the placement of the anchor bolt relative to the foundation's coordinate system."
    )

    pos_y: Length = Field(
        default_factory=Length,
        title="Position Y",
        description="The horizontal position of the anchor bolt along the Y-axis. This defines the placement of the anchor bolt relative to the foundation's coordinate system."
    )

    num_x: int = Field(
        default=2,
        title="Number of Anchor Bolts in X-direction",
        description="The number of anchor bolts arranged along the X-axis. This influences the distribution of forces and the overall stability of the connection."
    )

    num_y: int = Field(
        default=2,
        title="Number of Anchor Bolts in Y-direction",
        description="The number of anchor bolts arranged along the Y-axis. This also impacts the force distribution and the structural integrity of the foundation."
    )

    model_config = ConfigDict(
        title="Anchor Bolt Design",
        json_schema_extra={
            "description": "Anchor bolts are critical for securing structures to concrete foundations. They are designed to withstand large forces and loads applied to the structure, offering essential support. The design of anchor bolts varies based on the application, foundation material, and structural needs."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(steelbolt=SteelBolt(name=enBoltName.M16, matl=BoltMaterial.create_default(name=enBoltMaterialASTM.A193_B7, enum_list=enum_to_list(enBoltMaterialASTM))),
                       pos_x=Length(value=1.5, unit=enUnitLength.IN),
                       pos_y=Length(value=1.5, unit=enUnitLength.IN))
        else:
            return cls(steelbolt=SteelBolt(name=enBoltName.M16, matl=BoltMaterial.create_default(name=enBoltMaterialASTM.A193_B7, enum_list=enum_to_list(enBoltMaterialASTM))),
                       pos_x=Length(value=50, unit=enUnitLength.MM),
                       pos_y=Length(value=50, unit=enUnitLength.MM))

class SteelBolt_EC(MBaseModel):
    """
    Steel Bolt class representing a mechanical element used for connecting structural members.

    Args:
        name (str): The size of the bolt (e.g., M20, M10).
        matl (BoltMaterial_EC): The material of the bolt.
    """
    name: str = Field(default='M20', title="Bolt Size", description="The size of the bolt, typically denoted by the outer diameter (e.g., M20, M10)", enum=enum_to_list(enBoltName))
    matl: BoltMaterial_EC = Field(default=BoltMaterial_EC(), title="Bolt Material", description="The material used for the bolt, determining its strength and durability")

    model_config = ConfigDict(
        title="Steel Bolt",
        json_schema_extra={
            "description": """A bolt is a mechanical element that connects members of a structure and is used to transfer loads.
                \nDiameter: The outer diameter of a bolt, usually expressed in a metric system such as M6, M8, M10, etc.
                \nLength: The overall length of the bolt, determined by the thickness of the connecting members.
                \nClass: The strength rating, expressed as a class, for example 8.8, 10.9, etc., where higher numbers indicate greater strength.
            """
        }
    )

class ShearConnector(MBaseModel):
    """
    ShearConnector
    """
    bolt: SteelBolt = Field(default_factory=SteelBolt, description="stud bolt")
    num: int = Field(default=1, description="stud column")
    space: Length = Field(default_factory=lambda: Length(value=300.0, unit=enUnitLength.MM), description="stud spacing")
    length: Length = Field(default_factory=lambda: Length(value=100.0, unit=enUnitLength.MM), description="stud length")

    model_config = ConfigDict(
        title="Shear Connector",
        json_schema_extra={
            "description": "Shear Connector"
        }
    )

class ShearConnector_EC(MBaseModel):
    """
    Shear Connector class for defining the specifications of shear connectors used in structural connections.

    Args:
        bolt (SteelBolt_EC): Specifications for the stud bolt.
        num (int): Number of shear connectors.
        space (Length): Spacing between shear connectors.
        length (Length): Length of the shear connector (stud).
    """
    bolt: SteelBolt_EC = Field(default=SteelBolt_EC(name="M19"), title="Bolt Specifications", description="Stud bolt specifications, including size and material.")
    num: int = Field(default=1, title="Number of Shear Connectors", description="Number of shear connectors (stud bolts) used in the connection.")
    space: Length = Field(default=Length(value=300.0, unit=enUnitLength.MM), title="Shear Connector Spacing", description="Spacing between adjacent shear connectors (studs).")
    length: Length = Field(default=Length(value=100.0, unit=enUnitLength.MM), title="Shear Connector Length", description="Length of each shear connector (stud).")

    model_config = ConfigDict(
        title="Shear Connector",
        json_schema_extra={
            "description": "Shear connectors are critical in transferring forces between connected structural elements. They play a key role in ensuring the strength and stability of a structure, and are designed to meet specific requirements based on the materials, configuration, and design load. Proper selection and placement of shear connectors enhance the safety, strength, and durability of the structure."
        }
    )

class Welding(MBaseModel):
    """
    Welding
    """
    matl: SteelMaterial = Field(default_factory=SteelMaterial, description="Material")
    length: Length = Field(default_factory=Length, description="Leg of Length")

    model_config = ConfigDict(
        title="Welding",
        json_schema_extra={
            "description": "Welding"
        }
    )

class Welding_EC(Welding):
    """
    Welding class for reviewing welds on supporting members.

    Args:
        matl (SteelMaterial_EC): The material of the welding.
        length (Length): The length of the weld leg.
    """
    matl: SteelMaterial_EC = Field(default=SteelMaterial_EC(), title="Weld Material", description="The material used for the weld, determining its strength and compatibility with the connected materials")
    length: Length = Field(default=Length(value=6.0, unit=enUnitLength.MM), title="Weld Leg Length", description="The leg length of the weld, which affects its strength and capacity")

    model_config = ConfigDict(
        title="Welding",
        json_schema_extra={
            "description": "Information related to the welds used in connecting supporting members. This includes the material and length of the weld leg, both crucial for ensuring the strength and stability of the welded connections."
        }
    )

class SteelPlateMember(MBaseModel):
    """
    Steel Plate Member
    """
    matl: SteelMaterial = Field(default_factory=SteelMaterial, title="Plate material", description="Material")
    bolt_num: int = Field(default=4, title="Number of bolt", description="Number of Bolts")
    thk: Length = Field(default_factory=Length, title="Thickness", description="Thickness")

    model_config = ConfigDict(
        title="Steel Plate Member",
        json_schema_extra={
            "description": "Steel Plate Member"
        }
    )

class SteelPlateMember_EC(SteelPlateMember):
    """
    Steel Plate Member class representing a steel plate element with material properties, thickness, and bolt details.

    Args:
        matl (SteelMaterial_EC): Material properties for the steel plate.
        bolt_num (int): The number of bolts used in the plate connection.
        thk (Length): The thickness of the steel plate.
    """
    matl: SteelMaterial_EC = Field(default=SteelMaterial_EC(), title="Plate Material", description="The material properties of the steel plate, including strength and durability.")
    bolt_num: int = Field(default=4, title="Number of Bolts", description="The number of bolts used in the connection of the steel plate.")
    thk: Length = Field(default=Length(value=6.0, unit=enUnitLength.MM), title="Thickness", description="The thickness of the steel plate.")

    model_config = ConfigDict(
        title="Steel Plate Member",
        json_schema_extra={
            "description": "A steel plate member, typically used for load-bearing or connection purposes in structural design. It includes material properties, bolt count, and plate thickness for complete specification."
        }
    )

class ConnectType(MBaseModel):
    """
    Connect Type class representing different types of bolted connections.

    Args:
        type (str): The type of connection.
    """
    type: str = Field(default="Fin Plate - Beam to Beam", title="Connection Type", description="The type of bolted connection between structural elements", enum=enum_to_list(enConnectionType))

    model_config = ConfigDict(
        title="Connection Type",
        json_schema_extra={
            "description": """
                The four types of bolted connections mentioned are described below:
                \n
                1. Fin Plate - Beam to Beam (Fin_B_B) \n
                This is the use of a fin plate to connect two beams, where a fin plate is attached to the end of each beam to connect them together.
                \n\n
                2. Fin Plate - Beam to Column (Fin_B_C)\n
                A method of connecting beams to columns, where fin plates are attached to the sides of the columns and the ends of the beams to create a solid connection.
                \n\n
                3. End Plate - Beam to Beam (End_B_B)\n
                A method of connecting two beams using end plates at the ends. An end plate is attached to the end of each beam and connected via bolts.
                \n\n
                4. End Plate - Beam to Column (End_B_C)\n
                This method of connecting beams to columns uses end plates attached to the sides of the columns to connect with the ends of the beams. Bolts are secured to the column through the end plate.
            """
        }
    )

class BasePlate(MBaseModel):
    """
    Base Plate
    """
    matl: SteelMaterial = Field(default_factory=SteelMaterial, title="Base Plate Material Info", description="Input specification for baseplate material properties. This data includes detailed material composition and characteristics of the base component. The specification outlines essential material parameters for baseplate construction and assembly.")
    thk: Length = Field(default_factory=Length, title="Base Plate Thickness", description="Physical thickness dimension of the baseplate component. This parameter defines the vertical depth of the plate material and is crucial for structural integrity and load-bearing capacity.")
    width: Length = Field(default_factory=Length, title="Base Plate Width", description="Horizontal width measurement of the baseplate component. This dimension represents the lateral span of the plate and is essential for determining the overall footprint and load distribution capabilities")
    height: Length = Field(default_factory=Length, title="Base Plate Height", description="Vertical height measurement of the baseplate component. This dimension defines the upward extension of the plate and is critical for ensuring proper component fitment and structural support requirements.")
    fck: Stress = Field(default_factory=Stress, title="Concrete Strength", description="Characteristic compressive strength of concrete at 28 days. This parameter represents the structural concrete's design strength and is essential for determining the foundation's load-bearing capacity and structural performance.")

    model_config = ConfigDict(
        title="Base Plate Design Parameters",
        json_schema_extra={
            "description": "Comprehensive specifications for base plate design including material properties, geometric dimensions, and foundation strength parameters. This configuration defines essential structural components for steel column base plate connections."
        }
    )

    @classmethod
    def create_default(cls, unit_system: enUnitSystem):
        if unit_system == enUnitSystem.US:
            return cls(matl=SteelMaterial.create_default(code="ASTM", enum_list=enum_to_list(enSteelMaterial_ASTM)),
                       thk=Length(value=1, unit=enUnitLength.IN),
                       width=Length(value=18, unit=enUnitLength.IN),
                       height=Length(value=18, unit=enUnitLength.IN), fck=Stress(value=3000, unit=enUnitStress.psi))
        else:
            return cls(matl=SteelMaterial.create_default(code="ASTM", enum_list=enum_to_list(enSteelMaterial_ASTM)),
                       thk=Length(value=6, unit=enUnitLength.MM),
                       width=Length(value=390, unit=enUnitLength.MM),
                       height=Length(value=400, unit=enUnitLength.MM), fck=Stress(value=24, unit=enUnitStress.MPa))