from pydantic import BaseModel, Field
from typing import List, Literal, Optional


# ============= GEOMETRY ============= #
# -- Input/Output settings -- #
class CACStrandIOsettingsLoad(BaseModel):
    """
    Level 3: Class for Input/Output settings for the cable geometry
    """

    load_from_yaml: Optional[bool] = Field(
        default=False,
        description="True to load the geometry from a YAML file, false to generate the geometry.",
    )
    filename: Optional[str] = Field(
        default=None,
        description="Name of the YAML file from which to load the geometry.",
    )

class CACStrandIOsettingsSave(BaseModel):
    """
    Level 3: Class for Input/Output settings for the cable geometry
    """

    save_to_yaml: Optional[bool] = Field(
        default=False,
        description="True to save the geometry to a YAML-file, false to not save the geometry.",
    )
    filename: Optional[str] = Field(
        default=None,
        description="Name of the output geometry YAML file.",
    )

class CACStrandGeometryIOsettings(BaseModel):
    """
    Level 2: Class for Input/Output settings for the cable geometry
    """

    load: CACStrandIOsettingsLoad = (
        CACStrandIOsettingsLoad()
    )
    save: CACStrandIOsettingsSave = (
        CACStrandIOsettingsSave()
    )

# -- Strand geometry parameters -- #
class CACStrandGeometry(BaseModel):
    """
    Level 2: Class for strand geometry parameters
    """
    io_settings: CACStrandGeometryIOsettings = CACStrandGeometryIOsettings()
    hexagonal_filaments: Optional[bool] = Field(
        default=None,
        description="Field for specifying the shape of the filaments. True for hexagonal, False for circular.",
    )
    filament_circular_distribution: Optional[bool] = Field(
        default=None,
        description="Field for specifying the geometrical distribution of the filaments. Set True to distribute the filaments in a circular pattern and False to distribute them in a hexagonal pattern."
    )
    air_radius: Optional[float] = Field(
        default=None, description="Radius of the circular numerical air region (m)."
    )
    air_boundary_form: Optional[int] = Field(
        default=1, description="boundary form of the air region. 1:circle 2:square"
    )

# ============= MESH ============= #
# -- Filament mesh settings -- #
class CACStrandMeshFilaments(BaseModel):
    """
    Level 3: Class for FiQuS ConductorAC
    """

    boundary_mesh_size_ratio: Optional[float] = Field(
        default=None,
        description="Mesh size at filament boundaries, relative to the radius of the filaments. E.g. 0.1 means that the mesh size is 0.1 times the filament radius.",
    )
    center_mesh_size_ratio: Optional[float] = Field(
        default=None,
        description="Mesh size at filament center, relative to the radius of the filaments. E.g. 0.1 means that the mesh size is 0.1 times the filament radius.",
    )
    amplitude_dependent_scaling: Optional[bool] = Field(
        default=False,
        description="Amplitude dependent scaling uses the field amplitude to approximate the field penetration distance in the filaments to alter the filament mesh. If the field penetration distance is low (i.e. for low field amplitudes) this feature increases mesh density in the region where the field is expected to penetrate, and decreases the mesh resolution in the region where the field does not penetrate.",
    )
    field_penetration_depth_scaling_factor: Optional[float] = Field(
        default=None,
        description="Scaling factor for the estimate of the field penetration depth, used for amplitude dependent scaling. ",
    )
    desired_elements_in_field_penetration_region: Optional[float] = Field(
        default=None,
        description="Desired number of elements in the field penetration region. This parameter is used for amplitude dependent scaling, and determines the number of elements in the region where the field is expected to penetrate.",
    )

