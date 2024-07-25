#  developer Aleksandr Kolesnikov

## SystemInfoWidget

SystemInfoWidget — это скрипт на Python, представляющий собой виджет для отображения информации о системе. Он использует библиотеки psutil и PyQt5.
Виджет предназначен для отображения данных о батарее, загрузке процессора, виртуальной памяти, времени загрузки системы и температуре процессора.

### Установка зависимостей

Для работы скрипта необходимо установить Python, а также библиотеки psutil и PyQt5:

```bash
pip install psutil PyQt5
```

### Запуск скрипта

Скрипт не требует дополнительных настроек для запуска. Просто выполните его следующим образом:

```python

# main.py

from PyQt5.QtWidgets import QApplication
from source_code.system_info_widget import SystemInfoWidget

if __name__ == '__main__':
    app = QApplication([])

    widget = SystemInfoWidget()
    widget.show()

    app.exec_()
```

### Класс SystemInfoWidget

**Основные атрибуты:**

- `text_edit`: `QTextEdit` для отображения текста с информацией о системе.
- Флажки (`QCheckBox`) для выбора отображаемых параметров: батарея, загрузка CPU, виртуальная память, время загрузки системы, температура CPU.
- `hide_button`: кнопка для скрытия/отображения флажков.
- `font_size_slider`: `QSlider` для изменения размера шрифта в текстовом поле.

**Методы:**

- `update_info()`: обновляет текстовое поле с текущей информацией о системе.
- `hide_parameters()`: скрывает или показывает флажки и кнопку в зависимости от их текущего состояния.
- `change_font_size(value)`: изменяет размер шрифта в текстовом поле в зависимости от значения слайдера.

### Стилизация и отображение

Виджет имеет прозрачный фон, стилизованное текстовое поле и обрамление.
Он также устанавливает свои размеры и начальное положение на экране.

### Рекомендации

Для успешного использования скрипта на различных операционных системах убедитесь, что Python доступен в системной переменной PATH, а также что установлены и настроены необходимые зависимости (psutil и PyQt5).
Скрипт тестировался только на Linux, и работоспособность на других системах не гарантируется.

### Ссылки

- [Документация PyQt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Документация psutil](https://psutil.readthedocs.io/en/latest/)


### License

Данный скрипт является личной собственностью автора и может быть использован безвозмездно.


# SystemInfoWidget

SystemInfoWidget is a Python script that serves as a widget for displaying system information. It utilizes the psutil and PyQt5 libraries. The widget is designed to show data about battery status, CPU load, virtual memory, system boot time, and CPU temperature.

## Installation of Dependencies

To run the script, you need to have Python installed, as well as the psutil and PyQt5 libraries:

```bash
pip install psutil PyQt5
```

## Running the Script

The script does not require additional configuration to run. Simply execute it as follows:

```python

# main.py

from PyQt5.QtWidgets import QApplication
from source_code.system_info_widget import SystemInfoWidget

if __name__ == '__main__':
    app = QApplication([])

    widget = SystemInfoWidget()
    widget.show()

    app.exec_()
```

## Class SystemInfoWidget

**Main Attributes:**

- `text_edit`: `QTextEdit` for displaying text with system information.
- Checkboxes (`QCheckBox`) for selecting displayed parameters: battery, CPU load, virtual memory, system boot time, CPU temperature.
- `hide_button`: button to hide/show checkboxes.
- `font_size_slider`: `QSlider` for changing the font size in the text field.

**Methods:**

- `update_info()`: updates the text field with the current system information.
- `hide_parameters()`: hides or shows checkboxes and the button based on their current state.
- `change_font_size(value)`: changes the font size in the text field based on the slider value.

## Styling and Display

The widget features a transparent background, a styled text field, and a border. It also sets its dimensions and initial position on the screen.

## Recommendations

To successfully use the script on various operating systems, ensure that Python is available in the system PATH and that the necessary dependencies (psutil and PyQt5) are installed and configured. The script has only been tested on Linux, and functionality on other systems is not guaranteed.

## Links

- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [psutil Documentation](https://psutil.readthedocs.io/en/latest/)

## License

This script is the personal property of the author and can be used freely.

