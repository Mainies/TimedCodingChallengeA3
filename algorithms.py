"""
Part of Submission 3
Author: Samuel Mainwood
Student #: s3939120
"""


class Algorithm:
    # parent class
    def __init__(self, alg_name, year=None, authors=None):
        # demonstration of private variable
        self.__name = alg_name
        self.year = year
        self.authors = authors
        self.scores = {}

    @property
    def name(self):
        # demonstration of getter and property decorator
        return self.__name

    def update_scores(self, key, value):
        # used to update the score on a dataset
        self.scores[key] = value

    def calculate_average_score(self):
        """returns individual average score. As function allows it to change easy."""
        total = 0
        num = 0
        for key, value in self.scores.items():
            value = float(value)
            if value < 0:
                continue
            num += 1
            total += value
        if num <= 0:
            return total
        total /= num
        return total

    def min_max(self) -> (int, int):
        """Returns the minimum and maximum scores for a given algorithm"""
        max_value = 0
        min_value = 100
        # any score has to be or greater or smaller than the respective values
        if len(self.scores) == 0:
            # to be able to handle datasets without scores
            return "--", "--"
        for key, value in self.scores.items():
            value = float(value)
            if value < 0:
                # ongoing and invalid tests are ignored for range.
                continue
            if value > max_value:
                max_value = value
            if value < min_value:
                min_value = value
            else:
                continue

        return min_value, max_value

    def ongoing_tests(self) -> int:
        n_ongoing = 0
        for key, value in self.scores.items():
            if value == -404:
                n_ongoing += 1

        return n_ongoing


class DLAlgorithm(Algorithm):
    """Child class for Algorithm Maintains attributes required for a DL algorithm."""

    def __init__(self, alg_name, year, authors):
        super().__init__(alg_name, year, authors)

    def update_scores(self, key, value):
        self.scores[key] = value

    @property
    def name(self):
        # property attribute
        return super().name

    def check_success(self):
        """Checks for successful running of an algorithm per the DL algorithm criteria"""
        failed_datasets = []
        num_advanced_required = 2
        current_num_advanced = 0
        simple_failure = False
        for key, value in self.scores.items():
            value = float(value)
            if key[-1] == "S" and value == -1:
                failed_datasets.append(key)
                simple_failure = True
                continue
            elif key[-1] == "S" and value > 0:
                continue
            elif key[-1] == "A" and value > 0:
                current_num_advanced += 1
                continue
            elif key[-1] == "A" and value == -404:
                current_num_advanced += 1
                continue
            elif key[-1] == "A" and value == -1:
                failed_datasets.append(key)
            else:
                continue

        if simple_failure is True:
            # Immediate failure if not able to run on simple dataset
            return False, failed_datasets
        elif num_advanced_required <= current_num_advanced:
            # returns boolean for other functions and the failed datasets for printing.
            return True, failed_datasets
        else:
            return False, failed_datasets

    def calculate_average_score(self):
        return super().calculate_average_score()

    def min_max(self):
        return super().min_max()

    def ongoing_tests(self):
        return super().ongoing_tests()


class MLAlgorithm(Algorithm):
    """Child class for algorithm. Maintains attributes required for an ML Algorithm"""

    def __init__(self, alg_name, year, authors):
        super().__init__(alg_name, year, authors)

    def update_scores(self, key, value):
        self.scores[key] = value

    @property
    def name(self):
        return super().name

    def update_algorithm_info(self, year, authors):
        self.year = year
        self.authors = authors

    def check_success(self):
        """Checks for successful running of an algorithm per the DL algorithm criteria"""
        failed_datasets = []
        num_advanced_required = 1
        current_num_advanced = 0
        simple_failure = False
        for key, value in self.scores.items():
            value = float(value)
            if key[-1] == "S" and value == -1:
                failed_datasets.append(key)
                simple_failure = True
                continue
            elif key[-1] == "S" and value > 0:
                continue
            elif key[-1] == "A" and value > 0:
                current_num_advanced += 1
                continue
            elif key[-1] == "A" and value == -404:
                current_num_advanced += 1
                continue
            elif key[-1] == "A" and value == -1:
                failed_datasets.append(key)
            else:
                continue

        if simple_failure is True:
            return False, failed_datasets
        elif num_advanced_required <= current_num_advanced:
            return True, failed_datasets
        else:
            return False, failed_datasets

    def calculate_average_score(self):
        return super().calculate_average_score()

    def min_max(self):
        return super().min_max()

    def ongoing_tests(self):
        return super().ongoing_tests()
