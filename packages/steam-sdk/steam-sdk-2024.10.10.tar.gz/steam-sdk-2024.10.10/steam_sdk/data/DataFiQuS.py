from pydantic import BaseModel, Field, PositiveFloat, PositiveInt, NonNegativeFloat
from typing import Union, Dict, List, Literal, Optional, Annotated, Tuple
from annotated_types import Len

# from steam_sdk.data.DataConductor import ConstantJc, Bottura, CUDI3, Bordini, BSCCO_2212_LBNL, CUDI1, Summers, Round, \
#     Rectangular, Rutherford, Mono, Ribbon, Ic_A_NbTi
from steam_sdk.data.DataConductorFiQuS import Conductor as ConductorFiQuS
from steam_sdk.data.DataRoxieParser import RoxieData


from steam_sdk.data.DataModelCommon import Circuit_Class
from steam_sdk.data.DataModelCommon import PowerSupplyClass
from steam_sdk.data.DataFiQuSCWS import CWS
from steam_sdk.data.DataFiQuSConductorAC_Strand import CACStrand
from steam_sdk.data.DataFiQuSConductorAC_Rutherford import CACRutherford
from steam_sdk.data.DataFiQuSPancake3D import *


class CCTGeometryCWSInputs(BaseModel):
    """
        Level 3: Class for controlling if and where the conductor files and brep files are written for the CWS (conductor with step) workflow
    """
    write: bool = False             # if true only conductor and brep files are written, everything else is skipped.
    output_folder: Optional[str] = None       # this is relative path to the input file location


class CCTGeometryWinding(BaseModel):  # Geometry related windings _inputs
    """
        Level 2: Class for FiQuS CCT
    """
    names: Optional[List[str]] = None  # name to use in gmsh and getdp
    r_wms: Optional[List[float]] = None  # radius of the middle of the winding
    n_turnss: Optional[List[float]] = None  # number of turns
    ndpts: Optional[List[int]] = None  # number of divisions of turn, i.e. number of hexagonal elements for each turn
    ndpt_ins: Optional[List[int]] = None  # number of divisions of terminals ins
    ndpt_outs: Optional[List[int]] = None  # number of divisions of terminals outs
    lps: Optional[List[float]] = None  # layer pitch
    alphas: Optional[List[float]] = None  # tilt angle
    wwws: Optional[List[float]] = None  # winding wire widths (assuming rectangular)
    wwhs: Optional[List[float]] = None  # winding wire heights (assuming rectangular)


class CCTGeometryFQPCs(BaseModel):
    """
        Level 2: Class for FiQuS CCT
    """
    names: List[str] = []  # name to use in gmsh and getdp
    fndpls: Optional[List[int]] = None  # fqpl number of divisions per length
    fwws: Optional[List[float]] = None  # fqpl wire widths (assuming rectangular) for theta = 0 this is x dimension
    fwhs: Optional[List[float]] = None  # fqpl wire heights (assuming rectangular) for theta = 0 this is y dimension
    r_ins: Optional[List[float]] = None  # radiuses for inner diameter for fqpl (radial (or x direction for theta=0) for placing the fqpl
    r_bs: Optional[List[float]] = None  # radiuses for bending the fqpl by 180 degrees
    n_sbs: Optional[List[int]] = None  # number of 'bending segmetns' for the 180 degrees turn
    thetas: Optional[List[float]] = None  # rotation in deg from x+ axis towards y+ axis about z axis.
    z_starts: Optional[List[str]] = None  # which air boundary to start at. These is string with either: z_min or z_max key from the Air region.
    z_ends: Optional[List[float]] = None  # z coordinate of loop end


class CCTGeometryFormer(BaseModel):  # Geometry related formers _inputs
    """
        Level 2: Class for FiQuS CCT
    """
    names: Optional[List[str]] = None  # name to use in gmsh and getdp
    r_ins: Optional[List[float]] = None  # inner radius
    r_outs: Optional[List[float]] = None  # outer radius
    z_mins: Optional[List[float]] = None  # extend of former  in negative z direction
    z_maxs: Optional[List[float]] = None  # extend of former in positive z direction
    rotates: Optional[List[float]] = None  # rotation of the former around its axis in degrees


class CCTGeometryAir(BaseModel):  # Geometry related air_region _inputs
    """
        Level 2: Class for FiQuS CCT
    """
    name: Optional[str] = None  # name to use in gmsh and getdp
    sh_type: Optional[str] = None  # cylinder or cuboid are possible
    ar: Optional[float] = None  # if box type is cuboid a is taken as a dimension, if cylinder then r is taken
    z_min: Optional[float] = None  # extend of air region in negative z direction
    z_max: Optional[float] = None  # extend of air region in positive z direction


class CCTGeometry(BaseModel):
    """
        Level 2: Class for FiQuS CCT
    """
    CWS_inputs: CCTGeometryCWSInputs = CCTGeometryCWSInputs()
    windings: CCTGeometryWinding = CCTGeometryWinding()
    fqpcs: CCTGeometryFQPCs = CCTGeometryFQPCs()
    formers: CCTGeometryFormer = CCTGeometryFormer()
    air: CCTGeometryAir = CCTGeometryAir()


class CCTMesh(BaseModel):
    """
        Level 2: Class for FiQuS CCT
    """
    MaxAspectWindings: Optional[float] = None  # used in transfinite mesh_generators settings to define mesh_generators size along two longer lines of hex elements of windings
    ThresholdSizeMin: Optional[float] = None  # sets field control of Threshold SizeMin
    ThresholdSizeMax: Optional[float] = None  # sets field control of Threshold SizeMax
    ThresholdDistMin: Optional[float] = None  # sets field control of Threshold DistMin
    ThresholdDistMax: Optional[float] = None  # sets field control of Threshold DistMax


class CCTSolveWinding(BaseModel):  # Solution time used windings _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CCT
    """
    currents: Optional[List[float]] = None  # current in the wire
    sigmas: Optional[List[float]] = None  # electrical conductivity
    mu_rs: Optional[List[float]] = None  # relative permeability


class CCTSolveFormer(BaseModel):  # Solution time used formers _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CCT
    """
    sigmas: Optional[List[float]] = None  # electrical conductivity
    mu_rs: Optional[List[float]] = None  # relative permeability


class CCTSolveFQPCs(BaseModel):  # Solution time used windings _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CCT
    """
    currents: List[float] = []  # current in the wire
    sigmas: List[float] = []  # electrical conductivity
    mu_rs: List[float] = []  # relative permeability


class CCTSolveAir(BaseModel):  # Solution time used air _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CCT
    """
    sigma: Optional[float] = None  # electrical conductivity
    mu_r: Optional[float] = None  # relative permeability


class CCTSolve(BaseModel):
    """
        Level 2: Class for FiQuS CCT
    """
    windings: CCTSolveWinding = CCTSolveWinding()  # windings solution time _inputs
    formers: CCTSolveFormer = CCTSolveFormer()  # former solution time _inputs
    fqpcs: CCTSolveFQPCs = CCTSolveFQPCs()  # fqpls solution time _inputs
    air: CCTSolveAir = CCTSolveAir()  # air solution time _inputs
    pro_template: Optional[str] = None  # file name of .pro template file
    variables: Optional[List[str]] = None  # Name of variable to post-process by GetDP, like B for magnetic flux density
    volumes: Optional[List[str]] = None  # Name of volume to post-process by GetDP, line Winding_1
    file_exts: Optional[List[str]] = None  # Name of file extensions to post-process by GetDP, like .pos


class CCTPostproc(BaseModel):
    """
        Level 2: Class for  FiQuS CCT
    """
    windings_wwns: Optional[List[int]] = None  # wires in width direction numbers
    windings_whns: Optional[List[int]] = None  # wires in height direction numbers
    additional_outputs: Optional[List[str]] = None  # Name of software specific input files to prepare, like :LEDET3D
    winding_order: Optional[List[int]] = None
    fqpcs_export_trim_tol: Optional[List[float]] = None  # this multiplier times winding extend gives 'z' coordinate above(below) which hexes are exported for LEDET, length of this list must match number of fqpls
    variables: Optional[List[str]] = None  # Name of variable to post-process by python Gmsh API, like B for magnetic flux density
    volumes: Optional[List[str]] = None  # Name of volume to post-process by python Gmsh API, line Winding_1
    file_exts: Optional[List[str]] = None  # Name of file extensions o post-process by python Gmsh API, like .pos


class CCT(BaseModel):
    """
        Level 2: Class for FiQuS CCT
    """
    type: Literal['CCT_straight']
    geometry: CCTGeometry = CCTGeometry()
    mesh: CCTMesh = CCTMesh()
    solve: CCTSolve = CCTSolve()
    postproc: CCTPostproc = CCTPostproc()


# Multipole


class MultipoleSolveTimeParametersAdaptive(BaseModel):
    """
    Level 6: Class for FiQuS Multipole
    """
    initial_time_step: Optional[float] = Field(
        default=1E-10,
        description="It specifies the initial time step used at the beginning of the transient simulation.",
    )
    min_time_step: Optional[float] = Field(
        default=1E-12,
        description="It specifies the minimum possible value of the time step.",
    )
    max_time_step: Optional[float] = Field(
        default=10,
        description="It specifies the maximum possible value of the time step.",
    )
    breakpoints: Optional[List[float]] = Field(
        default=[],
        description="It forces the transient simulation to hit the time instants contained in this list.",
    )
    integration_method: Optional[str] = Field(
        default='Euler',
        description="It specifies the type of integration method to be used.",
    )
    rel_tol_time: Optional[float] = Field(
        default=1E-16,
        description="It specifies the relative tolerance.",
    )
    abs_tol_time: Optional[float] = Field(
        default=0.1,
        description="It specifies the absolute tolerance.",
    )
    norm_type: Optional[str] = Field(
        default='LinfNorm',
        description="It specifies the type of norm to be calculated for convergence assessment.",
    )


class MultipoleSolveTimeParametersFixed(BaseModel):
    """
    Level 6: Class for FiQuS Multipole
    """
    time_step: Optional[float] = Field(
        default=None,
        description="It specifies the value of the fixed time step used in the transient simulation.",
    )
    theta: Optional[Literal[1, 0.5]] = Field(
        default=1,
        description="It specifies the type of numerical method used: 1 for implicit Euler; 0.5 for Crank-Nicholson.",
    )


class MultipoleGeoElement(BaseModel):
    """
    Level 5: Class for FiQuS Multipole
    """
    lines: Optional[int] = Field(
        default=3,
        description="It specifies the number of Gaussian points for lines.",
    )
    triangles: Optional[Literal[1, 3, 4, 6, 7, 12, 13, 16]] = Field(
        default=3,
        description="It specifies the number of Gaussian points for triangles.",
    )
    quadrangles: Optional[Literal[1, 3, 4, 7]] = Field(
        default=4,
        description="It specifies the number of Gaussian points for quadrangles.",
    )


