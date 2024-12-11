# Appendix G Performance

This recipe generates a baseline Honeybee Model from the input Model, which is
consistent with ASHRAE 90.1 Appendix G 2016 (and later), This includes adjusting
the geometry, constructions, lighting, HVAC, SHW, and removing any clearly-defined
energy conservation measures like daylight controls.

Note that all schedules are essentially unchanged in the baseline model, meaning
that additional post-processing of setpoints may be necessary to account for
energy conservation strategies like expanded comfort ranges, ceiling fans, and
personal thermal comfort devices. It may also be necessary to adjust hot water
loads loads in cases where low-flow fixtures are implemented.

After the creation of the baseline model, this recipe will simulate it in
EnergyPlus, performing 4 separate simulations in parallel for each of the 4
cardinal directions per the Appendix G specification. Alongside these baseline
simulations, the input Model will be simulated to get the energy performance
of the proposed building. At the end, all energy use results will be
post-processed along with the energy costs inputs to estimate the Appendix G
PCI. An additional computation will also be run to estimate the number of
LEED "Optimize Energy Performance" points for LEED v4.

The recipe outputs a file called `appendix_g_summary.json`, which contains the PCI
improvement for the latest versions of ASHRAE 90.1 in the format below:

```json
{
    "proposed_eui": 112.866,
    "proposed_energy": 3517144.444,
    "proposed_cost": 703428.89,
    "baseline_eui": 235.3,
    "baseline_energy": 7332474.306,
    "baseline_cost": 1214797.19,
    "pci_t_2016": 0.666,
    "pci_t_2019": 0.591,
    "pci_t_2022": 0.574,
    "pci": 0.579,
    "pci_improvement_2016": 13.055,
    "pci_improvement_2019": 2.0219,
    "pci_improvement_2022": -0.880
}
```

The recipe also outputs a file called `leed_summary.json`, which contains the
ASHRAE 90.1-2016 PCI for both cost and carbon (GHG) emissions in the format below:

```json
{
  "proposed_eui": 112.866,
  "proposed_cost": 703428.89,
  "proposed_carbon": 464263.067,
  "baseline_eui": 235.3,
  "baseline_cost": 1214797.19,
  "baseline_carbon": 1577657.766,
  "pci": 0.579,
  "pci_target": 0.666,
  "pci_improvement": 13.055,
  "carbon": 0.294,
  "carbon_target": 0.633,
  "carbon_improvement": 53.511,
  "leed_points": 9
}
```
