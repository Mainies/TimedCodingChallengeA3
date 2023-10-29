"""
Part of Submission 3
Author: Samuel Mainwood
Student #: s3939120
"""


class Dataset:
    """Parent class for Datasets"""

    def __init__(self, data_id):
        self.source = ""
        self.size = None
        self.complexity = None
        self.__id = data_id
        self.name = ""
        self.scores = {}

    @property
    def get_id(self):
        # demonstration of private attributes
        return self.__id

    def set_id(self, new_id):
        # demonstration of setters
        self.__id = new_id

    def update_dataset(self, complexity=None, size=None, source=None, name=None):
        # function to update basic datasets if dataset exists.
        self.complexity = complexity
        self.size = size
        self.source = source
        self.name = name

    def update_scores(self, key, value):
        self.scores[key] = value

    def calculate_average_score(self):
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

    def min_max(self) -> (float, float):
        """Returns minimum and maximum values."""
        max_value = 0
        min_value = 100
        if len(self.scores) == 0:
            # to be able to handle datasets without scores
            return "--", "--"
        for key, value in self.scores.items():
            value = float(value)
            if value < 0:
                continue
            if value > max_value:
                max_value = value
            if value < min_value:
                min_value = value
            else:
                continue

        return min_value, max_value

    def failed_tests(self):
        n_fails = 0
        for key, value in self.scores.items():
            if value == -1:
                n_fails += 1

        return n_fails

    def ongoing_tests(self):
        n_ongoing = 0
        for key, value in self.scores.items():
            if value == -404:
                n_ongoing += 1

        return n_ongoing


class AdvancedDataset(Dataset):
    """Child Class for Datasets. Holds and maintains attributes for Advanced Datasets."""

    def __init__(self, data_id, complexity, size, source="", name=""):
        super().__init__(data_id)
        self.complexity = complexity
        self.size = size
        self.source = source
        self.name = name

    @property
    def get_id(self):
        return super().get_id

    def set_id(self, new_id):
        super().set_id(new_id)

    def update_dataset(self, complexity=None, size=None, source=None, name=None):
        """Update dataset file if it exists"""
        super().update_dataset()

    def update_scores(self, key, value):
        super().update_scores(key, value)

    def min_max(self):
        return super().min_max()

    def failed_tests(self):
        return super().failed_tests()

    def ongoing_tests(self):
        return super().ongoing_tests()


class SimpleDataset(Dataset):
    """Child class for Simple Datasets"""
    complexity = 1

    # all simple datasets have the same complexity.

    def __init__(self, data_id, size, source="", name=""):
        super().__init__(data_id)
        self.complexity = SimpleDataset.complexity
        self.size = size
        self.source = source
        self.name = name

    @property
    def get_id(self):
        return super().get_id

    def set_id(self, new_id):
        return super().set_id(new_id)

    def update_dataset(self, complexity=1, size=None, source=None, name=None):
        super().update_dataset()

    def update_scores(self, key, value):
        super().update_scores(key, value)

    def min_max(self):
        return super().min_max()

    def failed_tests(self):
        return super().failed_tests()

    def ongoing_tests(self):
        return super().ongoing_tests()