class MultipoleSolveConvectionBoundaryCondition(BaseModel):
    """
    Level 5: Class for FiQuS Multipole
    """
    boundaries: Optional[List[str]] = Field(
        default=[],
        description="It specifies the list of boundaries where the condition is applied."
                    "Each boundary is identified by a string of the form <half-turn/wedge reference number><side>,"
                    "where the accepted sides are i, o, l, h which correspond respectively to inner, outer, lower (angle), higher (angle): e.g., 1o",
    )
    const_heat_transfer_coefficient: Optional[float] = Field(
        default=None,
        description="It specifies the value of the heat transfer coefficient for this boundary condition.",
    )
    function_heat_transfer_coefficient: Optional[str] = Field(
        default=None,
        description="It specifies the name of the function the computes the heat transfer coefficient for this boundary condition.",
    )


class MultipoleSolveHeatFluxBoundaryCondition(BaseModel):
    """
    Level 5: Class for FiQuS Multipole
    """
    boundaries: Optional[List[str]] = Field(
        default=[],
        description="It specifies the list of boundaries where the condition is applied."
                    "Each boundary is identified by a string of the form <half-turn/wedge reference number><side>,"
                    "where the accepted sides are i, o, l, h which correspond respectively to inner, outer, lower (angle), higher (angle): e.g., 1o",
    )
    const_heat_flux: Optional[float] = Field(
        default=None,
        description="It specifies the value of the heat flux for this boundary condition.",
    )
    # function_heat_flux: Optional[str] = None


class MultipoleSolveTemperatureBoundaryCondition(BaseModel):
    """
    Level 5: Class for FiQuS Multipole
    """
    boundaries: Optional[List[str]] = Field(
        default=[],
        description="It specifies the list of boundaries where the condition is applied."
                    "Each boundary is identified by a string of the form <half-turn/wedge reference number><side>,"
                    "where the accepted sides are i, o, l, h which correspond respectively to inner, outer, lower (angle), higher (angle): e.g., 1o",
    )
    const_temperature: Optional[float] = Field(
        default=None,
        description="It specifies the value of the temperature for this boundary condition.",
    )
    # function_temperature: Optional[str] = None


class MultipoleSolveTimeParameters(BaseModel):
    """
    Level 5: Class for FiQuS Multipole
    """
    time_stepping: Optional[Literal["adaptive", "fixed"]] = Field(
        default="adaptive",
        description="It specifies the type of time stepping.",
    )
    initial_time: Optional[float] = Field(
        default=0.,
        description="It specifies the initial time of the simulation.",
    )
    final_time: Optional[float] = Field(
        default=None,
        description="It specifies the final time of the simulation.",
    )
    fixed: MultipoleSolveTimeParametersFixed = Field(
        default=MultipoleSolveTimeParametersFixed(),
        description="This dictionary contains the information about the time parameters of the fixed time stepping.",
    )
    adaptive: MultipoleSolveTimeParametersAdaptive = Field(
        default=MultipoleSolveTimeParametersAdaptive(),
        description="This dictionary contains the information about the time parameters of the adaptive time stepping.",
    )


class MultipoleSolveQuenchInitiation(BaseModel):
    """
    Level 5: Class for FiQuS Multipole
    """
    turns: Optional[List[int]] = Field(
        default=[],
        description="It specifies the list of reference numbers of half-turns that are set to quench.",
    )
    t_trigger: Optional[List[float]] = Field(
        default=[],
        description="It specifies the list of time instants at which the specified half-turns start quenching.",
    )


class MultipoleSolveBoundaryConditionsThermal(BaseModel):
    """
    Level 4: Class for FiQuS Multipole
    """
    temperature: Dict[str, MultipoleSolveTemperatureBoundaryCondition] = Field(
        default={},
        description="This dictionary contains the information about the Dirichlet boundary conditions."
                    "The keys are chosen by the user via the input yaml.",
    )
    heat_flux: Dict[str, MultipoleSolveHeatFluxBoundaryCondition] = Field(
        default={},
        description="This dictionary contains the information about the Neumann boundary conditions."
                    "The keys are chosen by the user via the input yaml.",
    )
    cooling: Dict[str, MultipoleSolveConvectionBoundaryCondition] = Field(
        default={},
        description="This dictionary contains the information about the Robin boundary conditions."
                    "The keys are chosen by the user via the input yaml.",
    )


class MultipoleSolveTransientElectromagnetics(BaseModel):
    """
    Level 4: Class for FiQuS Multipole
    """
    time_pars: MultipoleSolveTimeParameters = Field(
        default=MultipoleSolveTimeParameters(),
        description="This dictionary contains the information about the transient solver parameters.",
    )


class MultipoleSolveHeCooling(BaseModel):
    """
    Level 4: Class for FiQuS Multipole
    """
    sides: Optional[Literal["adiabatic", "external", "inner", "outer", "inner_outer"]] = Field(
        default="adiabatic",
        description="It specifies the general grouping of the boundaries where to apply cooling:"
                    "'adiabatic': no cooling; 'external': all external boundaries; 'inner': only inner boundaries; 'outer': only outer boundaries; 'inner_outer': inner and outer boundaries.",
    )
    const_heat_transfer_coefficient: Optional[float] = Field(
        default=None,
        description="It specifies the value of the constant heat transfer coefficient.",
    )
    function_heat_transfer_coefficient: Optional[str] = Field(
        default=None,
        description="It specifies the name of the function the computes the heat transfer coefficient.",
    )


class MultipoleSolveNonLinearSolver(BaseModel):
    """
    Level 4: Class for FiQuS Multipole
    """
    rel_tolerance: Optional[float] = Field(
        default=1E-16,
        description="It specifies the relative tolerance.",
    )
    abs_tolerance: Optional[float] = Field(
        default=0.1,
        description="It specifies the absolute tolerance.",
    )
    relaxation_factor: Optional[float] = Field(
        default=0.7,
        description="It specifies the relaxation factor.",
    )
    max_iterations: Optional[int] = Field(
        default=20,
        description="It specifies the maximum number of iterations if no convergence is reached.",
    )
    norm_type: Optional[str] = Field(
        default='LinfNorm',
        description="It specifies the type of norm to be calculated for convergence assessment.",
    )


class MultipoleSolveTransientThermal(BaseModel):
    """
    Level 4: Class for FiQuS Multipole
    """
    time_pars: MultipoleSolveTimeParameters = Field(
        default=MultipoleSolveTimeParameters(),
        description="This dictionary contains the information about the transient solver parameters.",
    )
    stop_temperature: Optional[float] = Field(
        default=300,
        description="If a computational region reaches this temperature, the simulation is stopped.",
    )
    quench_initiation: MultipoleSolveQuenchInitiation = Field(
        default=MultipoleSolveQuenchInitiation(),
        description="This dictionary contains the information about quenching regions.",
    )


class MultipoleSolveBasisOrder(BaseModel):
    """
    Level 4: Class for FiQuS Multipole
    """
    coil_and_wedges: Optional[int] = Field(
        default=1,
        description="It specifies the basis order for conductors and wedges.",
    )
    insulation: Optional[int] = Field(
        default=1,
        description="It specifies the basis order for the insulation regions.",
    )


class MultipoleSolveGaussianPoints(BaseModel):
    """
    Level 4: Class for FiQuS Multipole
    """
    conducting_elements: MultipoleGeoElement = Field(
        default=MultipoleGeoElement(),
        description="This dictionary contains the information about the Gaussian points for the conducting regions.",
    )
    insulation: MultipoleGeoElement = Field(
        default=MultipoleGeoElement(),
        description="This dictionary contains the information about the Gaussian points for the insulation regions.",
    )
    TSA: Optional[int] = Field(
        default=None,
        description="It specifies the Gaussian points for the thin-shells.",
    )  # needs to be reasonably large to properly integrate non-linearity (>= 2)


class MultipoleSolveInsulationBlockToBlock(BaseModel):
    """
    Level 4: Class for FiQuS Multipole
    """
    material: Optional[str] = Field(
        default=None,
        description="It specifies the default material of the insulation regions between the blocks insulation regions.",
    )
    # the order of blocks should be: [inner, outer] for mid-layer couples or [lower, higher] for mid-pole and mid-winding couples
    blocks_connection_overwrite: List[Tuple[str, str]] = Field(
        default=[],
        description="It specifies the blocks couples adjacent to the insulation region."
                    "The blocks must be ordered from inner to outer block for mid-layer insulation regions and from lower to higher angle block for mid-pole and mid-winding insulation regions.",
    )
    materials_overwrite: Optional[List[List[str]]] = Field(
        default=[],
        description="It specifies the list of materials making up the layered insulation region to be placed between the specified blocks."
                    "The materials must be ordered from inner to outer layers and lower to higher angle layers.",
    )
    thicknesses_overwrite: Optional[List[List[Optional[float]]]] = Field(
        default=[],
        description="It specifies the list of thicknesses of the specified insulation layers. The order must match the one of the materials list.",
    )


class MultipoleSolveInsulationExterior(BaseModel):
    """
    Level 4: Class for FiQuS Multipole
    """
    blocks: Optional[List[str]] = Field(
        default=[],
        description="It specifies the reference numbers of the blocks adjacent to the exterior insulation regions to modify.",
    )
    materials_append: Optional[List[List[str]]] = Field(
        default=[],
        description="It specifies the list of materials making up the layered insulation region to be appended to the block insulation."
                    "The materials must be ordered from the block outward.",
    )
    thicknesses_append: Optional[List[List[float]]] = Field(
        default=[],
        description="It specifies the list of thicknesses of the specified insulation layers. The order must match the one of the materials list.",
    )


class MultipoleSolveWedge(BaseModel):
    """
    Level 3: Class for FiQuS Multipole
    """
    material: Optional[str] = Field(
        default=None,
        description="It specifies the material of the wedge regions.",
    )
    RRR: Optional[float] = Field(
        default=None,
        description="It specifies the RRR of the wedge regions.",
    )
    T_ref_RRR_high: Optional[float] = Field(
        default=None,
        description="It specifies the reference temperature associated with the RRR.",
    )


class MultipoleSolveInsulationTSA(BaseModel):
    """
    Level 3: Class for FiQuS Multipole
    """
    block_to_block: MultipoleSolveInsulationBlockToBlock = Field(
        default=MultipoleSolveInsulationBlockToBlock(),
        description="This dictionary contains the information about the materials and thicknesses of the inner insulation regions (between blocks) modeled via thin-shell approximation.",
    )
    exterior: MultipoleSolveInsulationExterior = Field(
        default=MultipoleSolveInsulationExterior(),
        description="This dictionary contains the information about the materials and thicknesses of the outer insulation regions (exterior boundaries) modeled via thin-shell approximation.",
    )


