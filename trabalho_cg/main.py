from sys import _current_frames
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMainWindow, QFileDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMenuBar, QStatusBar, QGridLayout, QLineEdit, QSpacerItem, QSizePolicy, QScrollArea

from geometry.geometry import Line, Point, Polygon
from xmlReader import XmlReader
from viewport import Viewport
from window import Window
from draw import Draw
from windowToViewport import *
from clipping.cohen import *
from clipping.weiler import *

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

        self.main_window = Window(0, 1250, 0, 750)
        self.viewport = Viewport(0, 1250, 0, 750)
        self.setupUi(MainWindow)
        self.main_window_widget = MainWindow


    # Formulario do botao
    def createPointForm(self):
        self.point_dialog = QDialog(self)
        self.point_dialog.setWindowTitle("Add Point")

        form_layout = QVBoxLayout(self.point_dialog)

        self.label_x = QLabel("X:")
        self.label_x.setMaximumSize(300, 35)
        self.input_x = QLineEdit()
        self.input_x.setMaximumSize(300, 35)
        self.label_y = QLabel("Y:")
        self.label_y.setMaximumSize(300, 35)
        self.input_y = QLineEdit()
        self.input_y.setMaximumSize(300, 35)

        form_layout.addWidget(self.label_x)
        form_layout.addWidget(self.input_x)
        form_layout.addWidget(self.label_y)
        form_layout.addWidget(self.input_y)

        # Add confirm and cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.confirmPoint)
        button_box.rejected.connect(self.point_dialog.reject)
        form_layout.addWidget(button_box)

        self.point_dialog.setLayout(form_layout)
        self.point_dialog.exec_()  # Open the dialog as a modal

    # Formulario da reta
    def createLineForm(self):
        self.line_dialog = QDialog(self)
        self.line_dialog.setWindowTitle("Add Line")

        form_layout = QVBoxLayout(self.line_dialog)

        self.line_label_x1 = QLabel("X1:")
        self.line_label_x1.setMaximumSize(300, 35)
        self.line_input_x1 = QLineEdit()
        self.line_input_x1.setMaximumSize(300, 35)
        self.line_label_y1 = QLabel("Y1:")
        self.line_label_y1.setMaximumSize(300, 35)
        self.line_input_y1 = QLineEdit()
        self.line_input_y1.setMaximumSize(300, 35)
        self.line_label_x2 = QLabel("X2:")
        self.line_label_x2.setMaximumSize(300, 35)
        self.line_input_x2 = QLineEdit()
        self.line_input_x2.setMaximumSize(300, 35)
        self.line_label_y2 = QLabel("Y2:")
        self.line_label_y2.setMaximumSize(300, 35)
        self.line_input_y2 = QLineEdit()
        self.line_input_y2.setMaximumSize(300, 35)

        form_layout.addWidget(self.line_label_x1)
        form_layout.addWidget(self.line_input_x1)
        form_layout.addWidget(self.line_label_y1)
        form_layout.addWidget(self.line_input_y1)
        form_layout.addWidget(self.line_label_x2)
        form_layout.addWidget(self.line_input_x2)
        form_layout.addWidget(self.line_label_y2)
        form_layout.addWidget(self.line_input_y2)

        # Add confirm and cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.confirmLine)
        button_box.rejected.connect(self.line_dialog.reject)
        form_layout.addWidget(button_box)

        self.line_dialog.setLayout(form_layout)
        self.line_dialog.exec_()  # Open the dialog as a modal

    # Formulario do poligono
    def createPolygonForm(self):
        self.polygon_dialog = QDialog(self)
        self.polygon_dialog.setWindowTitle("Add Polygon")

        # Main layout for the dialog
        main_layout = QVBoxLayout(self.polygon_dialog)

        # Create a widget for the scroll area
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        self.polygon_labels_x = []
        self.polygon_inputs_x = []
        self.polygon_labels_y = []
        self.polygon_inputs_y = []

        # Function to add a new point input
        def addPoint():
            point_index = len(self.polygon_labels_x) + 1

            label_x = QLabel(f"X{point_index}")
            input_x = QLineEdit()
            label_y = QLabel(f"Y{point_index}")
            input_y = QLineEdit()

            self.polygon_labels_x.append(label_x)
            self.polygon_inputs_x.append(input_x)
            self.polygon_labels_y.append(label_y)
            self.polygon_inputs_y.append(input_y)

            scroll_layout.addWidget(label_x)
            scroll_layout.addWidget(input_x)
            scroll_layout.addWidget(label_y)
            scroll_layout.addWidget(input_y)

        # Add the first three points
        for i in range(3):
            addPoint()

        # Create the scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)

        # Create a button box and add "+" button
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        add_point_button = QPushButton("+")
        add_point_button.clicked.connect(addPoint)
        button_box.accepted.connect(self.confirmPolygon)
        button_box.rejected.connect(self.polygon_dialog.reject)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(button_box)
        button_layout.addWidget(add_point_button)

        # Add the button layout to the main layout
        main_layout.addLayout(button_layout)

        # Set the dialog layout
        self.polygon_dialog.setLayout(main_layout)
        self.polygon_dialog.exec_()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1600, 900))
        MainWindow.setMaximumSize(QtCore.QSize(1600, 900))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        main_layout = QHBoxLayout(self.centralwidget)

        self.widget = Draw(self.centralwidget)
        self.widget.setStyleSheet("background-color: black; border: 0.1px solid magenta")
        self.widget.setObjectName("widget")
        main_layout.addWidget(self.widget)
        self.widget.setMaximumSize(QtCore.QSize(1250, 750))
        self.widget.setMinimumSize(QtCore.QSize(1250, 750))

        controls_container = QWidget(self.centralwidget)
        controls_container.setMaximumWidth(300)
        controls_layout = QVBoxLayout(controls_container)

        self.pushButton = QPushButton(controls_container)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setMinimumSize(85, 35)
        self.pushButton.setMaximumSize(300, 35)
        self.pushButton.clicked.connect(self.changelabeltext)
        controls_layout.addWidget(self.pushButton)

        # Spacer to fill the empty space
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        controls_layout.addItem(spacer)

        # Scroll area for the form layout
        # scroll_area = QScrollArea(controls_container)
        # scroll_area.setWidgetResizable(True)
        # scroll_area.setMaximumWidth(300)
        self.form_widget = QWidget()
        # self.form_button_layout = QVBoxLayout(self.form_widget)
        # self.form_line_layout = QVBoxLayout(self.form_widget)

        #Form para poligono
        # self.form_widget.hide()
        # controls_layout.addWidget(scroll_area)



        # self.label = QLabel(controls_container)
        # self.label.setObjectName("label")
        # self.label.setMaximumSize(300, 35)
        # controls_layout.addWidget(self.label)

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

        # Adding arrow buttons in a grid layout
        arrows_container = QWidget(controls_container)
        arrows_container.setMaximumWidth(300)
        arrows_container.setMaximumHeight(150)
        arrow_layout = QGridLayout(arrows_container)

        self.arrow_up = QPushButton(arrows_container)
        self.arrow_up.setObjectName("arrow_up")
        self.arrow_up.setText("↑")
        self.arrow_up.setMinimumSize(85, 35)
        self.arrow_up.setMaximumSize(300, 35)
        self.arrow_up.clicked.connect(self.arrowUpFunction)  # Connect the button to its function
        arrow_layout.addWidget(self.arrow_up, 0, 1)

        self.arrow_left = QPushButton(arrows_container)
        self.arrow_left.setObjectName("arrow_left")
        self.arrow_left.setText("←")
        self.arrow_left.setMinimumSize(85, 35)
        self.arrow_left.setMaximumSize(300, 35)
        self.arrow_left.clicked.connect(self.arrowLeftFunction)  # Connect the button to its function
        arrow_layout.addWidget(self.arrow_left, 1, 0)

        self.arrow_right = QPushButton(arrows_container)
        self.arrow_right.setText("→")
        self.arrow_right.setMinimumSize(85, 35)
        self.arrow_right.setMaximumSize(300, 35)
        self.arrow_right.clicked.connect(self.arrowRightFunction)  # Connect the button to its function
        arrow_layout.addWidget(self.arrow_right, 1, 2)

        self.arrow_down = QPushButton(arrows_container)
        self.arrow_down.setObjectName("arrow_down")
        self.arrow_down.setText("↓")
        self.arrow_down.setMinimumSize(85, 35)
        self.arrow_down.setMaximumSize(300, 35)
        self.arrow_down.clicked.connect(self.arrowDownFunction)  # Connect the button to its function
        arrow_layout.addWidget(self.arrow_down, 2, 1)

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

        # print(self.widget.width())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Trabalho de CG"))
        self.pushButton.setText(_translate("MainWindow", "Save as xml"))
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

    def changelabeltext(self):
        self.label.setText("Saved")
        pathFilename = self.saveFileDialog()
        xml = XmlWriter(pathFilename)
        xml.write(self.viewPortPointsCoordinates,
                  self.viewPortLinesCoordinates, self.viewPortPolygonsCoordinates)
        self.pushButton.hide()

    # Show the form
    # def showPointForm(self):
    #     self.form_widget_point.show()

    # # Hide the form
    # def hidePointForm(self):
    #     self.form_widget_point.hide()

    # def hidePoygonForm(self):
    #     self.form_widget_polygon.hide()

    # Confirm the point and process it
    def confirmPoint(self):
        x = float(self.input_x.text())
        y = float(self.input_y.text())
        point = Point((x, y))
        conversor = WindowToViewportConversor()
        convertedPoint = conversor.convertToViewport(
            point, self.main_window, self.viewport)
        self.worldPointsCoordinates.append(point)
        self.widget.drawPoint(convertedPoint)
        self.point_dialog.accept()  # Close the dialog

    #Line functions below
    # def showLineForm(self):
    #     self.form_widget_line.show()

    # def hideLineForm(self):
    #     self.form_widget_line.hide()

    # def hidePolygonForm(self):
    #     self.form_widget_polygon.hide()

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
        self.widget.drawLine(convertedLine)
        self.line_dialog.accept()  # Close the dialog

    def confirmPolygon(self):
        points = []
        for i in range(len(self.polygon_inputs_x)):
            x_value = float(self.polygon_inputs_x[i].text())
            y_value = float(self.polygon_inputs_y[i].text())
            points.append(Point((x_value, y_value)))
        polygon = Polygon(*points)
        self.worldPolygonsCoordinates.append(polygon)
        conversor = WindowToViewportConversor()
        convertedPolygon = conversor.convertToViewport(
            polygon, self.main_window, self.viewport)
        self.worldPolygonsCoordinates.append(polygon)
        self.widget.drawPolygon(convertedPolygon)
        self.polygon_dialog.accept()


    # Define the functions for the buttons below
    def pontoFunction(self):
        self.createPointForm()

    def linhaFunction(self):
        self.createLineForm()

    def poligonoFunction(self):
        self.createPolygonForm()

    def moveWindow(self, delta_x, delta_y):
        # Atualiza as coordenadas da janela (Window)
        self.main_window.setXwMin(self.main_window.getXwMin() + delta_x)
        self.main_window.setXwMax(self.main_window.getXwMax() + delta_x)
        self.main_window.setYwMin(self.main_window.getYwMin() + delta_y)
        self.main_window.setYwMax(self.main_window.getYwMax() + delta_y)
        # print("Novas coordenadas mundo: ", self.main_window.getXwMin(), self.main_window.getXwMax(), self.main_window.getYwMin(), self.main_window.getYwMax())

        # Limpa as coordenadas do viewport para redesenho
        self.windowPointsCoordinates.clear()
        self.windowLinesCoordinates.clear()
        self.windowPolygonsCoordinates.clear()

        for point in self.worldPointsCoordinates:
            if (point.getPoint()[0] >= self.main_window.getXwMin() and point.getPoint()[0] <= self.main_window.getXwMax() and
                point.getPoint()[1] >= self.main_window.getYwMin() and point.getPoint()[1] <= self.main_window.getYwMax()
            ):
                self.windowPointsCoordinates.append(point)
                # print("Ponto: ", point.getPoint())

        cohen = CohenSutherland(self.main_window)
        for line in self.worldLinesCoordinates:
            if (cohen.cohen_sutherland_clip(line.getLine()[0][0], line.getLine()[0][1],
                line.getLine()[1][0], line.getLine()[1][1])):
                self.windowLinesCoordinates.append(line)
                # print("Linha: ", line.getLine())

        for polygon in self.worldPolygonsCoordinates:
            # print(polygon, self.main_window)
            weiler = WeilerAtherton(self.main_window)
            polygon_list = weiler.weiler_atherton(polygon)
            if ( len(polygon_list.getPolygon()) != 0):
                self.windowPolygonsCoordinates.append(polygon_list)
                # print("Polygon: ", polygon.getPolygon())

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
    def arrowUpFunction(self):
        self.moveWindow(0, -10)

    def arrowDownFunction(self):
        self.moveWindow(0, +10)

    def arrowLeftFunction(self):
        self.moveWindow(+10, 0)

    def arrowRightFunction(self):
        self.moveWindow(-10, 0)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    MainWindow.show()
    app.exec_()
