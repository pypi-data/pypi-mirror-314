from pollination_dsl.dag import Inputs, DAG, task, Outputs
from dataclasses import dataclass
from typing import Dict, List
from pollination.dragonfly_energy.translate import ModelToHoneybee
from pollination.honeybee_energy.simulate import SimulateModel
from pollination.honeybee_energy.result import EnergyUseIntensity

# input/output alias
from pollination.alias.inputs.model import dfjson_model_input
from pollination.alias.inputs.ddy import ddy_input
from pollination.alias.inputs.bool_options import use_multiplier_input
from pollination.alias.inputs.simulation import energy_simulation_parameter_input, \
    measures_input, idf_additional_strings_input
from pollination.alias.outputs.eui import parse_eui_results


@dataclass
class DragonflyAnnualEnergyUseEntryPoint(DAG):
    """Dragonfly annual energy use entry point."""

    # inputs
    model = Inputs.file(
        description='A Dragonfly model in DFJSON file format.',
        extensions=['json', 'dfjson'],
        alias=dfjson_model_input
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

    sim_par = Inputs.file(
        description='SimulationParameter JSON that describes the settings for the '
        'simulation.', path='sim-par.json', extensions=['json'], optional=True,
        alias=energy_simulation_parameter_input
    )

    measures = Inputs.folder(
        description='A folder containing an OSW JSON be used as the base for the '
        'execution of the OpenStuduo CLI. This folder must also contain all of the '
        'measures that are referenced within the OSW.', path='measures', optional=True,
        alias=measures_input
    )

    additional_string = Inputs.str(
        description='An additional text string to be appended to the IDF before '
        'simulation. The input should include complete EnergyPlus objects as a '
        'single string following the IDF format. This input can be used to include '
        'EnergyPlus objects that are not currently supported by honeybee.', default='',
        alias=idf_additional_strings_input
    )

    obj_per_model = Inputs.str(
        description='Text to describe how the input Model should be divided for '
        'parallel simulation. Choose from: District, Building, Story.', default='Story',
        spec={'type': 'string', 'enum': ['District', 'Building', 'Story']}
    )

    use_multiplier = Inputs.str(
        description='A switch to note whether the multipliers on each Building story '
        'should be passed along to the generated Honeybee Room objects or if full '
        'geometry objects should be written for each story of each dragonfly building.',
        default='full-geometry',
        spec={'type': 'string', 'enum': ['full-geometry', 'multiplier']},
        alias=use_multiplier_input
    )

    shade_dist = Inputs.str(
        description='A number to note the distance beyond which other buildings shade '
        'should be excluded from a given Honeybee Model. This can include the units of '
        'the distance (eg. 100ft) or, if no units are provided, the value will be '
        'interpreted in the dragonfly model units. If 0, shade from all neighboring '
        'buildings will be excluded from the resulting models.', default='50m'
    )

    units = Inputs.str(
        description='A switch to indicate whether the data in the final EUI file '
        'should be in SI (kWh/m2) or IP (kBtu/ft2). Valid values are "si" and "ip".',
        default='si', spec={'type': 'string', 'enum': ['si', 'ip']}
    )

    # tasks
    @task(template=ModelToHoneybee)
    def convert_to_honeybee(
        self, model=model, obj_per_model=obj_per_model,
        use_multiplier=use_multiplier, shade_dist=shade_dist
    ) -> List[Dict]:
        return [
            {
                'from': ModelToHoneybee()._outputs.output_folder,
                'to': 'models'
            },
            {
                'from': ModelToHoneybee()._outputs.hbjson_list,
                'description': 'Information about exported HBJSONs.'
            }
        ]

    @task(
        template=SimulateModel,
        needs=[convert_to_honeybee],
        loop=convert_to_honeybee._outputs.hbjson_list,
        sub_folder='results',  # create a subfolder for results
        sub_paths={'model': '{{item.path}}'}  # sub_path for sim_par arg
    )
    def run_simulation(
        self, model=convert_to_honeybee._outputs.output_folder, epw=epw, ddy=ddy,
        sim_par=sim_par, measures=measures, additional_string=additional_string
    ) -> List[Dict]:
        return [
            {'from': SimulateModel()._outputs.sql, 'to': 'sql/{{item.id}}.sql'},
            {'from': SimulateModel()._outputs.zsz, 'to': 'zsz/{{item.id}}_zsz.csv'},
            {'from': SimulateModel()._outputs.html, 'to': 'html/{{item.id}}.htm'},
            {'from': SimulateModel()._outputs.err, 'to': 'err/{{item.id}}.err'}
        ]

    @task(template=EnergyUseIntensity, needs=[run_simulation])
    def compute_eui(
        self, result_folder='results/sql', units=units
    ) -> List[Dict]:
        return [
            {'from': EnergyUseIntensity()._outputs.eui_json,
             'to': 'eui.json'}
        ]

    # outputs
    eui = Outputs.file(
        source='eui.json', description='A JSON containing energy use intensity '
        'information across the total model floor area. Values are either kWh/m2 '
        'or kBtu/ft2 depending upon the units input.',
        alias=parse_eui_results
    )

    hbjson = Outputs.folder(
        source='models',
        description='Folder containing the HBJSON models used for simulation.'
    )

    sql = Outputs.folder(
        source='results/sql',
        description='Folder containing the result SQL files output by the simulation.'
    )

    zsz = Outputs.folder(
        source='results/zsz', description='Folder containing the CSV files with '
        'the zone loads over the design day.', optional=True
    )

    html = Outputs.folder(
        source='results/html',
        description='Folder containing the result HTML pages with summary reports.'
    )

    err = Outputs.folder(
        source='results/err',
        description='Folder containing the error reports output by the simulation.'
    )
