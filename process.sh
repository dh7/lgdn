#!/bin/bash
for i in {0..15}
do
  python process.py --filename LA_TRANSITION_ECOLOGIQUE.csv --prefix ECO --q_id $i --limit 10000
done

for i in {0..7}
do
  python process.py --filename LA_FISCALITE_ET_LES_DEPENSES_PUBLIQUES.csv --prefix FIS --q_id $i --limit 10000
done

for i in {0..36}
do
  python process.py --filename DEMOCRATIE_ET_CITOYENNETE.csv  --prefix DEM --q_id $i --limit 10000
done

for i in {0..32}
do
  python process.py --filename ORGANISATION_DE_LETAT_ET_DES_SERVICES_PUBLICS.csv  --prefix ORG --q_id $i --limit 10000
done




