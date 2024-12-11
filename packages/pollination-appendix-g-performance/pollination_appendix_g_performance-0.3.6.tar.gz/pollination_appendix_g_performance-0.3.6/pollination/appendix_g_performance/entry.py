from pollination_dsl.dag import Inputs, task, Outputs, DAG
from dataclasses import dataclass
from typing import Dict, List
from pollination.honeybee_energy.baseline import ModelToBaseline, \
    AppendixGSummary, LeedV4Summary
from pollination.honeybee_energy.settings import SimParDefault, \
    BaselineOrientationSimPars
from pollination.honeybee_energy.simulate import SimulateModel

# input/output alias
from pollination.alias.inputs.model import hbjson_model_hvac_input
from pollination.alias.inputs.ddy import ddy_input
from pollination.alias.inputs.north import north_input
from pollination.alias.inputs.baseline import climate_zone_input, \
    building_type_input, energy_costs_input
from pollination.alias.inputs.emissions import electricity_emissions_input
from pollination.alias.inputs.bool_options import bldg_lighting_input
from pollination.alias.inputs.simulation import proposed_standard_input
from pollination.alias.outputs.summary import parse_appendix_g_summary, \
    parse_leed_summary, load_baseline_sqls


@dataclass
class AppendixGPerformanceEntryPoint(DAG):
    """Appendix G Performance entry point."""

    # inputs
    model = Inputs.file(
        description='An energy Model as either a HBJSON or HBPkl file.',
        extensions=['hbjson', 'json', 'hbpkl', 'pkl'],
        alias=hbjson_model_hvac_input
    )

    epw = Inputs.file(
        description='EPW weather file to be used for the annual energy simulation.',
        extensions=['epw']
    )

    ddy = Inputs.file(
        description='A DDY file with design days to be used for the initial '
        'sizing calculation.', extensions=['ddy'],
        alias=ddy_input
    )

    climate_zone = Inputs.str(
        description='Text indicating the ASHRAE climate zone. This can be a single '
        'integer (in which case it is interpreted as A) or it can include the '
        'A, B, or C qualifier (eg. 3C).',
        spec={
            'type': 'string',
            'enum': [
                '0', '1', '2', '3', '4', '5', '6', '7', '8',
                '0A', '1A', '2A', '3A', '4A', '5A', '6A',
                '0B', '1B', '2B', '3B', '4B', '5B', '6B',
                '3C', '4C', '5C'
            ]
        },
        alias=climate_zone_input
    )

    building_type = Inputs.str(
        description='Text for the building type that the Model represents. This is used '
        'to determine the baseline window-to-wall ratio and HVAC system. The '
        'following have specified systems per the standard: '
        'Residential, NonResidential, MidriseApartment, HighriseApartment, LargeOffice, '
        'MediumOffice, SmallOffice, Retail, StripMall, PrimarySchool, SecondarySchool, '
        'SmallHotel, LargeHotel, Hospital, Outpatient, Warehouse, SuperMarket, '
        'FullServiceRestaurant, QuickServiceRestaurant, Laboratory, Courthouse',
        spec={
            'type': 'string',
            'enum': [
                'Residential', 'NonResidential',
                'MidriseApartment', 'HighriseApartment',
                'LargeOffice', 'MediumOffice', 'SmallOffice',
                'Retail', 'StripMall',
                'PrimarySchool', 'SecondarySchool',
                'SmallHotel', 'LargeHotel',
                'Hospital', 'Outpatient',
                'Warehouse', 'SuperMarket',
                'FullServiceRestaurant', 'QuickServiceRestaurant',
                'Laboratory', 'Courthouse'
            ]
        },
        alias=building_type_input
    )

    north = Inputs.float(
        default=0,
        description='A a number between -360 and 360 for the counterclockwise '
        'difference between the North and the positive Y-axis in degrees.',
        spec={'type': 'number', 'minimum': -360, 'maximum': 360},
        alias=north_input
    )

    energy_costs = Inputs.str(
        description='A string of energy cost parameters to customize the cost '
        'assumptions used to calculate the Performance Cost Index (PCI). Note that '
        'not all of the energy sources need to be specified for this input to be valid. '
        'For example, if the input model contains no district heating or cooling, '
        'something like the following would be acceptable: --electricity-cost 0.20 '
        '--natural-gas-cost 0.09',
        default='--electricity-cost 0.12 --natural-gas-cost 0.06 '
        '--district-cooling-cost 0.04 --district-heating-cost 0.08',
        alias=energy_costs_input,
        spec={
            'type': 'string',
            'pattern': '(?:\s|^)(?:(--electricity-cost|--district-cooling-cost|' \
                '--district-heating-cost|--natural-gas-cost)\s+([0-9]+\.[0-9]+))' \
                '(?=(?:\s|$|\1))'
        }
    )

    electricity_emissions = Inputs.float(
        description='A number for the electric grid carbon emissions'
        'in kg CO2 per MWh. For locations in the USA, this can be obtained '
        'from he honeybee_energy.result.emissions future_electricity_emissions '
        'method. For locations outside of the USA where specific data is unavailable, '
        'the following rules of thumb may be used as a guide. (Default: 400).\n'
        '800 kg/MWh - for an inefficient coal or oil-dominated grid\n'
        '400 kg/MWh - for the US (energy mixed) grid around 2020\n'
        '100-200 kg/MWh - for grids with majority renewable/nuclear composition\n'
        '0-100 kg/MWh - for grids with nuclear or renewables and storage',
        default=400, alias=electricity_emissions_input
    )

    floor_area = Inputs.float(
        description='A number for the floor area of the building that the model '
        'is a part of in m2. Setting this value is useful when the input model '
        'represents a portion of the full building so it is necessary to explicitly '
        'specify the full floor area to ensure the correct baseline HVAC system is '
        'selected. If unspecified or 0, the model floor area will be used.', default=0
    )

    story_count = Inputs.int(
        description='An integer for the number of stories of the building that the '
        'model is a part of. Setting this value is useful when the input model '
        'represents a portion of the full building so it is necessary to explicitly '
        'specify the total story count to ensure the correct baseline HVAC system is '
        'selected. If unspecified or 0, the model stories will be used.', default=0,
        spec={'type': 'integer', 'minimum': 0}
    )

    lighting_method = Inputs.str(
        description='A switch to note whether the building-type should be used to '
        'assign the baseline lighting power density, which will use the same value '
        'for all Rooms in the model, or a space-by-space method should be used. '
        'To use the space-by-space method, the model should either be built '
        'with the programs that ship with Ladybug Tools in honeybee-energy-standards '
        'or the baseline_watts_per_area should be correctly '
        'assigned for all Rooms.', default='space',
        spec={'type': 'string', 'enum': ['space', 'building']},
        alias=bldg_lighting_input
    )

    proposed_efficiency_standard = Inputs.str(
        description='Text to set the efficiency standard to be used for the proposed '
        'building. When specified, this will automatically override the efficiencies '
        'of all HVAC equipment for the proposed standard. Note that providing a '
        'standard here will cause the OpenStudio translation process to perform an '
        'additional sizing calculation with EnergyPlus, which is needed since the '
        'default efficiencies of equipment vary depending on their size. Choose from '
        'the following: DOE_Ref_Pre_1980, DOE_Ref_1980_2004, ASHRAE_2004, ASHRAE_2007, '
        'ASHRAE_2010, ASHRAE_2013, ASHRAE_2016, ASHRAE_2019', default='',
        alias=proposed_standard_input
    )

    # tasks
    @task(template=ModelToBaseline)
    def model_to_baseline(
        self, model=model, climate_zone=climate_zone, building_type=building_type,
        floor_area=floor_area, story_count=story_count, lighting_method=lighting_method
    ) -> List[Dict]:
        return [
            {
                'from': ModelToBaseline()._outputs.baseline_model,
                'to': 'baseline_model.hbjson'
            }
        ]

    @task(template=BaselineOrientationSimPars)
    def create_sim_par(
        self, ddy=ddy, north=north, reporting_frequency='Monthly',
        climate_zone=climate_zone, building_type=building_type,
        efficiency_standard='ASHRAE_2004'
    ) -> List[Dict]:
        return [
            {
                'from': BaselineOrientationSimPars()._outputs.output_folder,
                'to': 'sim_par'
            },
            {
                'from': BaselineOrientationSimPars()._outputs.sim_par_list,
                'description': 'Simulation parameter information.'
            }
        ]

    @task(template=SimParDefault)
    def create_proposed_sim_par(
        self, ddy=ddy, north=north, reporting_frequency='Monthly',
        climate_zone=climate_zone, building_type=building_type,
        efficiency_standard=proposed_efficiency_standard
    ) -> List[Dict]:
        return [
            {
                'from': SimParDefault()._outputs.sim_par_json,
                'to': 'proposed_sim_par.json'
            }
        ]

    @task(template=SimulateModel, needs=[create_proposed_sim_par])
    def run_proposed_simulation(
        self, model=model, epw=epw,
        sim_par=create_proposed_sim_par._outputs.sim_par_json,
    ) -> List[Dict]:
        return [
            {'from': SimulateModel()._outputs.hbjson, 'to': 'proposed_model.hbjson'},
            {'from': SimulateModel()._outputs.result_folder, 'to': 'proposed_run'}
        ]

    @task(
        template=SimulateModel,
        needs=[model_to_baseline, create_sim_par],
        loop=create_sim_par._outputs.sim_par_list,
        sub_folder='baseline_run',  # create a subfolder for the simulations
        sub_paths={'sim_par': '{{item.path}}'}  # sub_path for sim_par arg
    )
    def run_baseline_simulations(
        self, model=model_to_baseline._outputs.baseline_model, epw=epw,
        sim_par=create_sim_par._outputs.output_folder
    ) -> List[Dict]:
        return [
            {'from': SimulateModel()._outputs.sql, 'to': '{{item.id}}.sql'}
        ]

    @task(
        template=AppendixGSummary,
        needs=[run_proposed_simulation, run_baseline_simulations]
    )
    def compute_appendix_g_summary(
        self, proposed_result='proposed_run/eplusout.sql',
        baseline_result_folder='baseline_run',
        climate_zone=climate_zone, building_type=building_type,
        energy_costs=energy_costs
    ) -> List[Dict]:
        return [
            {
                'from': AppendixGSummary()._outputs.summary_json,
                'to': 'appendix_g_summary.json'
            }
        ]

    @task(
        template=LeedV4Summary,
        needs=[run_proposed_simulation, run_baseline_simulations]
    )
    def compute_leed_v4_summary(
        self, proposed_result='proposed_run/eplusout.sql',
        baseline_result_folder='baseline_run',
        climate_zone=climate_zone, building_type=building_type,
        energy_costs=energy_costs, electricity_emissions=electricity_emissions
    ) -> List[Dict]:
        return [
            {
                'from': LeedV4Summary()._outputs.summary_json,
                'to': 'leed_summary.json'
            }
        ]

    # outputs
    appendix_g_summary = Outputs.file(
        source='appendix_g_summary.json',
        description='A JSON object with the following keys - proposed_eui, '
        'proposed_energy, proposed_cost, baseline_eui, baseline_energy, baseline_cost, '
        'pci_t_2016, pci_t_2019, pci_t_2022, pci, pci_improvement_2016, '
        'pci_improvement_2019, pci_improvement_2022. All energy and energy intensity '
        'values are in kWh or kWh/m2. All PCI values are fractional and all '
        '"improvement" values are in percent (from 0 to 100).',
        alias=parse_appendix_g_summary
    )

    leed_summary = Outputs.file(
        source='leed_summary.json',
        description='A JSON object with the following keys - proposed_eui, '
        'proposed_cost, proposed_carbon, baseline_eui, baseline_cost, baseline_carbon, '
        'pci_target, pci, pci_improvement, carbon_target, pci_carbon '
        'carbon_improvement, leed_points. All energy and energy intensity '
        'values are in kWh or kWh/m2. All carbon emission values are in kg CO2. '
        'All PCI values are fractional and all "improvement" values are in percent '
        '(from 0 to 100). LEED points are reported from 0 to (16, 18, 20) '
        'depending on the input building_type.',
        alias=parse_leed_summary
    )

    proposed_sql = Outputs.file(
        source='proposed_run/eplusout.sql',
        description='The result SQL file output by the proposed simulation.'
    )

    baseline_sqls = Outputs.folder(
        source='baseline_run',
        description='Folder containing all result SQL files output by the baseline '
        'simulations. There should be one SQL for each of the 4 building orientations.',
        alias=load_baseline_sqls
    )

    baseline_model = Outputs.file(
        source='baseline_model.hbjson',
        description='Path to a HBJSON file representing the baseline building.'
    )
