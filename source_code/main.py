import sys
from source_code.system_info_widget import SystemInfoWidget
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)

    widget = SystemInfoWidget()
    widget.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()