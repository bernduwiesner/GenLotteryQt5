from PyQt5.QtWidgets import (QDesktopWidget,
                             QDialog,
                             QLabel,
                             QLayout,
                             QVBoxLayout,
                             QPushButton,
                             )
from PyQt5.QtCore import Qt
from common import ResultsData


class ResultsWindow(QDialog):
    """The generator results window
    """

    def __init__(self, parent, results):
        QDialog.__init__(self, parent)
        self.base_layout = QVBoxLayout(self)
        self.base_layout.sizeConstraint = QLayout.SetDefaultConstraint
        self.base_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.init_ui(results)

    def init_ui(self, results: ResultsData):
        """Create the controls on the frame

        :param results: the data to display
        :return:
        """

        def unwrap(some: str) -> str:
            """Remove characters "[". "]" and "'" from a string

            :param some: str the string to process
            :return:
            """
            return some.translate({ord(i): None for i in "[]'"})

        row: int = 0
        action: str = "Generated "  if results.generated else "Stored "
        label: str = action + results.lottery_type_name + " Lottery numbers"
        type_lbl = QLabel(label)
        self.base_layout.addWidget(type_lbl, row)

        row += 1
        for line in range(results.get_data_length()):
            data_item = unwrap(results.get_data_item(line))
            label = QLabel(f"Line {line + 1:02d}: " + data_item)
            self.base_layout.addWidget(label, line + 1)

        row += results.get_data_length()
        ok_btn = QPushButton("OK", self)
        ok_btn.resize(ok_btn.sizeHint())
        ok_btn.clicked.connect(self.close_window)
        self.base_layout.addWidget(ok_btn, row)

        # MainWindow
        self.setLayout(self.base_layout)
        win_x, win_y, win_width, win_height = (0, 0, 0, 0)
        self.setGeometry(win_x, win_y, win_width, win_height)
        self.setWindowTitle("Generated Results")
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

    def close_window(self, event) -> None:
        """Process the options chosen and perform the action chosen

        :param event: not used
        :return: None
        """
        self.close()
