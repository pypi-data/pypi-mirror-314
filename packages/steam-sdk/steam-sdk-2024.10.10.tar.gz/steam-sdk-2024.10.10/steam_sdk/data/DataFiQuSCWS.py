from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Optional, Union


class CWSGeometryConductors(BaseModel):  # Conductor file data for geometry building
    """
    Level 2: Class for FiQuS CWS
    """

    skip_middle_from: Optional[List[int]] = (
        None  # decides which bricks are skipped in fuse operation, basically only a few bricks should overlap with the former.
    )
    skip_middle_to: Optional[List[int]] = (
        None  # decides which bricks are skipped in fuse operation, basically only a few bricks should overlap with the former.
    )
    file_names_large: Optional[List[str]] = None
    file_names: Optional[List[str]] = None  # Inner_17.1mm #[inner_FL, outer_FL] #
    ends_need_trimming: bool = (
        False  # If there are windings "sticking out" of the air region this needs to set to True. It removes 2 volumes per winding after the fragment operation
    )


class CWSGeometryFormers(BaseModel):  # STEP file data for geometry building
    """
    Level 2: Class for FiQuS CWS
    """

    file_names: Optional[List[str]] = None  # STEP file names to use
    air_pockets: Optional[List[int]] = (
        None  # number of air pockets (for e.g. for heater or temperature sensor pads) on the formers
    )


class CWSGeometryShells(BaseModel):  # STEP file data for geometry building
    """
    Level 2: Class for FiQuS CWS
    """

    file_names: Optional[List[str]] = None  # STEP file names to use


class CWSGeometryAir(BaseModel):  # Geometry related air_region _inputs
    """
    Level 2: Class for FiQuS CWS
    """

    name: Optional[str] = None  # name to use in gmsh and getdp
    sh_type: Optional[str] = (
        None  # cylinder, cuboid, cylinder_offset, cylinder_cov or cylinder_link are possible
    )
    ar: Optional[float] = (
        None  # if box type is cuboid 'a' is taken as a dimension, if cylinder then 'r' is taken
    )
    z_min: Optional[float] = (
        None  # extend of air region in negative z direction, for cylinder_cov this is ignored
    )
    z_max: Optional[float] = (
        None  # extend of air region in positive z direction, for cylinder_cov this is ignored
    )
    rotate: Optional[float] = None  # rotation around z axis in degrees
    xy_offset: Optional[List[float]] = (
        None  # list with x and y offset of the cylinder, only works if sh_type is set to cylinder_offset, e.g. [0, 0.3]
    )
    extension_distance: Optional[List[float]] = (
        None  # list with distances in meter to take along the line going through bricks of end terminals. For example to extend the air region by 0.5 m each way the entry could be [0.5, -0.5]
    )


class CWSGeometry(BaseModel):
    """
    Level 2: Class for FiQuS CWS for FiQuS input
    """

    use_fragment: Optional[bool] = Field(
        default=None, description="Controls if fragment is handled by gmsh only (false) or python with gmsh (ture)"
    )
    concurrent: Optional[bool] = Field(
        default=None, description="Controls if geometry operations are done in concurrent or sequential way"
    )
    conductors: CWSGeometryConductors = CWSGeometryConductors()
    formers: CWSGeometryFormers = CWSGeometryFormers()
    shells: CWSGeometryShells = CWSGeometryShells()
    air: CWSGeometryAir = CWSGeometryAir()


class CWSSolveMaterialPropertyListConductors(BaseModel):
    constant: Optional[List[float]] = None  # list of values if constant is used


class CWSSolveMaterialPropertyList(BaseModel):
    constant: Optional[List[float]] = None  # list of values if constant is used
    function: Optional[List[str]] = (
        None  # list of material property function names if function is used
    )


class CWSSolveMaterialPropertySingle(BaseModel):
    constant: Optional[float] = None  # value if constant is used
    function: Optional[str] = (
        None  # material property function name if function is used
    )


