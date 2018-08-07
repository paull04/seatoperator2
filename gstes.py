from give_score_to_each_seat import Ui_Dialog
from PyQt5.QtWidgets import QDialog, QApplication


class GsTes(Ui_Dialog, QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        self.setupUi(self)
        self.check_dict = {
            'how noisy': 0,
            'how friendly with couple': 0,
            'how visible': 0,
            'learning achieve': 0
        }

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main = GsTes()
    main.show()
    sys.exit(app.exec_())
