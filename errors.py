"""
Part of Submission 3
Author: Samuel Mainwood
Student #: s3939120
"""

import sys
import os


class file_existence_error(Exception):
    # Error for incorrect file usage or no files entered properly.
    @staticmethod
    def no_file_entered():
        # Error for incorrect file usage
        print("No results file entered.")
        print("[Usage:] python my_record.py <result_file> [dataset_file] [algorithm_file]")
        sys.exit()

    @staticmethod
    def some_file_entered():
        print("[Usage:] python my_record.py <result_file> [dataset_file] [algorithm_file]")


class invalid_data_error(Exception):
    # general invalid data for business rules
    @staticmethod
    def invalid_data(filename):
        print(f"Invalid Data in {filename}.")
        sys.exit()

    @staticmethod
    def empty_result_file(filename):
        # called if file size = 0
        print(f"No data found in {filename}. Closing system.")
        sys.exit()


class invalid_dataset_file(Exception):
    # specific error for Dataset errors.
    @staticmethod
    def invalid_dataset_id(filename):
        print(f"Invalid ID found in {filename}. ID must start with 2, have 2 integers and end with S or A.")
        sys.exit()


class nonexistent_file(Exception):
    # specific error for Dataset errors
    @staticmethod
    def missing_file(filename):
        print(f"{filename} cannot be found. Please check directory and spelling and try again.")
        sys.exit()


class File_Validator:
    # Class to hold file validators

    @staticmethod
    def valid_dataset_file(filename):
        """Checks if dataset is valid and returns an error if false"""
        with open(filename, "r") as dataset_file:
            for line in dataset_file:
                line = line.strip().split(",")
                ID = line[0].strip()
                if len(ID) != 4:
                    raise invalid_dataset_file.invalid_dataset_id(filename)
                elif ID[0] != "D":
                    raise invalid_dataset_file.invalid_dataset_id(filename)
                elif ID[-1] not in ("S", "A"):
                    raise invalid_dataset_file.invalid_dataset_id(filename)
                elif not ID[1:2].isdigit():
                    # check to ensure that dataset is a 2 digit ID.
                    raise invalid_dataset_file.invalid_dataset_id(filename)
                else:
                    pass
                complexity = int(line[2].strip())
                if ID[-1] == "S" and complexity != complexity:
                    raise invalid_dataset_file.invalid_dataset_id(filename)
                elif ID[-1] == "A" and complexity not in range(2, 6):
                    raise invalid_dataset_file.invalid_dataset_id(filename)

    @staticmethod
    def result_file_validator(filename):
        """Checks if the given results file is valid and returns an error if false."""
        with open(filename, 'r') as results:
            if os.stat(filename) == 0:
                raise invalid_data_error.empty_result_file(filename)
            for line in results:
                line = line.strip()
                line = line.split(",")
                for i in range(1, len(line)):
                    dataset = line[i].strip().split(":")
                    dataset_score = dataset[1].strip()
                    if dataset_score == "":
                        # allows for missing results
                        continue
                    try:
                        float(dataset_score)
                    except:
                        raise invalid_data_error.invalid_data(filename)