class MultipoleSolveThermal(BaseModel):
    """
    Level 3: Class for FiQuS Multipole
    """
    solved: Optional[Literal["", "stationary", "transient"]] = Field(
        default="",
        description="It determines whether the thermal transient problem is solved ('transient') or not ('').",
    )
    insulation_TSA: MultipoleSolveInsulationTSA = Field(
        default=MultipoleSolveInsulationTSA(),
        description="This dictionary contains the information about the materials and thicknesses of the insulation regions modeled via thin-shell approximation.",
    )
    gaussian_points: MultipoleSolveGaussianPoints = Field(
        default=MultipoleSolveGaussianPoints(),
        description="This dictionary contains the information for Gaussian points used in the solver.",
    )
    basis_order: MultipoleSolveBasisOrder = Field(
        default=MultipoleSolveBasisOrder(),
        description="This dictionary contains the information about the basis order for the solver.",
    )
    He_cooling: MultipoleSolveHeCooling = Field(
        default=MultipoleSolveHeCooling(),
        description="This dictionary contains the information about the Robin boundary condition for generic groups of boundaries.",
    )
    boundary_conditions: MultipoleSolveBoundaryConditionsThermal = Field(
        default=MultipoleSolveBoundaryConditionsThermal(),
        description="This dictionary contains the information about boundary conditions for explicitly specified boundaries.",
    )
    non_linear_solver: MultipoleSolveNonLinearSolver = Field(
        default=MultipoleSolveNonLinearSolver(),
        description="This dictionary contains the information about the parameters for the non-linear solver.",
    )
    transient: MultipoleSolveTransientThermal = Field(
        default=MultipoleSolveTransientThermal(),
        description="This dictionary contains the information about the parameters for the transient solver.",
    )
    initial_temperature: Optional[float] = None
    enforce_initial_temperature_as_minimum: bool = False


class MultipoleSolveElectromagnetics(BaseModel):
    """
    Level 3: Class for FiQuS Multipole
    """
    solved: Optional[Literal["", "stationary"]] = Field(
        default="",
        description="It determines whether the magneto-static problem is solved ('stationary') or not ('').",
    )
    gaussian_points: MultipoleSolveGaussianPoints = Field(
        default=MultipoleSolveGaussianPoints(),
        description="This dictionary contains the information for Gaussian points used in the solver.",
    )
    non_linear_solver: MultipoleSolveNonLinearSolver = Field(
        default=MultipoleSolveNonLinearSolver(),
        description="This dictionary contains the information about the parameters for the non-linear solver.",
    )
    transient: MultipoleSolveTransientElectromagnetics = Field(
        default=MultipoleSolveTransientElectromagnetics(),
        description="This dictionary contains the information about the parameters for the transient solver.",
    )


class MultipoleMeshThinShellApproximationParameters(BaseModel):
    """
    Level 4: Class for FiQuS Multipole
    """
    global_size: Optional[float] = Field(
        default=None,
        description="The thickness of the insulation region is divided by this parameter to determine the number of spacial discretizations across the thin-shell.",
    )
    minimum_discretizations: Optional[int] = Field(
        default=1,
        description="It specifies the number of minimum spacial discretizations across a thin-shell.",
    )
    global_size_QH: Optional[float] = Field(
        default=None,
        description="The thickness of the quench heater region is divided by this parameter to determine the number of spacial discretizations across the thin-shell.",
    )
    minimum_discretizations_QH: Optional[int] = Field(
        default=1,
        description="It specifies the number of minimum spacial discretizations across a thin-shell.",
    )


class MultipoleMeshThreshold(BaseModel):
    """
    Level 3: Class for FiQuS Multipole
    """
    SizeMin: Optional[float] = Field(
        default=None,
        description="It sets gmsh Mesh.MeshSizeMin.",
    )
    SizeMax: Optional[float] = Field(
        default=None,
        description="It sets gmsh Mesh.MeshSizeMax.",
    )
    DistMin: Optional[float] = Field(
        default=None,
        description="It sets gmsh Mesh.MeshDistMin.",
    )
    DistMax: Optional[float] = Field(
        default=None,
        description="It sets gmsh Mesh.MeshDistMax.",
    )


class MultipoleMeshTargetSize(BaseModel):
    """
    Level 3: Class for FiQuS Multipole
    """
    height: Optional[float] = Field(
        default=None,
        description="The height of the region (short side) is divided by this parameter to determine the number of elements to apply via transfinite curves.",
    )
    width: Optional[float] = Field(
        default=None,
        description="The width of the region (long side) is divided by this parameter to determine the number of elements to apply via transfinite curves.",
    )


class MultipoleMeshTransfiniteSurfaces(BaseModel):
    """
    Level 3: Class for FiQuS Multipole
    """
    conductors: bool = Field(
        default=True,
        description="It determines whether transfinite surfaces are applied to the conductor regions or not. If true, gmsh Fields won't be used.",
    )
    wedges: bool = Field(
        default=True,
        description="It determines whether transfinite surfaces are applied to the wedge regions or not. If true, gmsh Fields won't be used.",
    )


class MultipolePostProcThermal(BaseModel):
    """
    Level 2: Class for FiQuS Multipole
    """
    output_time_steps_pos: Optional[Union[bool, int]] = Field(
        default=True,
        description="It determines whether the solution for the .pos file is saved for all time steps (True), none (False), or equidistant time steps (int).",
    )
    output_time_steps_txt: Optional[Union[bool, int]] = Field(
        default=True,
        description="It determines whether the solution for the .txt file is saved for all time steps (True), none (False), or equidistant time steps (int).",
    )
    save_pos_at_the_end: bool = Field(
        default=True,
        description="It determines whether the solution for the .pos file is saved at the end of the simulation or during run time.",
    )
    save_txt_at_the_end: bool = Field(
        default=False,
        description="It determines whether the solution for the .txt file is saved at the end of the simulation or during run time.",
    )
    take_average_conductor_temperature: Optional[bool] = Field(
        default=True,
        description="It determines whether the output files are based on the average conductor temperature or not (map2d).",
    )
    plot_all: Optional[Literal["true", "false", ""]] = Field(
        default="",
        description="It determines whether the figures are generated and shown ('true'), generated only (''), or not generated ('false'). Useful for tests.",
    )
    variables: Optional[List[Literal["T"]]] = Field(
        default=["T"],
        description="It specifies the physical quantity to be output.",
    )
    volumes: Optional[List[
        Literal["omega", "powered", "induced", "iron", "conducting", "insulator"]]] = Field(
        default=["powered"],
        description="It specifies the regions associated with the physical quantity to be output.",
    )


class MultipolePostProcElectromagnetics(BaseModel):
    """
    Level 2: Class for FiQuS Multipole
    """
    output_time_steps_pos: Optional[Union[bool, int]] = Field(
        default=True,
        description="It determines whether the solution for the .pos file is saved for all time steps (True), none (False), or equidistant time steps (int).",
    )
    output_time_steps_txt: Optional[Union[bool, int]] = Field(
        default=True,
        description="It determines whether the solution for the .txt file is saved for all time steps (True), none (False), or equidistant time steps (int).",
    )
    save_pos_at_the_end: bool = Field(
        default=True,
        description="It determines whether the solution for the .pos file is saved at the end of the simulation or during run time.",
    )
    save_txt_at_the_end: bool = Field(
        default=False,
        description="It determines whether the solution for the .txt file is saved at the end of the simulation or during run time.",
    )
    compare_to_ROXIE: Optional[str] = Field(
        default=None,
        description="It contains the absolute path to a reference ROXIE map2d file. If provided, comparative plots with respect to the reference are generated.",
    )
    plot_all: Optional[Literal["true", "false", ""]] = Field(
        default="",
        description="It determines whether the figures are generated and shown ('true'), generated only (''), or not generated ('false'). Useful for tests.",
    )
    variables: Optional[List[Literal["a", "az", "b", "h", "js"]]] = Field(
        default=["b"],
        description="It specifies the physical quantity to be output.",
    )
    volumes: Optional[List[
        Literal["omega", "powered", "induced", "air", "air_far_field", "iron", "conducting", "insulator"]]] = Field(
        default=["powered"],
        description="It specifies the regions associated with the physical quantity to be output.",
    )


class MultipolePostProc(BaseModel):
    """
    Level 2: Class for FiQuS Multipole
    """
    electromagnetics: MultipolePostProcElectromagnetics = Field(
        default=MultipolePostProcElectromagnetics(),
        description="This dictionary contains the post-processing information for the electromagnetic solution.",
    )
    thermal: MultipolePostProcThermal = Field(
        default=MultipolePostProcThermal(),
        description="This dictionary contains the post-processing information for the thermal solution.",
    )


class MultipoleSolve(BaseModel):
    """
    Level 2: Class for FiQuS Multipole
    """
    wedges: MultipoleSolveWedge = Field(
        default=MultipoleSolveWedge(),
        description="This dictionary contains the material information of wedges.",
    )
    electromagnetics: MultipoleSolveElectromagnetics = Field(
        default=MultipoleSolveElectromagnetics(),
        description="This dictionary contains the solver information for the electromagnetic solution.",
    )
    thermal: MultipoleSolveThermal = Field(
        default=MultipoleSolveThermal(),
        description="This dictionary contains the solver information for the thermal solution.",
    )
    #pro_template: Optional[str] = None  # file name of .pro template file


class MultipoleMeshThermal(BaseModel):
    """
    Level 2: Class for FiQuS Multipole
    """
    transfinite_surfaces: MultipoleMeshTransfiniteSurfaces = Field(
        default=MultipoleMeshTransfiniteSurfaces(),
        description="This dictionary contains the mesh information for transfinite surfaces.",
    )
    conductor_target_sizes: MultipoleMeshTargetSize = Field(
        default=MultipoleMeshTargetSize(),
        description="This dictionary contains the mesh information about transfinite curves for the conductor regions.",
    )
    wedge_target_sizes: MultipoleMeshTargetSize = Field(
        default=MultipoleMeshTargetSize(),
        description="This dictionary contains the mesh information about transfinite curves for the wedge regions.",
    )
    coil_and_wedges: MultipoleMeshThreshold = Field(
        default=MultipoleMeshThreshold(),
        description="This dictionary contains the gmsh Field information for conductors and wedges.",
    )
    iron: MultipoleMeshThreshold = Field(
        default=MultipoleMeshThreshold(),
        description="This dictionary contains the gmsh Field information for the iron yoke region.",
    )
    insulation_constant_mesh_size: Optional[float] = Field(
        default=1e-4,
        description="This float value is the constant mesh size used for thermal reference simulations instead of the target size enforced by transfinite curves.",
    )
    TSA: MultipoleMeshThinShellApproximationParameters = Field(
        default=MultipoleMeshThinShellApproximationParameters(),
        description="This dictionary contains the mesh information for thin-shells.",
    )
    isothermal_conductors: bool = Field(
        default=False,
        description="It determines whether the conductors are considered isothermal or not using getDP Links.",
    )
    isothermal_wedges: bool = Field(
        default=False,
        description="It determines whether the wedges are considered isothermal or not using getDP Links.",
    )
    Algorithm: Optional[int] = Field(
        default=6,
        description="It sets gmsh Mesh.Algorithm.",
    )
    ElementOrder: Optional[int] = Field(
        default=1,
        description="It sets gmsh Mesh.ElementOrder.",
    )
    Optimize: Optional[int] = Field(
        default=1,
        description="It sets gmsh Mesh.Optimize.",
    )



