#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import sys
from argparse import ArgumentParser, RawTextHelpFormatter

from PySide6.QtWidgets import QApplication

from PreDoCS.ResultsViewer.ui.MainWindow import MainWindow
from PreDoCS.util.globals import core_init


def main():
    argument_parser = ArgumentParser(
        description='PreDoCS Results Viewer. Displays results from PreDoCS Solver.',
        formatter_class=RawTextHelpFormatter
    )
    argument_parser.add_argument(
        "file",
        help='Optimisation model file (mostly "optimisation_model.bin")',
        type=str,
        nargs='?',
    )
    options = argument_parser.parse_args()

    app = QApplication(sys.argv)
    app.setOrganizationName('DLR-FA')
    app.setOrganizationDomain('dlr.de/fa')
    app.setApplicationName('PreDoCS Results Viewer')

    # Logging
    core_init('.')

    # Main Window
    main_win = MainWindow()
    if options.file:
        main_win.load_file(options.file)
    main_win.show()
    app.exec_()


if __name__ == '__main__':
    main()