# -- Matrix mesh settings -- #
class CACStrandMeshMatrix(BaseModel):
    """
    Level 3: Class for FiQuS ConductorAC
    """

    mesh_size_matrix_ratio_inner: Optional[float] = Field(
        default=None,
        description="Mesh size at the matrix center, relative to the filament radius.",
    )
    mesh_size_matrix_ratio_middle: Optional[float] = Field(
        default=None,
        description="Mesh size at the matrix middle partition, relative to the filament radius.",
    )
    mesh_size_matrix_ratio_outer: Optional[float] = Field(
        default=None,
        description="Mesh size at the matrix outer boundary, relative to the filament radius.",
    )
    interpolation_distance_from_filaments_ratio: Optional[float] = Field(
        default=None,
        description="The mesh size is interpolated from the filament boundaries into the matrix, over a given distance. This parameter determines the distance over which the mesh size is interpolated.",
    )
    rate_dependent_scaling_matrix: Optional[bool] = Field(
        default=False,
        description="Rate dependent scaling uses the expected skin depth in the matrix to determine the matrix mesh. If the skin depth is low (i.e. for high frequencies) this feature increases mesh density in the region where the current is expected to flow, while decreasing the mesh resolution in the region where the current is not expected to flow.",
    )
    skindepth_scaling_factor: Optional[float] = Field(
        default=None,
        description="Scaling factor for the estimate of the skin depth, used for rate dependent scaling.",
    )
    desired_elements_in_skindepth: Optional[float] = Field(
        default=None, description="Desired number of elements in the skin depth region. This parameter is used for rate dependent scaling, and determines the number of elements in the region where the current is expected to flow."
    )

# -- Air mesh settings -- #
class CACStrandMeshAir(BaseModel):
    """
    Level 3: Class for FiQuS ConductorAC
    """

    max_mesh_size_ratio: Optional[float] = Field(
        default=None,
        description="Mesh size at the outer boundary of the air region, relative to the filament radius. E.g. 10 means that the mesh size is 10 times the filament radius.",
    )

# -- Strand mesh settings -- #
class CACStrandMesh(BaseModel):
    """
    Level 2: Class for FiQuS ConductorAC
    """

    scaling_global: Optional[float] = Field(
        default=1, description="Global scaling factor for mesh size."
    )
    filaments: CACStrandMeshFilaments = CACStrandMeshFilaments()
    matrix: CACStrandMeshMatrix = CACStrandMeshMatrix()
    air: CACStrandMeshAir = CACStrandMeshAir()


# ============= SOLVE ============= #
# -- General parameters -- #
class CACStrandSolveGeneralparameters(BaseModel):
    """
    Level 3: Class for general parameters
    """
    temperature: float = Field(default=1.9, description="Temperature (K) of the strand.")
    superconductor_linear: Optional[bool] = Field(default=False, description="For debugging: replace LTS by normal conductor.")


# -- Initial conditions -- #
class CACStrandSolveInitialconditions(BaseModel):
    """
    Level 3: Class for initial conditions
    """

    init_from_pos_file: bool = Field(
        default=False, description="This field is used to initialize the solution from a non-zero field solution stored in a .pos file."
    )
    pos_file_to_init_from: Optional[str] = Field(
        default=None,
        description="Name of .pos file for magnetic field (A/m) from which the solution should be initialized."
        " Should be in the Geometry_xxx/Mesh_xxx/ folder in which the Solution_xxx will be saved.",
    )


# -- Source parameters -- #
class CACStrandSolveSourceparametersSineSuperimposedDC(BaseModel):
    """
    Level 5: Class for superimposed DC field or current parameters for the sine source
    """
    field_magnitude: Optional[float] = Field(default=0.0, description="DC field magnitude (T) (direction along y-axis). Solution must be initialized with a non-zero field solution stored in a .pos file if non-zero DC field is used.")
    current_magnitude: Optional[float] = Field(default=0.0, description="DC current magnitude (A). Solution must be initialized with a non-zero field solution stored in a .pos file if non-zero DC current is used.")

class CACStrandSolveSourceparametersSine(BaseModel):
    """
    Level 4: Class for Sine source parameters
    """
    frequency: Optional[float] = Field(default=None, description="Frequency of the sine source (Hz).")
    field_amplitude: Optional[float] = Field(default=None, description="Amplitude of the sine field (T).")
    current_amplitude: Optional[float] = Field(default=None, description="Amplitude of the sine current (A).")
    field_angle: Optional[float] = Field(default=90, description="Angle of the sine field direction, with respect to the x-axis (degrees).")
    superimposed_DC: CACStrandSolveSourceparametersSineSuperimposedDC = CACStrandSolveSourceparametersSineSuperimposedDC()

