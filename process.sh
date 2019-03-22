#!/bin/bash

set -e
for i in {00..15}
do
  python process.py --filename LA_TRANSITION_ECOLOGIQUE.csv --prefix ECO --q_id $i --limit 10000 > logECO$i.txt
done

for i in {00..7}
do
  python process.py --filename LA_FISCALITE_ET_LES_DEPENSES_PUBLIQUES.csv --prefix FIS --q_id $i --limit 10000 > logFIS$i.txt
done

for i in {00..36}
do
  python process.py --filename DEMOCRATIE_ET_CITOYENNETE.csv  --prefix DEM --q_id $i --limit 10000 > logDEM$i.txt
done

for i in {00..32}
do
  python process.py --filename ORGANISATION_DE_LETAT_ET_DES_SERVICES_PUBLICS.csv  --prefix ORG --q_id $i --limit 10000 > logORG$i.txt
done




