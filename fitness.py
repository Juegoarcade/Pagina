import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QComboBox, QVBoxLayout, QFormLayout, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5 import QtGui  # Import necesario para cargar imagen

class BMRCalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de Tasa Metabólica Basal (TMB)")
        self.setGeometry(100, 100, 450, 700)  # Ajustado para dar espacio a la imagen
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Sexo
        self.sex_label = QLabel("Tu sexo")
        self.sex_combo = QComboBox()
        self.sex_combo.addItem("Selecciona tu sexo")
        self.sex_combo.addItem("Hombre")
        self.sex_combo.addItem("Mujer")
        form_layout.addRow(self.sex_label, self.sex_combo)

        # Edad
        self.age_label = QLabel("Tu edad")
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Introduce tu edad")
        form_layout.addRow(self.age_label, self.age_input)

        # Peso
        self.weight_label = QLabel("Tu peso <b>kg</b>")
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Introduce el peso en kg.")
        form_layout.addRow(self.weight_label, self.weight_input)

        # Altura
        self.height_label = QLabel("Tu altura <b>cm</b>")
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Introduce la altura en cm.")
        form_layout.addRow(self.height_label, self.height_input)

        # Actividad física
        self.activity_label = QLabel("¿Cuál es tu nivel de actividad física diaria?")
        self.activity_combo = QComboBox()
        self.activity_combo.addItem("Selecciona una opción")
        self.activity_combo.addItem("Poco o ningún ejercicio")
        self.activity_combo.addItem("Ejercicio ligero (1-3 días/semana)")
        self.activity_combo.addItem("Ejercicio moderado (3-5 días/semana)")
        self.activity_combo.addItem("Ejercicio fuerte (6-7 días/semana)")
        self.activity_combo.addItem("Ejercicio muy fuerte (dos veces al día, entrenamientos muy duros)")
        form_layout.addRow(self.activity_label, self.activity_combo)

        # Objetivo
        self.objective_label = QLabel("¿Cuál es tu objetivo?")
        self.objective_combo = QComboBox()
        self.objective_combo.addItem("Selecciona una opción")
        self.objective_combo.addItem("Mantener peso")
        self.objective_combo.addItem("Perder peso")
        self.objective_combo.addItem("Ganar peso")
        form_layout.addRow(self.objective_label, self.objective_combo)

        main_layout.addLayout(form_layout)

        # Imagen decorativa
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(QtGui.QPixmap("fitness.png").scaled(450, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        main_layout.addWidget(self.image_label)

        main_layout.addStretch(1)

        # Botón calcular
        self.calculate_button = QPushButton("Calcular")
        self.calculate_button.clicked.connect(self.calculate_bmr)
        main_layout.addWidget(self.calculate_button)

        # Resultado
        self.result_label = QLineEdit()
        self.result_label.setReadOnly(True)
        self.result_label.setPlaceholderText("El resultado de TMB aparecerá aquí...")
        self.result_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.result_label)

        # Estilos visuales
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                font-size: 13px;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QComboBox QAbstractItemView {
                selection-background-color: #333;
                selection-color: white;
            }
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005F99;
            }
            QLineEdit[readOnly="true"] {
                background-color: #f2f2f2;
                font-weight: bold;
                color: #333;
            }
        """)

        self.setLayout(main_layout)

    def calculate_bmr(self):
        try:
            sex = self.sex_combo.currentText()
            age_text = self.age_input.text()
            weight_text = self.weight_input.text()
            height_text = self.height_input.text()

            if sex == "Selecciona tu sexo":
                QMessageBox.warning(self, "Error de Entrada", "Por favor, selecciona tu sexo.")
                return

            if not age_text or not age_text.strip().isdigit():
                QMessageBox.warning(self, "Error de Entrada", "Por favor, introduce una edad válida (número entero).")
                return
            age = int(age_text)

            weight = float(weight_text.replace(',', '.'))
            height = float(height_text.replace(',', '.'))

            if not (1 <= age <= 120):
                QMessageBox.warning(self, "Error de Entrada", "Por favor, introduce una edad válida (1-120 años).")
                return
            if not (20 <= weight <= 300):
                QMessageBox.warning(self, "Error de Entrada", "Por favor, introduce un peso válido (20-300 kg).")
                return
            if not (50 <= height <= 250):
                QMessageBox.warning(self, "Error de Entrada", "Por favor, introduce una altura válida (50-250 cm).")
                return

            if sex == "Hombre":
                bmr = 66 + (13.75 * weight) + (5 * height) - (6.75 * age)
            elif sex == "Mujer":
                bmr = 655 + (9.56 * weight) + (1.85 * height) - (4.68 * age)
            else:
                QMessageBox.warning(self, "Error de Entrada", "Un error inesperado ocurrió con la selección de sexo.")
                self.result_label.setText("")
                return

            self.result_label.setText(f"Tu TMB es: {bmr:.2f} calorías/día")

        except ValueError:
            QMessageBox.critical(self, "Error de Entrada", "Por favor, introduce valores numéricos válidos para edad, peso y altura.")
            self.result_label.setText("")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error inesperado: {e}")
            self.result_label.setText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    bmr_app = BMRCalculatorApp()
    bmr_app.show()
    sys.exit(app.exec_())
