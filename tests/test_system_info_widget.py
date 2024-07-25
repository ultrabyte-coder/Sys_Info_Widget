import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QPointF, QEvent
from PyQt5.QtGui import QMouseEvent
from source_code.system_info_widget import SystemInfoWidget


class SystemInfoWidgetTests(unittest.TestCase):
    """
    Класс для тестирования функционала виджета системной информации.
    """

    def setUp(self):
        """
        Метод инициализации ресурсов перед выполнением каждого теста.

        Создает экземпляр QApplication для запуска приложения.
        Создает экземпляр SystemInfoWidget и отображает его на экране.
        """
        self.app = QApplication([])
        self.widget = SystemInfoWidget()
        self.widget.show()

    def tearDown(self):
        """
        Метод освобождения ресурсов после выполнения каждого теста.

        Закрывает виджет SystemInfoWidget.
        """
        self.widget.close()

    def test_components_displayed_correctly(self):
        """
        Проверяет корректность отображения всех компонентов при запуске.

        Проверяет, что все компоненты видны и в правильном порядке.
        Проверяет, что чекбоксы изначально скрыты.
        Проверяет правильность текста в кнопке "Показать параметры".
        """
        self.assertFalse(self.widget.text_edit.isHidden())
        self.assertFalse(self.widget.hide_button.isHidden())
        self.assertFalse(self.widget.font_size_slider.isHidden())

        self.assertTrue(self.widget.battery_checkbox.isHidden())
        self.assertTrue(self.widget.cpu_checkbox.isHidden())
        self.assertTrue(self.widget.virtual_memory_checkbox.isHidden())
        self.assertTrue(self.widget.boot_time_checkbox.isHidden())
        self.assertTrue(self.widget.cpu_temp_checkbox.isHidden())

        self.assertEqual(self.widget.hide_button.text(), "Показать параметры")

    def test_update_info(self):
        """
        Проверяет правильность обновления информации о системе.

        Обновляет информацию о системе с помощью метода update_info().
        Проверяет, что текст в QTextEdit не является пустым.
        Проверяет, что текст в QTextEdit содержит определенные ключевые слова.
        """
        self.widget.update_info()

        self.assertIsNotNone(self.widget.text_edit.toPlainText())

        system_info_text = self.widget.text_edit.toPlainText()
        self.assertIn("Батарея", system_info_text)
        self.assertIn("Общая загрузка процессора", system_info_text)
        self.assertIn("Используемая виртуальная память", system_info_text)
        self.assertIn("Время загрузки системы", system_info_text)
        self.assertIn("Средняя температура процессора", system_info_text)

    def test_hide_parameters(self):
        """
        Проверяет функциональность кнопки "Скрыть параметры".

        Проверяет, что кнопка "Показать параметры" отображается изначально.
        Проверяет, что чекбоксы изначально скрыты.
        Кликает на кнопку "Показать параметры", чтобы показать чекбоксы.
        Проверяет, что кнопка "Скрыть параметры" отображается после клика.
        Проверяет, что чекбоксы отображаются после клика.
        Кликает на кнопку "Скрыть параметры" снова, чтобы скрыть чекбоксы.
        Проверяет, что кнопка "Показать параметры" отображается после второго клика.
        Проверяет, что чекбоксы скрыты после второго клика.
        """
        self.assertEqual(self.widget.hide_button.text(), "Показать параметры")

        self.assertTrue(self.widget.battery_checkbox.isHidden())
        self.assertTrue(self.widget.cpu_checkbox.isHidden())
        self.assertTrue(self.widget.virtual_memory_checkbox.isHidden())
        self.assertTrue(self.widget.boot_time_checkbox.isHidden())
        self.assertTrue(self.widget.cpu_temp_checkbox.isHidden())

        self.widget.hide_button.click()

        self.assertEqual(self.widget.hide_button.text(), "Скрыть параметры")

        self.assertFalse(self.widget.battery_checkbox.isHidden())
        self.assertFalse(self.widget.cpu_checkbox.isHidden())
        self.assertFalse(self.widget.virtual_memory_checkbox.isHidden())
        self.assertFalse(self.widget.boot_time_checkbox.isHidden())
        self.assertFalse(self.widget.cpu_temp_checkbox.isHidden())

        self.widget.hide_button.click()

        self.assertEqual(self.widget.hide_button.text(), "Показать параметры")

        self.assertTrue(self.widget.battery_checkbox.isHidden())
        self.assertTrue(self.widget.cpu_checkbox.isHidden())
        self.assertTrue(self.widget.virtual_memory_checkbox.isHidden())
        self.assertTrue(self.widget.boot_time_checkbox.isHidden())
        self.assertTrue(self.widget.cpu_temp_checkbox.isHidden())

    def test_change_font_size(self):
        """
        Проверяет изменение размера шрифта в текстовом поле.

        Изменяет размер шрифта с помощью метода change_font_size().
        Проверяет, что размер шрифта равен заданному значению.
        """
        self.widget.change_font_size(16)
        font = self.widget.text_edit.font()
        self.assertEqual(font.pixelSize(), 16)

    def test_drag_and_drop(self):
        """
        Проверяет возможность перетаскивания виджета мышью.

        Генерирует события мыши для эмуляции перетаскивания.
        Проверяет, что курсор становится ArrowCursor после перетаскивания.
        """
        event = QMouseEvent(QEvent.MouseButtonPress, QPointF(50, 50), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        QApplication.postEvent(self.widget, event)

        event = QMouseEvent(QEvent.MouseMove, QPointF(80, 80), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        QApplication.postEvent(self.widget, event)

        event = QMouseEvent(QEvent.MouseButtonRelease, QPointF(80, 80), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        QApplication.postEvent(self.widget, event)

        final_cursor = self.widget.cursor().shape()

        self.assertEqual(final_cursor, Qt.ArrowCursor)


if __name__ == '__main__':
    unittest.main()
