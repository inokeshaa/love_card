import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PyQt6.QtGui import QFont, QColor, QPainter, QBrush

class MatrixBackground(QWidget):
    """Улучшенный фон Матрицы — больше символов, разная яркость"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.columns = []
        self.setFixedSize(parent.size() if parent else (800, 600))
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_matrix)
        self.timer.start(50)  # обновление каждые 50 мс — плавнее
        self.reset_columns()

    def reset_columns(self):
        width = self.width()
        # Больше столбцов — плотнее
        self.columns = [
            {
                'char': '',
                'y': random.randint(-500, 0),
                'speed': random.randint(2, 6),
                'brightness': random.choice([100, 150, 200])  # 3 уровня яркости
            }
            for _ in range(width // 8)  # больше столбцов
        ]

    def update_matrix(self):
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0))  # чёрный фон

        font = QFont("Courier", 10)
        painter.setFont(font)

        for col in self.columns:
            # Выбор символа
            char = random.choice("❤️")
            x = self.columns.index(col) * 8
            y = col['y']
            # Цвет: зелёный с разной яркостью
            green_val = col['brightness']
            painter.setPen(QColor(0, green_val, 0))
            painter.drawText(x, y, char)
            col['y'] += col['speed']
            if y > self.height():
                col['y'] = random.randint(-100, -10)
                col['brightness'] = random.choice([50,100, 150, 200])  # обновляем яркость


class TypingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Секретная открытка для кусаки💖")
        self.resize(700, 500)
        self.setStyleSheet("background-color: black;")

        # Фон Матрицы
        self.matrix_bg = MatrixBackground(self)
        self.matrix_bg.lower()

        # Текстовый лейбл
        self.text_label = QLabel("", self)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setFont(QFont("Courier", 16))
        self.text_label.setStyleSheet("color: lime; background-color: transparent;")
        self.text_label.setGeometry(0, 150, 700, 200)

        # Курсор (QLabel для мигания)
        self.cursor_label = QLabel("", self)
        self.cursor_label.setFont(QFont("Courier", 16))
        self.cursor_label.setStyleSheet("color: lime; background-color: transparent;")
        self.cursor_label.hide()

        # Состояния
        self.phases = [
            "Котик"
            "\n..."
            "\nВо-первых..."
            "\nТы мне сильно нравишься"
            "\n..."
            "\nВайбик схожий чтоли?"
            "\nА во-вторых."
            "\nЯ очень хочу тебе сказать...",
            "\nЯ тебя люблю"
        ]
        self.current_phase = 0
        self.current_text = ""
        self.target_text = ""
        self.is_typing = False

        # Запуск первой фазы
        QTimer.singleShot(1000, self.start_next_phase)

    def start_next_phase(self):
        if self.current_phase >= len(self.phases):
            self.show_choice_dialog()
            return

        self.target_text = self.phases[self.current_phase]
        self.current_text = ""
        self.is_typing = True
        self.type_timer = QTimer()
        self.type_timer.timeout.connect(self.type_next_char)
        self.type_timer.start(140)

        # Показываем курсор
        self.cursor_label.show()
        self.cursor_blink_timer = QTimer()
        self.cursor_blink_timer.timeout.connect(self.blink_cursor)
        self.cursor_blink_timer.start(500)  # мигает каждые 0.5 сек

    def type_next_char(self):
        if len(self.current_text) < len(self.target_text):
            self.current_text = self.target_text[:len(self.current_text) + 1]
            self.text_label.setText(self.current_text)
            # Обновляем позицию курсора
            self.update_cursor_position()
        else:
            self.type_timer.stop()
            self.is_typing = False
            self.cursor_blink_timer.stop()
            self.cursor_label.hide()
            self.current_phase += 1
            QTimer.singleShot(2300, self.start_next_phase)

    def update_cursor_position(self):
        # Позиция курсора — после последнего символа
        text_width = self.fontMetrics().boundingRect(self.current_text).width()
        label_x = self.text_label.x()
        cursor_x = label_x + text_width + 5  # небольшой отступ
        cursor_y = self.text_label.y() + self.text_label.height() // 2 + 5
        self.cursor_label.move(cursor_x, cursor_y)

    def blink_cursor(self):
        if self.cursor_label.isVisible():
            self.cursor_label.hide()
        else:
            self.cursor_label.show()

    def show_choice_dialog(self):
        # Диалог с выбором
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("lipstick, я наношу на себя lipstick")
        msg_box.setText("Тыкни куда сердце подскажет")
        msg_box.addButton("Люблю ❤️", QMessageBox.ButtonRole.YesRole)
        msg_box.addButton("Пепешнелеватафа", QMessageBox.ButtonRole.NoRole)  # это тоже "да" 😄
        msg_box.exec()

        # После выбора — финальное сообщение
        self.final_message()

    def final_message(self):
        self.text_label.setText("Спасибо, что ты есть ❤️\n\nТы — самое лучшее,\nчто случилось со мной.\n\n Я очень сильно тебя люблю <3")
        self.text_label.setFont(QFont("Courier", 20))
        self.text_label.setStyleSheet("color: lime; background-color: transparent;")
        self.cursor_label.hide()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("хмм... какой-то файлик")
        self.resize(500, 300)
        self.setStyleSheet("background-color: #111;")

        layout = QVBoxLayout()

        label = QLabel("Нажми пжпжпж")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont("Courier", 14))
        label.setStyleSheet("color: lime;")

        button = QPushButton("Нажать сюда❤️")
        button.setStyleSheet("""
            QPushButton {
                background-color: #222;
                color: lime;
                border: 2px solid lime;
                padding: 10px;
                font-family: Courier;
            }
            QPushButton:hover {
                background-color: lime;
                color: #000;
            }
        """)
        button.clicked.connect(self.open_typing_window)

        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)

    def open_typing_window(self):
        self.typing_window = TypingWindow()
        self.typing_window.show()


# Запуск приложения
app = QApplication(sys.argv)
app.setStyleSheet("""
    QMessageBox {
        background-color: #000000;
        color: #00ff00;
        font-family: 'Courier New', Courier, monospace;
        font-size: 14pt;
    }
    QMessageBox QLabel {
        color: #00ff00;
    }
    QMessageBox QPushButton {
        background-color: #222;
        color: #00ff00;
        border: 1px solid #00ff00;
        padding: 8px 16px;
        font-family: 'Courier';
    }
    QMessageBox QPushButton:hover {
        background-color: #00ff00;
        color: #000;
    }
""")
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
