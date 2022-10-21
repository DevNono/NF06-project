import sys
import random
import json
from PySide6 import QtCore, QtWidgets, QtGui

list_products = list()
filters = { "category": list(), "brand": list(), "year": 0 }
order_by = { "type": "nb_sold", "order": "desc" }

def hex2QColor(c):
    """Convert Hex color to QColor"""
    r=int(c[0:2],16)
    g=int(c[2:4],16)
    b=int(c[4:6],16)
    return QtGui.QColor(r,g,b)

class Product(object):
    _uid = int()
    _name = str()
    _price = float()
    _weight = float()
    _category = str()
    _brand = str()
    _year = int()
    _stock = int()
    _nb_sold = int()
    _review = float()

    def __init__(self, uid, name, price, weight, category, brand, year, stock, nb_sold, review):
        self._uid = uid
        self._name = name
        self._price = price
        self._weight = weight
        self._category = category
        self._brand = brand
        self._year = year
        self._stock = stock
        self._nb_sold = nb_sold
        self._review = review

def createProduct(uid, name, price, weight, category, brand, year, stock, nb_sold, review):
    product = Product(uid, name, price, weight, category, brand, year, stock, nb_sold, review)
    list_products.append(product)

def filterAndOrderProductList():
    list_products_filtered = list()
    for product in list_products:
        if product._category in filters["category"] and product._brand in filters["brand"] and product._year >= filters["year"]:
            list_products_filtered.append(product)

    if len(filters["category"]) == 0 and len(filters["brand"]) == 0 and filters["year"] == 0:
        list_products_filtered = list_products
    
    if order_by["type"] == "nb_sold":
        list_products_filtered.sort(key=lambda x: x._nb_sold, reverse=True)
    elif order_by["type"] == "stock":
        list_products_filtered.sort(key=lambda x: x._stock, reverse=True)
    elif order_by["type"] == "review":
        list_products_filtered.sort(key=lambda x: x._review, reverse=True)
    else:
        list_products_filtered.sort(key=lambda x: x._uid, reverse=True)

    return list_products_filtered