class CACStrandSolveSourceparametersPiecewise(BaseModel):
    """
    Level 4: Class for piecewise (linear) source parameters
    """
    source_csv_file: Optional[str] = Field(default=None, description="File name for the from_file source type defining the time evolution of current and field (in-phase). Multipliers are used for each of them. The file should contain two columns: 'time' (s) and 'value' (field/current (T/A)), with these headers. If this field is set, times, applied_fields_relative and transport_currents_relative are ignored.")
    times: Optional[List[float]] = Field(default=None, description="Time instants (s) defining the piecewise linear sources. Used only if source_csv_file is not set. Can be scaled by time_multiplier.")
    applied_fields_relative: Optional[List[float]] = Field(default=None, description="Applied fields relative to multiplier applied_field_multiplier at the time instants 'times'. Used only if source_csv_file is not set.")
    transport_currents_relative: Optional[List[float]] = Field(default=None, description="Transport currents relative to multiplier transport_current_multiplier at the time instants 'times'. Used only if source_csv_file is not set.")
    time_multiplier: Optional[float] = Field(default=None, description="Multiplier for the time values in times (scales the time values). Also used for the time values in the source_csv_file.")
    applied_field_multiplier: Optional[float] = Field(default=None, description="Multiplier for the applied fields in applied_fields_relative. Also used for the values in the source_csv_file.")
    transport_current_multiplier: Optional[float] = Field(default=None, description="Multiplier for the transport currents in transport_currents_relative. Also used for the values in the source_csv_file.")

class CACStrandSolveSourceparameters(BaseModel):
    """
    Level 3: Class for material properties
    """

    source_type: Literal['sine', 'piecewise'] = Field(
        default='sine',
        description="Time evolution of applied current and magnetic field. Supported options are: sine, piecewise.",
    )
    boundary_condition_type: str = Field(
        default="Natural",
        description="Boundary condition type. Supported options are: Natural, Essential. Do not use essential boundary condition with induced currents.",
    )
    sine: CACStrandSolveSourceparametersSine = CACStrandSolveSourceparametersSine()
    piecewise: CACStrandSolveSourceparametersPiecewise = CACStrandSolveSourceparametersPiecewise()


# -- Numerical parameters -- #
class CACStrandSolveNumericalparametersSine(BaseModel):
    """ 
    Level 4: Numerical parameters corresponding to the sine source
    """
    timesteps_per_period: Optional[float] = Field(default=None, description="Initial value for number of time steps (-) per period for the sine source. Determines the initial time step size.")
    number_of_periods_to_simulate: Optional[float] = Field(default=None, description="Number of periods (-) to simulate for the sine source.")

class CACStrandSolveNumericalparametersPiecewise(BaseModel):
    """
    Level 4: Numerical parameters corresponding to the piecewise source
    """
    time_to_simulate: Optional[float] = Field(default=None, description="Total time to simulate (s). Used for the piecewise source.")
    timesteps_per_time_to_simulate: Optional[float] = Field(default=None, description="If variable_max_timestep is False. Number of time steps (-) per period for the piecewise source.")
    force_stepping_at_times_piecewise_linear: bool = Field(default=False, description="If True, time-stepping will contain exactly the time instants that are in the times_source_piecewise_linear list (to avoid truncation maximum applied field/current values).")

    variable_max_timestep: bool = Field(default=False, description="If False, the maximum time step is kept constant through the simulation. If True, it varies according to the piecewise definition.")
    times_max_timestep_piecewise_linear: Optional[List[float]] = Field(default=None, description="Time instants (s) defining the piecewise linear maximum time step.")
    max_timestep_piecewise_linear: Optional[List[float]] = Field(default=None, description="Maximum time steps (s) at the times_max_timestep_piecewise_linear. Above the limits, linear extrapolation of the last two values.")

class CACStrandSolveNumericalparameters(BaseModel):
    """
    Level 3: Class for numerical parameters
    """

    sine: CACStrandSolveNumericalparametersSine = CACStrandSolveNumericalparametersSine()
    piecewise: CACStrandSolveNumericalparametersPiecewise = CACStrandSolveNumericalparametersPiecewise()


# -- Formulation parameters -- #
class CACStrandSolveFormulationparameters(BaseModel):
    """
    Level 3: Class for finite element formulation parameters
    """

    formulation: Literal['voltage_based'] = Field(
        default='voltage_based',
        description="Currently, only possible option is voltage_based."
    )
    dynamic_correction: Optional[bool] = Field(
        default=True,
        description="In the voltage_based case, do we activate the dynamic correction?",
    )
    compute_temperature: Optional[bool] = Field(
        default=False, description="Do we compute the temperature?"
    )

    two_ell_periodicity : Optional[bool] = Field(
        default=True, description="True to integrate over twice the shortest periodicity length, False to integrate over the shortest periodicity length. "
    )