class MultipoleMeshElectromagnetics(BaseModel):
    """
    Level 2: Class for FiQuS Multipole
    """
    transfinite_surfaces: MultipoleMeshTransfiniteSurfaces = Field(
        default=MultipoleMeshTransfiniteSurfaces(),
        description="This dictionary contains the mesh information for transfinite surfaces.",
    )
    conductor_target_sizes: MultipoleMeshTargetSize = Field(
        default=MultipoleMeshTargetSize(),
        description="This dictionary contains the mesh information for the conductor regions.",
    )
    wedge_target_sizes: MultipoleMeshTargetSize = Field(
        default=MultipoleMeshTargetSize(),
        description="This dictionary contains the mesh information for the wedge regions.",
    )
    coil_and_wedges: MultipoleMeshThreshold = Field(
        default=MultipoleMeshThreshold(),
        description="This dictionary contains the gmsh Field information for conductors and wedges.",
    )
    iron: MultipoleMeshThreshold = Field(
        default=MultipoleMeshThreshold(),
        description="This dictionary contains the gmsh Field information for the iron yoke region.",
    )
    bore: MultipoleMeshThreshold = Field(
        default=MultipoleMeshThreshold(),
        description="This dictionary contains the gmsh Field information for the bore region.",
    )
    Algorithm: Optional[int] = Field(
        default=6,
        description="It sets gmsh Mesh.Algorithm.",
    )
    ElementOrder: Optional[int] = Field(
        default=1,
        description="It sets gmsh Mesh.ElementOrder.",
    )
    Optimize: Optional[int] = Field(
        default=1,
        description="It sets gmsh Mesh.Optimize.",
    )


class MultipoleMesh(BaseModel):
    """
    Level 2: Class for FiQuS Multipole
    """
    electromagnetics: MultipoleMeshElectromagnetics = Field(
        default=MultipoleMeshElectromagnetics(),
        description="This dictionary contains the mesh information for the electromagnetic solution.",
    )
    thermal: MultipoleMeshThermal = Field(
        default=MultipoleMeshThermal(),
        description="This dictionary contains the mesh information for the thermal solution.",
    )


class MultipoleGeometryThermal(BaseModel):
    """
    Level 2: Class for FiQuS Multipole
    """
    with_iron_yoke: Optional[bool] = Field(
        default=None,
        description="It determines whether the iron yoke region is built or not.",
    )
    with_wedges: Optional[bool] = Field(
        default=None,
        description="It determines whether the wedge regions are built or not.",
    )
    use_TSA: Optional[bool] = Field(
        default=False,
        description="It determines whether the insulation regions are explicitly built or modeled via thin-shell approximation.",
    )


class MultipoleGeometryElectromagnetics(BaseModel):
    """
    Level 2: Class for FiQuS Multipole
    """
    with_iron_yoke: Optional[bool] = Field(
        default=None,
        description="It determines whether the iron yoke region is built or not.",
    )
    with_wedges: Optional[bool] = Field(
        default=None,
        description="It determines whether the wedge regions are built or not.",
    )
    symmetry: Optional[Literal["none", "xy", "x", "y"]] = Field(
        default='none',
        description="It determines the model regions to build according to the specified axis/axes.",
    )


class MultipoleGeometry(BaseModel):
    """
    Level 2: Class for FiQuS Multipole
    """
    geom_file_path: Optional[str] = Field(
        default=None,
        description="It contains the path to a .geom file. If null, the default .geom file produced by steam-sdk BuilderFiQuS will be used.",
    )
    plot_preview: Optional[bool] = Field(
        default=False,
        description="If true, it displays matplotlib figures of the magnet geometry with relevant information (e.g., conductor and block numbers).",
    )
    electromagnetics: MultipoleGeometryElectromagnetics = Field(
        default=MultipoleGeometryElectromagnetics(),
        description="This dictionary contains the geometry information for the electromagnetic solution.",
    )
    thermal: MultipoleGeometryThermal = Field(
        default=MultipoleGeometryThermal(),
        description="This dictionary contains the geometry information for the thermal solution.",
    )


class Multipole(BaseModel):
    """
    Level 1: Class for FiQuS Multipole
    """
    type: Literal["multipole"] = "multipole"
    geometry: MultipoleGeometry = Field(
        default=MultipoleGeometry(),
        description="This dictionary contains the geometry information.",
    )
    mesh: MultipoleMesh = Field(
        default=MultipoleMesh(),
        description="This dictionary contains the mesh information.",
    )
    solve: MultipoleSolve = Field(
        default=MultipoleSolve(),
        description="This dictionary contains the solution information.",
    )
    postproc: MultipolePostProc = Field(
        default=MultipolePostProc(),
        description="This dictionary contains the post-process information.",
    )



# Pancake3D
# NormalMaterialName = Literal[
#     "Copper", "Hastelloy", "Silver", "Indium", "Stainless Steel"
# ]
# SuperconductingMaterialName = Literal["HTSSuperPower"]
#
# PositionRequiredQuantityName = Literal[
#     "magneticField",
#     "axialComponentOfTheMagneticField",
#     "magnitudeOfMagneticField",
#     "currentDensity",
#     "magnitudeOfCurrentDensity",
#     "resistiveHeating",
#     "temperature",
#     "criticalCurrentDensity",
#     "heatFlux",
#     "resistivity",
#     "thermalConductivity",
#     "specificHeatCapacity",
#     "jHTSOverjCritical",
#     "criticalCurrent",
#     "debug",
# ]
# PositionNotRequiredQuantityName = Literal[
#     "currentThroughCoil",
#     "voltageBetweenTerminals",
#     "inductance",
#     "timeConstant",
#     "totalResistiveHeating",
#     "magneticEnergy",
# ]
#
#
# class Pancake3DPositionInCoordinates(BaseModel):
#     x: float = Field(
#         title="x coordinate",
#         description="x coordinate of the position.",
#     )
#     y: float = Field(
#         title="y coordinate",
#         description="y coordinate of the position.",
#     )
#     z: float = Field(
#         title="z coordinate",
#         description="z coordinate of the position.",
#     )
#
#
# class Pancake3DPositionInTurnNumbers(BaseModel):
#     turnNumber: Optional[float] = Field(
#         default=None,
#         title="Turn Number",
#         description=(
#             "Winding turn number as a position input. It starts from 0 and it can be a"
#             " float."
#         ),
#     )
#     whichPancakeCoil: Optional[PositiveInt] = Field(
#         default=None,
#         title="Pancake Coil Number",
#         description="The first pancake coil is 1, the second is 2, etc.",
#     )
#
#
# Pancake3DPosition = Pancake3DPositionInCoordinates | Pancake3DPositionInTurnNumbers
#
#
# class Pancake3DGeometryWinding(BaseModel):
#     # Mandatory:
#     r_i: Optional[PositiveFloat] = Field(
#         default=None,
#         alias="innerRadius",
#         title="Inner Radius",
#         description="Inner radius of the winding.",
#     )
#     t: Optional[PositiveFloat] = Field(
#         default=None,
#         alias="thickness",
#         title="Winding Thickness",
#         description="Thickness of the winding.",
#     )
#     N: Optional[float] = Field(
#         default=None,
#         alias="numberOfTurns",
#         ge=3,
#         title="Number of Turns",
#         description="Number of turns of the winding.",
#     )
#     h: Optional[PositiveFloat] = Field(
#         default=None,
#         alias="height",
#         title="Winding Height",
#         description="Height/width of the winding.",
#     )
#
#     # Optionals:
#     name: Optional[str] = Field(
#         default="winding",
#         title="Winding Name",
#         description="The The name to be used in the mesh..",
#         examples=["winding", "myWinding"],
#     )
#     NofVolPerTurn: Optional[int] = Field(
#         default=2,
#         validate_default=True,
#         alias="numberOfVolumesPerTurn",
#         ge=2,
#         title="Number of Volumes Per Turn (Advanced Input)",
#         description="The number of volumes per turn (CAD related, not physical).",
#     )
#
#
# class Pancake3DGeometryContactLayer(BaseModel):
#     # Mandatory:
#     tsa: Optional[bool] = Field(
#         default=None,
#         alias="thinShellApproximation",
#         title="Use Thin Shell Approximation",
#         description=(
#             "If True, the contact layer will be modeled with 2D shell elements (thin"
#             " shell approximation), and if False, the contact layer will be modeled"
#             " with 3D elements."
#         ),
#     )
#     t: Optional[PositiveFloat] = Field(
#         default=None,
#         alias="thickness",
#         title="Contact Layer Thickness",
#         description="Thickness of the contact layer.",
#     )
#
#     # Optionals:
#     name: Optional[str] = Field(
#         default="contactLayer",
#         title="Contact Layer Name",
#         description="The name to be used in the mesh.",
#         examples=["myContactLayer"],
#     )
#
#
# class Pancake3DGeometryTerminalBase(BaseModel):
#     # Mandatory:
#     t: Optional[PositiveFloat] = Field(
#         default=None,
#         alias="thickness",
#         title="Terminal Thickness",
#         description="Thickness of the terminal's tube.",
#     )  # thickness
#
#
# class Pancake3DGeometryInnerTerminal(Pancake3DGeometryTerminalBase):
#     name: Optional[str] = Field(
#         default="innerTerminal",
#         title="Terminal Name",
#         description="The name to be used in the mesh.",
#         examples=["innerTerminal", "outerTeminal"],
#     )
#
#
# class Pancake3DGeometryOuterTerminal(Pancake3DGeometryTerminalBase):
#     name: Optional[str] = Field(
#         default="outerTerminal",
#         title="Terminal Name",
#         description="The name to be used in the mesh.",
#         examples=["innerTerminal", "outerTeminal"],
#     )
#
#
# class Pancake3DGeometryTerminals(BaseModel):
#     # 1) User inputs:
#     i: Optional[Pancake3DGeometryInnerTerminal] = Field(
#         default=Pancake3DGeometryInnerTerminal(),
#         alias="inner"
#     )
#     o: Optional[Pancake3DGeometryOuterTerminal] = Field(
#         default=Pancake3DGeometryOuterTerminal(),
#         alias="outer"
#     )
#
#     # Optionals:
#     firstName: Optional[str] = Field(
#         default="firstTerminal", description="name of the first terminal"
#     )
#     lastName: Optional[str] = Field(
#         default="lastTerminal", description="name of the last terminal"
#     )
#
#
# class Pancake3DGeometryAirBase(BaseModel):
#     # Mandatory:
#     margin: Optional[PositiveFloat] = Field(
#         default=None,
#         alias="axialMargin",
#         title="Axial Margin of the Air",
#         description=(
#             "Axial margin between the ends of the air and first/last pancake coils."
#         ),
#     )  # axial margin
#
#     # Optionals:
#     name: Optional[str] = Field(
#         default="air",
#         title="Air Name",
#         description="The name to be used in the mesh.",
#         examples=["air", "myAir"],
#     )
#     shellTransformation: Optional[bool] = Field(
#         default=False,
#         alias="shellTransformation",
#         title="Use Shell Transformation",
#         description=(
#             "Generate outer shell air to apply shell transformation if True (GetDP"
#             " related, not physical)"
#         ),
#     )
#     shellTransformationMultiplier: Optional[float] = Field(
#         default=1.2,
#         gt=1.1,
#         alias="shellTransformationMultiplier",
#         title="Shell Transformation Multiplier (Advanced Input)",
#         description=(
#             "multiply the air's outer dimension by this value to get the shell's outer"
#             " dimension"
#         ),
#     )
#     cutName: Optional[str] = Field(
#         default="Air-Cut",
#         title="Air Cut Name",
#         description="name of the cut (cochain) to be used in the mesh",
#         examples=["Air-Cut", "myAirCut"],
#     )
#     shellVolumeName: Optional[str] = Field(
#         default="air-Shell",
#         title="Air Shell Volume Name",
#         description="name of the shell volume to be used in the mesh",
#         examples=["air-Shell", "myAirShell"],
#     )
#     fragment: Optional[bool] = Field(
#         default=False,
#         alias="generateGapAirWithFragment",
#         title="Generate Gap Air with Fragment (Advanced Input)",
#         description=(
#             "generate the gap air with gmsh/model/occ/fragment if true (CAD related,"
#             " not physical)"
#         ),
#     )
#
#
# class Pancake3DGeometryAirCylinder(Pancake3DGeometryAirBase):
#     type: Optional[Literal["cylinder"]] = Field(default="cylinder", title="Air Type")
#     r: Optional[PositiveFloat] = Field(
#         default=None,
#         alias="radius",
#         title="Air Radius",
#         description="Radius of the air (for cylinder type air).",
#     )
#
#
# class Pancake3DGeometryAirCuboid(Pancake3DGeometryAirBase):
#     type: Optional[Literal["cuboid"]] = Field(default="cuboid", title="Air Type")
#     a: Optional[PositiveFloat] = Field(
#         default=None,
#         alias="sideLength",
#         title="Air Side Length",
#         description="Side length of the air (for cuboid type air).",
#     )
#
#
# Pancake3DGeometryAir = Pancake3DGeometryAirCylinder | Pancake3DGeometryAirCuboid
#
#
# class Pancake3DMeshWinding(BaseModel):
#     # Mandatory:
#     axne: Optional[list[PositiveInt] | PositiveInt] = Field(
#         default=None,
#         alias="axialNumberOfElements",
#         title="Axial Number of Elements",
#         description=(
#             "The number of axial elements for the whole height of the coil. It can be"
#             " either a list of integers to specify the value for each pancake coil"
#             " separately or an integer to use the same setting for each pancake coil."
#         ),
#     )
#
#     ane: Optional[list[PositiveInt] | PositiveInt] = Field(
#         default=None,
#         alias="azimuthalNumberOfElementsPerTurn",
#         title="Azimuthal Number of Elements Per Turn",
#         description=(
#             "The number of azimuthal elements per turn of the coil. It can be either a"
#             " list of integers to specify the value for each pancake coil separately or"
#             " an integer to use the same setting for each pancake coil."
#         ),
#     )
#
#     rne: Optional[list[PositiveInt] | PositiveInt] = Field(
#         default=None,
#         alias="radialNumberOfElementsPerTurn",
#         title="Winding Radial Number of Elements Per Turn",
#         description=(
#             "The number of radial elements per tape of the winding. It can be either a"
#             " list of integers to specify the value for each pancake coil separately or"
#             " an integer to use the same setting for each pancake coil."
#         ),
#     )
#
#     # Optionals:
#     axbc: Optional[list[PositiveFloat] | PositiveFloat] = Field(
#         default=[1],
#         alias="axialDistributionCoefficient",
#         title="Axial Bump Coefficients",
#         description=(
#             "If 1, it won't affect anything. If smaller than 1, elements will get finer"
#             " in the axial direction at the ends of the coil. If greater than 1,"
#             " elements will get coarser in the axial direction at the ends of the coil."
#             " It can be either a list of floats to specify the value for each pancake"
#             " coil separately or a float to use the same setting for each pancake coil."
#         ),
#     )
#
#     elementType: Optional[(
#         list[Literal["tetrahedron", "hexahedron", "prism"]]
#         | Literal["tetrahedron", "hexahedron", "prism"]
#     )] = Field(
#         default=["tetrahedron"],
#         title="Element Type",
#         description=(
#             "The element type of windings and contact layers. It can be either a"
#             " tetrahedron, hexahedron, or a prism. It can be either a list of strings"
#             " to specify the value for each pancake coil separately or a string to use"
#             " the same setting for each pancake coil."
#         ),
#     )
#

