![icon](icon.png)

<hr>

# better-moles-patent-finder
A tool designed to enhance patent discovery by leveraging MongoDB for efficient storage, querying, and analysis of patent data. This repository includes features to streamline patent searches, improve retrieval accuracy, and support advanced filtering and indexing capabilities.

[![Coverage](https://codecov.io/github/fabiobove-dr/better-moles-patent-finder/coverage.svg?branch=main)](https://codecov.io/gh/tacclab/bio_dataset_manager)  
[![PyPI Latest Release](https://img.shields.io/pypi/v/better-moles-patent-finder.svg)](https://pypi.org/project/better-moles-patent-finder/)  
![Unit Tests](https://github.com/fabiobove-dr/better-moles-patent-finder/actions/workflows/codecov.yml/badge.svg)<br>
[![Powered by Fabio](https://img.shields.io/badge/powered%20by-Fabio-orange.svg?style=flat&colorA=E1523D&colorB=007D8A)]()  
[![License](https://img.shields.io/github/license/fabiobove-dr/better-moles-patent-finder.svg)](https://github.com/tacclab/bio_dataset_manager/blob/main/LICENSE)<br>


## Overview 
This project offers a powerful platform for patent research, combining advanced search features with a MongoDB backend to store, retrieve, and analyze patent-related data efficiently. It allows users to search for patents associated with chemical compounds, leveraging SMILES, InChI, and other molecular representations. The system also supports filtering by molecular structure, patent ID, and other criteria.
<hr>

This project is based on the **PatCID** paper, which focuses on the identification and classification of patent data related to molecular structures. The techniques and methodologies from the PatCID framework are utilized to enhance patent search results by leveraging chemical informatics and advanced query techniques. The core concept of this project builds upon PatCID's ability to match molecular structures with relevant patent information, improving the overall efficiency and accuracy of patent searches.
To check out their incredible work, visit the [PatCID GitHub repository](https://github.com/DS4SD/PatCID).
![scratches(1).png](..%2F..%2F..%2F..%2FDownloads%2Fscratches%281%29.png)<hr>

**Key Features:**
- **Patent Search**: Search patents by their ID or associated molecular properties.
- **Advanced Filtering**: Filter patents based on molecular structure, chemical formula, and other relevant fields.
- **Efficient Querying**: Use MongoDB's indexing and querying capabilities to retrieve patents quickly.
- **Data Model**: The system stores patents and associated molecules in a structured format, making it easy to extend and scale.


## Authors:
   - Fabio Bove | fabio.bove.dr@gmail.com<br> 
<hr>

## What is it?
This tool is designed to assist researchers and patent professionals in finding relevant patents related to chemical compounds using molecular representations like SMILES and InChI. By using MongoDB as the backend, it efficiently stores and indexes large volumes of patent and molecular data. Users can easily query patents, filter based on molecular structures, and retrieve precise results with high speed.

**Key Features:**
- **Patent Search**: Search patents by their ID or associated molecular properties.
- **Advanced Filtering**: Filter patents based on molecular structure, chemical formula, and other relevant fields.
- **Efficient Querying**: Use MongoDB's indexing and querying capabilities to retrieve patents quickly.
- **Data Model**: The system stores patents and associated molecules in a structured format, making it easy to extend and scale.

<hr>

## Mongo Documents Format

The MongoDB documents used by this project follow the structure below, which includes information about the molecule (using SMILES, InChI, etc.) and the associated patent IDs:

```json
{
  "molecule": {
    "smiles": "Brc1cc(-c2ccccc2)nc(-c2ccc3c4ccccc4c4ccccc4c3c2)c1",
    "inchi": "InChI=1S/C29H18BrN/c30-21-17-28(19-8-2-1-3-9-19)31-29(18-21)20-14-15-26-24-12-5-4-10-22(24)23-11-6-7-13-25(23)27(26)16-20/h1-18H",
    "inchikey": "UPAWJZOAEGLCFP-UHFFFAOYSA-N",
    "sum_formula": "C29H18BrN",
    "conf": 0.57
  },
  "patents": [
    {"id": "US20200136057A1"},
    {"id": "US20200136057"}
  ]
}
```

## Mongo Documents Format

- **molecule**: Contains the molecular data (SMILES, InChI, InChIKey, sum formula).
- **patents**: A list of patent IDs that are associated with the molecule.

<hr>

## Usage

### Installation

You can install the `better-moles-patent-finder` package via `pip` from PyPI or clone the repository to run locally:

#### Install from PyPI:
```bash
pip install better-moles-patent-finder
```

#### Basic Usage

Once installed, you can start querying patents using the provided API or Running as a Script

You can run the project as a script by passing a configuration file path:
```bash
better-moles-patent-finder --config-path /path/to/config_file.yaml
```

```python
from better_moles_patent_finder import PatentFinder

# Create a PatentFinder instance
pf = PatentFinder()

# Search for a patent by ID
result = pf.search_by_patent_id('US20200136057A1')

# Search for patents by molecule structure (SMILES)
result = pf.search_by_smiles('Brc1cc(-c2ccccc2)nc(-c2ccc3c4ccccc4c4ccccc4c3c2)c1')

# Print the result
print(result)
```

MongoDB Connection

Ensure MongoDB is running and accessible. The default connection string is configured in the project. You can modify it if necessary in the mongo_connector.py file.
```python
from better_moles_patent_finder import MongoConnector

# Connect to the MongoDB database
mongo = MongoConnector()
mongo.connect()

# Perform queries and operations
```

---
## License
This project is licensed under the terms of the GNU General Public License, Version 3.
