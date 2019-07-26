#
#   Copyright (c) 2019 Bernd Wiesner. bernduwiesner@yahoo.co.uk
#   All rights reserved
#
"""Lottery generator common classes using wxPython
"""
import dataclasses
from typing import Union
import constants as C


@dataclasses.dataclass
class OptionsData:
    """Options store
    """

    lottery_type: int = C.LOTTERY_DEFAULT
    number_of_lines: int = 2
    option: int = C.OPTIONS_DEFAULT

    def get_lottery_name(self):
        """Return a text of the type of lottery to generate numbers for

        :return: str the text of the selected lottery type
        """
        return C.LOTTERY_CHOICES[self.lottery_type]

    def get_option_name(self):
        """Return a text value of action to be performed

        :return: str the text of the action option
        """
        return C.OPTIONS_CHOICES[self.option]


@dataclasses.dataclass
class ResultsData:
    """Data to be passed to the results display frame
    """

    saved: bool = False
    # generated is True if generated or
    # False if retrieved from file
    generated: bool = True
    number_of_lines: int = 0
    stored_date: str = None
    lottery_type_name: str = ""
    data = []

    @classmethod
    def clear_data(cls) -> None:
        """Remove all data items

        :return: None
        """
        del cls.data[: cls.get_data_length()]

    @classmethod
    def is_retrieved(cls) -> bool:
        """Does the data come from a file

        :return: bool True if the data was returned from a saved file
        """
        return not cls.generated

    @classmethod
    def get_data_length(cls) -> int:
        """Return the number of results

        :return: the number of results in memory
        """
        return len(cls.data)

    @classmethod
    def get_data_item(cls, item: int) -> Union[str, None]:
        """Return a item of data

        :param item: the index of the required data
        :return: a string if valid data is held or None if not
        """
        if item < 0 or item > len(cls.data):
            return None
        return cls.data[item]

    @classmethod
    def set_data_item(cls, result: str) -> None:
        """Add a dat item to the list of results

        :param result: the data to append to the list of results
        :return: None
        """
        if result is not None:
            cls.data.append(result)
