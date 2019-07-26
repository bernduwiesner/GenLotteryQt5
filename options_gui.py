#
#   Copyright (c) 2019 Bernd Wiesner. bernduwiesner@yahoo.co.uk
#   All rights reserved
#
"""Lottery generator options interface
"""
from PyQt5.QtWidgets import (QAction,
                             qApp,
                             QApplication,
                             QComboBox,
                             QDesktopWidget,
                             QHBoxLayout,
                             QLabel,
                             QLayout,
                             QLineEdit,
                             QMainWindow,
                             QMessageBox,
                             QPushButton,
                             QRadioButton,
                             QVBoxLayout,
                             QWidget,
                             )
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from pathlib import Path
from random import sample
from typing import List, Union
import shelve
import time
from common import OptionsData, ResultsData
import constants as C
from data_gui import ResultsWindow


class MainWindow(QMainWindow):
    """The main window used for selecting options
    """

    def __init__(self):
        QMainWindow.__init__(self)
        self.options_data = OptionsData()
        self._saved_file: str = C.SAVE_FILE_DIR +\
            self.options_data.get_lottery_name()
        self.central_widget = QWidget(self)
        self.base_layout = QVBoxLayout(self.central_widget)
        self.base_layout.sizeConstraint = QLayout.SetDefaultConstraint
        self.base_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setCentralWidget(self.central_widget)
        self.init_ui()

    def init_ui(self):
        """ Add the controls to the window and window settings

        :return:
        """
        # self.setUnifiedTitleAndToolBarOnMac(True)

        # statusBar
        self.statusBar().showMessage("Ready")

        # Menus
        menu = self.menuBar()
        # Put the menu in the MainWindow on Mac OS
        menu.setNativeMenuBar(False)
        file_mnu = menu.addMenu('&File')
        exit_itm = QAction("&Exit", self)
        exit_itm.setShortcut('Ctrl+Q')
        exit_itm.setStatusTip('Exit application')
        exit_itm.triggered.connect(qApp.quit)
        file_mnu.addAction(exit_itm)
        help_mnu = menu.addMenu("&Help")
        about_itm = QAction("&About", self)
        about_itm.setStatusTip("About this application")
        about_itm.triggered.connect(self.show_about)
        help_mnu.addAction(about_itm)

        # widgets
        row: int = 0
        h_box1 = QHBoxLayout()
        h_box1.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        tip = "Choose the type of lottery to generate numbers for"
        type_lbl = QLabel("Lottery type:")
        type_lbl.setToolTip(tip)
        type_cbo = QComboBox()
        type_cbo.setToolTip(tip)
        type_cbo.activated.connect(self.lottery_type_changed)
        type_cbo.addItems(C.LOTTERY_CHOICES)
        type_cbo.setCurrentIndex(C.LOTTERY_DEFAULT)
        type_cbo.resize(type_cbo.sizeHint())
        type_cbo.setEditable(False)
        type_lbl.setBuddy(type_cbo)
        h_box1.addWidget(type_lbl)
        h_box1.addWidget(type_cbo, 0, Qt.AlignLeft)
        self.base_layout.addLayout(h_box1, row)

        row += 1
        h_box2 = QHBoxLayout()
        h_box2.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        tip: str = f"Enter a number in the range: {C.MIN_LINES}-{C.MAX_LINES}"
        lines_lbl = QLabel("Number of lines:")
        lines_lbl.setToolTip(tip)
        lines_lbl.setFixedWidth(100)
        lines_edt = QLineEdit(self)
        lines_edt.setToolTip(tip)
        lines_edt.setText(str(C.DEFAULT_LINES))
        regexp = QRegExp('^([0]?[0-9]?[0-9])$')
        validator = QRegExpValidator(regexp)
        lines_edt.setValidator(validator)
        lines_edt.setFixedWidth(40)
        lines_edt.textEdited.connect(self.number_of_lines_changed)
        lines_lbl.setBuddy(lines_edt)
        h_box2.addWidget(lines_lbl)
        h_box2.addWidget(lines_edt, 0, Qt.AlignLeft)
        self.base_layout.addLayout(h_box2, row)

        row += 1
        h_box3 = QHBoxLayout()
        h_box3.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        action_btn0 = QRadioButton(C.OPTIONS_CHOICES[0])
        action_btn0.clicked.connect(lambda: self.action_clicked(0))
        h_box3.addWidget(action_btn0)
        action_btn1 = QRadioButton(C.OPTIONS_CHOICES[1])
        action_btn1.setChecked(True)
        action_btn1.clicked.connect(lambda: self.action_clicked(1))
        h_box3.addWidget(action_btn1)
        action_btn2 = QRadioButton(C.OPTIONS_CHOICES[2])
        action_btn2.clicked.connect(lambda: self.action_clicked(2))
        h_box3.addWidget(action_btn2)
        action_btn3 = QRadioButton(C.OPTIONS_CHOICES[3])
        action_btn3.clicked.connect(lambda: self.action_clicked(3))
        h_box3.addWidget(action_btn3)
        self.base_layout.addLayout(h_box3, row)

        row += 1
        h_box4 = QHBoxLayout()
        h_box4.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        ok_btn = QPushButton("OK", self)
        ok_btn.resize(ok_btn.sizeHint())
        ok_btn.clicked.connect(self.ok_clicked)
        cancel_btn = QPushButton("Cancel", self)
        instance = QApplication.instance()
        cancel_btn.clicked.connect(instance.quit)
        cancel_btn.resize(cancel_btn.sizeHint())
        h_box4.addWidget(ok_btn)
        h_box4.addWidget(cancel_btn)
        self.base_layout.addLayout(h_box4, row)

        # MainWindow
        win_x, win_y, win_width, win_height = (0, 0, 0, 0)
        self.setGeometry(win_x, win_y, win_width, win_height)
        self.setWindowTitle("Lottery Number Generator")
        self.centre()
        self.show()

    def centre(self) -> None:
        """Centre the window on the screen

        :return: None
        """
        geometry = self.frameGeometry()
        centre = QDesktopWidget().availableGeometry().center()
        geometry.moveCenter(centre)
        self.move(geometry.topLeft())

    def show_about(self) -> None:
        """Display about MessageBox

        :return: None
        """
        QMessageBox.about(self, "About",
                          "Lottery Generator\n\n"
                          "Version: 0.0.1\n\n"
                          "Author: Bernd U. Wiesner\n\n"
                          "(c) Copyright 2019-"
                          )

    def update_status(self, text=None) -> None:
        """Utility function used to update the status bar
        :param text: text to display
        :return: None
        """
        status_bar = self.statusBar()
        if text is None:
            status_bar.showMessage(f"OPTIONS - Action: "
                                   f"{ self.options_data.get_option_name()}"
                                   f", Type: "
                                   f"{ self.options_data.get_lottery_name()}"
                                   f", Lines: "
                                   f"{ self.options_data.number_of_lines}"
                                   )
        else:
            status_bar.showMessage(text)

    def lottery_type_changed(self, value: int) -> None:
        """A lottery type has been chosen

        :param value: the index number of the type of lottery chosen
        :return: None
        """
        print(f"Lottery type = {C.LOTTERY_CHOICES[value]}")
        opt = self.options_data
        opt.lottery_type = value
        self.update_status()

    def number_of_lines_changed(self, text: str) -> None:
        """The number of lines to be generated was chosen

        :param text: the number of lines to generate as a string
        :return: None
        """
        self.options_data.number_of_lines = int(text)
        self.update_status()

    def action_clicked(self, action: int) -> None:
        """The user chose an action to perform

        :param action: the action the user has chosen
        :return: None
        """
        self.options_data.option = action
        self.update_status()

    def ok_clicked(self, event) -> None:
        """Process the options chosen and perform the action chosen

        :param event: not used
        :return: None
        """
        if self.options_data.option == 3:
            self.delete_saved_file()
        elif self.options_data.option == 2:
            self.show_saved()
        else:
            self.generate_numbers()

    def closeEvent(self, event) -> None:
        """Make sure the user wants to quit

        :param event: this is a system event to close the window
        :return: None
        """
        msg_box = QMessageBox
        reply = msg_box.question(self,
                                 "Quit",
                                 "Are you sure you want to quit?",
                                 msg_box.Yes | msg_box.No,
                                 msg_box.No,
                                 )

        if reply == msg_box.Yes:
            event.accept()
        else:
            event.ignore()

    def generate_numbers(self) -> None:
        """Generate several random numbers and optionally save them
        :return:
        """

        def add_leading_zero(values: List) -> List:
            """Add a leading zero to numbers in the list < 10
            :param values: list of numbers
            :return: array containing formatted numbers
            """
            return [f"{v:02d}" for v in values]

        def choose_numbers(maximum: int, quantity: int) -> List:
            """Generate the random numbers required
            :param maximum: the highest number to choose from
            :param quantity: the number of numbers to generate
            :return: a sorted list of generated numbers
            """
            valid_range: range = range(C.RULE_START, maximum)
            return add_leading_zero(sorted(sample(valid_range, quantity)))

        result = ResultsData
        result.clear_data()

        opt = self.options_data
        result.lottery_type_name = opt.get_lottery_name()
        result.number_of_lines = opt.number_of_lines

        main_max, main_qty,\
            extra_max, extra_qty = C.RULES[opt.get_lottery_name()]

        shelf = None
        result.generated = True
        if opt.option == 1:
            msg: str = "The generated numbers have not been saved"
            result.saved = False
            self.update_status(msg)
        else:
            result.saved = True
            directory = Path(C.SAVE_FILE_DIR)
            if not directory.exists():
                directory.mkdir(parents=True)
            shelf = shelve.open(filename=self._saved_file,
                                protocol=C.SHELF_PROTOCOL)
            shelf[C.SHELF_ARGS["DATE"]] = time.time()
            shelf[C.SHELF_ARGS["TYPE"]] = C.LOTTERY_CHOICES[opt.lottery_type]
            shelf[C.SHELF_ARGS["LINES"]] = opt.number_of_lines

        # count the actual number of lines generated
        count: int = 0
        # generate the required number of lines
        for _ in range(opt.number_of_lines):
            # x_1 holds the first group of numbers generated
            # main_max is the the highest number to generate plus 1
            # main_qty is the quantity of numbers to generate each line
            x_1: List[str] = choose_numbers(maximum=main_max,
                                            quantity=main_qty)

            # x_2 holds the secondary group of numbers generated if
            # any are required
            # extra_max is the the highest number to generate plus 1
            # extra_qty is the quantity of numbers to
            # generate in each line
            x_2: List[Union[str, None]] = [None]
            # only generate the second group of numbers if required
            # if extra_qty > 0
            if extra_qty:
                x_2 = choose_numbers(maximum=extra_max, quantity=extra_qty)
            # If shelf is None it means no_save was specified
            if shelf is not None:
                shelf[C.SHELF_ARGS["PART1"] + str(count)] = x_1
                # Save the extra numbers even if there are none to save
                # will return None on subsequent reading
                shelf[C.SHELF_ARGS["PART2"] + str(count)] = x_2
            count += 1
            if x_2 == [None]:
                result.data.append(str(x_1))
            else:
                result.data.append(str(x_1) + " - " + str(x_2))
        # close the save file if there is one
        if opt.get_option_name() != C.OPTIONS_CHOICES[1]:
            shelf.close()
        test: bool = opt.get_option_name() == C.OPTIONS_CHOICES[1]
        msg: str = (
            f"The numbers have{' not' if test else ''}"
            f" been saved and {count} lines were generated"
        )
        self.update_status(msg)
        frm = ResultsWindow(self, result)

    def delete_saved_file(self) -> None:
        """Delete a previously saved file
        :return: None
        """
        # add the filename extension
        file_name: str = self._saved_file + C.SAVE_FILE_TYPE
        path = Path(file_name)
        file_exists: bool = path.exists()
        if file_exists:
            path.unlink()
        msg: str = f"File: <{file_name}> was "\
            f"{'deleted' if file_exists else 'not found'}"
        self.update_status(msg)

    def show_saved(self) -> None:
        """Display a previously generated and saved batch of numbers
        :return: None
        """
        opt = self.options_data
        # add the filename extension
        path = Path(self._saved_file + C.SAVE_FILE_TYPE)
        if path.exists() and path.is_file():
            shelf = shelve.open(
                filename=self._saved_file,
                flag=C.SHELF_READONLY,
                protocol=C.SHELF_PROTOCOL,
            )
            save_time = time.localtime(shelf[C.SHELF_ARGS["DATE"]])
            result = ResultsData
            result.clear_data()

            result.saved = False
            result.generated = False
            result.lottery_type_name = opt.get_lottery_name()
            result.stored_date = time.strftime(C.DATE_FORMAT, save_time)
            count: int = 0
            for line in range(shelf[C.SHELF_ARGS["LINES"]]):
                # Don't display second group if none exist
                x_1: List[str] = shelf[C.SHELF_ARGS["PART1"] + str(line)]
                x_2: List[Union[str, None]] = shelf[C.SHELF_ARGS["PART2"]
                                                    + str(line)]
                if x_2 == [None]:
                    result.set_data_item(str(x_1))
                else:
                    result.set_data_item(str(x_1) + " - " + str(x_2))
                count += 1
            result.number_of_lines = count
            shelf.close()
            frm = ResultsWindow(self, result)
        else:
            msg: str = f"File <{path}> is missing"
            self.update_status(msg)
