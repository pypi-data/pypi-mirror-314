#############################################################################
##
## Copyright (C) 2021 Riverbank Computing Limited
## Copyright (C) 2012 Digia Plc
## All rights reserved.
##
## This file is part of the examples of PyQtChart.
##
## $QT_BEGIN_LICENSE$
## Licensees holding valid Qt Commercial licenses may use this file in
## accordance with the Qt Commercial License Agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and Digia.
## $QT_END_LICENSE$
##
#############################################################################


import sys

from PyQt6.QtCharts import QAreaSeries, QChart, QChartView, QLineSeries
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QGradient, QLinearGradient, QPainter, QPen
from PyQt6.QtWidgets import QApplication, QMainWindow


app = QApplication(sys.argv)

series0 = QLineSeries()
series1 = QLineSeries()

series0 << QPointF(1, 5) << QPointF(3, 7) << QPointF(7, 6) << QPointF(9, 7) \
        << QPointF(12, 6) << QPointF(16, 7) << QPointF(18, 5)
series1 << QPointF(1, 3) << QPointF(3, 4) << QPointF(7, 3) << QPointF(8, 2) \
        << QPointF(12, 3) << QPointF(16, 4) << QPointF(18, 3)

series = QAreaSeries(series0, series1)
series.setName("Batman")
pen = QPen(0x059605)
pen.setWidth(3)
series.setPen(pen)

gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 1))
gradient.setColorAt(0.0, 0x3cc63c)
gradient.setColorAt(1.0, 0x26f626)
gradient.setCoordinateMode(QGradient.CoordinateMode.ObjectBoundingMode)
series.setBrush(gradient)

chart = QChart()
chart.addSeries(series)
chart.setTitle("Simple areachart example")
chart.createDefaultAxes()
chart.axes(Qt.Orientation.Horizontal)[0].setRange(0, 20)
chart.axes(Qt.Orientation.Vertical)[0].setRange(0, 10)

chartView = QChartView(chart)
chartView.setRenderHint(QPainter.RenderHint.Antialiasing)

window = QMainWindow()
window.setCentralWidget(chartView)
window.resize(400, 300)
window.show()

sys.exit(app.exec())