class CWSSolveConductorsExcitationFunction(
    BaseModel
):  # Solution time used Conductor _inputs (materials and BC)
    """
    Level 2: Class for FiQuS CWS
    """

    initials: Optional[List[float]] = Field(
        default=None, description="Initial current or voltage in the conductor"
    )
    names: Optional[List[Literal["exp_decrease", "exp_increase", "linear_decrease", "linear_increase_from_zero"]]] = Field(
        default=['exp_decrease'],
        description="Currently, these function names are supported: exp_decrease, exp_increase, linear_decrease, linear_increase ",
    )
    taus: Optional[List[float]] = Field(
        default=None,
        description="Time constant for exponential: Amplitude*Exp(-time/tau), for linear: Amplitude*(time-time_initial)/tau ",
    )


class CWSSolveExcitationFromFile(
    BaseModel
):  # Solution time used Conductor _inputs (materials and BC)
    """
    Level 2: Class for FiQuS CWS
    """

    file_name: Optional[str] = (
        None  # full file name (i.e. with extension) in the input folder or complete path
    )
    time_header: Optional[str] = (
        None  # string defining the time signal header in the txt file
    )
    value_headers: Optional[List[str]] = Field(
        default=None,
        description="string defining the value (typically current [A] or power [W]) signal header in the txt file",
    )


class CWSSolveConductorsExcitation(
    BaseModel
):  # Solution time used Conductor _inputs (materials and BC)
    """
    Level 2: Class for FiQuS CWS
    """

    conductors_nw: Optional[List[int]] = Field(
        default=None,
        description="Number of conductors in channel in the height direction (pointing out of the channel direction)",
    )
    conductors_nh: Optional[List[int]] = Field(
        default=None,
        description="Number of conductors in channel in the width direction",
    )
    multips: Optional[List[float]] = Field(
        default=None,
        description="This is decide on polarity of powering the magnet, most often value of 1 or -1 is used. However, arbitrary multiplication is also supported",
    )
    function: CWSSolveConductorsExcitationFunction = (
        CWSSolveConductorsExcitationFunction()
    )
    from_file: CWSSolveExcitationFromFile = (
        CWSSolveExcitationFromFile()
    )
    transient_use: Optional[Literal["function", "from_file"]] = Field(
        default="function",
        title="Use Material Property as",
        description="Either values from a function or from_file can be used",
    )  # function or from_file allowed


class CWSSolveConductors(
    BaseModel
):  # Solution time used Conductor _inputs (materials and BC)
    """
    Level 2: Class for FiQuS CWS
    """

    excitation: CWSSolveConductorsExcitation = CWSSolveConductorsExcitation()
    conductivity_el: CWSSolveMaterialPropertyListConductors = (
        CWSSolveMaterialPropertyListConductors()
    )
    permeability: Optional[List[float]] = None  # relative permeability


class CWSSolveInduced(BaseModel):  # Solution time used fqpls _inputs (materials and BC)
    """
    Level 2: Class for FiQuS CWS
    """

    use: Optional[Literal["function", "constant"]] = Field(
        default="function",
        title="Use Material Property as",
        description="Either values from a function or constant can be used",
    )
    RRR_functions: Optional[List[float]] = None  # RRR to use in material functions
    conductivity_el: CWSSolveMaterialPropertyList = CWSSolveMaterialPropertyList()
    permeability: List[float] = []  # relative permeability
    conductivity_th: CWSSolveMaterialPropertyList = Field(
        default=CWSSolveMaterialPropertyList(),
        alias="conductivity_th",
        description="W/mK",
    )
    heat_capacity: CWSSolveMaterialPropertyList = Field(
        default=CWSSolveMaterialPropertyList(),
        alias="heat_capacity",
        description="J/m^3 K",
    )


class CWSSolveHeaterFunction(BaseModel):
    """
    Defines entries for function to use in a form of linearly interpolated LOOK-UP-TABLE (LUT) of power vs time
    """
    times: Optional[List[List[float]]] = Field(
        default=None,
        title="Time look up table",
        description="Time values for power values. This list must be the same length as power_LUT. It is list of list, with each list per heater.",
    )
    powers: Optional[List[List[float]]] = Field(
        default=None,
        title="Time look up table",
        description="Power values [W] for time values specified. This list must be the same length as time_LUT. It is list of list, with each list per heater.",
    )


