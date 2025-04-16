# SynthBench
A synthetic hypothesis testing environment for testing synthesizability filters.

## Filters
Two set of filters have been implemented. The filters are in the <b>Filters</b> directory.
1. stoichiometry_filters.py: Filters a list of novel materials based on whether their stoichiometries have been previously seen in literature.
2. isovalent_generator.py: generates materials using isovalent substituition rules.
3. utils.py: contains various utlity functions used for finding icsd matches, saving the data, plotting etc.


## Run
1. To run the <b>stoichiometry filter</b> use  <b>Test_Bench_Stoichiometry_filter.ipnyb</b>
2. To run the <b>isovalent substitution filter</b> use  <b>Test_Bench_isovalent_generator.ipynb</b>


## Materials
Different materials file is provided in the <b>Materials</b> directory.
1. 'extracted_table.csv': is the database the codebase uses for refering to charge state, ionic radii and coordination number of various elements in the periodic table. The list is prepared by extracting data from this webpage : http://abulafia.mt.ic.ac.uk/shannon/radius.php
2. 'icsd_materials.csv': is the database of all materials in ICSD as obtained from materials project database on June 9, 2022.
3. '03172025_ternary_perovskites_inspired_materials.csv': is the database of novel ternary perovskite inspired materials that are used to test the stoichiometry filter and is generated using the legacy code https://github.com/PV-Lab/Synthesizability-Filter

## Results
The results generated from running the *.ipnyb notebooks are stored in the <b>Results</b> directory.


## Packages
1. python == 3.12.0
2. matplotlib == 3.10.0
3. pandas == 2.2.3