# class Pancake3DMeshContactLayer(BaseModel):
#     # Mandatory:
#     rne: Optional[list[PositiveInt]] = Field(
#         default=None,
#         alias="radialNumberOfElementsPerTurn",
#         title="Contact Layer Radial Number of Elements Per Turn",
#         description=(
#             "The number of radial elements per tape of the contact layer. It can be"
#             " either a list of integers to specify the value for each pancake coil"
#             " separately or an integer to use the same setting for each pancake coil."
#         ),
#     )
#
#
# class Pancake3DMeshAirAndTerminals(BaseModel):
#     # Optionals:
#     structured: Optional[bool] = Field(
#         default=False,
#         title="Structure Mesh",
#         description=(
#             "If True, the mesh will be structured. If False, the mesh will be"
#             " unstructured."
#         ),
#     )
#     radialElementSize: Optional[PositiveFloat] = Field(
#         default=1,
#         title="Radial Element Size",
#         description=(
#             "If structured mesh is used, the radial element size can be set. It is the"
#             " radial element size in terms of the winding's radial element size."
#         ),
#     )
#
#
# class Pancake3DSolveAir(BaseModel):
#     # 1) User inputs:
#
#     # Mandatory:
#     permeability: Optional[PositiveFloat] = Field(
#         default=None,
#         title="Permeability of Air",
#         description="Permeability of air.",
#     )
#
#
# class Pancake3DSolveIcVsLength(BaseModel):
#     lengthValues: Optional[list[float]] = Field(
#         default=None,
#         title="Tape Length Values",
#         description="Tape length values that corresponds to criticalCurrentValues.",
#     )
#     criticalCurrentValues: Optional[list[float]] = Field(
#         default=None,
#         title="Critical Current Values",
#         description="Critical current values that corresponds to lengthValues.",
#     )
#
#
# class Pancake3DSolveMaterialBase(BaseModel):
#     name: Optional[str] = None
#
#     # Optionals:
#     rrr: Optional[PositiveFloat] = Field(
#         default=100,
#         alias="residualResistanceRatio",
#         title="Residual Resistance Ratio",
#         description=(
#             "Residual-resistivity ratio (also known as Residual-resistance ratio or"
#             " just RRR) is the ratio of the resistivity of a material at reference"
#             " temperature and at 0 K."
#         ),
#     )
#     rrrRefT: Optional[PositiveFloat] = Field(
#         default=295,
#         alias="residualResistanceRatioReferenceTemperature",
#         title="Residual Resistance Ratio Reference Temperature",
#         description="Reference temperature for residual resistance ratio",
#     )
#
#
# class Pancake3DSolveNormalMaterial(Pancake3DSolveMaterialBase):
#     # Mandatory:
#     name: Optional[NormalMaterialName] = Field(
#         default=None,
#         title="Material Name",
#     )
#
#
# class Pancake3DSolveSuperconductingMaterial(Pancake3DSolveMaterialBase):
#     # Mandatory:
#     name: Optional[SuperconductingMaterialName] = Field(
#         default=None,
#         title="Superconduncting Material Name",
#     )
#     nValue: Optional[PositiveFloat] = Field(
#         default=30,
#         alias="N-Value for E-J Power Law",
#         description="N-value for E-J power law.",
#     )
#     IcAtTinit: Optional[PositiveFloat | str | Pancake3DSolveIcVsLength] = Field(
#         default=None,
#         alias="criticalCurrentAtInitialTemperature",
#         title="Critical Current at Initial Temperature",
#         description=(
#             "Critical current at initial temperature. The critical current value will"
#             " change with temperature depending on the superconductor material.\nEither"
#             " the same critical current for the whole tape or the critical current with"
#             " respect to the tape length can be specified. To specify the same critical"
#             " current for the entire tape, just use a scalar. To specify critical"
#             " current with respect to the tape length: a CSV file can be used, or"
#             " lengthValues and criticalCurrentValues can be given as lists. The data"
#             " will be linearly interpolated.\nIf a CSV file is to be used, the input"
#             " should be the name of a CSV file (which is in the same folder as the"
#             " input file) instead of a scalar. The first column of the CSV file will be"
#             " the tape length, and the second column will be the critical current."
#         ),
#         examples=[230, "IcVSlength.csv"],
#     )
#
#     # Optionals:
#     electricFieldCriterion: Optional[PositiveFloat] = Field(
#         default=1e-4,
#         title="Electric Field Criterion",
#         description=(
#             "The electric field that defines the critical current density, i.e., the"
#             " electric field at which the current density reaches the critical current"
#             " density."
#         ),
#     )
#     jCriticalScalingNormalToWinding: Optional[PositiveFloat] = Field(
#         default=1,
#         title="Critical Current Scaling Normal to Winding",
#         description=(
#             "Critical current scaling normal to winding, i.e., along the c_axis. "
#             " We have Jc_cAxis = scalingFactor * Jc_abPlane."
#             " A factor of 1 means no scaling such that the HTS layer is isotropic."
#         ),
#     )
#     minimumPossibleResistivity: Optional[NonNegativeFloat] = Field(
#         default=0,
#         title="Minimum Possible Resistivity",
#         description=(
#             "The resistivity of the winding won't be lower than this value, no matter"
#             " what."
#         ),
#     )
#     maximumPossibleResistivity: Optional[PositiveFloat] = Field(
#         default=1,
#         title="Maximum Possible Resistivity",
#         description=(
#             "The resistivity of the winding won't be higher than this value, no matter"
#             " what."
#         ),
#     )
#
#
# class Pancake3DSolveHTSMaterialBase(BaseModel):
#     relativeThickness: Optional[float] = Field(
#         default=None,
#         le=1,
#         title="Relative Thickness (only for winding)",
#         description=(
#             "Winding tapes generally consist of more than one material. Therefore, when"
#             " materials are given as a list in winding, their relative thickness,"
#             " (thickness of the material) / (thickness of the winding), should be"
#             " specified."
#         ),
#     )
#
#
# class Pancake3DSolveHTSNormalMaterial(
#     Pancake3DSolveHTSMaterialBase, Pancake3DSolveNormalMaterial
# ):
#     pass
#
#
# class Pancake3DSolveHTSSuperconductingMaterial(
#     Pancake3DSolveHTSMaterialBase, Pancake3DSolveSuperconductingMaterial
# ):
#     pass
#
#
# class Pancake3DSolveHTSShuntLayerMaterial(Pancake3DSolveNormalMaterial):
#     name: Optional[NormalMaterialName] = Field(
#         default="Copper",
#         title="Material Name",
#     )
#     relativeHeight: Optional[float] = Field(
#         default=0.0,
#         ge=0,
#         le=1,
#         title="Relative Height of the Shunt Layer",
#         description=(
#             "HTS 2G coated conductor are typically plated, usually "
#             " using copper. The relative height of the shunt layer is the "
#             " width of the shunt layer divided by the width of the tape. "
#             " 0 means no shunt layer."
#         ),
#     )
#
#
# class Pancake3DSolveMaterial(BaseModel):
#     # 1) User inputs:
#
#     # Mandatory:
#
#     # Optionals:
#     resistivity: Optional[PositiveFloat] = Field(
#         default=None,
#         title="Resistivity",
#         description=(
#             "A scalar value. If this is given, material properties won't be used for"
#             " resistivity."
#         ),
#     )
#     thermalConductivity: Optional[PositiveFloat] = Field(
#         default=None,
#         title="Thermal Conductivity",
#         description=(
#             "A scalar value. If this is given, material properties won't be used for"
#             " thermal conductivity."
#         ),
#     )
#     specificHeatCapacity: Optional[PositiveFloat] = Field(
#         default=None,
#         title="Specific Heat Capacity",
#         description=(
#             "A scalar value. If this is given, material properties won't be used for"
#             " specific heat capacity."
#         ),
#     )
#     material: Optional[Pancake3DSolveNormalMaterial] = Field(
#         default=None,
#         title="Material",
#         description="Material from STEAM material library.",
#     )
#
#
# class Pancake3DSolveShuntLayerMaterial(Pancake3DSolveMaterial):
#     material: Optional[Pancake3DSolveHTSShuntLayerMaterial] = Field(
#         default=Pancake3DSolveHTSShuntLayerMaterial(),
#         title="Material",
#         description="Material from STEAM material library.",
#     )
#
#
# class Pancake3DSolveContactLayerMaterial(Pancake3DSolveMaterial):
#     resistivity: Optional[PositiveFloat | Literal["perfectlyInsulating"]] = Field(
#         default=None,
#         title="Resistivity",
#         description=(
#             'A scalar value or "perfectlyInsulating". If "perfectlyInsulating" is'
#             " given, the contact layer will be perfectly insulating. If this value is"
#             " given, material properties won't be used for resistivity."
#         ),
#     )
#     numberOfThinShellElements: Optional[PositiveInt] = Field(
#         default=1,
#         title="Number of Thin Shell Elements (Advanced Input)",
#         description=(
#             "Number of thin shell elements in the FE formulation (GetDP related, not"
#             " physical and only used when TSA is set to True)"
#         ),
#     )
#
#
# Pancake3DHTSMaterial = Pancake3DSolveHTSNormalMaterial | Pancake3DSolveHTSSuperconductingMaterial
#
#
# class Pancake3DSolveWindingMaterial(Pancake3DSolveMaterial):
#     material: Optional[list[Pancake3DHTSMaterial]] = Field(
#         default=None,
#         title="Materials of HTS CC",
#         description="List of materials of HTS CC.",
#     )
#
#     shuntLayer: Optional[Pancake3DSolveShuntLayerMaterial] = Field(
#         default=Pancake3DSolveShuntLayerMaterial(),
#         title="Shunt Layer Properties",
#         description="Material properties of the shunt layer.",
#     )
#
#
# class Pancake3DSolveTerminalMaterialAndBoundaryCondition(Pancake3DSolveMaterial):
#     cooling: Optional[Literal["adiabatic", "fixedTemperature", "cryocooler"]] = Field(
#         default="fixedTemperature",
#         title="Cooling condition",
#         description=(
#             "Cooling condition of the terminal. It can be either adiabatic, fixed"
#             " temperature, or cryocooler."
#         ),
#     )
#     transitionNotch: Optional[Pancake3DSolveMaterial] = Field(
#         default=None,
#         title="Transition Notch Properties",
#         description="Material properties of the transition notch volume.",
#     )
#     terminalContactLayer: Optional[Pancake3DSolveMaterial] = Field(
#         default=None,
#         title="Transition Layer Properties",
#         description=(
#             "Material properties of the transition layer between terminals and"
#             " windings."
#         ),
#     )
#
#
# class Pancake3DSolveToleranceBase(BaseModel):
#     # Mandatory:
#     quantity: Optional[str] = None
#     relative: Optional[NonNegativeFloat] = Field(
#         default=None,
#         title="Relative Tolerance",
#         description="Relative tolerance for the quantity.",
#     )
#     absolute: Optional[NonNegativeFloat] = Field(
#         default=None,
#         title="Absolute Tolerance", description="Absolute tolerance for the quantity"
#     )
#
#     # Optionals:
#     normType: Optional[Literal["L1Norm", "MeanL1Norm", "L2Norm", "MeanL2Norm", "LinfNorm"]] = (
#         Field(
#             default="L2Norm",
#             alias="normType",
#             title="Norm Type",
#             description=(
#                 "Sometimes, tolerances return a vector instead of a scalar (ex,"
#                 " solutionVector). Then, the magnitude of the tolerance should be"
#                 " calculated with a method. Norm type selects this method."
#             ),
#         )
#     )
#
#
# class Pancake3DSolvePositionRequiredTolerance(Pancake3DSolveToleranceBase):
#     # Mandatory:
#     quantity: Optional[PositionRequiredQuantityName] = Field(
#         title="Quantity", description="Name of the quantity for tolerance."
#     )
#     position: Optional[Pancake3DPosition] = Field(
#         title="Probing Position of the Quantity",
#         description="Probing position of the quantity for tolerance.",
#     )
#
# #
# class Pancake3DSolvePositionNotRequiredTolerance(Pancake3DSolveToleranceBase):
#     # Mandatory:
#     quantity: Optional[(
#         Literal[
#             "solutionVector",
#             "solutionVector",
#         ]
#         | PositionNotRequiredQuantityName
#     )] = Field(
#         default=None,
#         title="Quantity",
#         description="Name of the quantity for tolerance.",
#     )

