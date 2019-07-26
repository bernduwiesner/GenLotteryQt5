#!/usr/bin/env python3
#
#   Copyright (c) 2019 Bernd Wiesner. bernduwiesner@yahoo.co.uk
#   All rights reserved
#
"""Lottery generator using pyQt5
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
import constants as C
from options_gui import MainWindow


def main() -> None:
    """Application main

    :return: None
    """

    app = QApplication([])
    app.setStyle("macintosh")
    app.setFont(QFont(C.FONT_FACE, C.FONT_POINT_SIZE))
    _ = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
