import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.buttonPert = QtWidgets.QPushButton("Afficher le graphe de la méthode PERT")
        self.buttonGantt = QtWidgets.QPushButton("Afficher le diagramme de GANTT")
        self.buttonTasks = QtWidgets.QPushButton("Réalisation des tâches")
        

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.buttonPert)
        self.layout.addWidget(self.buttonGantt)
        self.layout.addWidget(self.buttonTasks)

        self.buttonPert.clicked.connect(self.pert)
        self.buttonGantt.clicked.connect(self.gantt)
        self.buttonTasks.clicked.connect(self.tasks)

    @QtCore.Slot()
    def pert(self):
        print("Pert")
    
    @QtCore.Slot()
    def gantt(self):
        print("Gantt")

    @QtCore.Slot()
    def tasks(self):
        print("Tasks")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())