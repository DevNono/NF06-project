from ctypes import alignment
import sys
import random
import json
import numpy as np
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
        if (len(filters["category"]) == 0 or product._category in filters["category"]) and (len(filters["brand"]) == 0 or product._brand in filters["brand"]) and (filters["year"] == 0 or product._year >= filters["year"]):
            list_products_filtered.append(product)

    if len(filters["category"]) == 0 and len(filters["brand"]) == 0 and filters["year"] == 0:
        list_products_filtered = list_products
    
    if order_by["type"] == "nb_sold":
        if order_by["order"] == "desc":
            list_products_filtered.sort(key=lambda x: x._nb_sold, reverse=True)
        else:
            list_products_filtered.sort(key=lambda x: x._nb_sold, reverse=False)
    elif order_by["type"] == "stock":
        if order_by["order"] == "desc":
            list_products_filtered.sort(key=lambda x: x._stock, reverse=True)
        else:
            list_products_filtered.sort(key=lambda x: x._stock, reverse=False)
    elif order_by["type"] == "review":
        if order_by["order"] == "desc":
            list_products_filtered.sort(key=lambda x: x._review, reverse=True)
        else:
            list_products_filtered.sort(key=lambda x: x._review, reverse=False)
    else:
        list_products_filtered.sort(key=lambda x: x._uid, reverse=False)

    return list_products_filtered

class OrderByDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(OrderByDialog, self).__init__(parent)
        self.setWindowTitle("Order by")

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel("Order by")
        self.layout.addWidget(self.label)

        self.combo = QtWidgets.QComboBox()
        self.combo.addItems(["Nombre de commandes", "Quantité", "Avis"])

        if order_by["type"] == "nb_sold":
            self.combo.setCurrentIndex(0)
        elif order_by["type"] == "stock":
            self.combo.setCurrentIndex(1)
        elif order_by["type"] == "review":
            self.combo.setCurrentIndex(2)
        
        self.layout.addWidget(self.combo)

        self.ascend = QtWidgets.QRadioButton("Ascend")
        self.desc = QtWidgets.QRadioButton("Descend")
        if order_by["order"] == "asc":
            self.ascend.setChecked(True)
        else:
            self.desc.setChecked(True)

        self.layout.addWidget(self.ascend)
        self.layout.addWidget(self.desc)

        self.button = QtWidgets.QPushButton("OK")
        self.button.clicked.connect(lambda: self.onOK(parent))
        self.layout.addWidget(self.button)

    def onOK(self, parent):
        global order_by
        if self.combo.currentIndex() == 0:
            order_by["type"] = "nb_sold"
        elif self.combo.currentIndex() == 1:
            order_by["type"] = "stock"
        elif self.combo.currentIndex() == 2:
            order_by["type"] = "review"

        if self.ascend.isChecked():
            order_by["order"] = "asc"
        else:
            order_by["order"] = "desc"

        parent.updateProductList()
        self.close()

class FiltersDialog(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()

        list_category = list()
        list_brand = list()
        for product in list_products:
            if product._category not in list_category:
                list_category.append(product._category)
            if product._brand not in list_brand:
                list_brand.append(product._brand)

        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.layout = QtWidgets.QVBoxLayout()

        self.filters_category = QtWidgets.QGroupBox("Category")
        self.layout_filters_category = QtWidgets.QVBoxLayout()
        self.filters_category.setLayout( self.layout_filters_category)
        self.filters_category.setCheckable(True)
        self.filters_category.setChecked(False)
        if(len(filters["category"]) > 0):
            self.filters_category.setChecked(True)
       

        self.filters_category_button = list()
        for category in list_category:
            button = QtWidgets.QCheckBox(category)
            if (category in filters["category"]):
                button.setChecked(True)
            self.filters_category_button.append(button)
            self.layout_filters_category.addWidget(button)
        self.layout.addWidget(self.filters_category)

        self.filters_brand = QtWidgets.QGroupBox("Brand")
        self.layout_filters_brand = QtWidgets.QVBoxLayout()
        self.filters_brand.setLayout(self.layout_filters_brand)
        self.filters_brand.setCheckable(True)
        self.filters_brand.setChecked(False)
        if(len(filters["brand"]) > 0):
            self.filters_brand.setChecked(True)
        
        self.filters_brand_button = list()
        for brand in list_brand:
            button = QtWidgets.QCheckBox(brand)
            if (brand in filters["brand"]):
                button.setChecked(True)
            self.filters_brand_button.append(button)
            self.layout_filters_brand.addWidget(button)
        self.layout.addWidget(self.filters_brand)

        self.filters_year = QtWidgets.QGroupBox("Année de sortie (>=)")
        self.layout_filters_year = QtWidgets.QVBoxLayout()
        self.filters_year.setLayout(self.layout_filters_year)
        self.filters_year.setCheckable(True)
        self.filters_year.setChecked(False)
        self.filters_year_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.filters_year_slider.setMinimum(1980)
        self.filters_year_slider.setMaximum(2021)
        self.filters_year_slider.setValue(filters["year"])
        self.filters_year_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.filters_year_slider.setTickInterval(10)
        self.layout_filters_year.addWidget(self.filters_year_slider)
        self.layout.addWidget(self.filters_year)

        self.apply_button = QtWidgets.QPushButton("Apply")
        self.apply_button.clicked.connect(lambda: self.on_apply_button_clicked(parent))
        self.layout.addWidget(self.apply_button)

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel_button_clicked)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)
    
    def on_apply_button_clicked(self, parent):
        global filters
        filters["category"] = list()
        filters["brand"] = list()
        for button in self.filters_category_button:
            if button.isChecked():
                filters["category"].append(button.text())
        for button in self.filters_brand_button:
            if button.isChecked():
                filters["brand"].append(button.text())
        if(self.filters_year_slider.value() != 1980):
            filters["year"] = self.filters_year_slider.value()
        else:
            filters["year"] = 0
        print(filters)
        parent.updateProductList()
        self.close()

    def on_cancel_button_clicked(self):
        self.close()