class CACStrandSolveDiffusionBarriers(BaseModel):
    enable: Optional[bool] = Field(
        default=False, description="Set True to enable diffusion barriers."
    )

    load_data_from_yaml: Optional[bool] = Field(
        default=False, description="Set True to load the diffusion barrier data from the input YAML-file. Otherwise, the thickness and resistivity specified in this file are used."
    )

    resistivity: Optional[float] = Field(
        default=1e-6, description="Resistivity of the diffusion barriers (Ohm*m)."
    )
    thickness: Optional[float] = Field(
        default=1e-6, description="Thickness of the diffusion barriers (m)."
    )

class CACStrandSolve(BaseModel):
    """
    Level 2: Class for FiQuS ConductorAC Strand solver settings
    """
    pro_template: Optional[Literal['ConductorAC_template.pro']] = Field(
        default='ConductorAC_template.pro',
        description="Name of the .pro template file."
    )
    conductor_name: Optional[str] = Field(
        default=None, description="Name of the conductor. Must match a conductor name in the conductors section of the input YAML-file."
    )
    formulation_parameters: CACStrandSolveFormulationparameters = (
        CACStrandSolveFormulationparameters()
    )
    general_parameters: CACStrandSolveGeneralparameters = (
        CACStrandSolveGeneralparameters()
    )
    initial_conditions: CACStrandSolveInitialconditions = (
        CACStrandSolveInitialconditions()
    )
    diffusion_barriers: CACStrandSolveDiffusionBarriers = (
        CACStrandSolveDiffusionBarriers()
    )
    source_parameters: CACStrandSolveSourceparameters = (
        CACStrandSolveSourceparameters()
    )
    numerical_parameters: CACStrandSolveNumericalparameters = (
        CACStrandSolveNumericalparameters()
    )


# ============= POSTPROC ============= #
class CACStrandPostprocBatchpostprocLossMapCrossSection(BaseModel):
    """
    Level 5: Class with settings for plotting a cross-section of the loss map.
    """
    plot_cross_section: bool = Field(
        default=False, description="Set True to plot a cross-section of the loss map."
    )
    save_plot: bool = Field(default=False, description="Set True to save the plot.")
    filename: str = Field(default="cross_section", description="Name of the plot file.")
    axis_to_cut: str = Field(
        default="x", description="Axis to cut for the cross-section."
    )
    cut_value: float = Field(
        default=0, description="Value of the axis to cut for the cross-section."
    )

    ylabel: str = Field(default="Loss", description="Label of the y-axis.")
    title: Optional[str] = Field(
        default=None,
        description="Title of the plot. The placeholder <<cut_value>> can be used to indicate the value of the cut axis.",
    )


class CACStrandPostprocBatchpostprocLossMapCrossSectionSweep(BaseModel):
    """
    Level 5: Class with settings for animating a cross-section sweep of the loss map along one axis.
    """
    animate_cross_section_sweep: bool = Field(
        default=False,
        description="Set True to animate a cross-section sweep of the loss map along one axis.",
    )
    save_plot: bool = Field(
        default=False, description="Set True to save the animation."
    )
    filename: str = Field(
        default="crossSectionSweep", description="Name of the animation file."
    )
    axis_to_sweep: str = Field(
        default="x", description="Axis to sweep for the animation."
    )
    ylabel: str = Field(default="Loss", description="Label of the y-axis.")
    title: Optional[str] = Field(
        default=None,
        description="Title of the plot. Use <<sweep_value>> to indicate the value of the sweep axis.",
    )