class CWSSolveCoolingHeatTransferCoefficients(BaseModel):

    use: Optional[Literal["function", "constant", "disabled"]] = Field(
        default="disabled",
        title="Controls what type of cooling is applied to surfaces specified in mesh.cooled_surfaces. The list lengths must match for number of surfaces and constants of functions",
        description="Either values from a function or constant or disabled can be used",
    )
    constant: Optional[List[float]] = None  # heat transfer coefficient in W m^-2 K^-1
    function: Optional[List[str]] = None  # Names of material function to use


class CWSSolveCoolingChannelsInsulationConductivityTh(BaseModel):
    use: Optional[Literal["function", "constant", "disabled"]] = Field(
        default="disabled",
        title="Controls what type of cooling is applied to surfaces specified in mesh.cooled_surfaces. The list lengths must match for number of surfaces and constants of functions",
        description="Either values from a function or constant or disabled can be used",
    )
    constant: Optional[float] = None  # thermal conductivity value
    function: Optional[str] = None  # thermal conductivity funcion name

class CWSSolveCoolingChannels(BaseModel):
    insulation_thickness: Optional[float] = None
    scaling_factor: Optional[float] = None
    insulation_conductivity_th: CWSSolveCoolingChannelsInsulationConductivityTh = CWSSolveCoolingChannelsInsulationConductivityTh()


class CWSSolveCooling(BaseModel):
    heat_transfer_coefficients: CWSSolveCoolingHeatTransferCoefficients = CWSSolveCoolingHeatTransferCoefficients()
    channels: CWSSolveCoolingChannels = CWSSolveCoolingChannels()

class CWSSolveHeaters(BaseModel):  # Solver options for applying BC for heaters
    """
    Level 2: Class for FiQuS CWS
    """

    transient_use: Literal["LUT", "from_file", "disabled"] = Field(
        default="disabled",
        title="Use Material Property as",
        description="Either values from a function or from_file can be used",
    )
    LUT: CWSSolveHeaterFunction = (
        CWSSolveConductorsExcitationFunction()
    )
    from_file: CWSSolveExcitationFromFile = (
        CWSSolveExcitationFromFile()
    )


class CWSSolveInsulation(BaseModel):
    """
    Level 2: Class for FiQuS CWS
    """

    thickness: Optional[float] = Field(
        default=None,
        description="Thickness of insulation former to former or former to shell",
    )  #
    conductivity_th: CWSSolveMaterialPropertySingle = CWSSolveMaterialPropertySingle()
    heat_capacity: CWSSolveMaterialPropertySingle = Field(
        default=CWSSolveMaterialPropertySingle(),
        alias="heat_capacity",
        description="J/m^3 K",
    )


class CWSSolveAir(BaseModel):  # Solution time used air _inputs (materials and BC)
    """
    Level 2: Class for FiQuS CWS
    """

    conductivity_el: Optional[float] = Field(
        default=None, description="Electrical conductivity"
    )
    permeability: Optional[float] = Field(
        default=None, description="Relative permeability"
    )


class CWSSolveOutputResample(BaseModel):  # Solution outputs definition
    enabled: Optional[bool] = Field(
        default=None, description="Flag to decide if the output is resampled or not"
    )
    delta_t: Optional[float] = Field(
        default=None, description="Delta time for resampling"
    )


class CWSSolveOutput(BaseModel):  # Solution outputs definition
    saved: Optional[bool] = Field(
        default=None, description="Flat to decide if the output is saved"
    )
    resample: CWSSolveOutputResample = CWSSolveOutputResample()
    variables: Optional[List[str]] = Field(
        default=None, description="Name of variable to post-process by GetDP"
    )
    volumes: Optional[List[str]] = Field(
        default=None, description="Name of volume to post-process by GetDP"
    )
    file_exts: Optional[List[str]] = Field(
        default=None, description="Name of file extensions to output by GetDP"
    )


class CWSSolveStaticSettings(BaseModel):
    solved: Optional[bool] = Field(
        default=None,
        description="Chooses if static solution is solved. Note the transient solution starts with a static solution, so if this and the transient are set to true, the static is solved twice",
    )
    output: CWSSolveOutput = CWSSolveOutput()


class CWSSolveTime(BaseModel):
    initial: Optional[float] = Field(default=None, description="Initial time")
    end: Optional[float] = Field(default=None, description="End time")


class CWSSolveTimeFixed(BaseModel):
    step: Optional[float] = Field(default=None, description="Time step")
    theta: Optional[float] = Field(default=None, description="Time stepping scheme")


