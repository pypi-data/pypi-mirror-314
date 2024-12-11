from pollination.appendix_g_performance.entry import AppendixGPerformanceEntryPoint
from queenbee.recipe.dag import DAG


def test_appendix_g_performance():
    recipe = AppendixGPerformanceEntryPoint().queenbee
    assert recipe.name == 'appendix-g-performance-entry-point'
    assert isinstance(recipe, DAG)