class CACStrandPostprocBatchpostprocLossMap(BaseModel):
    """
    Level 4: Class with settings for generating loss maps
    """
    produce_loss_map: bool = Field(
        default=False, description="Set True to produce a loss map."
    )
    save_plot: bool = Field(default=False, description="Set True to save the plot.")
    filename: str = Field(default="loss_map", description="Name of the plot file.")
    x_val: Optional[str] = Field(
        default=None, description="Parameter to be plotted on the x-axis. This field corresponds to a parameter in the input YAML-file. E.g. 'solve.source_parameters.sine.frequency' will plot the loss map for different frequencies."
    )
    y_val: Optional[str] = Field(
        default=None, description="Parameter to be plotted on the y-axis. This field corresponds to a parameter in the input YAML-file. E.g. 'solve.source_parameters.sine.field_amplitude' will plot the loss map for different applied field amplitudes."
    )
    x_steps: int = Field(default=20, description="Number of steps on the x-axis.")
    y_steps: int = Field(default=20, description="Number of steps on the y-axis.")
    loss_type: Literal['TotalLoss', 'FilamentLoss', 'CouplingLoss', 'EddyLoss'] = Field(
        default='TotalLoss',
        description="Type of loss to be plotted. Supported options are: TotalLoss, FilamentLoss, CouplingLoss, EddyLoss."
    )
    x_log: bool = Field(
        default=True, description="Set True to plot x-axis in log-scale."
    )
    y_log: bool = Field(
        default=True, description="Set True to plot y-axis in log-scale."
    )
    loss_log: bool = Field(
        default=True, description="Set True to plot loss in log-scale."
    )
    x_norm: float = Field(default=1, description="Normalization factor for x-axis.")
    y_norm: float = Field(default=1, description="Normalization factor for y-axis.")
    loss_norm: float = Field(default=1, description="Normalization factor for the AC-loss.")
    show_datapoints: bool = Field(
        default=True, description="Set True to show markers for all the datapoints in the loss map."
    )

    title: Optional[str] = Field(default=None, description="Title for the plot.")
    xlabel: Optional[str] = Field(default=None, description="Label for the x-axis.")
    ylabel: Optional[str] = Field(default=None, description="Label for the y-axis.")

    # lossType_dominance_contour: CACStrandPostprocBatchpostprocLossMapDominanceCountour = (
    #     CACStrandPostprocBatchpostprocLossMapDominanceCountour()
    # )

    show_loss_type_dominance_contour: bool = Field(
        default=False,
        description="Set True to plot a contour curve separating regions where different loss types dominate. ",
    )

    cross_section: CACStrandPostprocBatchpostprocLossMapCrossSection = (
        CACStrandPostprocBatchpostprocLossMapCrossSection()
    )
    cross_section_sweep: CACStrandPostprocBatchpostprocLossMapCrossSectionSweep = (
        CACStrandPostprocBatchpostprocLossMapCrossSectionSweep()
    )


class CACStrandPostprocBatchpostprocPlot2d(BaseModel):
    """
    Level 4: Class for 2D plot settings
    """
    produce_plot2d: bool = Field(
        default=False, description="Set True to produce a 2D plot."
    )
    combined_plot: bool = Field(
        default=False,
        description="Set True to produce a combined plot for all simulations. If False, a separate plot is produced for each simulation.",
    )
    save_plot: bool = Field(default=False, description="Set True to save the plot.")
    filename: str = Field(default="plot2d", description="Name of the plot file.")
    x_val: Optional[str] = Field(
        default=None, description="Value to be plotted on the x-axis. Parameters in the input YAML-file and class-variables from the plotter 'SimulationData' class can be accessed trough the notation << . >>. E.g. '<<solve.source_parameters.sine.frequency>>' will create a 2D plot with frequency on the x-axis. '<<time>>' will create a plot with time on the x-axis."
    )
    y_vals: Optional[List[str]] = Field(
        default=None, description=" List of values to be plotted on the y-axis. Parameters in the input YAML-file and class-variables from the plotter 'SimulationData' class can be accessed trough the notation << . >>. E.g. total AC-loss per cycle can be accessed as ['<<total_power_per_cycle['TotalLoss_dyn']>>']."
    )
    labels: Optional[List[str]] = Field(
        default=None,
        description="List of labels for the plot. Each label corresponding to a value in y_val.",
    )
    linestyle: Optional[str] = Field(
        default=None, description="Linestyle for the plot."
    )

    title: Optional[str] = Field(default=None, description="Title for the plot.")
    xlabel: Optional[str] = Field(default=None, description="Label for the x-axis.")
    ylabel: Optional[str] = Field(default=None, description="Label for the y-axis.")
    x_log: bool = Field(default=False, description="Set True to plot x-axis in log-scale.")
    y_log: bool = Field(default=False, description="Set True to plot y-axis in log-scale.")
    legend: bool = Field(default=True, description="Set True to show legend.")


class CACStrandPostprocBatchpostprocFilter(BaseModel):
    """
    Level 4: Field for filtering simulations based on simulation parameters for batch post-processing
    """
    apply_filter: bool = Field(
        default=False,
        description="Set True to filter simulations by parameters from the input YAML-file.",
    )
    filter_criterion: Optional[str] = Field(
        default=None,
        description="Criterion used to filter simulations based on simulation parameters. For example will '<<solve.source_parameters.sine.frequency>> > 100' disregard simulations done with frequencies lower than 100Hz.",
    )