class Color(QtWidgets.QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
        self.setPalette(palette)








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
        self.topLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.setSpacing(0)

        self.titles = QtWidgets.QVBoxLayout()

        self.titles.setContentsMargins(-20, -20, -20, -20)
        self.titles.setSpacing(0)
        self.title = QtWidgets.QLabel("e-Zone Manager")
        self.title.setFont(QtGui.QFont("Poppins SemiBold", 17))
        self.title.setStyleSheet("color: #000000;")

        self.subtitle = QtWidgets.QLabel("Gestionnaire de produits")
        self.subtitle.setFont(QtGui.QFont("Poppins Regular", 11))
        self.subtitle.setStyleSheet("color: #CBCBCB;")

        self.titles.addWidget(self.title)
        self.titles.addWidget(self.subtitle)
        self.topLayout.addLayout(self.titles)

        self.topRightLayout = QtWidgets.QHBoxLayout()
        self.topRightLayout.setContentsMargins(0, 0, 0, 0)
        self.topRightLayout.setSpacing(10)
        self.topRightLayout.addStretch()
        
        self.Button = QtWidgets.QPushButton()
        self.Button.setIcon(QtGui.QIcon("assets/export.svg"))
        self.Button.setToolTip("Exporter la liste des produits")
        self.Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Button.clicked.connect(self.exportProductListToJSON)
        self.topRightLayout.addWidget(self.Button)

        self.Button = QtWidgets.QPushButton()
        self.Button.setIcon(QtGui.QIcon("assets/import.svg"))
        self.Button.setToolTip("Importer une liste de produits")
        self.Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Button.clicked.connect(self.importProductListFromJSON)
        self.topRightLayout.addWidget(self.Button)

        self.topLayout.addLayout(self.topRightLayout)

        self.midLayout = QtWidgets.QHBoxLayout()
        self.changePage = QtWidgets.QPushButton("Produits")
        self.midLayout.addWidget(self.changePage)
        self.orderby = QtWidgets.QPushButton("Trier par")
        self.orderby.setIcon(QtGui.QIcon("assets/orderby.svg"))
        self.orderby.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.orderby.clicked.connect(self.showOrderBy)
        self.midLayout.addWidget(self.orderby)
        self.filters = QtWidgets.QPushButton("Filtres")
        self.filters.setIcon(QtGui.QIcon("assets/filter.svg"))
        self.filters.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.filters.clicked.connect(self.showFilters)
        self.midLayout.addWidget(self.filters)


        self.bottomLayout = QtWidgets.QStackedLayout()
        
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
        self.table.data = filterAndOrderProductList()
        self.table.setRowCount(len(self.table.data))
        self.setData(self.table)
        self.bottomLayout.addWidget(self.table)

        # -----------------------------------
        #             STATISTICS
        # -----------------------------------
       
        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.totalSellingsEuros = QtWidgets.QLabel("0")
        self.totalSellingsEuros.setFont(QtGui.QFont("Poppins SemiBold", 20))
        self.totalSellingsEuros.setStyleSheet("color: #000000;")
        self.totalSellingsEurosTitle = QtWidgets.QLabel("Ventes totales (€)")
        self.totalSellingsEurosTitle.setFont(QtGui.QFont("Poppins Regular", 11))
        self.totalSellingsEurosTitle.setStyleSheet("color: #CBCBCB;")
        self.totalSellingsEurosLayout = QtWidgets.QVBoxLayout()
        self.totalSellingsEurosLayout.addWidget(self.totalSellingsEuros)
        self.totalSellingsEurosLayout.addWidget(self.totalSellingsEurosTitle)
        self.totalSellingsEurosLayout.setContentsMargins(0, 0, 0, 0)
        self.totalSellingsEurosLayout.setSpacing(0)
        self.totalSellingsEurosWidget = QtWidgets.QWidget()
        self.totalSellingsEurosWidget.setLayout(self.totalSellingsEurosLayout)
        self.totalSellingsEurosWidget.setStyleSheet("background-color: #F2F2F2;")
        self.totalSellingsEurosWidget.setContentsMargins(0, 0, 0, 0)

        self.grid.addWidget(self.totalSellingsEurosWidget, 0, 0, 2, 1)
        self.grid.addWidget(Color('blue'), 2, 0, 2, 1)
        self.grid.addWidget(Color('green'), 4, 0, 2, 1)

        self.grid.addWidget(Color('yellow'), 0, 2, 3, 2)
        self.grid.addWidget(Color('purple'), 3, 2, 3, 2)

        self.gridWidget = QtWidgets.QWidget()
        self.gridWidget.setLayout(self.grid)
        self.bottomLayout.addWidget(self.gridWidget)

        self.bottomLayout.setCurrentIndex(1)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.midLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

        with open("style.qss", "r") as f:
            _style = f.read()
            app.setStyleSheet(_style)
    
    def showOrderBy(self):
        self.orderBy = OrderByDialog(self)
        self.orderBy.show()

    def showFilters(self):
        self.filtersDialog = FiltersDialog(self)
        self.filtersDialog.show()
        
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
            self.updateProductList()
        
    def updateProductList(self):
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

    program = Program()
    program.resize(800, 600)
    program.show()

    sys.exit(app.exec())