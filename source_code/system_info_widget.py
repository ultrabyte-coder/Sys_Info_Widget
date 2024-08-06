# Импортируем необходимые модули
import psutil
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QCheckBox, QPushButton, QSlider
from PyQt5.QtCore import Qt, QTimer, QPoint, QEvent


class SystemInfoWidget(QWidget):
    """
    Класс SystemInfoWidget - это пользовательский виджет PyQt5, предназначенный для отображения различных системных данных,
    включая состояние батареи, загрузку процессора, использование виртуальной памяти, время загрузки системы и температуру процессора.
    Он предоставляет пользовательский интерфейс с флажками для выбора отображаемых данных и ползунком для регулировки размера шрифта.
    """

    def __init__(self):
        """
        Конструктор класса инициализирует виджет и настраивает его компоненты.
        """
        super().__init__()

        # Установка флагов окна, чтобы сделать виджет безрамочным и всегда сверху
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Установка атрибута, чтобы сделать фон прозрачным
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Изменение размера виджета и перемещение его в левый нижний угол экрана
        self.resize(400, 320)
        self.move(10, self.screen().availableGeometry().height() - 120)

        # Создание текстового поля
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("background-color: transparent; color: #BFFF00;")
        font = self.text_edit.font()
        font.setPixelSize(14)
        self.text_edit.setFont(font)
        self.text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Создание флажков
        self.battery_checkbox = QCheckBox("Батарея")
        self.battery_checkbox.setChecked(True)
        self.battery_checkbox.setStyleSheet("color: red;")
        
        self.cpu_checkbox = QCheckBox("Общая загрузка процессора")
        self.cpu_checkbox.setChecked(True)
        self.cpu_checkbox.setStyleSheet("color: red;")
        
        self.virtual_memory_checkbox = QCheckBox("Виртуальная память")
        self.virtual_memory_checkbox.setChecked(True)
        self.virtual_memory_checkbox.setStyleSheet("color: red;")
        
        self.boot_time_checkbox = QCheckBox("Время загрузки системы")
        self.boot_time_checkbox.setChecked(True)
        self.boot_time_checkbox.setStyleSheet("color: red;")
        
        self.cpu_temp_checkbox = QCheckBox("Температура процессора")
        self.cpu_temp_checkbox.setChecked(True)
        self.cpu_temp_checkbox.setStyleSheet("color: red;")

        # Создание кнопки скрытия
        self.hide_button = QPushButton("Показать параметры")
        self.hide_button.clicked.connect(self.hide_parameters)
        # self.hide_button.setStyleSheet("background-color: #007BFF; color: white;")
        # Расскомментировав параметр выше вы сделает кнопку ПОКАЗАТЬ ПАРАМЕТРЫ с синим фоном и белым шрифтом.
        # Но есть риск, что этим самым полетят тесты, но видимость виджета как на белом так и на чёрном фоне станет лучше.
        
        # Создание ползунка размера шрифта
        self.font_size_slider = QSlider(Qt.Horizontal, self)
        self.font_size_slider.setMinimum(8)
        self.font_size_slider.setMaximum(24)
        self.font_size_slider.setValue(14)
        self.font_size_slider.valueChanged.connect(self.change_font_size)

        # Создание макета и добавление компонентов к нему
        self.parameters_layout = QVBoxLayout()
        self.parameters_layout.addWidget(self.battery_checkbox)
        self.parameters_layout.addWidget(self.cpu_checkbox)
        self.parameters_layout.addWidget(self.virtual_memory_checkbox)
        self.parameters_layout.addWidget(self.boot_time_checkbox)
        self.parameters_layout.addWidget(self.cpu_temp_checkbox)
        self.parameters_layout.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.hide_button)
        layout.addLayout(self.parameters_layout)
        layout.addWidget(self.font_size_slider)
        layout.setContentsMargins(0, 0, 0, 0)

        # Скрываем флажки изначально
        self.battery_checkbox.hide()
        self.cpu_checkbox.hide()
        self.virtual_memory_checkbox.hide()
        self.boot_time_checkbox.hide()
        self.cpu_temp_checkbox.hide()

        self.update_info()

        # Запуск таймера для обновления системных данных каждые 100 миллисекунд
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.update_info())
        self.timer.start(100)

        self.installEventFilter(self)

        self.drag_position = QPoint()

        # Установка стиля виджета
        self.setStyleSheet("border: 2px solid black;")

    def update_info(self):
        """
        Метод обновляет системные данные, отображаемые в текстовом поле.
        """
        # Получение состояния батареи
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        percent = battery.percent

        # Получение загрузки процессора
        cpu_load = psutil.cpu_percent(interval=0.1)

        # Получение информации о виртуальной памяти
        virtual_memory = psutil.virtual_memory()
        virtual_memory_used = virtual_memory.used
        virtual_memory_total = virtual_memory.total
        virtual_memory_available = virtual_memory.available

        # Получение времени загрузки системы
        boot_time_timestamp = psutil.boot_time()
        boot_time = datetime.datetime.fromtimestamp(boot_time_timestamp)

        # Получение температуры процессора
        try:
            cpu_temp_sensors = psutil.sensors_temperatures()['coretemp']
            if cpu_temp_sensors:
                cpu_temp = sum(sensor.current for sensor in cpu_temp_sensors) / len(cpu_temp_sensors)
                cpu_temp = f'{cpu_temp:.2f}°C'
            else:
                cpu_temp = "Нет данных о температуре процессора"
        except (KeyError, IndexError):
            cpu_temp = "Нет данных о температуре процессора"

        # Форматирование полученных данных в строку
        text = ""
        if self.battery_checkbox.isChecked():
            text += f'Батарея: {"заряжается" if plugged else "разряжается"} ({round(percent, 3)}%)\n'
        if self.cpu_checkbox.isChecked():
            text += f'Общая загрузка процессора: {cpu_load}%\n'
        if self.virtual_memory_checkbox.isChecked():
            text += f'Используемая виртуальная память: {virtual_memory_used / 1024 / 1024:.2f} MB\n'
            text += f'Общий объем виртуальной памяти: {virtual_memory_total / 1024 / 1024:.2f} MB\n'
            text += f'Доступно виртуальной памяти: {virtual_memory_available / 1024 / 1024:.2f} MB\n'
        if self.boot_time_checkbox.isChecked():
            text += f'Время загрузки системы: {boot_time}\n'
        if self.cpu_temp_checkbox.isChecked():
            text += f'Средняя температура процессора: {cpu_temp}\n'

        # Обновление текстового поля сформированной строкой
        self.text_edit.setPlainText(text)

    def hide_parameters(self):
        """
        Метод переключает видимость флажков.
        """
        if self.hide_button.text() == "Показать параметры":
            self.battery_checkbox.show()
            self.cpu_checkbox.show()
            self.virtual_memory_checkbox.show()
            self.boot_time_checkbox.show()
            self.cpu_temp_checkbox.show()
            self.hide_button.setText("Скрыть параметры")
        else:
            self.battery_checkbox.hide()
            self.cpu_checkbox.hide()
            self.virtual_memory_checkbox.hide()
            self.boot_time_checkbox.hide()
            self.cpu_temp_checkbox.hide()
            self.hide_button.setText("Показать параметры")

    def change_font_size(self, value):
        """
        Метод изменяет размер шрифта текстового поля в зависимости от значения ползунка.
        """
        font = self.text_edit.font()
        font.setPixelSize(value)
        self.text_edit.setFont(font)

    def mousePressEvent(self, event):
        """
        Метод позволяет виджету быть перетаскиваемым и перемещаемым по экрану.
        """
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()

    def mouseMoveEvent(self, event):
        """
        Метод позволяет виджету быть перетаскиваемым и перемещаемым по экрану.
        """
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """
        Метод позволяет виджету быть перетаскиваемым и перемещаемым по экрану.
        """
        self.setCursor(Qt.ArrowCursor)
        event.accept()

    def eventFilter(self, obj, event):
        """
        Метод фильтрует события и позволяет виджету быть перетаскиваемым и перемещаемым по экрану.
        """
        if event.type() == QEvent.MouseButtonPress and obj == self:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return True
        return super().eventFilter(obj, event)


if __name__ == '__main__':
    app = QApplication([])

    widget = SystemInfoWidget()
    widget.show()

    app.exec_()