class CWSSolveTimeAdaptiveLTEInputs(BaseModel):
    names: Optional[List[str]] = Field(
        default=None, description="string: name of post operation to use"
    )
    relatives: Optional[List[float]] = Field(
        default=None, description="relative tolerance"
    )
    absolutes: Optional[List[float]] = Field(
        default=None, description="absolute tolerance"
    )
    normTypes: Optional[List[str]] = Field(
        default=None,
        description="string with norm type, allowed: L1Norm, MeanL1Norm, L2Norm, MeanL2Norm, LinfNorm",
    )


class CWSSolveTimeAdaptiveLTE(BaseModel):
    System: CWSSolveTimeAdaptiveLTEInputs = (
        CWSSolveTimeAdaptiveLTEInputs()
    )  # Quantities of interest specified at system level
    PostOperation: CWSSolveTimeAdaptiveLTEInputs = (
        CWSSolveTimeAdaptiveLTEInputs()
    )  # Quantities of interest specified at PostOperation level


class CWSSolveTimeAdaptive(BaseModel):
    initial_fixed_time_step: Optional[float] = Field(
        default=-1.0,
        description="If this value is set to > 0 then an initial fixed time step is performed",
    )
    initial_step: Optional[float] = Field(
        default=None,
        description="Initial time step. Note this is only used when not starting from previous result",
    )
    min_step: Optional[float] = Field(default=None, description="Minimum time step")
    max_step: Optional[float] = Field(default=None, description="Maximum time step")
    integration_method: Optional[str] = Field(
        default=None,
        description="string: Euler, Trapezoidal, Gear_2, Gear_3, Gear_4, Gear_5, Gear_6",
    )
    breakpoints_every: Optional[float] = Field(
        default=None,
        description="this creates a list from initial to end time with this step",
    )
    additional_breakpoints: Optional[List[float]] = Field(
        default=[],
        description="Additional break points to request, typically when the solution is expected to change steeply, like t_PC_off of LEDET",
    )
    LTE: CWSSolveTimeAdaptiveLTE = CWSSolveTimeAdaptiveLTE()  # local_truncation_errors


class CWSSolveNonLinearThermalSettingsTolerance(BaseModel):
    name: Optional[str] = Field(
        default=None, description="string: name of post operation to use"
    )
    relative: Optional[float] = Field(default=None, description="relative tolerance")
    absolute: Optional[float] = Field(default=None, description="absolute tolerance")
    normType: Optional[str] = Field(
        default=None,
        description="string with norm type, allowed: L1Norm, MeanL1Norm, L2Norm, MeanL2Norm, LinfNorm",
    )


class CWSSolveNonLinearThermalSettings(BaseModel):
    enabled: Optional[bool] = Field(
        default=None,
        description="Flag to decide if constant material properties or nonlinear material functions should be used",
    )
    maximumNumberOfIterations: Optional[int] = Field(
        default=None, description="Number of iterations to use"
    )
    relaxationFactor: Optional[float] = Field(
        default=None, description="Relaxation factor to use"
    )
    tolerance: CWSSolveNonLinearThermalSettingsTolerance = (
        CWSSolveNonLinearThermalSettingsTolerance()
    )


class CWSSolveTransientSettings(BaseModel):
    solved: Optional[bool] = Field(
        default=None,
        description="Flag to decide if a transient solution is solved (when true), when false the transient is skipped",
    )
    with_thermal: Optional[bool] = Field(
        default=None,
        description="Flag to decide if thermal transient is is solved and weakly coupled to the electromagnetic (when true), when false only electromagnetic is considered (depending on the flag 'solved' above)",
    )
    thermal_TSA_N_elements: Optional[int] = Field(
        default=None,
        description="When set to 0 the thermal TSA is disabled so the is no heat flow between induced parts. Otherwise, this is number of elements across the thin shell",
    )
    nonlinear_thermal_iterations: CWSSolveNonLinearThermalSettings = (
        CWSSolveNonLinearThermalSettings()
    )
    time_stepping: Optional[Literal["fixed", "adaptive"]] = Field(
        default=None, description="either 'fixed' or 'adaptive'"
    )
    time: CWSSolveTime = CWSSolveTime()
    fixed: CWSSolveTimeFixed = CWSSolveTimeFixed()
    adaptive: CWSSolveTimeAdaptive = CWSSolveTimeAdaptive()
    em_output: CWSSolveOutput = CWSSolveOutput()
    th_output: CWSSolveOutput = CWSSolveOutput()


