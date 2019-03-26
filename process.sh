#!/bin/bash

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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




