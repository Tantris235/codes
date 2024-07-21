import sys
import json
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QInputDialog
from PyQt5.QtCore import QTimer

class Postac:
    def __init__(self, imie, zdrowie, sila):
        self.imie = imie
        self.zdrowie = zdrowie
        self.sila = sila

    def atakuj(self, inny):
        obrazenia = self.sila
        inny.zdrowie -= obrazenia
        return obrazenia

    def __str__(self):
        return f"{self.imie} (Zdrowie: {self.zdrowie}, Siła: {self.sila})"

class Wrog:
    def __init__(self, imie, zdrowie, sila):
        self.imie = imie
        self.zdrowie = zdrowie
        self.sila = sila

    def atakuj(self, inny):
        obrazenia = self.sila
        inny.zdrowie -= obrazenia
        return obrazenia

    def __str__(self):
        return f"{self.imie} (Zdrowie: {self.zdrowie}, Siła: {self.sila})"

def generuj_wroga(trudnosc):
    imiona_wrogow = ["Goblin", "Ork", "Troll"]
    sila = random.randint(5, 10) + (trudnosc - 1)
    if sila > 10:
        sila = 10
    imie = "Smok" if sila == 10 else random.choice(imiona_wrogow)
    zdrowie = random.randint(30, 50) + (trudnosc - 1) * 10
    return Wrog(imie, zdrowie, sila)

class Gra(QWidget):
    def __init__(self):
        super().__init__()

        self.gracz = Postac("Hero", 100, 10)
        self.monety = 0
        self.trudnosc = 1
        self.wrog = generuj_wroga(self.trudnosc)

        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.regeneracja_hp)
        self.timer.start(2000)  # co 2 sekundy

    def init_ui(self):
        self.setWindowTitle('Gra RPG')

        self.status_label = QLabel(self.pobierz_status())
        self.monety_label = QLabel(f"Monety: {self.monety}")

        self.atakuj_btn = QPushButton("Atakuj")
        self.atakuj_btn.clicked.connect(self.atakuj)

        self.ucieczka_btn = QPushButton("Ucieczka")
        self.ucieczka_btn.clicked.connect(self.ucieczka)

        self.sklep_btn = QPushButton("Sklep")
        self.sklep_btn.clicked.connect(self.otworz_sklep)

        self.zamknij_btn = QPushButton("Zamknij")
        self.zamknij_btn.clicked.connect(self.zamknij)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.monety_label)
        layout.addWidget(self.atakuj_btn)
        layout.addWidget(self.ucieczka_btn)
        layout.addWidget(self.sklep_btn)
        layout.addWidget(self.zamknij_btn)

        self.setLayout(layout)

    def pobierz_status(self):
        return f"Gracz: {self.gracz}\nWrog: {self.wrog}"

    def atakuj(self):
        if self.wrog.zdrowie > 0:
            obrazenia = self.gracz.atakuj(self.wrog)
            if self.wrog.zdrowie <= 0:
                self.monety += 2
                self.trudnosc += 1
                self.wrog = generuj_wroga(self.trudnosc)
            else:
                self.wrog.atakuj(self.gracz)
                if self.gracz.zdrowie <= 0:
                    self.show_message("Przegrałeś! Restartuję grę...")
                    self.restartuj()
                    return
            self.status_label.setText(self.pobierz_status())
        self.monety_label.setText(f"Monety: {self.monety}")

    def ucieczka(self):
        self.show_message("Uciekłeś z walki. Możesz teraz kontynuować grę.")
        self.wrog = generuj_wroga(self.trudnosc)
        self.status_label.setText(self.pobierz_status())

    def otworz_sklep(self):
        wybor, ok = QInputDialog.getItem(self, 'Sklep', 'Wybierz miecz:', ['Miecz Żelazny (50 monet)', 'Miecz Diamentowy (100 monet)'], 0, False)
        if ok:
            if wybor == 'Miecz Żelazny (50 monet)':
                self.kup_miecz_zelazny()
            elif wybor == 'Miecz Diamentowy (100 monet)':
                self.kup_miecz_diamentowy()

    def kup_miecz_zelazny(self):
        if self.monety >= 50:
            self.monety -= 50
            self.gracz.sila = 20
            self.monety_label.setText(f"Monety: {self.monety}")
        else:
            self.show_message("Brak monet!")

    def kup_miecz_diamentowy(self):
        if self.monety >= 100:
            self.monety -= 100
            self.gracz.sila = 50
            self.monety_label.setText(f"Monety: {self.monety}")
        else:
            self.show_message("Brak monet!")

    def regeneracja_hp(self):
        if self.gracz.zdrowie < 100:  # Maksymalne zdrowie gracza
            self.gracz.zdrowie += 2
            self.status_label.setText(self.pobierz_status())

    def restartuj(self):
        self.zapisz_wyniki()  # Zapisywanie wyników przed restartem
        self.gracz = Postac("Hero", 100, 10)
        self.monety = 0
        self.trudnosc = 1
        self.wrog = generuj_wroga(self.trudnosc)
        self.status_label.setText(self.pobierz_status())
        self.monety_label.setText(f"Monety: {self.monety}")

    def show_message(self, message):
        QMessageBox.information(self, "Informacja", message)

    def zapisz_wyniki(self):
        dane = {
            'gracz': {
                'imie': self.gracz.imie,
                'zdrowie': self.gracz.zdrowie,
                'sila': self.gracz.sila
            },
            'monety': self.monety,
            'trudnosc': self.trudnosc,
            'wrog': {
                'imie': self.wrog.imie,
                'zdrowie': self.wrog.zdrowie,
                'sila': self.wrog.sila
            }
        }
        try:
            with open('wyniki.json', 'w') as plik:
                json.dump(dane, plik, indent=4)
            print("Wyniki zapisane pomyślnie!")
        except Exception as e:
            print(f"Błąd podczas zapisywania wyników: {e}")

    def zamknij(self):
        reply = QMessageBox.question(self, 'Zamknąć grę?', 'Czy na pewno chcesz zamknąć grę?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.zapisz_wyniki()  # Zapisz wyniki przed zamknięciem
            QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gra = Gra()
    gra.show()
    sys.exit(app.exec_())
