# CIS6930SP24-ASSIGNMENT1

# Author: Stavan Shah

# Assignment Description 

Sensitive information is frequently included in documents such as police reports, court transcripts, and medical records. To safeguard privacy, it's essential to redact or censor this information before sharing documents publicly. However, manual redaction processes are often costly and time-consuming. To address this challenge, the Redaction Pipeline System automates the detection and censoring of sensitive information within plain text documents.

## Table of Contents

- How to Install
- How to Run 
- Functions
- Output

## How to Install
  1. Clone repository to your local machine:
    $ git clone 
    $ cd cis6930sp24-assignment1
  2. Using Pipenv and Installing prerequisites:
    $ pipenv install
  3. Verify Installation: Once the command in step 3 is completed, verify if the dependencies are installed correctly by runing the following command:
    $ pipenv --version
## How to Run
- We must execute the following command in order to run the censor:
  ```
  pipenv run python redactor.py --input '*.txt' \
                    --names --dates --phones --genders --address\
                    --concept 'kids' \
                    --output 'files/' \
                    --stats stderr
  ```                  
## censoror.py
   This script provides functionality to censor sensitive information like names, dates, phone   numbers, and addresses from input files. It leverages various libraries and tools for natural language processing (NLP) and weak supervision.

- **Dependencies:**
   - `argparse`: Used for parsing command-line arguments.
   - `glob`: Used for file pattern matching.
   - `sys`: Provides access to some variables used or maintained by the Python interpreter.
   - `os`: Used for interacting with the operating system, such as file operations.
   - `assignment1.main`: Imports the functions defined in the `main.py` file of an `assignment1` module.

## Functions Summary

### `process_files(args)`
- Input: `args` (parsed command-line arguments)
- Output: List of raw file paths
- Description: Expands file globs in the input paths and returns a list of raw file paths.

### `censor_data(raw_file, data, censor_functions)`
- Inputs:
  - `raw_file`: Path to the raw file
  - `data`: Contents of the raw file
  - `censor_functions`: List of censoring functions
- Outputs: 
  - Censored data
  - Censor counts
  - Censor lists
- Description: Applies censoring functions to the provided data, tracks censor counts, and generates censor lists.

### `write_to_file(output_path, data)`
- Inputs:
  - `output_path`: Path to the output file
  - `data`: Data to write to the file
- Description: Writes the provided data to a file specified by the output path.

### `censor_stats(args, censor_counts, censor_list)`
- Inputs:
  - `args`: Parsed command-line arguments
  - `censor_counts`: Dictionary containing censor counts
  - `censor_list`: Dictionary containing censor lists
- Output: Formatted string containing censoring statistics
- Description: Generates statistics based on the censoring process, including the number of items censored for each specified type of data.

### `main(args)`
- Input: `args` (parsed command-line arguments)
- Description: 
  - Defines censor functions to apply to the data.
  - Iterates through each input file, reads the file, applies censoring functions, and writes the censored data.
  - Gathers censoring statistics and writes them to standard output/error or specified statistics file. 
- **Censoring Functions:**
   - `censor_dates(data)`, `censor_phones(data)`, `censor_address(data)`, and `censor_names_snorkel(data)`: These functions individually censor dates, phone numbers, addresses, and names from the input text. They utilize different techniques, such as regular expressions, NER, and weak supervision with Snorkel, to identify and censor sensitive information.
         
      ## censor_names(text)
- **Description**: Censors names (entities labeled as 'PERSON' or 'GPE') in the provided text.
- **Dependencies**:
  - `nltk`: Natural Language Toolkit
- **Returns**: 
  - Censored text with replaced names (Unicode block character), list of censored names.

## censor_dates(text)
- **Description**: Censors dates mentioned in the provided text.
- **Dependencies**:
  - `spacy`: For named entity recognition (NER)
  - `re`: Regular expression module
- **Returns**: 
  - Censored text with replaced dates (Unicode block character), list of censored dates.

## censor_phones(text)
- **Description**: Censors phone numbers mentioned in the provided text.
- **Dependencies**:
  - `commonregex`: For phone number extraction
- **Returns**: 
  - Censored text with replaced phone numbers (Unicode block character), list of censored phone numbers.

## censor_genders(text)
- **Description**: Censors gender-related terms mentioned in the provided text.
- **Dependencies**:
  - `nltk`: Natural Language Toolkit
- **Returns**: 
  - Censored text with replaced gender terms (Unicode block character), list of censored gender terms.

## censor_addresses(text)
- **Description**: Censors addresses mentioned in the provided text.
- **Dependencies**:
  - `pyap`: Python Address Parser
- **Returns**: 
  - Censored text with replaced addresses (Unicode block character), list of censored addresses.

## censor_concepts(text, concepts)
- **Description**: Censors sentences containing specified concepts in the provided text.
- **Dependencies**:
  - `nltk`: Natural Language Toolkit
- **Parameters**:
  - `concepts`: List of concepts to be censored.
- **Returns**: 
  - Censored text with replaced sentences (Unicode block character), list of censored sentences.
- **Execution from Command Line**:
   Users can run the script from the command line by specifying input files, types of information to censor, output formats, and where to print statistics.


## Output
- [Video Output](https://drive.google.com/file/d/1j9iyU4fUAfKgeKfpaBxFv0A6T9k7wXXb/view?usp=sharing)

## Author 
  - Stavan Shah
  - Email: stavannikhi.shah@ufl.edu
  - UFID: 76557015