#
# Pancake3DSolveTolerance = Pancake3DSolvePositionRequiredTolerance | Pancake3DSolvePositionNotRequiredTolerance
#
# class Pancake3DSolveSettingsWithTolerances(BaseModel):
#     tolerances: Optional[list[Pancake3DSolveTolerance]] = Field(
#         default=None,
#         title="Tolerances for Adaptive Time Stepping",
#         description=(
#             "Time steps or nonlinear iterations will be refined until the tolerances"
#             " are satisfied."
#         ),
#     )
#
#
# class Pancake3DSolveAdaptiveTimeLoopSettings(Pancake3DSolveSettingsWithTolerances):
#     # Mandatory:
#     initialStep: Optional[PositiveFloat] = Field(
#         default=None,
#         alias="initialStep",
#         title="Initial Step for Adaptive Time Stepping",
#         description="Initial step for adaptive time stepping",
#     )
#     minimumStep: Optional[PositiveFloat] = Field(
#         default=None,
#         alias="minimumStep",
#         title="Minimum Step for Adaptive Time Stepping",
#         description=(
#             "The simulation will be aborted if a finer time step is required than this"
#             " minimum step value."
#         ),
#     )
#     maximumStep: Optional[PositiveFloat] = Field(
#         default=None,
#         alias="maximumStep",
#         description="Bigger steps than this won't be allowed",
#     )
#
#     # Optionals:
#     integrationMethod: Literal[
#         "Euler", "Gear_2", "Gear_3", "Gear_4", "Gear_5", "Gear_6"
#     ] = Field(
#         default="Euler",
#         alias="integrationMethod",
#         title="Integration Method",
#         description="Integration method for transient analysis",
#     )
#     breakPoints_input: Optional[list[float]] = Field(
#         default=[0],
#         alias="breakPoints",
#         title="Break Points for Adaptive Time Stepping",
#         description="Make sure to solve the system for these times.",
#     )
#
#
# class Pancake3DSolveFixedTimeLoopSettings(BaseModel):
#     # Mandatory:
#     step: Optional[PositiveFloat] = Field(
#         default=None,
#         title="Step for Fixed Time Stepping",
#         description="Time step for fixed time stepping.",
#     )
#
#
# class Pancake3DSolveFixedLoopInterval(BaseModel):
#     # Mandatory:
#     startTime: Optional[NonNegativeFloat] = Field(
#         default=None,
#         title="Start Time of the Interval",
#         description="Start time of the interval.",
#     )
#     endTime: Optional[NonNegativeFloat] = Field(
#         default=None,
#         title="End Time of the Interval",
#         description="End time of the interval.",
#     )
#     step: Optional[PositiveFloat] = Field(
#         default=None,
#         title="Step for the Interval",
#         description="Time step for the interval",
#     )
#
#
# class Pancake3DSolveTimeBase(BaseModel):
#     # Mandatory:
#     start: Optional[float] = Field(
#         default=None,
#         title="Start Time", description="Start time of the simulation."
#     )
#     end: Optional[float] = Field(
#         default=None,
#         title="End Time",
#         description="End time of the simulation."
#     )
#
#     # Optionals:
#     extrapolationOrder: Optional[Literal[0, 1, 2, 3]] = Field(
#         default=1,
#         alias="extrapolationOrder",
#         title="Extrapolation Order",
#         description=(
#             "Before solving for the next time steps, the previous solutions can be"
#             " extrapolated for better convergence."
#         ),
#     )
#
#
# class Pancake3DSolveTimeAdaptive(Pancake3DSolveTimeBase):
#     timeSteppingType: Optional[Literal["adaptive"]] = "adaptive"
#     adaptive: Optional[Pancake3DSolveAdaptiveTimeLoopSettings] = Field(
#         default=None,
#         alias="adaptiveSteppingSettings",
#         title="Adaptive Time Loop Settings",
#         description=(
#             "Adaptive time loop settings (only used if stepping type is adaptive)."
#         ),
#     )


