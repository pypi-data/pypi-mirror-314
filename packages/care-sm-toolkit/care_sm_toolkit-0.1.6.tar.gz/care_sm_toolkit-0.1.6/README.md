# CARE-SM Toolkit

**CSV datatable toolkit for CARE semantic model implementation**

The implementation of the Clinical And Registry Entries (CARE) Semantic Model for CSV data entails a meticulous and technically advanced workflow. By leveraging the power of the CARE-SM, YARRRML templates and incorporating the critical curation step executed by the CARE-SM toolkit, this implementation achieves robustness, accuracy, and reliability in generating RDF-based CDE-oriented patient data.

The toolkit serves as a module dedicated to performing a curation step prior to the conversion of data into RDF. The primary transformations carried out by the toolkit include:

* Quality control for column names.

* Adding every domain specific ontological term required to define every instances of the model, these terms are specific for every data element.

* Splitting the column labeled as `value` into distinct datatypes. This enables YARRRML to interpret each datatype differently, facilitating the subsequent processing.

* Conducting a quality control among `age`/`date`, `stardate` and `enddate` columns to ensure data consistency and validity.

* Eliminating any row that lacks of the minimal required data to minimize the generation of incomplete RDF transformations.

* Creation of the column called `uniqid` that assigns a unique identifier to each observation. This prevents the RDF instances from overlapping with one another, ensuring their distinctiveness and integrity.

## Dockerized implementation

There's a Docker-based implementation controlled via API (using FastAPI) that you can use for mounting this data transformation step as a part of your CARE-SM implementation. Use our docker compose to control your Docker image, ports where its located and volumes in order to pass your CSV-based patient data:

```yaml
version: "3.3"

services:
  api:
    image: pabloalarconm/care-sm-toolkit:latest # check for latest version
    ports:
      - "8000:8000"
    volumes:
      - ./data:/code/data
```

## Local implementation

If you are not interested on running Docker image, you can install the Pyhton module for local implementation.

###  Installation:

```bash
pip install CARE-SM-Toolkit
```
**Requirements:**

- CSV data table glossary with every data element documented at [CARE-SM implementation](https://github.com/CARE-SM/CARE-SM-Implementation/blob/main/CSV/README.md)

**Test:**

```py
import pandas as pd
from main import Toolkit

test= Toolkit()

test_done = test.whole_quality_control(input_data="toolkit/exemplar_data/preCARE.csv")
test_done.to_csv ("toolkit/exemplar_data/CARE.csv", index = False, header=True)
```