class CWSSolve(BaseModel):
    """
    Level 2: Class for FiQuS CWS
    """
    temperature: Optional[float] = None  # Initial temperature for the thermal solve
    link: Optional[bool] = Field(
        default=None,
        description="Decides if powering volumes in a 'linked way' (two windings powered in series with only two terminals) is used. This does not work well, so do not use for now",
    )
    save_last: bool = Field(
        default=False,
        description="This controls if lastTime step only solution is save to allow starting from previous solution",
    )
    start_from_previous: Optional[bool] = Field(
        default=None,
        description="flag to decide if the previous solution (time window of transient should be used as a starting point for this time window)",
    )
    conductors: CWSSolveConductors = (
        CWSSolveConductors()
    )  # windings solution time _inputs
    formers: CWSSolveInduced = CWSSolveInduced()  # formers solution time _inputs
    shells: CWSSolveInduced = CWSSolveInduced()  # shells solution time _inputs
    cooling: CWSSolveCooling = CWSSolveCooling()
    heaters: CWSSolveHeaters = CWSSolveHeaters()  # shells solution time _inputs
    insulation_th: CWSSolveInsulation = (
        CWSSolveInsulation()
    )  # insulation former to former or former to shell, thermal properties only.
    insulation_el: Optional[bool] = Field(
        default=None,
        description="Flag to decide if windings are insulated from formers and formers from each other",
    )
    air: CWSSolveAir = CWSSolveAir()  # air solution time _inputs
    pro_template: Optional[str] = None  # file name of .pro template file
    static: CWSSolveStaticSettings = (
        CWSSolveStaticSettings()
    )  # transient solution settings
    transient: CWSSolveTransientSettings = (
        CWSSolveTransientSettings()
    )  # transient solution settings


class CWSPMeshFieldCoils(BaseModel):
    enabled: Optional[bool] = Field(
        default=False, description="If true the coils lines are added."
    )
    coils: Optional[Dict[Union[str, int], List[List[float]]]] = Field(
        default=None,
        description="Dictionary with structure: key: [[p1_x,p1_y,p1_z], [p2_x,p2_y,p2_z], [p3_x,p3_y,p3_z], [p4_x,p4_y,p4_z]]. At least 3 points are needed. All the pints will be used to create a closed surface.",
    )


class CWSPMeshThCooledSurfaces(BaseModel):
    enabled: Optional[bool] = Field(default=False, description="If true the coils lines are added.")
    surfaces: Optional[List[Union[Literal['auto'], List[int]]]] = Field(default=None,
                                                                        description="Specifies lists of surfaces of the brep file to group together to apply cooling power."
                                                                                    "If 'auto' is chosen it loops through list of formers + shell and creates automatically a list of surfaces that touch air region")
    names: Optional[List[str]] = Field(default=None, description="Specifies user friendly names for the surfaces")


class CWSPMeshThSensorAndHeater(BaseModel):
    enabled: Optional[bool] = Field(default=False, description="If true the coils lines are added.")
    surfaces: Optional[List[int]] = Field(default=None, description="Specifies surfaces of the brep file to average temperature over or apply heater power.")
    names: Optional[List[str]] = Field(default=None, description="Specifies user friendly names for the surfaces")