class Program(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # add font
        QtGui.QFontDatabase.addApplicationFont("assets/Poppins-Regular.ttf")
        QtGui.QFontDatabase.addApplicationFont("assets/Poppins-SemiBold.ttf")

        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.backgroundColor = hex2QColor("ffffff")
        self.foregroundColor = hex2QColor("eeeeee")

        self.draggable = True
        self.dragging_threshould = 5
        self.__mousePressPos = None
        self.__mouseMovePos = None

        self.borderRadius = 15

        self.setWindowTitle("e-Zone Manager")
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(20)
        self.topLayout = QtWidgets.QHBoxLayout()

        self.titles = QtWidgets.QVBoxLayout()
        self.title = QtWidgets.QLabel("e-Zone Manager")
        self.title.setFont(QtGui.QFont("Poppins SemiBold", 18))
        self.title.setStyleSheet("color: #000000;")
        self.subtitle = QtWidgets.QLabel("Gestionnaire de produits")
        self.subtitle.setFont(QtGui.QFont("Poppins Regular", 12))
        self.subtitle.setStyleSheet("color: #000000;")
        self.titles.addWidget(self.title)
        self.titles.addWidget(self.subtitle)
        self.topLayout.addWidget(self.titles)

        self.Button = QtWidgets.QPushButton()
        self.Button.setIcon(QtGui.QIcon("assets/export.svg"))
        self.Button.setToolTip("Exporter la liste des produits")
        self.Button.clicked.connect(self.exportProductListToJSON)
        self.topLayout.addWidget(self.Button)

        self.Button = QtWidgets.QPushButton()
        self.Button.setIcon(QtGui.QIcon("assets/import.svg"))
        self.Button.setToolTip("Importer une liste de produits")
        self.Button.clicked.connect(self.importProductListFromJSON)
        self.topLayout.addWidget(self.Button)

        self.midLayout = QtWidgets.QHBoxLayout()
        self.changePage = QtWidgets.QPushButton("Produits")
        self.midLayout.addWidget(self.changePage)
        self.filters = QtWidgets.QPushButton("Filtres")
        self.filters.setIcon(QtGui.QIcon("assets/filter.svg"))
        self.midLayout.addWidget(self.filters)


        self.bottomLayout = QtWidgets.QHBoxLayout()
        # self.rectangle = QtWidgets.QWidget()
        # self.rectangle.setStyleSheet("background-color: #12782D;")
        # self.bottomLayout.addWidget(self.rectangle)
        
        # -----------------------------------
        #             TABLE
        # -----------------------------------
        
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(["UID", "Nom", "Prix", "Poids", "Catégorie", "Marque", "Année", "Stock", "Nb Vendu", "Note"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("QTableWidget::item:selected {background-color: #12782D; color: #ffffff;}")
        self.table.data = filterAndOrderProductList()
        self.table.setRowCount(len(self.table.data))
        self.setData(self.table)
        self.bottomLayout.addWidget(self.table)

        # -----------------------------------
        #             STATISTICS
        # -----------------------------------
       
        # self.grid = QtWidgets.QGridLayout()
        # self.grid.setContentsMargins(0, 0, 0, 0)
        # self.grid.setSpacing(0)
        # self.bottomLayout.addLayout(self.grid)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.midLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

        with open("style.qss", "r") as f:
            _style = f.read()
            app.setStyleSheet(_style)

    def setData(self, table): 
        for i in range(len(table.data)):
            #enumerate
            for n, j in enumerate(table.data[i].__dict__.values()):
                item = QtWidgets.QTableWidgetItem(str(j))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(i, n, item)
    
    def exportProductListToJSON(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Exporter Fichier', filter="JSON (*.json)")

        if name[0] != "":
            with open(name[0], "w") as f:
                json.dump([product.__dict__ for product in list_products], f, indent = 4)

    def importProductListFromJSON(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Importer Fichier', filter="JSON (*.json)")
        if name[0] != "":
            list_products.clear()
            with open(name[0], 'r') as openfile:
                json_object = json.load(openfile)
                for product in json_object:
                    createProduct(product["_uid"], product["_name"], product["_price"], product["_weight"], product["_category"], product["_brand"], product["_year"], product["_stock"], product["_nb_sold"], product["_review"])
        self.table.data = filterAndOrderProductList()
        self.table.setRowCount(len(self.table.data))
        self.setData(self.table)
            
    def paintEvent(self, event):
        # get current window size
        s = self.size()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setPen(self.foregroundColor)
        qp.setBrush(self.backgroundColor)
        qp.drawRoundedRect(0, 0, s.width(), s.height(),
                           self.borderRadius, self.borderRadius)
        qp.end()

    def mousePressEvent(self, event):
        if self.draggable and event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPosition().toPoint()                # global
            self.__mouseMovePos = event.globalPosition().toPoint() - self.pos()    # local
        super(Program, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() & QtCore.Qt.LeftButton:
            globalPos = event.globalPosition().toPoint()
            moved = globalPos - self.__mousePressPos
            if moved.manhattanLength() > self.dragging_threshould:
                # move when user drag window more than dragging_threshould
                diff = globalPos - self.__mouseMovePos
                self.move(diff)
                self.__mouseMovePos = globalPos - self.pos()
        super(Program, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            if event.button() == QtCore.Qt.LeftButton:
                moved = event.globalPosition().toPoint() - self.__mousePressPos
                if moved.manhattanLength() > self.dragging_threshould:
                    # do not call click event or so on
                    event.ignore()
                self.__mousePressPos = None
        super(Program, self).mouseReleaseEvent(event)

        # close event
        if event.button() == QtCore.Qt.RightButton:
            QtGui.qApp.exit()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    createProduct("1", "Produit 1", 10, 1, "Catégorie 1", "Marque 1", 2020, 10, 0, 0)

    program = Program()
    program.resize(800, 600)
    program.show()

    sys.exit(app.exec())