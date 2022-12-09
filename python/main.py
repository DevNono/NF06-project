from ctypes import alignment
import sys
import random
import matplotlib
import json
import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

list_products = list()
filters = { "category": list(), "brand": list(), "year": 0 }
order_by = { "type": "nb_sold", "order": "desc" }
to_export = list()
trucksize = 0

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

def getTotalSellingsEuros():
    total = 0
    for product in list_products:
        total += product._nb_sold * product._price
    return total

def getProduct(is_best, category = None, brand = None):
    if(category == None and brand == None):
        return None
    if(brand == None):
        products = list(filter(lambda x: x._category == category, list_products))
        if(is_best):
            products.sort(key=lambda x: x._nb_sold, reverse=False)
        else:
            products.sort(key=lambda x: x._nb_sold, reverse=True)
        
        if(len(products) > 0):
            return products[0]
        else:
            return None
    elif(category == None):
        products = list(filter(lambda x: x._brand == brand, list_products))
        if(is_best):
            products.sort(key=lambda x: x._nb_sold, reverse=False)
        else:
            products.sort(key=lambda x: x._nb_sold, reverse=True)

        if(len(products) > 0):
            return products[0]
        else:
            return None
    else:
        return None

def getTotalSellingsByBrand(brand):
    total = 0
    for product in list_products:
        if product._brand == brand:
            total += product._nb_sold * product._price
    return total

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
class AddProductDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AddProductDialog, self).__init__(parent)
        self.setWindowTitle("Ajouter un produit")

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel("Ajouter un produit")
        self.layout.addWidget(self.label)

        self.name = QtWidgets.QLineEdit()
        self.name.setPlaceholderText("Nom")
        self.layout.addWidget(self.name)

        self.price = QtWidgets.QLineEdit()
        self.price.setPlaceholderText("Prix")
        self.layout.addWidget(self.price)

        self.weight = QtWidgets.QLineEdit()
        self.weight.setPlaceholderText("Poids")
        self.layout.addWidget(self.weight)

        self.category = QtWidgets.QLineEdit()
        self.category.setPlaceholderText("Catégorie")
        self.layout.addWidget(self.category)

        self.brand = QtWidgets.QLineEdit()
        self.brand.setPlaceholderText("Marque")
        self.layout.addWidget(self.brand)

        self.year = QtWidgets.QLineEdit()
        self.year.setPlaceholderText("Année")
        self.layout.addWidget(self.year)

        self.stock = QtWidgets.QLineEdit()
        self.stock.setPlaceholderText("Stock")
        self.layout.addWidget(self.stock)

        self.button = QtWidgets.QPushButton("OK")
        self.button.clicked.connect(lambda: self.onOK(parent))
        self.layout.addWidget(self.button)

    def onOK(self, parent):
        global list_products
        uid = len(list_products) + 1
        name = self.name.text()
        price = float(self.price.text())
        weight = float(self.weight.text())
        category = self.category.text()
        brand = self.brand.text()
        year = int(self.year.text())
        stock = int(self.stock.text())
        review = 0
        nb_sold = 0
        product = Product(uid, name, price, weight, category, brand, year, stock, review, nb_sold)
        list_products.append(product)

        parent.updateProductList()
        self.close()
class ExportProductsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ExportProductsDialog, self).__init__(parent)
        self.setWindowTitle("Exporter des produits")

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel("Exporter des produits")
        self.layout.addWidget(self.label)

        self.index = 0

        if(self.index <= len(list_products) - 1):
            self.product = list_products[self.index]
            self.name = QtWidgets.QLabel(self.product._name)
            self.layout.addWidget(self.name)

            self.brand = QtWidgets.QLabel(self.product._brand)
            self.layout.addWidget(self.brand)

            self.stock = QtWidgets.QLabel(str(self.product._stock))
            self.layout.addWidget(self.stock)

            self.category = QtWidgets.QLabel(self.product._category)
            self.layout.addWidget(self.category)

            self.quantity = QtWidgets.QSpinBox()
            self.quantity.setMinimum(0)
            self.quantity.setMaximum(self.product._stock)
            self.quantity.setValue(0)
            self.layout.addWidget(self.quantity)

        self.button = QtWidgets.QPushButton("OK")
        self.button.clicked.connect(lambda: self.onOK(parent))
        self.layout.addWidget(self.button)

    def onOK(self, parent):
        if(self.index < len(list_products) - 1):
            to_export.append({
                self.product._name,
                self.product._weight,
                self.product._price,
                self.quantity.value()
            })
            self.index += 1
            self.product = list_products[self.index]
            self.name.setText(self.product._name)
            self.brand.setText(self.product._brand)
            self.stock.setText(str(self.product._stock))
            self.category.setText(self.product._category)
            self.quantity.setMinimum(0)
            self.quantity.setMaximum(self.product._stock)
            self.quantity.setValue(0)
        elif(self.index == len(list_products) - 1):
            to_export.append({
                self.product._name,
                self.product._weight,
                self.product._price,
                self.quantity.value()
            })
            self.index += 1

            self.layout.removeWidget(self.name)
            self.layout.removeWidget(self.brand)
            self.layout.removeWidget(self.stock)
            self.layout.removeWidget(self.category)
            self.layout.removeWidget(self.quantity)
            self.layout.removeWidget(self.button)

            self.name.deleteLater()
            self.brand.deleteLater()
            self.stock.deleteLater()
            self.category.deleteLater()
            self.quantity.deleteLater()

            self.truckWeight = QtWidgets.QLineEdit()
            self.truckWeight.setPlaceholderText("Poids du camion")
            self.layout.addWidget(self.truckWeight)
            self.layout.addWidget(self.button)
        else:
            if(self.truckWeight.text() == ""):
                return
            trucksize = float(self.truckWeight.text())
            print(trucksize)
            print(to_export)
            # TODO: Add export function (cf. Gaudry)
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
        self.filters_category.setLayout(self.layout_filters_category)
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
        parent.updateProductList()
        self.close()

    def on_cancel_button_clicked(self):
        self.close()