class CWSMesh(BaseModel):
    """
    Level 2: Class for FiQuS CWS
    """

    MaxAspectWindings: Optional[float] = (
        None  # used in transfinite mesh_generators settings to define mesh_generators size along two longer lines of hex elements of windings
    )
    Min_length_windings: Optional[float] = (
        None  # sets how small the edge length for the winding geometry volumes could be used. Overwrites the calculated value if it is smaller than this number.
    )
    ThresholdSizeMinWindings: Optional[float] = (
        None  # sets field control of Threshold SizeMin
    )
    ThresholdSizeMaxWindings: Optional[float] = (
        None  # sets field control of Threshold SizeMax
    )
    ThresholdDistMinWindings: Optional[float] = (
        None  # sets field control of Threshold DistMin
    )
    ThresholdDistMaxWindings: Optional[float] = (
        None  # sets field control of Threshold DistMax
    )
    ThresholdSizeMinFormers: Optional[float] = (
        None  # sets field control of Threshold SizeMin
    )
    ThresholdSizeMaxFormers: Optional[float] = (
        None  # sets field control of Threshold SizeMax
    )
    ThresholdDistMinFormers: Optional[float] = (
        None  # sets field control of Threshold DistMin
    )
    ThresholdDistMaxFormers: Optional[float] = (
        None  # sets field control of Threshold DistMax
    )
    link_terminal: Optional[List[List[int]]] = Field(
        default=None,
        description="Specify which windings are connected by giving indexes of winding to connect in the file_names. This is 0 based indexing. To connect first with second winding this is the entry [[0, 1]]",
    )
    cooled_surfaces: CWSPMeshThCooledSurfaces = CWSPMeshThCooledSurfaces()
    temperature_sensors: CWSPMeshThSensorAndHeater = CWSPMeshThSensorAndHeater()
    heaters: CWSPMeshThSensorAndHeater = CWSPMeshThSensorAndHeater()
    field_coils: CWSPMeshFieldCoils = CWSPMeshFieldCoils()


class CWSPostproc_FieldMap(BaseModel):
    process_static: Optional[bool] = (
        None  # flag to switch on and off processing of static solution for field map
    )
    process_transient: Optional[bool] = (
        None  # flag to switch on and off processing of transient solution for field map
    )
    channel_ws: Optional[List[float]] = None  # wire width
    channel_hs: Optional[List[float]] = None  # wire height
    winding_order: Optional[List[int]] = Field(
        default=None, description="[1, 2, 3, 4, 5, 6, 7, 8]"
    )
    trim_from: Optional[List[int]] = None
    trim_to: Optional[List[int]] = None
    n_points_for_B_avg: Optional[List[int]] = (
        None  # number of points to extract for calculating average for B in the center of each wire turn
    )
    variable: Optional[str] = Field(
        default=None, description="Name of variable to post-process by gmsh for LEDET"
    )  # Name of variable to post-process by python Gmsh API, like B for magnetic flux density
    volume: Optional[str] = Field(
        default=None, description="Name of volume to post-process by gmsh for LEDET"
    )  # Name of volume to post-process by python Gmsh API, line Winding_1
    file_ext: Optional[str] = Field(
        default=None,
        description="Name of file extensions to output to by gmsh for LEDET",
    )  # Name of file extensions o post-process by python Gmsh API, like .pos


class CWSPostprocStaticOrTransient(BaseModel):
    process_static: Optional[bool] = Field(
        default=None,
        description="If true the postprocessing is performed, if false it is not performed",
    )
    process_transient: Optional[bool] = Field(
        default=None,
        description="If true the postprocessing is performed, if false it is not performed",
    )


class CWSPostprocTemperature(BaseModel):
    process_transient: Optional[bool] = (
        None  # flag to switch on and off processing of transient solution of temperature
    )


class CWSPostprocCircuitValues(BaseModel):
    process_static_and_transient: Optional[bool] = (
        None  # flag to switch on and off processing of static and transient solutions for circuit values
    )


class CWSPostproc(BaseModel):
    """
    Class for FiQuS CWS input file
    """

    field_map: CWSPostproc_FieldMap = CWSPostproc_FieldMap()
    temperature_map: CWSPostprocTemperature = CWSPostprocTemperature()
    temperature_sensors: CWSPostprocTemperature = CWSPostprocTemperature()
    inductance: CWSPostprocStaticOrTransient = CWSPostprocStaticOrTransient()
    circuit_values: CWSPostprocCircuitValues = CWSPostprocCircuitValues()
    field_coils: CWSPostprocStaticOrTransient = CWSPostprocStaticOrTransient()


class CWS(BaseModel):
    """
    Level 1: Class for FiQuS CWS
    """

    type: Literal["CWS"]
    geometry: CWSGeometry = CWSGeometry()
    mesh: CWSMesh = CWSMesh()
    solve: CWSSolve = CWSSolve()
    postproc: CWSPostproc = CWSPostproc()
