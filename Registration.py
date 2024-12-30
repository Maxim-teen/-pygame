import os
import csv
import re
import sys
from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox, QApplication


WALLET_FILE = "wallet.csv"


class LoginDialog(QDialog):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 400)

        layout = QFormLayout()
        self.username_input = QLineEdit(self)
        layout.addRow("Username:", self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Password:", self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_login)
        layout.addRow(self.login_button)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.open_registration_dialog)
        layout.addRow(self.register_button)

        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.username_exists(username):
            if self.validate_login(username, password):
                self.app.close_all_windows()
                self.app.open_menu_dialog(username)
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Invalid username or password.")
        else:
            QMessageBox.warning(self, "Error", "User  does not exist.")

    def username_exists(self, username):
        try:
            if os.path.exists(WALLET_FILE):
                with open(WALLET_FILE, 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == username:
                            return True
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to check username: {e}")
        return False

    def validate_login(self, username, password):
        try:
            if os.path.exists(WALLET_FILE):
                with open(WALLET_FILE, 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == username and row[2] == password:
                            return True
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to validate login: {e}")
        return False

    def open_registration_dialog(self):
        registration_dialog = RegistrationDialog(self.app)
        registration_dialog.exec()


class RegistrationDialog(QDialog):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Registration")
        self.setGeometry(100, 100, 400, 400)

        layout = QFormLayout()
        self.username_input = QLineEdit(self)
        layout.addRow("Username:", self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Password:", self.password_input)

        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Confirm Password:", self.confirm_password_input)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.check_registration)
        layout.addRow(self.ok_button)

        self.setLayout(layout)

    def check_registration(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not self.validate_username(username):
            QMessageBox.warning(self, "Error",
                                "Username must be between 3 and 15 characters and contain only letters and digits.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        if self.username_exists(username):
            QMessageBox.warning(self, "Error", "User  already exists.")
            return

        self.save_user(username, password)
        QMessageBox.information(self, "Success", "Registration successful!")
        self.app.close_all_windows()
        self.app.open_menu_dialog(username)
        self.accept()

    def validate_username(self, username):
        return 3 <= len(username) <= 15 and re.match("^[A-Za-z0-9]+$", username)

    def username_exists(self, username):
        try:
            if os.path.exists(WALLET_FILE):
                with open(WALLET_FILE, 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == username:
                            return True
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to check username: {e}")
        return False

    def save_user(self, username, password):
        try:
            with open(WALLET_FILE, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, 0, password])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save user: {e}")


class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_dialog = LoginDialog(self)

    def run(self):
        self.login_dialog.exec()

    def close_all_windows(self):
        self.login_dialog.close()

    def open_menu_dialog(self, username):
        QMessageBox.information(None, "Welcome", f"Welcome, {username}!")


if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
