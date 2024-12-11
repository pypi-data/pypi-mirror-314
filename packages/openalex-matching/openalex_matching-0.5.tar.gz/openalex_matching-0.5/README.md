# OpenAlex Matching

## Description

OpenAlex Matching is a Python package designed to match research authors with their corresponding OpenAlex ID using filters such as institutional publication history, author primary topics, and ORCID IDs. The package also includes functionality to read and output data in CSV format. 

## Installation
You can install OpenAlex Matching via pip:

```bash
pip install "openalex-matching == 0.4"

```
Alternatively, you can install from GitHub

```bash
pip install git+https://github.com/byuk729/openalex_matching

```


## Examples

### OpenAlex_person_match_v1 Example:
Demonstrates how to match single author to their corresponding OpenAlex ID 
Shows how to read from a CSV file, run the matching algorithm, and output the OpenAlex IDs for each author into a new CSV file.

### orcid_topic_algorithms Example:
Demonstrates how to match authors using ORCID to OpenAlex ID, as well as how to filter authors based on name, institution, and research topics.





