import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        print('Ведите координаты через пробел:')
        self.cor = input()
        if ',' in self.cor:
            print('Координаты введены не верно')
        print('Введите маштаб в %:')
        print('Чем меньше число, тем больше охват карты')
        self.mash = input()
        self.check()
        super().__init__()
        self.initUI()

    def keyPressEvent(self, event):
        w = {1: '0', 2: '210', 3: '110', 4: '45', 5: '22', 6: '12', 7: '6', 8: '4', 9: '2', 10: '0.8', 11: '0.5',
             12: '0.2', 13: '0.1015', 14: '0.0482', 15: '0.0237', 16: '0.0109', 17: '0.0066'}
        latitude, longitude = float(self.cor.split(',')[1]), float(self.cor.split(',')[0])
        if event.key() == 16777235:  # up
            if latitude + float(w[self.mash]) <= 90:
                latitude += float(w[self.mash]) / 2
            else:
                latitude = 90
        if event.key() == 16777237:  # down
            if latitude - float(w[self.mash]) >= -90:
                latitude -= float(w[self.mash]) / 2
            else:
                latitude = -90
        if event.key() == 16777236:  # right
            if longitude + float(w[self.mash]) <= 180:
                longitude += float(w[self.mash])
            else:
                num1 = 180 - longitude
                longitude = -180 + num1
        if event.key() == 16777234:  # left
            if longitude - float(w[self.mash]) >= -180:
                longitude -= float(w[self.mash])
            else:
                num1 = -180 - longitude
                longitude = 180 - abs(num1)
            # 37.530887 55.703118
            '''
            16777235 up
            16777237 down
            16777236 right
            16777234 left
            '''
        self.cor = str(longitude) + ',' + str(latitude)
        self.getImage()

    def check(self):
        self.cor = ','.join(self.cor.split())
        if 100 < float(self.mash):
            self.prov = 1
            print('Маштаб должен быть введен в диапазоне от 0 до 100!')
        self.mash = round(0.17 * int(self.mash))
        if self.mash < 0:
            self.mash = 0
        if self.mash > 17:
            self.mash = 17

    def getImage(self):
        map_request = "http://static-maps.yandex.ru/1.x/?ll=" + self.cor + "&z=" + str(self.mash) + "&size=600,450&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.set_image(self.map_file)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.image = QLabel(self)
        self.getImage()

    def set_image(self, map):
        self.pixmap = QPixmap(map)
        self.image.move(0, 0)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())