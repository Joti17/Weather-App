import requests
import sys
import os
import tempfile
import time

import threading
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import screeninfo
import random
global city, data, tmp_path, URL

def get_api_key_from_args():
    """
    Parses command line arguments looking for a flag that starts with '-'.
    If found, uses that flag (without the leading '-') as the API key.
    Example:
        python main.py -MY_API_KEY
    Will extract 'MY_API_KEY' as the API key.
    """
    for arg in sys.argv[1:]:
        if arg.startswith('-') and len(arg) > 1:
            return arg[1:]  # Remove the leading dash and return the rest as API key
    print("Get an api Key here: https://www.weatherapi.com/")
    return None
API_KEY = get_api_key_from_args()
if not API_KEY:
    API_KEY = "KEY"
URL = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q=" #&q=location&api=yes

screen = screeninfo.get_monitors()[1]
global x, y, fontsize, bgs, tmp_path
window_width = 500
window_height = 500

default_img = "https://cdn.weatherapi.com/weather/64x64/day/113.png"
with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
    response = requests.get(default_img)
    response.raise_for_status()
    tmp_file.write(response.content)
    tmp_path = tmp_file.name


bgs = ["bg.jpg", "bg2.jpeg", "bg3.jpeg", "bg4.jpeg", "bg5.jpeg"]
fontsize = 80
x = screen.x + (screen.width - window_width) // 2
y = screen.y + (screen.height - window_height) // 2
class Window(QWidget):
    def __init__(self):
        self.url = create_url("london") #default
        super().__init__()

        self.city = "london"
        self.temp = 30
        self.setWindowTitle("Weather App")
        self.setGeometry(x, y, window_width, window_height)


        self.bg_pixmap = QPixmap(random.choice(bgs))


        self.AppNameLabel = QLabel("Weather App")
        self.AppNameLabel.setAlignment(Qt.AlignCenter)
        self.AppNameLabel.setStyleSheet("color: black; font-weight: bold;")
        self.AppNameLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.ConditionLabel = QLabel()
        self.ConditionLabel.setAlignment(Qt.AlignCenter)
        self.ConditionLabel.setScaledContents(True)
        self.ConditionPixmap = QPixmap(tmp_path)
        self.ConditionLabel.setPixmap(self.ConditionPixmap)

        self.ConditionText = QLabel()
        self.ConditionText.setAlignment(Qt.AlignCenter)
        self.ConditionText.setStyleSheet("color: white; font-weight: bold; background: transparent;")
        self.ConditionText.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.InputCity = QLineEdit(self)
        self.InputCity.setPlaceholderText("Enter City")
        self.InputCity.setStyleSheet("""
    QLineEdit {
        border: 2px solid #555555;
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 16px;
        color: #222222;
        background-color: #f5f5f5;
        selection-background-color: #3399ff;
    }
    QLineEdit:focus {
        border-color: #3399ff;
        background-color: #ffffff;
    }
""")
        self.InputCity.setFixedHeight(30)
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.setFixedHeight(35)
        self.submit_button.setStyleSheet("""
                    QPushButton {
                        background-color: #3399ff;
                        color: white;
                        font-weight: bold;
                        border-radius: 8px;
                        padding: 6px 12px;
                    }
                    QPushButton:hover {
                        background-color: #267acc;
                    }
                    QPushButton:pressed {
                        background-color: #1a4d99;
                    }
                """)
        self.submit_button.clicked.connect(self.on_submit_clicked)
        layout = QGridLayout()
        layout.addWidget(self.AppNameLabel, 0, 0, 1, 1, alignment=Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(self.InputCity, 1, 0, alignment=Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(self.submit_button, 2, 0, alignment=Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(self.ConditionLabel, 4, 0, alignment=Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(self.ConditionText, 3, 0, alignment=Qt.AlignHCenter | Qt.AlignTop)
        layout.setRowStretch(5, 1)

        self.setLayout(layout)

        self.base_fontsize = fontsize
        self.update_ui_sizes()
        self.data = self.get_data()
        if self.data and "current" in self.data:
            self.temp = self.data["current"]["temp_c"]
        else:
            self.temp = 30

    def on_submit_clicked(self):
        self.city = self.InputCity.text()
        self.url = create_url(self.city)
        self.data = self.get_data()
        self.update_ui(self.data)


    def update(self, temp, new_file):
        """Update weather icon and temperature text"""
        self.ConditionPixmap = QPixmap(new_file)
        self.ConditionLabel.setPixmap(self.ConditionPixmap)
        self.ConditionText.setText(f"{temp} °C")
        self.update_ui_sizes()

    def update_ui(self, data):
        icon_url = data["current"]["condition"]["icon"]
        temp_c = data["current"]["temp_c"]
        update_icon(icon_url, self.ConditionLabel)
        self.ConditionText.setText(f"{temp_c} °C")
        self.update_ui_sizes()


    def update_ui_sizes(self):
        """Update fonts and pixmap sizes dynamically on window resize"""

        font_size = max(10, min(self.base_fontsize, int(self.width() * 0.1)))
        self.AppNameLabel.setFont(QFont("Arial", font_size))

        temp_font_size = max(8, int(font_size * 0.75))
        self.ConditionText.setFont(QFont("Arial", temp_font_size))

        icon_size = int(self.width() * 0.5)
        scaled_pixmap = self.ConditionPixmap.scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ConditionLabel.setPixmap(scaled_pixmap)
        self.ConditionLabel.setFixedSize(scaled_pixmap.size())

    def paintEvent(self, event):
        painter = QPainter(self)
        scaled_bg = self.bg_pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        painter.drawPixmap(0, 0, scaled_bg)
        super().paintEvent(event)

    def resizeEvent(self, event):
        self.update_ui_sizes()
        super().resizeEvent(event)


    def get_data(self):
        request = requests.get(self.url)
        if check_url(request) == 0:
            request.raise_for_status()
            data = request.json()
            update_icon(data["current"]["condition"]["icon"], self.ConditionLabel)
            self.update_ui(data)
            return data
        else:
            print(f"Invalid URL, Error: {check_url(request)}")




def create_url(location, url=URL):
    return url + location.lower() + "&api=yes"

def check_url(request: requests.models.Response) -> int: #0 is ok, val>=1 is error
    Status = request.status_code
    if Status in range(200, 227):
        return 0
    else:
        return Status



request = requests.get(create_url("London"))
request_json = request.json()

def update_icon(condition_icon_url, label):
    # condition_icon_url is something like: "//cdn.weatherapi.com/weather/64x64/day/113.png"
    full_icon_url = "https:" + condition_icon_url

    try:
        response = requests.get(full_icon_url)
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            tmp_file.write(response.content)
            icon_path = tmp_file.name

        pixmap = QPixmap(icon_path)
        label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))


    except requests.RequestException as e:
        print(f"Failed to download icon: {e}")





def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    old_temp = 0

    def periodic_task():
        while True:
            window.data = window.get_data()

            time.sleep(10)
    thread = threading.Thread(target=periodic_task, daemon=True)
    thread.start()

    window.data = window.get_data()
    while True:
        if old_temp != window.temp:
            window.update(window.temp, tmp_path)
        window.temp = window.data["current"]["temp_c"]
        old_temp = window.temp


        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    os.remove(tmp_path)
