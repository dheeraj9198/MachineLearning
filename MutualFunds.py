import requests
from scipy.signal import argrelextrema
from datetime import datetime
import matplotlib
# prevent NoneType error for versions of matplotlib 3.1.0rc1+ by calling matplotlib.use()
# For more on why it's necessary, see
# https://stackoverflow.com/questions/59656632/using-qt5agg-backend-with-matplotlib-3-1-2-get-backend-changes-behavior
matplotlib.use('qt5agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QVBoxLayout
import matplotlib.pyplot as plt
import sys


timeframe = 400

fundNamesToTrackMinima = [("INF769K01DM9", "Mirae Asset ELSS Tax Saver Fund"), # Equity Linked Savings Scheme, 18,843 Crs, 3 years, 20.67%, 0%

                          ("INF109K01Z48", "ICICI Prudential Technology"), # Tech Fund,  11,580 Crs, No, 25.87%, 1%

                          ("INF109K016L0", "ICICI Prudential Bluechip Fund"), # Large-Cap, 44,425.37 Cr, No, 17.73%, 1%

                          ("INF179K01XQ0", "HDFC Mid-Cap Opportunities Fund"), # Mid-Cap, 52,137.70 Cr, No, 23.59%, 1%

                          ("INF179KA1RW5", "HDFC Small Cap Fund"), # Small-Cap, 25,408.97 Cr, No, 23.62%, 1%

                          ("INF109K012K1", "ICICI Prudential Value Discovery Fund"), # Value Oriented, 35,089.33 Cr, No, 21.67%, 1%

                         # ("INF179KC1GI5", "HDFC Defence Fund"), # defence sector, 1,591.46 Cr.,No, 149%, 1% (NEW FUND)

                          ("NIFTY50","NIFTY 50"),("BANKNIFTY","BANK NIFTY"),
                          ("AMZN","US AMAZON"),("AAPL", "US APPLE"),("MSFT","US MICROSOFT"),("GOOG","US GOOGLE"),("NVDA","US NVIDIA")
                           ]

def getNormalisedArray(data):
    max1 = max(data)
    temp = []
    for a in data:
        temp.append((a/max1 * 100))
    return temp

def getTrimmedArray(data,size):
    return data[-size:]

def getData(url):
    if 'coin' in url:
        r = requests.get(url)
        return r.json()['data']
    elif 'groww' in url:
        r = requests.get(url)
        return r.json()['candles']
    else:
        return []

class plotWindow():
    def __init__(self, parent=None):
        self.app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.MainWindow.__init__()
        self.MainWindow.setWindowTitle("ALGO TRADING")
        self.canvases = []
        self.figure_handles = []
        self.toolbar_handles = []
        self.tab_handles = []
        self.current_window = -1
        self.tabs = QTabWidget()
        self.MainWindow.setCentralWidget(self.tabs)
        self.MainWindow.resize(1280, 900)
        self.MainWindow.show()

    def addPlot(self, title, figure):
        new_tab = QWidget()
        layout = QVBoxLayout()
        new_tab.setLayout(layout)

        figure.subplots_adjust(left=0.05, right=0.99, bottom=0.05, top=0.91, wspace=0.2, hspace=0.2)
        new_canvas = FigureCanvas(figure)
        new_toolbar = NavigationToolbar(new_canvas, new_tab)

        layout.addWidget(new_canvas)
        layout.addWidget(new_toolbar)
        self.tabs.addTab(new_tab, title)

        self.toolbar_handles.append(new_toolbar)
        self.canvases.append(new_canvas)
        self.figure_handles.append(figure)
        self.tab_handles.append(new_tab)

    def show(self):
        self.app.exec_()

if __name__ == '__main__':
    import numpy as np

    pw = plotWindow()

    for toTrackMinima in fundNamesToTrackMinima:
        url = "https://staticassets.zerodha.com/coin/historical-nav/" + toTrackMinima[0] + ".json"
        if "NIFTY" in toTrackMinima[0]:
            url = "https://groww.in/v1/api/charting_service/v2/chart/delayed/exchange/NSE/segment/CASH/NIFTY/3y?intervalInDays=1&minimal=true"
        if "US" in toTrackMinima[1]:
            url = "https://groww.in/v1/api/us_charting_service/v2/chart/exchange/US/segment/CASH/" + toTrackMinima[
                0] + "/3y?intervalInDays=1&minimal=true"

        data = getData(url)
        dates, price = zip(*data)
        dates = getTrimmedArray(dates, timeframe)
        price = getTrimmedArray(price, timeframe)
        price = getNormalisedArray(price)

        fig = plt.figure()
        ax = fig.gca()
        ax.set_yticks(np.arange(0, 101, 1))
        ax.set_xticks(np.arange(0, timeframe, 1))

        plt.plot(price, label=toTrackMinima[1])
        pw.addPlot(toTrackMinima[1], fig)
        plt.legend()
        plt.grid()

        minimaDates = argrelextrema(np.array(price), np.less)
        minimaDates = list(minimaDates)

        datesList = list(dates)

        stack = []

        for d in minimaDates:
            for dd in d:
                stack.append((datesList[dd], price[dd]))

        last = stack.pop()
        now = datetime.now()
        delta = now - datetime.fromtimestamp(last[0])

        if delta.days < 10:
            print(toTrackMinima[1] + " ===> " + str(datetime.fromtimestamp(last[0])))

    pw.show()