class CACStrandPostprocBatchpostprocSort(BaseModel):
    """
    Level 4: Field for sorting simulations based on simulation parameters for batch post-processing
    """
    apply_sort: bool = Field(default=False, description="Set True to sort simulations.")
    sort_key: Optional[str] = Field(
        default=None,
        description="Criterion used to sort simulations based on simulation parameters. For example will 'sd.total_power_per_cycle['TotalLoss'] sort simulations based on the total loss.",
    )


class CACStrandPostprocBatchpostproc(BaseModel):
    """
    Level 3: Class for batch post-processing settings
    """
    postProc_csv: Optional[str] = Field(
        default=None,
        description="Name of the .csv file for post-processing (without file extension). This file specifies the simulations to be post-processed. The file is structured into three columns, specifying the folder names to access the simulation results: 'input.run.geometry', 'input.run.mesh' and 'input.run.solve'. Each row corresponds to a simulation to be post-processed.",
    )
    output_folder: Optional[str] = Field(
        default=None,
        description="Batch post-processing creates a folder with the given name in the output directory, where all the plots are saved.",
    )
    filter: CACStrandPostprocBatchpostprocFilter = CACStrandPostprocBatchpostprocFilter()
    sort: CACStrandPostprocBatchpostprocSort = CACStrandPostprocBatchpostprocSort()
    loss_map: CACStrandPostprocBatchpostprocLossMap = CACStrandPostprocBatchpostprocLossMap()
    plot2d: CACStrandPostprocBatchpostprocPlot2d = CACStrandPostprocBatchpostprocPlot2d()


class CACStrandPostprocPlotInstPower(BaseModel):
    """
    Level 3: Class with settings for generating plots of instantaneous power
    """
    show: bool = Field(default=False, description="Creates a plot for the calculated instantaneous AC loss (W/m) as a function of time (s).")
    title: str = Field(default="Instantaneous Power", description="Title for the plot.")
    save: bool = Field(default=False, description="Set True to save the plot.")
    save_file_name: str = Field(
        default="instantaneous_power", description="Name of the plot file."
    )


class CACStrandPostprocCleanup(BaseModel):
    """
    Level 3: Class for cleanup settings
    """
    remove_pre_file: bool = Field(
        default=False,
        description="Set True to remove the .pre-file after post-processing, to save disk space.",
    )
    remove_res_file: bool = Field(
        default=False,
        description="Set True to remove the .res-file after post-processing, to save disk space.",
    )
    remove_msh_file: bool = Field(
        default=False,
        description="Set True to remove the .msh-file after post-processing, to save disk space.",
    )


class CACStrandPostproc(BaseModel):
    """
    Level 2: Class for FiQuS ConductorAC
    """

    generate_pos_files: bool = Field(
        default=True,
        description="Set True to generate .pos-files during post-processing",
    )
    plot_instantaneous_power: CACStrandPostprocPlotInstPower = (
        CACStrandPostprocPlotInstPower()
    )
    compute_current_per_filament: bool = Field(
        default=False,
        description="Computes current in every filament, with decomposition into magnetization and transport current.",
    )
    save_last_current_density: Optional[str] = Field(
        default=None,
        description="Saves the last current density field solution (out-of-plane) in the file given as a string."
        " The '.pos' extension will be appended to it. Nothing is done if None."
        " This can be for using the current density as an initial condition (but not implemented yet).",
    )
    save_last_magnetic_field: Optional[str] = Field(
        default=None,
        description="Saves the last magnetic field solution (in-plane) in the file given as a string."
        " The '.pos' extension will be appended to it. Nothing is done if None."
        " This is for using the magnetic field as an initial condition for another resolution.",
    )
    cleanup: CACStrandPostprocCleanup = CACStrandPostprocCleanup()
    batch_postproc: CACStrandPostprocBatchpostproc = CACStrandPostprocBatchpostproc()

# ============= BASE ============= #
class CACStrand(BaseModel):
    """
    Level 1: Class for FiQuS ConductorAC
    """

    type: Literal["CACStrand"]
    geometry: CACStrandGeometry = CACStrandGeometry()
    mesh: CACStrandMesh = CACStrandMesh()
    solve: CACStrandSolve = CACStrandSolve()
    postproc: CACStrandPostproc = CACStrandPostproc()
    