# class Pancake3DSolveTimeFixed(Pancake3DSolveTimeBase):
#     timeSteppingType: Optional[Literal["fixed"]] = "fixed"
#     fixed: (
#         list[Pancake3DSolveFixedLoopInterval] | Pancake3DSolveFixedTimeLoopSettings
#     ) = Field(
#         default=None,
#         alias="fixedSteppingSettings",
#         title="Fixed Time Loop Settings",
#         description="Fixed time loop settings (only used if stepping type is fixed).",
#     )
#
#
# Pancake3DSolveTime = Pancake3DSolveTimeAdaptive | Pancake3DSolveTimeFixed
#
# class Pancake3DSolveNonlinearSolverSettings(Pancake3DSolveSettingsWithTolerances):
#     # Optionals:
#     maxIter: Optional[PositiveInt] = Field(
#         default=100,
#         alias="maximumNumberOfIterations",
#         title="Maximum Number of Iterations",
#         description="Maximum number of iterations allowed for the nonlinear solver.",
#     )
#     relaxationFactor: Optional[float] = Field(
#         default=0.7,
#         gt=0,
#         alias="relaxationFactor",
#         title="Relaxation Factor",
#         description=(
#             "Calculated step changes of the solution vector will be multiplied with"
#             " this value for better convergence."
#         ),
#     )
#
#
# class Pancake3DSolveInitialConditions(BaseModel):
#     # 1) User inputs:
#
#     # Mandatory:
#     T: Optional[PositiveFloat] = Field(
#         default=None,
#         alias="temperature",
#         title="Initial Temperature",
#         description="Initial temperature of the pancake coils.",
#     )
#
#
# class Pancake3DSolveLocalDefect(BaseModel):
#     # Mandatory:
#     value: Optional[NonNegativeFloat] = Field(
#         default=None,
#         alias="value",
#         title="Value",
#         description="Value of the local defect.",
#     )
#     startTurn: Optional[NonNegativeFloat] = Field(
#         default=None,
#         alias="startTurn",
#         title="Start Turn",
#         description="Start turn of the local defect.",
#     )
#     endTurn: Optional[PositiveFloat] = Field(
#         default=None,
#         alias="endTurn",
#         title="End Turn",
#         description="End turn of the local defect.",
#     )
#
#     startTime: Optional[NonNegativeFloat] = Field(
#         default=None,
#         alias="startTime",
#         title="Start Time",
#         description="Start time of the local defect.",
#     )
#
#     # Optionals:
#     transitionDuration: Optional[NonNegativeFloat] = Field(
#         default=0,
#         title="Transition Duration",
#         description=(
#             "Transition duration of the local defect. If not given, the transition will"
#             " be instantly."
#         ),
#     )
#     whichPancakeCoil: Optional[PositiveInt] = Field(
#         default=None,
#         title="Pancake Coil Number",
#         description="The first pancake coil is 1, the second is 2, etc.",
#     )
#
#
# class Pancake3DSolveLocalDefects(BaseModel):
#     # 1) User inputs:
#
#     jCritical: Optional[Pancake3DSolveLocalDefect] = Field(
#         default=None,
#         alias="criticalCurrentDensity",
#         title="Local Defect for Critical Current Density",
#         description="Set critical current density locally.",
#     )
#
#
# class Pancake3DSolveQuantityBase(BaseModel):
#     # Mandatory:
#     quantity: Optional[PositionNotRequiredQuantityName | PositionRequiredQuantityName] = Field(
#         default=None,
#         title="Quantity",
#         description="Name of the quantity to be saved.",
#     )
#
#
# class Pancake3DSolveSaveQuantity(Pancake3DSolveQuantityBase):
#     # Optionals:
#     timesToBeSaved: Optional[list[float]] = Field(
#         default=[],
#         title="Times to be Saved",
#         description=(
#             "List of times that wanted to be saved. If not given, all the time steps"
#             " will be saved."
#         ),
#     )
#
#
# class Pancake3DPostprocessTimeSeriesPlotBase(Pancake3DSolveQuantityBase):
#     # Mandatory:
#     quantity: Optional[str] = None
#
#
# class Pancake3DPostprocessTimeSeriesPlotPositionRequired(
#     Pancake3DPostprocessTimeSeriesPlotBase
# ):
#     # Mandatory:
#     quantity: Optional[PositionRequiredQuantityName] = Field(
#         default=None,
#         title="Quantity",
#         description="Name of the quantity to be plotted.",
#     )
#
#     position: Optional[Pancake3DPosition] = Field(
#         default=None,
#         title="Probing Position",
#         description="Probing position of the quantity for time series plot.",
#     )
#
#
# class Pancake3DPostprocessTimeSeriesPlotPositionNotRequired(
#     Pancake3DPostprocessTimeSeriesPlotBase
# ):
#     # Mandatory:
#     quantity: Optional[PositionNotRequiredQuantityName] = Field(
#         default=None,
#         title="Quantity",
#         description="Name of the quantity to be plotted.",
#     )
#
#
# Pancake3DPostprocessTimeSeriesPlot = Pancake3DPostprocessTimeSeriesPlotPositionRequired | Pancake3DPostprocessTimeSeriesPlotPositionNotRequired
#
# class Pancake3DPostprocessMagneticFieldOnPlane(BaseModel):
#     # Optional:
#     colormap: Optional[str] = Field(
#         default="viridis",
#         title="Colormap",
#         description="Colormap for the plot.",
#     )
#     streamLines: Optional[bool] = Field(
#         default=True,
#         title="Stream Lines",
#         description=(
#             "If True, streamlines will be plotted. Note that magnetic field vectors may"
#             " have components perpendicular to the plane, and streamlines will be drawn"
#             " depending on the vectors' projection onto the plane."
#         ),
#     )
#     interpolationMethod: Optional[Literal["nearest", "linear", "cubic"]] = Field(
#         default="linear",
#         title="Interpolation Method",
#         description=(
#             "Interpolation type for the plot.\nBecause of the FEM basis function"
#             " selections of FiQuS, each mesh element has a constant magnetic field"
#             " vector. Therefore, for smooth 2D plots, interpolation can be"
#             " used.\nTypes:\nnearest: it will plot the nearest magnetic field value to"
#             " the plotting point.\nlinear: it will do linear interpolation to the"
#             " magnetic field values.\ncubic: it will do cubic interpolation to the"
#             " magnetic field values."
#         ),
#     )
#     timesToBePlotted: Optional[list[float]] = Field(
#         default=None,
#         title="Times to be Plotted",
#         description=(
#             "List of times that wanted to be plotted. If not given, all the time steps"
#             " will be plotted."
#         ),
#     )
#     planeNormal: Optional[Annotated[list[float], Len(min_length=3, max_length=3)]] = Field(
#         default=[1, 0, 0],
#         title="Plane Normal",
#         description="Normal vector of the plane. The default is YZ-plane (1, 0, 0).",
#     )
#     planeXAxisUnitVector: Optional[Annotated[list[float], Len(min_length=3, max_length=3)]] = (
#         Field(
#             default=[0, 1, 0],
#             title="Plane X Axis",
#             description=(
#                 "If an arbitrary plane is wanted to be plotted, the arbitrary plane's X"
#                 " axis unit vector must be specified. The dot product of the plane's X"
#                 " axis and the plane's normal vector must be zero."
#             ),
#         )
#     )
#
#
# class Pancake3DGeometry(BaseModel):
#     # Mandatory:
#     N: Optional[PositiveInt] = Field(
#         default=None,
#         ge=1,
#         alias="numberOfPancakes",
#         title="Number of Pancakes",
#         description="Number of pancake coils stacked on top of each other.",
#     )
#
#     gap: Optional[PositiveFloat] = Field(
#         default=None,
#         alias="gapBetweenPancakes",
#         title="Gap Between Pancakes",
#         description="Gap distance between the pancake coils.",
#     )
#
#     wi: Optional[Pancake3DGeometryWinding] = Field(
#         default=None,
#         alias="winding",
#         title="Winding Geometry",
#         description="This dictionary contains the winding geometry information.",
#     )
#
#     ii: Optional[Pancake3DGeometryContactLayer] = Field(
#         default=None,
#         alias="contactLayer",
#         title="Contact Layer Geometry",
#         description="This dictionary contains the contact layer geometry information.",
#     )
#
#     ti: Optional[Pancake3DGeometryTerminals] = Field(
#         default=None,
#         alias="terminals",
#         title="Terminals Geometry",
#         description="This dictionary contains the terminals geometry information.",
#     )
#
#     ai: Optional[Pancake3DGeometryAir] = Field(
#         default=None,
#         alias="air",
#         title="Air Geometry",
#         description="This dictionary contains the air geometry information.",
#     )
#
#     # Optionals:
#     dimTol: Optional[PositiveFloat] = Field(
#         default=1e-8,
#         alias="dimensionTolerance",
#         description="dimension tolerance (CAD related, not physical)",
#     )
#     pancakeBoundaryName: Optional[str] = Field(
#         default="PancakeBoundary",
#         description=(
#             "name of the pancake's curves that touches the air to be used in the mesh"
#         ),
#     )
#     contactLayerBoundaryName: Optional[str] = Field(
#         default="contactLayerBoundary",
#         description=(
#             "name of the contact layers's curves that touches the air to be used in the"
#             " mesh (only for TSA)"
#         ),
#     )
#
#
# class Pancake3DMesh(BaseModel):
#     # Mandatory:
#     wi: Optional[Pancake3DMeshWinding] = Field(
#         default=Pancake3DMeshWinding(),
#         alias="winding",
#         title="Winding Mesh",
#         description="This dictionary contains the winding mesh information.",
#     )
#     ii: Optional[Pancake3DMeshContactLayer] = Field(
#         default=Pancake3DMeshContactLayer(),
#         alias="contactLayer",
#         title="Contact Layer Mesh",
#         description="This dictionary contains the contact layer mesh information.",
#     )
#
#     # Optionals:
#     ti: Optional[Pancake3DMeshAirAndTerminals] = Field(
#         default=Pancake3DMeshAirAndTerminals(),
#         alias="terminals",
#         title="Terminal Mesh",
#         description="This dictionary contains the terminal mesh information.",
#     )
#     ai: Optional[Pancake3DMeshAirAndTerminals] = Field(
#         default=Pancake3DMeshAirAndTerminals(),
#         alias="air",
#         title="Air Mesh",
#         description="This dictionary contains the air mesh information.",
#     )
#
#     # Mandatory:
#     relSizeMin: Optional[PositiveFloat] = Field(
#         default=None,
#         alias="minimumElementSize",
#         title="Minimum Element Size",
#         description=(
#             "The minimum mesh element size in terms of the largest mesh size in the"
#             " winding. This mesh size will be used in the regions close the the"
#             " winding, and then the mesh size will increate to maximum mesh element"
#             " size as it gets away from the winding."
#         ),
#     )
#     relSizeMax: Optional[PositiveFloat] = Field(
#         default=None,
#         alias="maximumElementSize",
#         title="Maximum Element Size",
#         description=(
#             "The maximum mesh element size in terms of the largest mesh size in the"
#             " winding. This mesh size will be used in the regions close the the"
#             " winding, and then the mesh size will increate to maximum mesh element"
#             " size as it gets away from the winding."
#         ),
#     )
#
#
# class Pancake3DSolve(BaseModel):
#     # 1) User inputs:
#     t: Optional[Pancake3DSolveTime] = Field(
#         default=None,
#         alias="time",
#         title="Time Settings",
#         description="All the time related settings for transient analysis.",
#     )
#
#     nls: Optional[Pancake3DSolveNonlinearSolverSettings] = Field(
#         default=Pancake3DSolveNonlinearSolverSettings(),
#         alias="nonlinearSolver",
#         title="Nonlinear Solver Settings",
#         description="All the nonlinear solver related settings.",
#     )
#
#     wi: Optional[Pancake3DSolveWindingMaterial] = Field(
#         default=Pancake3DSolveWindingMaterial(),
#         alias="winding",
#         title="Winding Properties",
#         description="This dictionary contains the winding material properties.",
#     )
#     ii: Optional[Pancake3DSolveContactLayerMaterial] = Field(
#         default=Pancake3DSolveContactLayerMaterial(),
#         alias="contactLayer",
#         title="Contact Layer Properties",
#         description="This dictionary contains the contact layer material properties.",
#     )
#     ti: Optional[Pancake3DSolveTerminalMaterialAndBoundaryCondition] = Field(
#         default=Pancake3DSolveTerminalMaterialAndBoundaryCondition(),
#         alias="terminals",
#         title="Terminals Properties",
#         description=(
#             "This dictionary contains the terminals material properties and cooling"
#             " condition."
#         ),
#     )
#     ai: Optional[Pancake3DSolveAir] = Field(
#         default=Pancake3DSolveAir(),
#         alias="air",
#         title="Air Properties",
#         description="This dictionary contains the air material properties.",
#     )
#
#     ic: Optional[Pancake3DSolveInitialConditions] = Field(
#         default=Pancake3DSolveInitialConditions(),
#         alias="initialConditions",
#         title="Initial Conditions",
#         description="Initial conditions of the problem.",
#     )
#
#     save: Optional[list[Pancake3DSolveSaveQuantity]] = Field(
#         default=None,
#         alias="quantitiesToBeSaved",
#         title="Quantities to be Saved",
#         description="List of quantities to be saved.",
#     )
#
#     # Mandatory:
#     type: Optional[Literal["electromagnetic", "thermal", "weaklyCoupled", "stronglyCoupled"]] = (
#         Field(
#             default=None,
#             title="Simulation Type",
#             description=(
#                 "FiQuS/Pancake3D can solve only electromagnetics and thermal or"
#                 " electromagnetic and thermal coupled. In the weaklyCoupled setting,"
#                 " thermal and electromagnetics systems will be put into different"
#                 " matrices, whereas in the stronglyCoupled setting, they all will be"
#                 " combined into the same matrix. The solution should remain the same."
#             ),
#         )
#     )
#
#     # Optionals:
#     proTemplate: Optional[str] = Field(
#         default="Pancake3D_template.pro",
#         description="file name of the .pro template file",
#     )
#
#     localDefects: Optional[Pancake3DSolveLocalDefects] = Field(
#         default=Pancake3DSolveLocalDefects(),
#         alias="localDefects",
#         title="Local Defects",
#         description=(
#             "Local defects (like making a small part of the winding normal conductor at"
#             " some time) can be introduced."
#         ),
#     )
#
#     initFromPrevious: Optional[str] = Field(
#         default="",
#         title="Full path to res file to continue from",
#         description=(
#             "The simulation is continued from an existing .res file.  The .res file is"
#             " from a previous computation on the same geometry and mesh. The .res file"
#             " is taken from the folder Solution_<<initFromPrevious>>"
#         ),
#     )
#
#     isothermalInAxialDirection: Optional[bool] = Field(
#         default=False,
#         title="Equate DoF along axial direction",
#         description=(
#             "If True, the DoF along the axial direction will be equated. This means"
#             " that the temperature will be the same along the axial direction reducing"
#             " the number of DoF. This is only valid for the thermal analysis."
#         ),
#     )
#
#
# class Pancake3DPostprocess(BaseModel):
#     """
#     TO BE UPDATED
#     """
#
#     # 1) User inputs:
#     timeSeriesPlots: Optional[list[Pancake3DPostprocessTimeSeriesPlot]] = Field(
#         default=None,
#         title="Time Series Plots",
#         description="Values can be plotted with respect to time.",
#     )
#
#     magneticFieldOnCutPlane: Optional[Pancake3DPostprocessMagneticFieldOnPlane] = Field(
#         default=None,
#         title="Magnetic Field on a Cut Plane",
#         description=(
#             "Color map of the magnetic field on the YZ plane can be plotted with"
#             " streamlines."
#         ),
#     )