class Program(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # add font
        QtGui.QFontDatabase.addApplicationFont("assets/Poppins-Regular.ttf")
        QtGui.QFontDatabase.addApplicationFont("assets/Poppins-SemiBold.ttf")

        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.backgroundColor = QtGui.QColor(255,255,255)
        self.foregroundColor = QtGui.QColor(238,238,238)

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
        self.Button.setIcon(QtGui.QIcon("assets/deliver.svg"))
        self.Button.setToolTip("Exporter des produits (livraison)")
        self.Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Button.clicked.connect(self.exportProducts)
        self.topRightLayout.addWidget(self.Button)

        self.Button = QtWidgets.QPushButton()
        self.Button.setIcon(QtGui.QIcon("assets/add.svg"))
        self.Button.setToolTip("Ajouter un produit")
        self.Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Button.clicked.connect(self.addProduct)
        self.topRightLayout.addWidget(self.Button)
        
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
        self.changePages = QtWidgets.QPushButton("Statistiques")
        self.changePages.clicked.connect(self.changePage)
        self.midLayout.addWidget(self.changePages)
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

        # Ventes totales

        self.totalSellingsEuros = QtWidgets.QLabel("0")
        self.totalSellingsEuros.setAlignment(QtCore.Qt.AlignCenter)
        self.totalSellingsEuros.setFont(QtGui.QFont("Poppins SemiBold", 20))
        self.totalSellingsEuros.setStyleSheet("color: #000000;")
        self.totalSellingsEurosTitle = QtWidgets.QLabel("Ventes totales (€)")
        self.totalSellingsEurosTitle.setFont(QtGui.QFont("Poppins Regular", 11))
        self.totalSellingsEurosTitle.setStyleSheet("color: #CBCBCB;")
        self.totalSellingsEurosLayout = QtWidgets.QVBoxLayout()
        self.totalSellingsEurosLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.totalSellingsEurosLayout.addWidget(self.totalSellingsEuros)
        self.totalSellingsEurosLayout.addWidget(self.totalSellingsEurosTitle)
        self.totalSellingsEurosLayout.setContentsMargins(0, 0, 0, 0)
        self.totalSellingsEurosLayout.setSpacing(0)
        self.totalSellingsEurosWidget = QtWidgets.QWidget()
        self.totalSellingsEurosWidget.setLayout(self.totalSellingsEurosLayout)
        self.totalSellingsEurosWidget.setStyleSheet("background-color: #F2F2F2;")
        self.totalSellingsEurosWidget.setContentsMargins(0, 0, 0, 0)

        # Graph of number of products per category using matplotlib
        self.graphLayout = QtWidgets.QVBoxLayout()
        self.graphLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.graphLayout.setContentsMargins(0, 0, 0, 0)
        self.graphLayout.setSpacing(0)
        self.graphWidget = QtWidgets.QWidget()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Nombre de produits par catégorie")
        self.ax.set_xlabel("")
        self.ax.set_ylabel("Nombre de produits")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_facecolor("#F2F2F2")
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["bottom"].set_visible(False)
        self.ax.spines["left"].set_visible(False)
    

        self.categories = []
        self.productsPerCategory = []
        for product in self.table.data:
            if product["category"] not in self.categories:
                self.categories.append(product["category"])
                self.productsPerCategory.append(1)
            else:
                self.productsPerCategory[self.categories.index(product["category"])] += 1
        self.ax.bar(self.categories, self.productsPerCategory, color="#000000")
        self.canvas.draw()
        self.canvas.setContentsMargins(0, 0, 0, 0)
        self.canvas.setStyleSheet("background-color: #F2F2F2;")
        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.graphLayout.addWidget(self.canvas)
        self.graphWidget.setLayout(self.graphLayout)
        

        self.list_category = list()
        self.list_brand = list()

        # Graph of total sales per brand using matplotlib and a select menu to choose the category
        self.totalSellingsByBrandLayout = QtWidgets.QVBoxLayout()
        self.totalSellingsByBrandLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.totalSellingsByBrandLayout.setContentsMargins(0, 0, 0, 0)
        self.totalSellingsByBrandLayout.setSpacing(0)
        self.totalSellingsByBrandWidget = QtWidgets.QWidget()
        self.figure2 = Figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.ax2 = self.figure2.add_subplot(111)
        self.ax2.set_title("Ventes totales par marque")
        self.ax2.set_xlabel("")
        self.ax2.set_ylabel("Ventes totales (€)")
        self.ax2.set_xticks([])
        self.ax2.set_yticks([])
        self.ax2.set_facecolor("#F2F2F2")
        self.ax2.spines["top"].set_visible(False)
        self.ax2.spines["right"].set_visible(False)
        self.ax2.spines["bottom"].set_visible(False)
        self.ax2.spines["left"].set_visible(False)
        self.canvas2.draw()
        self.canvas2.setContentsMargins(0, 0, 0, 0)
        self.canvas2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.totalSellingsByBrandLayout.addWidget(self.canvas2)
        
        self.totalSellingsByBrandWidget.setLayout(self.totalSellingsByBrandLayout)


        # Best product by number of sales by category
        # Using a select menu to choose the category and a switch to choose between best and worst products

        self.bestProductByCategory = QtWidgets.QWidget()

        self.bestProductByCategoryLayout = QtWidgets.QVBoxLayout()
        self.bestProductByCategoryLayout.setAlignment(QtCore.Qt.AlignCenter)

        # Select menu
        self.bestProductByCategorySelectMenu = QtWidgets.QComboBox()
        self.bestProductByCategorySelectMenu.addItems(self.list_category)
        self.bestProductByCategorySelectMenu.setStyleSheet("background-color: #F2F2F2; border: 1px solid #CBCBCB; border-radius: 5px; padding: 5px;")
        self.bestProductByCategorySelectMenu.currentIndexChanged.connect(self.updateBestProductsByCategory)

        # Text
        self.bestProductByCategoryText = QtWidgets.QLabel("0")
        self.bestProductByCategoryText.setAlignment(QtCore.Qt.AlignCenter)
        self.bestProductByCategoryText.setFont(QtGui.QFont("Poppins SemiBold", 20))
        self.bestProductByCategoryText.setStyleSheet("color: #000000;")
        self.bestProductByCategoryTitle = QtWidgets.QLabel("Meilleur produit de la categorie")
        self.bestProductByCategoryTitle.setFont(QtGui.QFont("Poppins Regular", 11))
        self.bestProductByCategoryTitle.setStyleSheet("color: #CBCBCB;")
        self.bestProductByCategoryTextLayout = QtWidgets.QVBoxLayout()
        self.bestProductByCategoryTextLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.bestProductByCategoryTextLayout.addWidget(self.bestProductByCategoryText)
        self.bestProductByCategoryTextLayout.addWidget(self.bestProductByCategoryTitle)
        self.bestProductByCategoryTextLayout.setContentsMargins(0, 0, 0, 0)
        self.bestProductByCategoryTextLayout.setSpacing(0)

        # Switch
        self.bestProductByCategorySwitch = QtWidgets.QPushButton("Meilleur")
        self.bestProductByCategorySwitch.setCheckable(True)
        self.bestProductByCategorySwitch.setStyleSheet("background-color: #F2F2F2; border: 1px solid #CBCBCB; border-radius: 5px; padding: 5px;")
        self.bestProductByCategorySwitch.clicked.connect(self.switchBestProductByCategory)

        # Add widgets to layout
        self.bestProductByCategoryLayout.addWidget(self.bestProductByCategorySelectMenu)
        self.bestProductByCategoryLayout.addStretch()
        self.bestProductByCategoryLayout.addLayout(self.bestProductByCategoryTextLayout)
        self.bestProductByCategoryLayout.addStretch()
        self.bestProductByCategoryLayout.addWidget(self.bestProductByCategorySwitch)

        self.bestProductByCategory.setLayout(self.bestProductByCategoryLayout)
        self.bestProductByCategory.setStyleSheet("background-color: #ffffff;")

        self.updateBestProductsByCategory()

        # Best product by number of sales by brand
        # Using a select menu to choose the brand and a switch to choose between best and worst products

        self.bestProductByBrand = QtWidgets.QWidget()

        self.bestProductByBrandLayout = QtWidgets.QVBoxLayout()
        self.bestProductByBrandLayout.setAlignment(QtCore.Qt.AlignCenter)

        # Select menu
        self.bestProductByBrandSelectMenu = QtWidgets.QComboBox()
        self.bestProductByBrandSelectMenu.addItems(self.list_brand)
        self.bestProductByBrandSelectMenu.setStyleSheet("background-color: #F2F2F2; border: 1px solid #CBCBCB; border-radius: 5px; padding: 5px;")
        self.bestProductByBrandSelectMenu.currentIndexChanged.connect(self.updateBestProductsByBrand)

        # Text
        self.bestProductByBrandText = QtWidgets.QLabel("0")
        self.bestProductByBrandText.setAlignment(QtCore.Qt.AlignCenter)
        self.bestProductByBrandText.setFont(QtGui.QFont("Poppins SemiBold", 20))
        self.bestProductByBrandText.setStyleSheet("color: #000000;")
        self.bestProductByBrandTitle = QtWidgets.QLabel("Meilleur produit de la marque")
        self.bestProductByBrandTitle.setFont(QtGui.QFont("Poppins Regular", 11))
        self.bestProductByBrandTitle.setStyleSheet("color: #CBCBCB;")
        self.bestProductByBrandTextLayout = QtWidgets.QVBoxLayout()
        self.bestProductByBrandTextLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.bestProductByBrandTextLayout.addWidget(self.bestProductByBrandText)
        self.bestProductByBrandTextLayout.addWidget(self.bestProductByBrandTitle)
        self.bestProductByBrandTextLayout.setContentsMargins(0, 0, 0, 0)
        self.bestProductByBrandTextLayout.setSpacing(0)

        # Switch
        self.bestProductByBrandSwitch = QtWidgets.QPushButton("Meilleur")
        self.bestProductByBrandSwitch.setCheckable(True)
        self.bestProductByBrandSwitch.setStyleSheet("background-color: #F2F2F2; border: 1px solid #CBCBCB; border-radius: 5px; padding: 5px;")
        self.bestProductByBrandSwitch.clicked.connect(self.switchBestProductByBrand)

        # Add widgets to layout
        self.bestProductByBrandLayout.addWidget(self.bestProductByBrandSelectMenu)
        self.bestProductByBrandLayout.addStretch()
        self.bestProductByBrandLayout.addLayout(self.bestProductByBrandTextLayout)
        self.bestProductByBrandLayout.addStretch()
        self.bestProductByBrandLayout.addWidget(self.bestProductByBrandSwitch)

        self.bestProductByBrand.setLayout(self.bestProductByBrandLayout)
        self.bestProductByBrand.setStyleSheet("background-color: #eeeeff;")

        self.updateBestProductsByBrand()
        

        self.grid.addWidget(self.totalSellingsEurosWidget, 0, 0, 2, 1)
        self.grid.addWidget(self.bestProductByCategory, 2, 0, 2, 1)
        self.grid.addWidget(self.bestProductByBrand, 4, 0, 2, 1)

        self.grid.addWidget(self.graphWidget, 0, 2, 3, 2)
        self.grid.addWidget(self.totalSellingsByBrandWidget, 3, 2, 3, 2)

        self.gridWidget = QtWidgets.QWidget()
        self.gridWidget.setLayout(self.grid)
        self.bottomLayout.addWidget(self.gridWidget)

        self.bottomLayout.setCurrentIndex(0)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.midLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

        with open("style.qss", "r") as f:
            _style = f.read()
            app.setStyleSheet(_style)
    
    def addProduct(self):
        self.addProductDialog = AddProductDialog(self)
        self.addProductDialog.show()
    
    def exportProducts(self):
        self.exportProductsDialog = ExportProductsDialog(self)
        self.exportProductsDialog.show()

    def showOrderBy(self):
        self.orderBy = OrderByDialog(self)
        self.orderBy.show()

    def showFilters(self):
        self.filtersDialog = FiltersDialog(self)
        self.filtersDialog.show()

    def changePage(self):
        if self.bottomLayout.currentIndex() == 0:
            self.bottomLayout.setCurrentIndex(1)
            self.changePages.setText("Produits")
        else:
            self.bottomLayout.setCurrentIndex(0)
            self.changePages.setText("Statistiques")
        
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
        self.updateStatistics()
    
    def updateStatistics(self):
        self.totalSellingsEuros.setText(str(getTotalSellingsEuros()))
        self.canvas.figure.clear()
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.set_title("Ventes par catégorie")
        self.ax.set_xlabel("")
        self.ax.set_ylabel("Ventes")

        self.categories = []
        self.productsPerCategory = []
        for product in list_products:
            if product._category not in self.categories:
                self.categories.append(product._category)
                self.productsPerCategory.append(1)
            else:
                self.productsPerCategory[self.categories.index(product._category)] += 1
        self.ax.bar(self.categories, self.productsPerCategory, color="#000000")
        # set random colors
        for i in range(len(self.ax.patches)):
            self.ax.patches[i].set_color("#%06x" % random.randint(0, 0xFFFFFF))
        self.canvas.draw()

        self.list_category = list()
        self.list_brand = list()
        for product in list_products:
            if product._category not in self.list_category:
                self.list_category.append(product._category)
            if product._brand not in self.list_brand:
                self.list_brand.append(product._brand)
        self.list_category.sort()
        self.list_brand.sort()

        self.bestProductByCategorySelectMenu.clear()
        self.bestProductByCategorySelectMenu.addItems(sorted(self.list_category))    
        self.updateBestProductsByCategory()

        self.bestProductByBrandSelectMenu.clear()
        self.bestProductByBrandSelectMenu.addItems(sorted(self.list_brand))
        self.updateBestProductsByBrand()

        self.updateTotalSellingsByBrand()
    
    def updateTotalSellingsByBrand(self):
        self.canvas2.figure.clear()
        self.ax2 = self.canvas2.figure.add_subplot(111)
        self.ax2.set_title("Ventes totales par marque")
        self.ax2.set_xlabel("")
        self.ax2.set_ylabel("Ventes totales (€)")
        self.ax2.bar(self.list_brand, [getTotalSellingsByBrand(brand) for brand in self.list_brand], color="#000000")
        # set random colors
        for i in range(len(self.ax2.patches)):
            self.ax2.patches[i].set_color("#%06x" % random.randint(0, 0xFFFFFF))
        self.canvas2.draw()


    def updateBestProductsByCategory(self):

        # Get the category selected
        self.categorySelected = self.bestProductByCategorySelectMenu.currentText()

        # Get the best product of the category selected
        self.bestProduct = getProduct(self.bestProductByCategorySwitch.isChecked(), self.categorySelected, None)

        if(self.bestProduct != None):
            # Update the best product label
            self.bestProductByCategoryText.setText(self.bestProduct._name)

    def switchBestProductByCategory(self):
        if self.bestProductByCategorySwitch.isChecked():
            self.bestProductByCategorySwitch.setText("Pire")
            self.bestProductByCategoryTitle.setText("Pire produit de la catégorie")
        else:
            self.bestProductByCategorySwitch.setText("Meilleur")
            self.bestProductByCategoryTitle.setText("Meilleur produit de la catégorie")
        self.updateBestProductsByCategory()

    def updateBestProductsByBrand(self):
        # Get the category selected
        self.brandSelected = self.bestProductByBrandSelectMenu.currentText()

        # Get the best product of the category selected
        self.bestProduct = getProduct(self.bestProductByBrandSwitch.isChecked(), None, self.brandSelected)

        if(self.bestProduct != None):
            # Update the best product label
            self.bestProductByBrandText.setText(self.bestProduct._name)

    def switchBestProductByBrand(self):
        if self.bestProductByBrandSwitch.isChecked():
            self.bestProductByBrandSwitch.setText("Pire")
            self.bestProductByBrandTitle.setText("Pire produit de la marque")
        else:
            self.bestProductByBrandSwitch.setText("Meilleur")
            self.bestProductByBrandTitle.setText("Meilleur produit de la marque")
        self.updateBestProductsByBrand()


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
    program.resize(960, 720)
    program.show()

    sys.exit(app.exec())