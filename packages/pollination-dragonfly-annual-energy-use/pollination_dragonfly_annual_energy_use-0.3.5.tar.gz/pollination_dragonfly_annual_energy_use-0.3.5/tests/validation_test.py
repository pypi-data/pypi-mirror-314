from pollination.dragonfly_annual_energy_use.entry import \
    DragonflyAnnualEnergyUseEntryPoint
from queenbee.recipe.dag import DAG


def test_dragonfly_annual_energy_use():
    recipe = DragonflyAnnualEnergyUseEntryPoint().queenbee
    assert recipe.name == 'dragonfly-annual-energy-use-entry-point'
    assert isinstance(recipe, DAG)
