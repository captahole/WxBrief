# Gets METAR TAF Delays with UI
import sys
import os
import platform
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
import requests

class WxBrief(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Wx Brief')

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Input fields for airports
        airportLayout = QHBoxLayout()
        layout.addLayout(airportLayout)
        self.departureInput = QLineEdit()
        self.departureInput.setPlaceholderText('Departure (JFK)')
        airportLayout.addWidget(self.departureInput)
        self.arrivalInput = QLineEdit()
        self.arrivalInput.setPlaceholderText('Arrival (LAX)')
        airportLayout.addWidget(self.arrivalInput)

        # Button to fetch weather
        self.weatherButton = QPushButton('--> Fetch Weather <--')
        self.weatherButton.setStyleSheet("font-weight: bold")
        self.weatherButton.clicked.connect(self.getWeather)
        self.weatherButton.clicked.connect(self.playClickSound)
        layout.addWidget(self.weatherButton)

        # Text area to display weather
        self.weatherOutput = QTextEdit()
        self.weatherOutput.setReadOnly(True)
        layout.addWidget(self.weatherOutput)

        # Button to fetch DATIS
        self.datisButton = QPushButton('--> Fetch DATIS <--')
        self.datisButton.setStyleSheet("font-weight: bold")
        self.datisButton.clicked.connect(self.getDatis)
        self.datisButton.clicked.connect(self.playClickSound)
        layout.addWidget(self.datisButton)

        # Text area to display DATIS
        self.datisOutput = QTextEdit()
        self.datisOutput.setReadOnly(True)
        layout.addWidget(self.datisOutput)

        # Button to fetch airport status
        self.statusButton = QPushButton('--> Fetch Airport Status <--')
        self.statusButton.setStyleSheet("font-weight: bold")
        self.statusButton.clicked.connect(self.getAirportStatus)
        self.statusButton.clicked.connect(self.playClickSound)
        layout.addWidget(self.statusButton)


        # Text area to display airport status
        self.statusOutput = QTextEdit()
        self.statusOutput.setReadOnly(True)
        layout.addWidget(self.statusOutput)

        # Exit button
        self.exitButton = QPushButton('Exit')
        self.exitButton.setStyleSheet("font-weight: bold")
        self.exitButton.clicked.connect(self.close)
        self.exitButton.clicked.connect(self.playClickSound)
        layout.addWidget(self.exitButton)

        self.show()

    def getWeather(self):
        airport1 = self.departureInput.text()
        airport2 = self.arrivalInput.text()
        weather_data = self.fetchWeather(airport1, airport2)
        if weather_data is not None:
            self.weatherOutput.setText(weather_data)

    def getDatis(self):
        airport1 = self.departureInput.text()
        airport2 = self.arrivalInput.text()
        datis1 = self.fetchDatis(airport1)
        datis2 = self.fetchDatis(airport2)
        self.datisOutput.setText(f'Departure DATIS:\n{datis1}\n\nArrival DATIS:\n{datis2}')

    def getAirportStatus(self):
        airport1 = self.departureInput.text()
        airport2 = self.arrivalInput.text()
        status1 = self.fetchAirportStatus(airport1)
        status2 = self.fetchAirportStatus(airport2)
        self.statusOutput.setText(f'Departure Airport Status:\n{status1}\n\nArrival Airport Status:\n{status2}')

    def fetchWeather(self, airport1, airport2):
        airport1 = f'K{airport1}'
        airport2 = f'K{airport2}'
        base_url = "https://aviationweather.gov/api/data/taf?"
        params = {
            "ids": f"{airport1},{airport2}",
            "format": "raw",
            "metar": "true",
            "time": "valid",
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def fetchDatis(self, airport_code):
        url = f"https://datis.clowd.io/api/K{airport_code}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()[0]
                return data['datis']
            except (KeyError, IndexError):
                return "The 'datis' field is not present in the response."
        else:
            return f"No DATIS Avaliable. Status code: {response.status_code}"

    def fetchAirportStatus(self, airport_code):
        url = f'https://external-api.faa.gov/asws/api/airport/status/{airport_code}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'Status' in data:
                return f"{data['ICAO']}, {data['Status']}"
            else:
                return "The 'Status' field is not present in the response."
        else:
            return f"Failed to fetch data. Status code: {response.status_code}"

    def playClickSound(self):
        if platform.system() == 'Windows':
            import winsound
            winsound.Beep(2500, 1000)
        else:
            import os
            os.system('afplay /System/Library/Sounds/Glass.aiff')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { color: black; font-family: Courier New; font-size: 14pt; }")
    ex = WxBrief()
    sys.exit(app.exec_())
