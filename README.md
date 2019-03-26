# lgdn-dataviz

## Le Grand Débat National
[le Grand Débat National](https://www.gouvernement.fr/le-grand-debat-national) is a major national debate on four themes that cover major issues of the french nation: taxation and public spending, state organization of public services, ecological transition , democracy and citizenship.

## Open Data
All the open data from the consultation are available [here](https://www.data.gouv.fr/en/datasets/donnees-ouvertes-du-grand-debat-national/#_) and also from an API [there](https://granddebat.fr/developer).

## Dataviz
The goal of this project is to make a simple dataviz to display all the questions and answers from the public.

## The code
* **download.sh** is a bash script to download the data from the open data website.
* **process.sh** is a bash script to process all the questions and generates the data needed for the dataviz
* **process.py** is a python script to process one question. It is called multiple times by **process.sh**
* **dataviz.html** is an html page to display the dataviz for one question.
* **index.html** is an html page to browse all the questions. It use **dataviz.html** in an i-frame.

## Contributors

[Damien Henry](https://github.com/dh7)

## License

Copyright 2018 Google Inc.

Licensed under the Apache License, Version 2.0 (the “License”); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

## Final Thoughts

We encourage open sourcing projects as a way of learning from each other. Please respect our and other creators’ rights, including copyright and trademark rights when present, when sharing these works and creating derivative work. If you want more info on Google's policy, you can find that [here](https://www.google.com/permissions/).

N.B.: *This is not an official Google product.*
