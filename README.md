# Timed Coding Challenge - CLI Reporting Program

This project was part of a short-term (1-week) challenge that involved creating a command-line interface (CLI) program for handling various command line inputs and formatting output as specified in the assignment.

## Assignment Details

- **Objective:** Design a CLI program using Object-Oriented programming principles.
- **Requirements:** The program should be able to run with various combinations of input files, including:
  - `my_record.py`
  - `my_record.py results.txt`
  - `my_record.py result.txt datasets.txt`
  - `my_record.py results.txt datasets.txt algorithms.txt`
- **Exception Handling:** While exceptions were required to be handled, the order of inputted files (results, datasets, and algorithms) always remained consistent, and these files maintained a standard structure.

## Usage

You can use the program by running `my_record.py` with the following optional arguments:

- `results.txt` (Path to the results file)
- `datasets.txt` (Path to the datasets file)
- `algorithms.txt` (Path to the algorithms file)

Example usages:

```bash
python my_record.py
python my_record.py results.txt
python my_record.py results.txt datasets.txt
python my_record.py results.txt datasets.txt algorithms.txt
