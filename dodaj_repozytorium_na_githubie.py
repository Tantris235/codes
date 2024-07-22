import sys
import json
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QStackedWidget, QMessageBox
from PyQt5.QtCore import Qt

class GitHubRepoCreator(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        self.stack = QStackedWidget(self)
        self.repoForm = QWidget()
        self.loginForm = QWidget()
        
        self.initRepoForm()
        self.initLoginForm()
        
        self.stack.addWidget(self.repoForm)
        self.stack.addWidget(self.loginForm)
        
        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)
        
        self.setWindowTitle('GitHub Repo Creator')
        self.setGeometry(100, 100, 400, 200)
        self.show()

    def initRepoForm(self):
        layout = QFormLayout()

        self.repoName = QLineEdit()
        self.repoDescription = QLineEdit()

        addButton = QPushButton('Dodaj Repozytorium')
        addButton.clicked.connect(self.showLoginForm)

        layout.addRow('Nazwa Repozytorium:', self.repoName)
        layout.addRow('Opis Repozytorium (opcjonalnie):', self.repoDescription)
        layout.addRow(addButton)

        self.repoForm.setLayout(layout)
    
    def initLoginForm(self):
        layout = QFormLayout()

        self.username = QLineEdit()
        self.token = QLineEdit()
        self.token.setEchoMode(QLineEdit.Password)

        loginButton = QPushButton('Zaloguj')
        loginButton.clicked.connect(self.createRepo)

        layout.addRow('Nazwa Użytkownika:', self.username)
        layout.addRow('Token:', self.token)
        layout.addRow(loginButton)

        self.loginForm.setLayout(layout)

    def showLoginForm(self):
        self.stack.setCurrentWidget(self.loginForm)

    def createRepo(self):
        repo_name = self.repoName.text()
        repo_description = self.repoDescription.text()
        token = self.token.text()  # Pobieramy token z pola tekstowego

        if not token:
            self.showMessage('Brak tokena.', 'error')
            return

        url = 'https://api.github.com/user/repos'
        data = {
            'name': repo_name,
            'description': repo_description
        }
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 201:
            self.showMessage('Repozytorium zostało utworzone pomyślnie!', 'success')
        else:
            self.showMessage(f'Wystąpił błąd: {response.json().get("message", "Nieznany błąd")}', 'error')

    def showMessage(self, message, messageType):
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Information if messageType == 'success' else QMessageBox.Critical)
        msgBox.setText(message)
        msgBox.setWindowTitle('Informacja')
        msgBox.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GitHubRepoCreator()
    sys.exit(app.exec_())
