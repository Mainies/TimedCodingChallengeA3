"""
Part of Submission 3
Author: Samuel Mainwood
Student #: s3939120
"""

from errors import file_existence_error, invalid_data_error
import sys
import os
from datetime import datetime
from datasets import Dataset, AdvancedDataset, SimpleDataset
from algorithms import Algorithm, MLAlgorithm, DLAlgorithm


class Records:
    cli_inputs = sys.argv
    # first is results, 2nd is datasets and 3rd argument is algorithms (always in this order)
    if len(cli_inputs) <= 1 or len(cli_inputs) > 4:
        raise file_existence_error.no_file_entered()

    algorithms = []
    datasets = []
    alg_total_scores = {}

    results_report = []
    datasets_report = []
    algorithm_report = []

    # Read result - read file from command line
    # Display results

    @staticmethod
    def read_results():
        if len(Records.cli_inputs) == 0:
            raise file_existence_error.no_file_entered()
        else:
            with open(Records.cli_inputs[1], 'r') as results:
                if os.stat(Records.cli_inputs[1]) == 0:
                    raise invalid_data_error.empty_result_file(Records.cli_inputs[1])
                for line in results:
                    line = line.strip()
                    line = line.split(",")
                    for i in range(len(line)):
                        if i == 1:
                            break
                        alg = line[i].strip()
                        if Records.is_algorithm(alg):
                            pass
                        else:
                            newalg = Algorithm(alg)
                            Records.algorithms.append(newalg)
                        currentalg = Records.get_alg(alg)

                    for i in range(1, len(line)):
                        dataset = line[i].strip().split(":")
                        dataset_name = dataset[0].strip()
                        dataset_score = dataset[1].strip()
                        if dataset_score == "404":
                            dataset_score = -404
                        elif dataset_score == "":
                            dataset_score = -1
                        else:
                            pass

                        if Records.is_dataset(dataset_name):
                            pass

                        else:
                            newset = Dataset(dataset_name)
                            Records.datasets.append(newset)

                        currentset = Records.get_dataset(dataset_name)
                        currentset.update_scores(alg, dataset_score)
                        currentalg.update_scores(dataset_name, dataset_score)

    @staticmethod
    def make_results_report():
        num_sets = len(Records.datasets)
        print_length = 22 + (10 * num_sets)
        nonexistant = 0
        ongoing = 0
        Records.results_report.append("RESULTS")
        Records.results_report.append("_".ljust(print_length, "_"))
        header = "| Algorithms".ljust(20, " ")
        for dataset in Records.datasets:
            dataset_name = dataset.get_id
            header += dataset_name.rjust(10)
        header += " |"
        Records.results_report.append(header)
        Records.results_report.append("_".ljust(print_length, "_"))
        for algorithm in Records.algorithms:
            new_line = "| "
            new_line += algorithm.name.ljust(18)
            for dataset in Records.datasets:
                add_score = algorithm.scores[dataset.get_id]
                if add_score == -404:
                    new_line += "--".rjust(10)
                    ongoing += 1
                elif add_score == -1:
                    new_line += "XX".rjust(10)
                    nonexistant += 1
                else:
                    new_line += f"{add_score}".rjust(10)
            new_line += " |"
            Records.results_report.append(new_line)
        Records.results_report.append("_".ljust(print_length, "_"))
        Records.results_report.append("\n")
        Records.results_report.append("RESULTS SUMMARY")
        summary = f"There are {len(Records.algorithms)} algorithms and {len(Records.datasets)} datasets."
        Records.results_report.append(summary)
        summary = f"The number of non-existent results is {nonexistant} and on-going results is {ongoing}."
        Records.results_report.append(summary)
        Records.results_report.append("\n")

    @staticmethod
    def print_results_report():
        for line in Records.results_report:
            print(line)

    @staticmethod
    def read_algorithms():
        with open(Records.cli_inputs[3], "r") as algs_file:
            for line in algs_file:
                line = line.strip()
                line = line.split(',')
                alg_name = line[0].strip()
                alg_type = line[1].strip()
                year = int(line[2].strip())
                authors = line[3:]
                for author in authors:
                    author = author.strip()
                if alg_type == "ML":
                    new_alg = MLAlgorithm(alg_name, year, authors)
                    Records.algorithms.append(new_alg)
                else:
                    new_alg = DLAlgorithm(alg_name, year, authors)
                    Records.algorithms.append(new_alg)

    @staticmethod
    def read_datasets():
        with open(Records.cli_inputs[2], "r") as data_file:
            for line in data_file:
                line = line.strip()
                line = line.split(',')
                dataset_id = line[0].strip()
                dataset_name = line[1].strip()
                complexity = int(line[2].strip())
                no = int(line[3].strip())
                source = line[4].strip()
                if dataset_id[-1] == "S":
                    datatype = "Simple"
                elif dataset_id[-1] == "A":
                    datatype = "Advanced"
                else:
                    raise invalid_data_error(Records.cli_inputs[2])

                current_dataset = Records.is_dataset(dataset_id)
                # Structured this way to try and cater for different ordering of reading files.
                if current_dataset and datatype == "Simple":
                    if complexity != 1:
                        raise invalid_data_error(Records.cli_inputs[2])
                    old_dataset = Records.get_dataset(dataset_id)
                    old_dataset = old_dataset.update_dataset(1, no, source, dataset_name)

                elif current_dataset and datatype == "Advanced":
                    old_dataset = Records.get_dataset(dataset_id)
                    old_dataset = old_dataset.update_dataset(complexity, no, source, dataset_name)

                elif not current_dataset and datatype == "Simple":
                    if complexity != 1:
                        raise invalid_data_error(Records.cli_inputs[2])
                    new_set = SimpleDataset(dataset_id, no, source, dataset_name)
                    Records.datasets.append(new_set)

                elif not current_dataset and datatype == "Advanced":
                    new_set = AdvancedDataset(dataset_id, complexity, no, source, dataset_name)
                    Records.datasets.append(new_set)

                else:
                    raise invalid_data_error(Records.cli_inputs[2])

    @staticmethod
    def is_algorithm(value):
        for algo in Records.algorithms:
            if value == algo.name:
                return True
        return False

    @staticmethod
    def is_dataset(value):
        for dataset in Records.datasets:
            if value == dataset.get_id:
                return True
        return False

    @staticmethod
    def get_alg(search_value):
        for algorithm in Records.algorithms:
            if search_value == algorithm.name:
                return algorithm

    @staticmethod
    def get_dataset(search_value):
        for dataset in Records.datasets:
            if search_value == dataset.get_id:
                return dataset

    @staticmethod
    def calculate_total_scores():
        Records.alg_total_scores = {}
        for algorithm in Records.algorithms:
            Records.alg_total_scores[algorithm.name] = 0
        for dataset in Records.datasets:
            numerical_dict = {}
            for key, value in dataset.scores.items():
                numerical_dict[key] = float(value)
            sorted_items = sorted(numerical_dict.items(), key=lambda item: item[1], reverse=True)
            sorted_keys = [item[0] for item in sorted_items if item[1] > 0]
            for i in range(len(sorted_keys)):
                if i == 0:
                    Records.alg_total_scores[sorted_keys[0]] += 3
                elif i == 1:
                    Records.alg_total_scores[sorted_keys[1]] += 2
                elif i == 2:
                    Records.alg_total_scores[sorted_keys[2]] += 1
                else:
                    continue

    @staticmethod
    def order_datasets(list_of_datasets):
        dataset_scores = {}
        for dataset in list_of_datasets:
            dataset_scores[dataset.get_id] = dataset.calculate_average_score()
        ordered_datasets = sorted(dataset_scores.items(), key=lambda item: item[1], reverse=True)
        ordered_dataset_keys = [item[0] for item in ordered_datasets if item[1] > 0]
        return ordered_dataset_keys

    @staticmethod
    def dataset_splitter():
        simple_datasets = []
        complex_datasets = []
        for dataset in Records.datasets:
            if isinstance(dataset, SimpleDataset):
                simple_datasets.append(dataset)
            else:
                complex_datasets.append(dataset)

        return simple_datasets, complex_datasets

    @staticmethod
    def algorithm_splitter():
        ml_algs = []
        dl_algs = []
        for algorithm in Records.algorithms:
            if isinstance(algorithm, DLAlgorithm):
                dl_algs.append(algorithm)
            else:
                ml_algs.append(algorithm)
        return ml_algs, dl_algs

    @staticmethod
    def alg_orderer(list_of_algorithms):
        current_scores = {}
        for algorithm in list_of_algorithms:
            current_scores[algorithm.name] = Records.alg_total_scores[algorithm.name]
        ordered_algorithms = sorted(current_scores.items(), key=lambda item: item[1], reverse=True)
        ordered_alg_keys = [item[0] for item in ordered_algorithms]
        return ordered_alg_keys

    @staticmethod
    def make_datasets_report():
        simple_set, complex_set = Records.dataset_splitter()
        simple_order = Records.order_datasets(simple_set)
        complex_order = Records.order_datasets(complex_set)
        challenge_dataset = ""
        challenge_score = 100
        most_fails = ""
        most_fails_no = 0
        Records.datasets_report.append("SIMPLE DATASET INFORMATION")
        x = 0
        # For ease of adjustments to print length
        for i in [15, 15, 5, 10, 10, 15, 10, 15, 10, 2]:
            x += i
        Records.datasets_report.append("_".ljust(x, "_"))
        Records.datasets_report.append("| DatasetID".ljust(15) + "Name".ljust(15) + "Type".rjust(5) + "Weight".rjust(10)
                                       + "NData".rjust(10) + "Source".rjust(15) + "Average".rjust(10) + "Range".rjust(
            15)
                                       + "Nfail".rjust(10) + " |")
        Records.datasets_report.append("_".ljust(x, "_"))

        for data_id in simple_order:
            dataset = Records.get_dataset(data_id)
            newline = "| "
            newline += dataset.get_id.ljust(13)
            newline += dataset.name.ljust(15)
            dtype = "A" if dataset.get_id[-1] == "A" else "S"
            newline += dtype.rjust(5)
            newline += f"{dataset.complexity}".rjust(10)
            newline += f"{dataset.size}".rjust(10)
            newline += dataset.source.rjust(15)
            avg = dataset.calculate_average_score()
            if avg < challenge_score:
                challenge_dataset = dataset.name
                challenge_score = avg
            newline += f"{avg:.2f}".rjust(10)
            dmin, dmax = dataset.min_max()
            newline += f"{dmin}-{dmax}".rjust(15)
            fails = dataset.failed_tests()
            fails = int(fails)
            if fails >= most_fails_no:
                most_fails = dataset.name
                most_fails_no = fails
            newline += f"{fails}".rjust(10)
            newline += " |"
            Records.datasets_report.append(newline)
        Records.datasets_report.append("_".ljust(x, "_"))
        Records.datasets_report.append("\n")
        Records.datasets_report.append("ADVANCED DATASET INFORMATION")
        x = 0
        # For ease of adjustments to print length
        for i in [15, 15, 5, 10, 10, 15, 10, 15, 10, 2]:
            x += i
        Records.datasets_report.append("_".ljust(x, "_"))
        Records.datasets_report.append("| DatasetID".ljust(15) + "Name".ljust(15) + "Type".rjust(5) + "Weight".rjust(10)
                                       + "NData".rjust(10) + "Source".rjust(15) + "Average".rjust(10) + "Range".rjust(
            15)
                                       + "Nfail".rjust(10) + " |")
        Records.datasets_report.append("_".ljust(x, "_"))

        for data_id in complex_order:
            dataset = Records.get_dataset(data_id)
            newline = "| "
            newline += dataset.get_id.ljust(13)
            newline += dataset.name.ljust(15)
            dtype = "A" if dataset.get_id[-1] == "A" else "S"
            newline += dtype.rjust(5)
            newline += f"{dataset.complexity}".rjust(10)
            newline += f"{dataset.size}".rjust(10)
            newline += dataset.source.rjust(15)
            avg = dataset.calculate_average_score()
            if avg < challenge_score:
                challenge_dataset = dataset.name
                challenge_score = avg
            newline += f"{avg:.2f}".rjust(10)
            dmin, dmax = dataset.min_max()
            newline += f"{dmin}-{dmax}".rjust(15)
            fails = dataset.failed_tests()
            fails = int(fails)
            if fails >= most_fails_no:
                most_fails = dataset.name
                most_fails_no = fails
            newline += f"{fails}".rjust(10)
            newline += " |"
            Records.datasets_report.append(newline)
        Records.datasets_report.append("_".ljust(x, "_"))
        Records.datasets_report.append("\n")
        Records.datasets_report.append("DATASET SUMMARY")
        summary = f"The most difficult dataset was {challenge_dataset} with an average score of {challenge_score:.2f}."
        Records.datasets_report.append(summary)
        summary = f"The dataset with the most failed tests was {most_fails} with {most_fails_no} failed tests."
        Records.datasets_report.append(summary)
        Records.datasets_report.append("\n")

    @staticmethod
    def print_dataset_report():
        for line in Records.datasets_report:
            print(line)

    @staticmethod
    def make_algorithms_report():
        ml_set, dl_set = Records.algorithm_splitter()
        dl_order = Records.alg_orderer(dl_set)
        ml_order = Records.alg_orderer(ml_set)
        best_alg = ""
        best_score = 0
        least_failures_alg = ""
        least_failures_score = 100

        Records.algorithm_report.append("DL ALGORITHM INFORMATION")
        x = 0
        for i in [20, 5, 10, 20, 10, 10, 8, 15, 10, 2]:
            x += i
        Records.algorithm_report.append("_".ljust(x, "_"))
        Records.algorithm_report.append("| Name".ljust(20) + "Type".rjust(5) + "Year".rjust(10) + "Authors".rjust(20) +
                                        "Score".rjust(10) + "Average".rjust(10) + "Nfail".rjust(
            8) + "FailDataset".rjust(15) +
                                        "Nongoing".rjust(10) + " |")
        Records.algorithm_report.append("_".ljust(x, "_"))
        for algorithm in dl_order:
            algorithm = Records.get_alg(algorithm)
            isfail, nfails = algorithm.check_success()
            newline = "| "
            name = algorithm.name
            if isfail:
                name += " (!)"
            newline += name.ljust(18)
            algtype = "DL"
            newline += algtype.rjust(5)
            year = str(algorithm.year)
            newline += year.rjust(10)
            author_string = ""
            for i in range(len(algorithm.authors)):
                if i == 0:
                    author_string += algorithm.authors[i].strip()
                else:
                    author_string += "-" + algorithm.authors[i].strip()
            newline += author_string.rjust(20)
            score = Records.alg_total_scores[algorithm.name]
            newline += f"{score}".rjust(10)
            average = algorithm.calculate_average_score()
            if average > best_score:
                best_alg = name
                best_score = average
            newline += f"{average:.2f}".rjust(10)
            nfail = str(len(nfails))
            if len(nfails) < least_failures_score:
                least_failures_alg = name
                least_failures_score = len(nfails)
            newline += nfail.rjust(8)
            fail_sets_string = ""
            for i in range(len(nfails)):
                if i == 0:
                    fail_sets_string += str(nfails[0])
                else:
                    fail_sets_string += "-" + str(nfails[i])
            newline += fail_sets_string.rjust(15)
            ongoing = str(algorithm.ongoing_tests())
            newline += ongoing.rjust(10)
            newline += " |"
            Records.algorithm_report.append(newline)

        Records.algorithm_report.append("_".ljust(x, "_"))
        Records.algorithm_report.append("\n")
        Records.algorithm_report.append("ML ALGORITHM INFORMATION")
        x = 0
        for i in [20, 5, 10, 20, 10, 10, 8, 15, 10, 2]:
            x += i
        Records.algorithm_report.append("_".ljust(x, "_"))
        Records.algorithm_report.append("| Name".ljust(20) + "Type".rjust(5) + "Year".rjust(10) +
                                        "Authors".rjust(20) + "Score".rjust(10) + "Average".rjust(10) +
                                        "Nfail".rjust(8) + "FailDataset".rjust(15) + "Nongoing".rjust(10) + " |")
        Records.algorithm_report.append("_".ljust(x, "_"))
        for algorithm in ml_order:
            algorithm = Records.get_alg(algorithm)
            isfail, nfails = algorithm.check_success()
            newline = "| "
            name = algorithm.name
            if isfail:
                name += " (!)"
            newline += name.ljust(18)
            algtype = "ML"
            newline += algtype.rjust(5)
            year = str(algorithm.year)
            newline += year.rjust(10)
            author_string = ""
            for i in range(len(algorithm.authors)):
                if i == 0:
                    author_string += algorithm.authors[i].strip()
                else:
                    author_string += "-" + algorithm.authors[i].strip()
            newline += author_string.rjust(20)
            score = Records.alg_total_scores[algorithm.name]
            newline += f"{score}".rjust(10)
            average = algorithm.calculate_average_score()
            if average > best_score:
                best_alg = name
                best_score = average
            newline += f"{average:.2f}".rjust(10)
            nfail = str(len(nfails))
            if len(nfails) < least_failures_score:
                least_failures_alg = name
                least_failures_score = len(nfails)
            newline += nfail.rjust(8)
            fail_sets_string = ""
            for i in range(len(nfails)):
                if i == 0:
                    fail_sets_string += str(nfails[0])
                else:
                    fail_sets_string += "-" + str(nfails[i])
            newline += fail_sets_string.rjust(15)
            ongoing = str(algorithm.ongoing_tests())
            newline += ongoing.rjust(10)
            newline += " |"
            Records.algorithm_report.append(newline)
        Records.algorithm_report.append("_".ljust(x, "_"))
        Records.algorithm_report.append("\n")
        Records.algorithm_report.append("ALGORITHM SUMMARY")
        Records.algorithm_report.append(f"The best algorithm is {best_alg} with an average result of {best_score}.")
        Records.algorithm_report.append((f"The algorithm with the least failures is {least_failures_alg}" +
                                         f" with the number of failures being {least_failures_score}."))
        Records.algorithm_report.append("\n")

    @staticmethod
    def print_algorithm_report():
        for line in Records.algorithm_report:
            print(line)


class Report:
    current_report = []
    previous_reports = []

    @staticmethod
    def write_report():
        with open("reports.txt", "w") as reports:
            for line in Report.current_report:
                reports.writelines([line, "\n"])
            for line in Report.previous_reports:
                reports.writelines(line)
            reports.close()

    @staticmethod
    def save_old_report():
        try:
            with open("reports.txt") as old_report:
                for line in old_report:
                    Report.previous_reports.append(line)
        except:
            print("No previous reports found.")

    @staticmethod
    def timestamp():
        start = "Report Submitted "
        now = datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%S")
        # now = str(now)[:23]
        start += now
        Report.current_report.append(start)
        Report.current_report.append("\n")

    @staticmethod
    def save_reports():
        for line in Records.results_report:
            Report.current_report.append(line)

        for line in Records.datasets_report:
            Report.current_report.append(line)

        for line in Records.algorithm_report:
            Report.current_report.append(line)
