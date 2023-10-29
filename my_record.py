"""
Main File for Assignment 3 Submission. Run for program function.

Name: Samuel Mainwood
Student: s3939120
Due: 29/10/2023

All parts complete (HD)
No known bugs
"""

# Import Classes and Errors from Adjacent Files
import sys
from errors import File_Validator, file_existence_error, nonexistent_file
from records import Records, Report

# Dataset(s) and Algorithm(s) classes are called in other files.

"""
Reflection:

This was a more challenging assessment than #2, partly due to its differences from the Taxi booking system so I had to 
consider a new programming design and get used to incorporating the CLI as a part of a program. 

My biggest challenge was the management of data. In the end I decided to keep each algorithm class and dataset
with their own scores. I was considering a "results" class but I thought that this would not solve my encapsulation 
dilemma and this allowed for better encapsulation for other statistics. I also used custom exceptions much more
than in the previous assignment and I think they may be the most useful skill I have picked up from this course. I am
still not a master at them but will endeavour to improve on this aspect.

If I were to repeat this task, I would consider starting from HD and beginning with a class diagram. This would make
it easier for me to visualise the relationships. I would also try and encapsulate the printing better and I think
this will be a program I revisit over the summer holidays. Nevertheless I am quietly very content with how it
turned out.
"""


class main_class:

    @staticmethod
    def read_1():
        # Runs with 1 File (Results)
        File_Validator.result_file_validator(sys.argv[1])
        Records.read_results()
        Records.make_results_report()
        Records.print_results_report()
        Report.save_reports()

    @staticmethod
    def read_2():
        # Runs with 2 Files (Results, Datasets)
        File_Validator.valid_dataset_file(sys.argv[2])
        Records.read_datasets()
        File_Validator.result_file_validator(sys.argv[1])
        Records.read_results()
        Records.make_results_report()
        Records.make_datasets_report()
        Records.print_results_report()
        Records.print_dataset_report()
        Report.save_reports()

    @staticmethod
    def read_3():
        # Runs with 3 Files (Results, Datasets)
        File_Validator.valid_dataset_file(sys.argv[2])
        File_Validator.result_file_validator(sys.argv[1])
        Records.read_datasets()
        Records.read_algorithms()
        Records.read_results()
        Records.calculate_total_scores()
        Records.make_results_report()
        Records.make_datasets_report()
        Records.make_algorithms_report()
        Records.print_results_report()
        Records.print_dataset_report()
        Records.print_algorithm_report()
        Report.save_reports()

    @staticmethod
    def find_files():
        for filename in sys.argv:
            try:
                valid = open(filename)
                valid.close()
            except:
                raise nonexistent_file.missing_file(filename)

    @staticmethod
    def check_length():
        arguments = len(sys.argv)
        return arguments

    @staticmethod
    def run():
        main_class.find_files()
        Report.timestamp()
        Report.save_old_report()
        # Checks for Correct File names
        if main_class.check_length() > 4:
            raise file_existence_error.some_file_entered()
        elif main_class.check_length() < 2:
            raise file_existence_error.no_file_entered()
        elif main_class.check_length() == 2:
            main_class.read_1()
        elif main_class.check_length() == 3:
            main_class.read_2()
        else:
            # last use case is check_length() == 4
            main_class.read_3()
        Report.write_report()


if __name__ == "__main__":
    main_class.run()
