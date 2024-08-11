from sys import _current_frames
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView, QDialog, QDialogButtonBox, QHeaderView, QMainWindow, QFileDialog, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMenuBar, QStatusBar, QGridLayout, QLineEdit, QSpacerItem, QSizePolicy, QScrollArea
from geometry.geometry import Line, Point, Polygon
from xmlReader import XmlReader
from xmlWriter import XmlWriter
from viewport import Viewport
from window import Window
from draw import Draw
from windowToViewport import *
from clipping.cohen import *
from clipping.weiler import *
import numpy as np

# TODO : XmlReader, Rotação e ajuste de coordenadas

class Ui_MainWindow(QMainWindow):
    def __init__(self, MainWindow) -> None:
        super().__init__(MainWindow)

        self.viewPortPointsCoordinates = []
        self.viewPortLinesCoordinates = []
        self.viewPortPolygonsCoordinates = []


        self.windowPointsCoordinates = []
        self.windowLinesCoordinates = []
        self.windowPolygonsCoordinates = []

        self.worldPointsCoordinates = []
        self.worldLinesCoordinates = []
        self.worldPolygonsCoordinates = []

        self.main_window = Window(0, 600, 0, 550)
        self.mouse_window = self.main_window
        self.viewport = Viewport(0, 600, 0, 550)
        self.setupUi(MainWindow)
        self.main_window_widget = MainWindow
        self.selected_row = -1


    # Formulario do botao
    def createPointForm(self, point=None):
        self.point_dialog = QDialog(self)
        self.point_dialog.setWindowTitle("Edit Point" if point else "Add Point")
        self.flag_updated = False
        form_layout = QVBoxLayout(self.point_dialog)

        self.label_x = QLabel("X:")
        self.input_x = QLineEdit()
        self.label_y = QLabel("Y:")
        self.input_y = QLineEdit()

        if point:
            self.input_x.setText(str(point.getPoint()[0]))
            self.input_y.setText(str(point.getPoint()[1]))
        else:
            self.input_x.setText("")
            self.input_y.setText("")

        form_layout.addWidget(self.label_x)
        form_layout.addWidget(self.input_x)
        form_layout.addWidget(self.label_y)
        form_layout.addWidget(self.input_y)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.point_returned = Point()
        def execConfirmPoint(self):
            self.flag_updated = True
            self.point_returned = self.confirmPoint()
        button_box.accepted.connect(lambda: execConfirmPoint(self))
        button_box.rejected.connect(self.point_dialog.reject)
        form_layout.addWidget(button_box)

        self.point_dialog.setLayout(form_layout)
        self.point_dialog.exec_()
        return self.point_returned, self.flag_updated

    # Formulario da reta
    def createLineForm(self, line=None):
        self.flag_updated = False
        self.line_dialog = QDialog(self)
        self.line_dialog.setWindowTitle("Edit Line" if line else "Add Line")

        form_layout = QVBoxLayout(self.line_dialog)

        self.line_label_x1 = QLabel("X1:")
        self.line_input_x1 = QLineEdit()
        self.line_label_y1 = QLabel("Y1:")
        self.line_input_y1 = QLineEdit()
        self.line_label_x2 = QLabel("X2:")
        self.line_input_x2 = QLineEdit()
        self.line_label_y2 = QLabel("Y2:")
        self.line_input_y2 = QLineEdit()

        if line:
            x1, y1 = line.getLine()[0]
            x2, y2 = line.getLine()[1]
            self.line_input_x1.setText(str(x1))
            self.line_input_y1.setText(str(y1))
            self.line_input_x2.setText(str(x2))
            self.line_input_y2.setText(str(y2))
        else:
            self.line_input_x1.setText("")
            self.line_input_y1.setText("")
            self.line_input_x2.setText("")
            self.line_input_y2.setText("")

        form_layout.addWidget(self.line_label_x1)
        form_layout.addWidget(self.line_input_x1)
        form_layout.addWidget(self.line_label_y1)
        form_layout.addWidget(self.line_input_y1)
        form_layout.addWidget(self.line_label_x2)
        form_layout.addWidget(self.line_input_x2)
        form_layout.addWidget(self.line_label_y2)
        form_layout.addWidget(self.line_input_y2)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.line_returned = line
        def execConfirmLine(self):
            self.flag_updated = True
            self.line_returned = self.confirmLine()
        button_box.accepted.connect(lambda: execConfirmLine(self))
        button_box.rejected.connect(self.line_dialog.reject)
        form_layout.addWidget(button_box)

        self.line_dialog.setLayout(form_layout)
        self.line_dialog.exec_()
        return self.line_returned, self.flag_updated

    # Formulario do poligono
    def createPolygonForm(self, polygon=None):
        self.polygon_dialog = QDialog(self)
        self.polygon_dialog.setWindowTitle("Edit Polygon" if polygon else "Add Polygon")
        self.flag_updated = False
        main_layout = QVBoxLayout(self.polygon_dialog)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        self.polygon_labels_x = []
        self.polygon_inputs_x = []
        self.polygon_labels_y = []
        self.polygon_inputs_y = []

        def addPoint(x=None, y=None):
            point_index = len(self.polygon_labels_x) + 1

            label_x = QLabel(f"X{point_index}")
            input_x = QLineEdit()
            if x is not None:
                input_x.setText(str(x))
            label_y = QLabel(f"Y{point_index}")
            input_y = QLineEdit()
            if y is not None:
                input_y.setText(str(y))

            self.polygon_labels_x.append(label_x)
            self.polygon_inputs_x.append(input_x)
            self.polygon_labels_y.append(label_y)
            self.polygon_inputs_y.append(input_y)

            scroll_layout.addWidget(label_x)
            scroll_layout.addWidget(input_x)
            scroll_layout.addWidget(label_y)
            scroll_layout.addWidget(input_y)

        if polygon:
            for point in polygon.getPolygon():
                x, y = point.getPoint()
                addPoint(x, y)
        else:
            for _ in range(3):
                addPoint()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        main_layout.addWidget(scroll_area)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        add_point_button = QPushButton("+")
        add_point_button.clicked.connect(lambda: addPoint(None, None))
        self.polygon_returned = polygon
        def execConfirmPolygon(self):
            self.polygon_returned = self.confirmPolygon()
            self.flag_updated = True
        button_box.accepted.connect(lambda: execConfirmPolygon(self))
        button_box.rejected.connect(self.polygon_dialog.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(button_box)
        button_layout.addWidget(add_point_button)

        main_layout.addLayout(button_layout)

        self.polygon_dialog.setLayout(main_layout)
        self.polygon_dialog.exec_()
        return self.polygon_returned, self.flag_updated

    #Xml form
    def createXmlForm(self):
        self.point_dialog = QDialog(self)
        self.point_dialog.setWindowTitle("Exportar Figuras")

        form_layout = QVBoxLayout(self.point_dialog)

        btn_export_viewport = QPushButton("Exportar figuras na ViewPort", self.point_dialog)
        btn_export_world = QPushButton("Exportar figuras do mundo", self.point_dialog)

        btn_export_viewport.clicked.connect(self.exportFiguresInViewPort)
        btn_export_world.clicked.connect(self.exportFiguresInWorld)

        form_layout.addWidget(btn_export_viewport)
        form_layout.addWidget(btn_export_world)

        self.point_dialog.setLayout(form_layout)
        self.point_dialog.exec_()

    # Exemplos de métodos para exportação (implemente conforme necessário)
    def exportFiguresInViewPort(self):
        self.saveXmlFunction(self.viewPortPointsCoordinates,
                  self.viewPortLinesCoordinates, self.viewPortPolygonsCoordinates)

    def exportFiguresInWorld(self):
        self.saveXmlFunction(self.worldPointsCoordinates,
                  self.worldLinesCoordinates, self.worldPolygonsCoordinates)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 630))
        MainWindow.setMaximumSize(QtCore.QSize(1000, 630))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        main_layout = QHBoxLayout(self.centralwidget)

        self.widget = Draw(self.centralwidget)
        self.widget.setStyleSheet("background-color: black; border: 0.1px solid magenta")
        self.widget.setObjectName("widget")
        main_layout.addWidget(self.widget)
        self.widget.setMaximumSize(QtCore.QSize(600, 550))
        self.widget.setMinimumSize(QtCore.QSize(600, 550))

        controls_container = QWidget(self.centralwidget)
        controls_container.setMaximumWidth(300)
        controls_layout = QVBoxLayout(controls_container)

        self.erase_button = QPushButton(controls_container)
        self.erase_button.setObjectName("erase_button")
        self.erase_button.setMinimumSize(85, 35)
        self.erase_button.setMaximumSize(300, 35)
        self.erase_button.clicked.connect(self.eraseFunction)
        controls_layout.addWidget(self.erase_button)

        self.edit_button = QPushButton(controls_container)
        self.edit_button.setObjectName("edit_button")
        self.edit_button.setMinimumSize(85, 35)
        self.edit_button.setMaximumSize(300, 35)
        self.edit_button.clicked.connect(self.editFigureFunction)
        controls_layout.addWidget(self.edit_button)

        # Track Figures Scroll Area
        self.track_figures_area = QScrollArea(controls_container)
        self.track_figures_area.setWidgetResizable(True)
        controls_layout.addWidget(self.track_figures_area)

        # Adding content to the scroll area
        self.track_figures_content = QWidget()
        self.track_figures_layout = QVBoxLayout(self.track_figures_content)

        # Create the table widget
        self.table_widget = QTableWidget(self.track_figures_content)
        self.table_widget.setColumnCount(3)  # 3 columns for ID, FIGURE, COORDINATES
        self.table_widget.setHorizontalHeaderLabels(["ID", "Figure", "Coordinate"])
        self.table_widget.setMinimumHeight(400)  # Ensure minimum height

        # Set dynamic width for the columns
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # ID column
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # FIGURE column

        # Make the table items non-editable
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Ensure that selecting a row selects all columns of that row
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Create a QScrollArea to contain the table_widget
        self.table_scroll_area = QScrollArea(self.track_figures_content)
        self.table_scroll_area.setWidgetResizable(True)  # Make the scroll area resizable
        self.table_scroll_area.setWidget(self.table_widget)  # Set the table_widget as the widget for the scroll area

        # Add the scroll area to the layout instead of the table widget directly
        self.track_figures_layout.addWidget(self.table_scroll_area)

        # Connect the signal to the slot
        self.table_widget.itemSelectionChanged.connect(self.onRowSelected)

        # Set the content widget of the scroll area
        self.track_figures_area.setWidget(self.track_figures_content)

        # Spacer to fill the empty space
        # spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # controls_layout.addItem(spacer)

        self.form_widget = QWidget()

        # Adding new buttons
        self.button_ponto = QPushButton(controls_container)
        self.button_ponto.setObjectName("button_ponto")
        self.button_ponto.setMinimumSize(85, 35)
        self.button_ponto.setMaximumSize(300, 35)
        self.button_ponto.clicked.connect(self.pontoFunction)  # Connect the button to show the form
        controls_layout.addWidget(self.button_ponto)

        self.button_linha = QPushButton(controls_container)
        self.button_linha.setObjectName("button_linha")
        self.button_linha.setMinimumSize(85, 35)
        self.button_linha.setMaximumSize(300, 35)
        self.button_linha.clicked.connect(self.linhaFunction)  # Connect the button to its function
        controls_layout.addWidget(self.button_linha)

        self.button_poligono = QPushButton(controls_container)
        self.button_poligono.setObjectName("button_poligono")
        self.button_poligono.setMinimumSize(85, 35)
        self.button_poligono.setMaximumSize(300, 35)
        self.button_poligono.clicked.connect(self.poligonoFunction)  # Connect the button to its function
        controls_layout.addWidget(self.button_poligono)

        arrows_container = QWidget(controls_container)
        arrows_container.setMaximumWidth(300)
        arrows_container.setMaximumHeight(150)
        arrow_layout = QGridLayout(arrows_container)

        self.rotate_left = QPushButton(arrows_container)
        self.rotate_left.setText("↻")  # Símbolo de rotação para esquerda
        self.rotate_left.setMinimumSize(85, 35)
        self.rotate_left.setMaximumSize(300, 35)
        self.rotate_left.clicked.connect(self.rotateLeftFunction)  # Connect to rotate left
        arrow_layout.addWidget(self.rotate_left, 0, 0)

        self.arrow_up = QPushButton(arrows_container)
        self.arrow_up.setObjectName("arrow_up")
        self.arrow_up.setText("↑")
        self.arrow_up.setMinimumSize(85, 35)
        self.arrow_up.setMaximumSize(300, 35)
        self.arrow_up.clicked.connect(self.arrowUpFunction)  # Connect the button to its function
        arrow_layout.addWidget(self.arrow_up, 0, 1)

        self.rotate_right = QPushButton(arrows_container)
        self.rotate_right.setText("↺")  # Símbolo de rotação para direita
        self.rotate_right.setMinimumSize(85, 35)
        self.rotate_right.setMaximumSize(300, 35)
        self.rotate_right.clicked.connect(self.rotateRightFunction)  # Connect to rotate right
        arrow_layout.addWidget(self.rotate_right, 0, 2)

        self.arrow_left = QPushButton(arrows_container)
        self.arrow_left.setObjectName("arrow_left")
        self.arrow_left.setText("←")
        self.arrow_left.setMinimumSize(85, 35)
        self.arrow_left.setMaximumSize(300, 35)
        self.arrow_left.clicked.connect(self.arrowLeftFunction)  # Connect the button to its function
        arrow_layout.addWidget(self.arrow_left, 1, 0)

        # Salvar xml
        self.save_xml = QPushButton(arrows_container)
        self.save_xml.setObjectName("save_xml")
        self.save_xml.setText(".xml")
        self.save_xml.setMinimumSize(85, 35)
        self.save_xml.setMaximumSize(300, 35)
        self.save_xml.clicked.connect(self.xmlFunction)  # Connect the button to its function
        arrow_layout.addWidget(self.save_xml, 1, 1)

        self.arrow_down = QPushButton(arrows_container)
        self.arrow_down.setObjectName("arrow_down")
        self.arrow_down.setText("↓")
        self.arrow_down.setMinimumSize(85, 35)
        self.arrow_down.setMaximumSize(300, 35)
        self.arrow_down.clicked.connect(self.arrowDownFunction)  # Connect the button to its function
        arrow_layout.addWidget(self.arrow_down, 2, 1)

        self.arrow_right = QPushButton(arrows_container)
        self.arrow_right.setText("→")
        self.arrow_right.setMinimumSize(85, 35)
        self.arrow_right.setMaximumSize(300, 35)
        self.arrow_right.clicked.connect(self.arrowRightFunction)  # Connect the button to its function
        arrow_layout.addWidget(self.arrow_right, 1, 2)

        self.zoom_in = QPushButton(arrows_container)
        self.zoom_in.setText("🔍+")  # Símbolo de zoom in
        self.zoom_in.setMinimumSize(85, 35)
        self.zoom_in.setMaximumSize(300, 35)
        self.zoom_in.clicked.connect(self.zoomInFunction)  # Connect to zoom in
        arrow_layout.addWidget(self.zoom_in, 2, 0)

        self.zoom_out = QPushButton(arrows_container)
        self.zoom_out.setText("🔍-")  # Símbolo de zoom out
        self.zoom_out.setMinimumSize(85, 35)
        self.zoom_out.setMaximumSize(300, 35)
        self.zoom_out.clicked.connect(self.zoomOutFunction)  # Connect to zoom out
        arrow_layout.addWidget(self.zoom_out, 2, 2)

        controls_layout.addWidget(arrows_container)

        self.coordinates_label = QLabel(controls_container)
        self.coordinates_label.setObjectName("coordinates_label")
        self.coordinates_label.setStyleSheet("""
            QLabel {
                border: 1px solid grey;
            }
        """)
        self.coordinates_label.setMaximumSize(300, 20)
        self.coordinates_label.setAlignment(QtCore.Qt.AlignCenter)
        controls_layout.addWidget(self.coordinates_label)

        main_layout.addWidget(controls_container)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuOptions.addAction(self.actionOpen)

        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuOptions.addAction(self.actionExit)

        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionExit.triggered.connect(self.exitProgram)
        conversor = WindowToViewportConversor()

        self.widget.newPoint.connect(
            lambda p: self.coordinates_label.setText(
                'Coordinates: ( %d : %d )' % conversor.convertToViewport(
                    Point((p.x(), p.y())), self.main_window, self.viewport).getPoint()
            )
        )

    def updateDrawing(self):
        self.windowPointsCoordinates.clear()
        self.windowLinesCoordinates.clear()
        self.windowPolygonsCoordinates.clear()

        for point in self.worldPointsCoordinates:
            if (point.getPoint()[0] >= self.main_window.getXwMin() and point.getPoint()[0] <= self.main_window.getXwMax() and
                point.getPoint()[1] >= self.main_window.getYwMin() and point.getPoint()[1] <= self.main_window.getYwMax()
            ):
                self.windowPointsCoordinates.append(point)

        cohen = CohenSutherland(self.main_window)
        for line in self.worldLinesCoordinates:
            if (cohen.cohen_sutherland_clip(line.getLine()[0][0], line.getLine()[0][1],
                line.getLine()[1][0], line.getLine()[1][1])):
                self.windowLinesCoordinates.append(line)

        for polygon in self.worldPolygonsCoordinates:
            weiler = WeilerAtherton(self.main_window)
            polygon_list = weiler.weiler_atherton(polygon)
            if ( len(polygon_list.getPolygon()) != 0):
                self.windowPolygonsCoordinates.append(polygon_list)

        conversor = WindowToViewportConversor()
        self.widget.polygons.clear()
        self.widget.lines.clear()
        self.widget.points.clear()
        self.viewPortPointsCoordinates.clear()
        self.viewPortLinesCoordinates.clear()
        self.viewPortPolygonsCoordinates.clear()

        # Converte e redesenha os pontos
        for point in self.windowPointsCoordinates:
            convertedPoint = conversor.convertToViewport(
                point, self.main_window, self.viewport)
            self.viewPortPointsCoordinates.append(convertedPoint)
            self.widget.drawPoint(convertedPoint)

        # Converte e redesenha as linhas
        for line in self.windowLinesCoordinates:
            convertedLine = conversor.convertToViewport(
                line, self.main_window, self.viewport)
            self.viewPortLinesCoordinates.append(convertedLine)
            self.widget.drawLine(convertedLine)

        # Converte e redesenha os polígonos
        for polygon in self.windowPolygonsCoordinates:
            convertedPolygon = conversor.convertToViewport(
                polygon, self.main_window, self.viewport)
            self.viewPortPolygonsCoordinates.append(convertedPolygon)
            self.widget.drawPolygon(convertedPolygon)

        self.widget.update()



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Trabalho de CG"))
        self.erase_button.setText(_translate("MainWindow", "🗑️"))
        self.edit_button.setText(_translate("MainWindow", "📝"))
        self.save_xml.setText(_translate("MainWindow", ".xml"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.button_ponto.setText(_translate("MainWindow", "Point"))
        self.button_linha.setText(_translate("MainWindow", "Line"))
        self.button_poligono.setText(_translate("MainWindow", "Polygon"))
        self.arrow_up.setText(_translate("MainWindow", "↑"))
        self.arrow_left.setText(_translate("MainWindow", "←"))
        self.arrow_right.setText(_translate("MainWindow", "→"))
        self.arrow_down.setText(_translate("MainWindow", "↓"))
        self.coordinates_label.setText(_translate("MainWindow", "Coordinates: (0, 0)"))

    def populateTable(self):
        # Combine the three lists into one
        geometries = self.worldPointsCoordinates + self.worldLinesCoordinates + self.worldPolygonsCoordinates

        # Set the number of rows in the table
        self.table_widget.setRowCount(len(geometries))\

        for i, geometry in enumerate(geometries):
            # Populate the ID
            id_item = QTableWidgetItem(str(geometry.getId()))
            self.table_widget.setItem(i, 0, id_item)

            # Populate the Figure type
            figure_item = QTableWidgetItem(geometry.getFigure())
            self.table_widget.setItem(i, 1, figure_item)

            # Populate the Coordinates
            coordinate_item = QTableWidgetItem(geometry.__str__())
            self.table_widget.setItem(i, 2, coordinate_item)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "XML Files (*.xml)", options=options)
        if fileName:
            return fileName

    def exitProgram(self):
        self.main_window_widget.close()

    def openFile(self):
        filePath = self.openFileNameDialog()
        xmlReader = XmlReader(filePath)
        conversor = WindowToViewportConversor()
        self.main_window = xmlReader.getWindow()
        self.viewport = xmlReader.getViewport()
        self.widget.setViewport(self.viewport)
        self.worldFilePointsCoordinates = xmlReader.getPontos()
        self.worldFileLinesCoordinates = xmlReader.getRetas()
        self.worldFilePolygonsCoordinates = xmlReader.getPoligonos()

        for point in self.worldFilePolygonsCoordinates:
            convertedPoint = conversor.convertToViewport(
                point, self.main_window, self.viewport)
            self.viewPortPointsCoordinates.append(convertedPoint)

        for line in self.worldFileLinesCoordinates:
            convertedLine = conversor.convertToViewport(
                line, self.main_window, self.viewport)
            self.viewPortLinesCoordinates.append(convertedLine)

        for polygon in self.worldFilePolygonsCoordinates:
            convertedPolygon = conversor.convertToViewport(
                polygon, self.main_window, self.viewport)
            self.viewPortPolygonsCoordinates.append(convertedPolygon)

        for ponto in self.viewPortPointsCoordinates:
            self.widget.drawPoint(ponto)

        for line in self.viewPortLinesCoordinates:
            self.widget.drawLine(line)

        for polygon in self.viewPortPolygonsCoordinates:
            self.widget.drawPolygon(polygon)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "", "XML Files (*.xml)", options=options)
        if fileName:
            return fileName

    def saveXmlFunction(self, points_vector, lines_vector, polygons_vector):
        pathFilename = self.saveFileDialog()
        xml = XmlWriter(pathFilename)
        xml.write(points_vector, lines_vector, polygons_vector)
        # self.pushButton.hide()

    def eraseFunction(self):
        if self.selected_row == -1: return
        selected_id = self.table_widget.item(self.selected_row, 0).text()
        erased = False
        if (self.table_widget.item(self.selected_row, 1).text() == "Point"):
            erased = self.removeGeometryById(self.worldPointsCoordinates,int(selected_id))
        elif (self.table_widget.item(self.selected_row, 1).text() == "Line"):
            erased = self.removeGeometryById(self.worldLinesCoordinates,int(selected_id))
        else:
            erased = self.removeGeometryById(self.worldPolygonsCoordinates,int(selected_id))
        if erased :
            self.table_widget.removeRow(self.selected_row)
            self.selected_row = -1
            self.updateDrawing()

    def editFigureFunction(self):
        if self.selected_row == -1: return
        selected_id = self.table_widget.item(self.selected_row, 0).text()
        index = None
        if (self.table_widget.item(self.selected_row, 1).text() == "Point"):
            index = self.findFigureById(self.worldPointsCoordinates,int(selected_id))
            new_point, flag_updated = self.createPointForm(self.worldPointsCoordinates[index])
            if not flag_updated: return
            if new_point.getPoint() is not None and self.table_widget.item(self.selected_row, 2) is not None:
                old_id = self.worldPointsCoordinates[index].getId()
                self.worldPointsCoordinates[index] = new_point
                self.worldPointsCoordinates[index].setId(old_id)
                self.worldPointsCoordinates.pop()
                self.table_widget.removeRow(self.table_widget.rowCount() - 1)
                self.table_widget.item(self.selected_row, 2).setText(self.worldPointsCoordinates[index].__str__())
        elif (self.table_widget.item(self.selected_row, 1).text() == "Line"):
            index = self.findFigureById(self.worldLinesCoordinates,int(selected_id))
            new_line, flag_updated = self.createLineForm(self.worldLinesCoordinates[index])
            if not flag_updated: return
            if type(new_line) == Line and new_line.getLine() is not None and self.table_widget.item(self.selected_row, 2) is not None:
                old_id = self.worldLinesCoordinates[index].getId()
                self.worldLinesCoordinates[index] = new_line
                self.worldLinesCoordinates[index].setId(old_id)
                self.worldLinesCoordinates.pop()
                self.table_widget.removeRow(self.table_widget.rowCount() - 1)
                self.table_widget.item(self.selected_row, 2).setText(str(self.worldLinesCoordinates[index]))
        else:
            index = self.findFigureById(self.worldPolygonsCoordinates,int(selected_id))
            new_polygon, flag_updated = self.createPolygonForm(self.worldPolygonsCoordinates[index])
            if not flag_updated: return
            if new_polygon.getPolygon() is not None and self.table_widget.item(self.selected_row, 2) is not None:
                old_id = self.worldPolygonsCoordinates[index].getId()
                self.worldPolygonsCoordinates[index] = new_polygon
                self.worldPolygonsCoordinates[index].setId(old_id)
                self.worldPolygonsCoordinates.pop()
                self.table_widget.removeRow(self.table_widget.rowCount() - 1)
            self.table_widget.item(self.selected_row, 2).setText(self.worldPolygonsCoordinates[index].__str__())
        self.updateDrawing()


    # Confirm the point and process it
    def confirmPoint(self):
        x = float(self.input_x.text())
        y = float(self.input_y.text())
        point = Point((x, y))
        conversor = WindowToViewportConversor()
        convertedPoint = conversor.convertToViewport(
            point, self.main_window, self.viewport)
        self.worldPointsCoordinates.append(point)
        self.viewPortPointsCoordinates.append(convertedPoint)
        self.widget.drawPoint(convertedPoint)
        self.populateTable()
        self.point_dialog.accept()  # Close the dialog
        return point

    def confirmLine(self):
        x1 = float(self.line_input_x1.text())
        y1 = float(self.line_input_y1.text())
        x2 = float(self.line_input_x2.text())
        y2 = float(self.line_input_y2.text())
        line = Line(
            (tuple([x1, y1])),
            (tuple([x2, y2]))
        )
        conversor = WindowToViewportConversor()
        convertedLine = conversor.convertToViewport(
            line, self.main_window, self.viewport)
        self.worldLinesCoordinates.append(line)
        self.viewPortLinesCoordinates.append(convertedLine)
        self.widget.drawLine(convertedLine)
        self.populateTable()
        self.line_dialog.accept()  # Close the dialog
        return line

    def confirmPolygon(self):
        points = []
        for i in range(len(self.polygon_inputs_x)):
            x_value = float(self.polygon_inputs_x[i].text())
            y_value = float(self.polygon_inputs_y[i].text())
            points.append(Point((x_value, y_value)))
        polygon = Polygon(*points)
        conversor = WindowToViewportConversor()
        convertedPolygon = conversor.convertToViewport(
            polygon, self.main_window, self.viewport)
        self.worldPolygonsCoordinates.append(polygon)
        self.viewPortPolygonsCoordinates.append(convertedPolygon)
        self.widget.drawPolygon(convertedPolygon)
        self.populateTable()
        self.polygon_dialog.accept()
        return polygon

    # Define the functions for the buttons below
    def pontoFunction(self):
        self.createPointForm()

    def xmlFunction(self):
        self.createXmlForm()

    def linhaFunction(self):
        self.createLineForm()

    def poligonoFunction(self):
        self.createPolygonForm()

    def arrowUpFunction(self):
        self.main_window.moveWindow(0, 10)
        self.updateDrawing()

    def arrowLeftFunction(self):
        self.main_window.moveWindow(-10, 0)
        self.updateDrawing()

    def arrowRightFunction(self):
        self.main_window.moveWindow(+10, 0)
        self.updateDrawing()

    def arrowDownFunction(self):
        self.main_window.moveWindow(0, -10)
        self.updateDrawing()

    def rotateLeftFunction(self):
        self.main_window.rotate(-45)  # Rotaciona 10 graus para a esquerda
        self.updateDrawing()

    def rotateRightFunction(self):
        self.main_window.rotate(45)  # Rotaciona 10 graus para a direita
        self.updateDrawing()

    def zoomInFunction(self):
        self.main_window.zoom(0.9)  # Aumenta o zoom
        self.updateDrawing()

    def zoomOutFunction(self):
        self.main_window.zoom(1.1)  # Diminui o zoom
        self.updateDrawing()

    def onRowSelected(self):
        self.selected_items = self.table_widget.selectedItems()
        if self.selected_items:
            self.selected_row = self.selected_items[0].row()  # Get the row of the first selected item
            column_count = self.table_widget.columnCount()

            row_values = []
            for col in range(column_count):
                cell_value = self.table_widget.item(self.selected_row, col).text()
                row_values.append(cell_value)

            # You can now use the row_values list as needed

    def findFigureById(self, geometry_array: List[Geometry], target_id: int) -> int:
        left, right = 0, len(geometry_array) - 1

        while left <= right:
            mid = (left + right) // 2
            mid_id = geometry_array[mid].getId()  # Assuming getId() method exists

            if mid_id == target_id:
                return mid
            elif mid_id < target_id:
                left = mid + 1
            else:
                right = mid - 1

        return -1  # Return None if the target_id is not found

    def removeGeometryById(self,geometry_array: List[Geometry], target_id: int):
        low, high = 0, len(geometry_array) - 1

        while low <= high:
            mid = (low + high) // 2
            current_id = geometry_array[mid].id

            if current_id == target_id:
                del geometry_array[mid]
                return True  # Element found and removed
            elif current_id < target_id:
                low = mid + 1
            else:
                high = mid - 1

        return False  # Element not found

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    MainWindow.show()
    app.exec_()