# class Pancake3D(BaseModel):
#     """
#     Level 1: Class for FiQuS Pancake3D
#     """
#
#     type: Literal["Pancake3D"]
#     geometry: Optional[Pancake3DGeometry] = Field(
#         default=None,
#         title="Geometry",
#         description="This dictionary contains the geometry information.",
#     )
#     mesh: Optional[Pancake3DMesh] = Field(
#         default=None,
#         title="Mesh",
#         description="This dictionary contains the mesh information.",
#     )
#     solve: Optional[Pancake3DSolve] = Field(
#         default=None,
#         title="Solve",
#         description="This dictionary contains the solve information.",
#     )
#     postproc: Optional[Pancake3DPostprocess] = Field(
#         default=None,
#         title="Postprocess",
#         description="This dictionary contains the postprocess information.",
#     )
#     input_file_path: Optional[str] = Field(
#         default=None,
#         description="path of the input file (calculated by FiQuS)",
#         exclude=True,
#     )


# class MultipoleConductor(BaseModel):
#     """
#         Class for conductor type for FiQuS input (.yaml)
#     """
#     version: Optional[str] = None
#     case: Optional[str] = None
#     state: Optional[str] = None
#     cable: Union[Rutherford, Ribbon, Mono] = {'type': 'Rutherford'}
#     strand: Union[Round, Rectangular] = {'type': 'Round'}  # TODO: Tape, WIC
#     Jc_fit: Union[ConstantJc, Bottura, CUDI1, CUDI3, Summers, Bordini, BSCCO_2212_LBNL, Ic_A_NbTi] = {
#         'type': 'CUDI1'}  # TODO: CUDI other numbers? , Roxie?


class MultipoleRoxieGeometry(BaseModel):
    """
        Class for FiQuS multipole Roxie data (.geom)
    """
    Roxie_Data: RoxieData = RoxieData()


class RunFiQuS(BaseModel):
    """
    Class for FiQuS run
    """

    type: Optional[Literal[
        "start_from_yaml",
        "mesh_only",
        "geometry_only",
        "geometry_and_mesh",
        "pre_process_only",
        "mesh_and_solve_with_post_process_python",
        "solve_with_post_process_python",
        "solve_only",
        "post_process_getdp_only",
        "post_process_python_only",
        "post_process",
        "batch_post_process_python",
    ]] = Field(
        default="start_from_yaml",
        title="Run Type of FiQuS",
        description="FiQuS allows you to run the model in different ways. The run type can be specified here. For example, you can just create the geometry and mesh or just solve the model with previous mesh, etc.",
    )
    geometry: Optional[Union[str, int]] = Field(
        default=None,
        title="Geometry Folder Key",
        description="This key will be appended to the geometry folder.",
    )
    mesh: Optional[Union[str, int]] = Field(
        default=None,
        title="Mesh Folder Key",
        description="This key will be appended to the mesh folder.",
    )
    solution: Optional[Union[str, int]] = Field(
        default=None,
        title="Solution Folder Key",
        description="This key will be appended to the solution folder.",
    )
    launch_gui: Optional[bool] = Field(
        default=False,
        title="Launch GUI",
        description="If True, the GUI will be launched after the run.",
    )
    overwrite: Optional[bool] = Field(
        default=False,
        title="Overwrite",
        description="If True, the existing folders will be overwritten, otherwise new folders will be created.",
    )
    comments: str = Field(
        default="",
        title="Comments",
        description="Comments for the run. These comments will be saved in the run_log.csv file.",
    )
    verbosity_Gmsh: int = Field(
        default=5,
        title="verbosity_Gmsh",
        description="Level of information printed on the terminal and the message console (0: silent except for fatal errors, 1: +errors, 2: +warnings, 3: +direct, 4: +information, 5: +status, 99: +debug)",
    )
    verbosity_GetDP: int = Field(
        default=5,
        title="verbosity_GetDP",
        description="Level of information printed on the terminal and the message console. Higher number prints more, good options are 5 or 6.",
    )
    verbosity_FiQuS: bool = Field(
        default=True,
        title="verbosity_FiQuS",
        description="Level of information printed on the terminal and the message console by FiQuS. Only True of False for now.",
    )


class General(BaseModel):
    """
        Class for FiQuS general
    """
    magnet_name: Optional[str] = None


class EnergyExtraction(BaseModel):
    """
        Level 3: Class for FiQuS Multipole
    """
    t_trigger: Optional[float] = None
    R_EE: Optional[float] = None
    power_R_EE: Optional[float] = None
    L: Optional[float] = None
    C: Optional[float] = None


class QuenchHeaters(BaseModel):
    """
        Level 3: Class for FiQuS Multipole
    """
    N_strips: Optional[int] = None
    t_trigger: Optional[List[float]] = None
    U0: Optional[List[float]] = None
    C: Optional[List[float]] = None
    R_warm: Optional[List[float]] = None
    w: Optional[List[float]] = None
    h: Optional[List[float]] = None
    h_ins: List[List[float]] = []
    type_ins: List[List[str]] = []
    h_ground_ins: List[List[float]] = []
    type_ground_ins: List[List[str]] = []
    l: Optional[List[float]] = None
    l_copper: Optional[List[float]] = None
    l_stainless_steel: Optional[List[float]] = None
    ids: Optional[List[int]] = None
    turns: Optional[List[int]] = None
    turns_sides: Optional[List[str]] = None


class Cliq(BaseModel):
    """
        Level 3: Class for FiQuS Multipole
    """
    t_trigger: Optional[float] = None
    current_direction: Optional[List[int]] = None
    sym_factor: Optional[int] = None
    N_units: Optional[int] = None
    U0: Optional[float] = None
    C: Optional[float] = None
    R: Optional[float] = None
    L: Optional[float] = None
    I0: Optional[float] = None

class ESC(BaseModel):
    """
        Level 2: Class for the ESC parameters
    """
    t_trigger: Optional[List[float]] = None
    U0: Optional[List[float]] = None
    C: Optional[List[float]] = None
    R_unit: Optional[List[float]] = None
    R_leads: Optional[List[float]] = None
    Ud_Diode: Optional[List[float]] = None

class QuenchProtection(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    energy_extraction:  EnergyExtraction = EnergyExtraction()
    quench_heaters: QuenchHeaters = QuenchHeaters()
    cliq: Cliq = Cliq()
    esc: ESC = ESC()

class QuenchDetection(BaseModel):
    """
    Level 2: Class for FiQuS
    """

    voltage_thresholds: Optional[List[float]] = Field(
        default=None,
        title="List of quench detection voltage thresholds",
        description="Voltage thresholds for quench detection. The quench detection will be triggered when the voltage exceeds these thresholds continuously for a time larger than the discrimination time.",
    )

    discrimination_times: Optional[List[float]] = Field(
        default=None,
        title="List of quench detection discrimination times",
        description="Discrimination times for quench detection. The quench detection will be triggered when the voltage exceeds the thresholds continuously for a time larger than these discrimination times.",
    )

    voltage_tap_pairs: Optional[List[List[int]]] = Field(
        default=None,
        title="List of quench detection voltage tap pairs",
        description="Voltage tap pairs for quench detection. The voltage difference between these pairs will be used for quench detection.",
    )

class DataFiQuS(BaseModel):
    """
        This is data structure of FiQuS Input file
    """
    general: General = General()
    run: RunFiQuS = RunFiQuS()
    magnet: Union[CCT, CWS, Multipole, Pancake3D, CACStrand, CACRutherford] = {'type': 'multipole'}
    circuit: Circuit_Class = Circuit_Class()
    power_supply: PowerSupplyClass = PowerSupplyClass()
    quench_protection: QuenchProtection = QuenchProtection()
    quench_detection: QuenchDetection = QuenchDetection()
    conductors: Dict[str, ConductorFiQuS] = {}
