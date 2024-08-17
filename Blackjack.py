
import sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, 
                             QHBoxLayout, QSpinBox, QComboBox, QMessageBox)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

# Kartlar ve değerleri
cards = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

class BlackjackGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Pencere ayarları
        self.setWindowTitle('Blackjack')
        self.setGeometry(100, 100, 800, 600)
        
        # Başlangıç coin miktarı
        self.coins = 1000
        self.bet = 0
        self.odds = 5  # Varsayılan kazanç/kayıp oranı
        self.difficulty = 'Kolay'  # Varsayılan zorluk seviyesi
        
        # Kart destesini oluştur
        self.deck = self.create_deck()
        
        # Başlangıçta oyuncu ve dealer ellerini oluştur
        self.player_hand = []
        self.dealer_hand = []
        
        # GUI bileşenleri
        self.coins_label = QLabel(f"Mevcut Coin: {self.coins}", self)
        self.coins_label.setAlignment(Qt.AlignCenter)
        self.coins_label.setFont(QFont('Arial', 16))
        
        self.bet_label = QLabel(f"Bahis: {self.bet}", self)
        self.bet_label.setAlignment(Qt.AlignCenter)
        self.bet_label.setFont(QFont('Arial', 16))
        
        self.info_label = QLabel("Oyun başlamadan önce bahis ve oran belirleyin.", self)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setFont(QFont('Arial', 14))
        
        self.dealer_label = QLabel("", self)
        self.dealer_label.setAlignment(Qt.AlignCenter)
        self.dealer_label.setFont(QFont('Arial', 14))
        
        self.player_card_layout = QHBoxLayout()
        self.dealer_card_layout = QHBoxLayout()
        
        self.hit_button = QPushButton('Kart Çek', self)
        self.stand_button = QPushButton('Dur', self)
        self.start_button = QPushButton('Oyuna Başla', self)
        
        self.bet_spinbox = QSpinBox(self)
        self.bet_spinbox.setRange(1, self.coins)
        self.bet_spinbox.setValue(50)
        
        self.odds_spinbox = QSpinBox(self)
        self.odds_spinbox.setRange(1, 10)  # 1x ile 10x arasında oran seçimi
        self.odds_spinbox.setValue(self.odds)
        
        self.difficulty_combo = QComboBox(self)
        self.difficulty_combo.addItems(['Kolay', 'Orta', 'Zor'])
        self.difficulty_combo.currentTextChanged.connect(self.change_difficulty)
        
        # Buton bağlantıları
        self.hit_button.clicked.connect(self.hit)
        self.stand_button.clicked.connect(self.stand)
        self.start_button.clicked.connect(self.start_game)
        
        # Buton stili
        self.hit_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px;")
        self.stand_button.setStyleSheet("background-color: #f44336; color: white; font-size: 16px;")
        self.start_button.setStyleSheet("background-color: #2196F3; color: white; font-size: 16px;")
        
        # Düzen
        top_layout = QVBoxLayout()
        top_layout.addWidget(self.coins_label)
        top_layout.addWidget(self.bet_label)
        top_layout.addWidget(QLabel("Bahis Miktarı:", self))
        top_layout.addWidget(self.bet_spinbox)
        top_layout.addWidget(QLabel("Oran (x):", self))
        top_layout.addWidget(self.odds_spinbox)
        top_layout.addWidget(QLabel("Zorluk:", self))
        top_layout.addWidget(self.difficulty_combo)
        top_layout.addWidget(self.start_button)
        
        middle_layout = QVBoxLayout()
        middle_layout.addWidget(self.info_label)
        middle_layout.addLayout(self.player_card_layout)
        middle_layout.addWidget(self.dealer_label)
        middle_layout.addLayout(self.dealer_card_layout)
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.hit_button)
        bottom_layout.addWidget(self.stand_button)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(bottom_layout)
        
        self.setLayout(main_layout)
        
        # Başlangıçta bazı butonlar devre dışı
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)
        
    def create_deck(self):
        """Desteyi oluşturur."""
        deck = list(cards.keys()) * 4
        random.shuffle(deck)
        return deck

    def calculate_hand_value(self, hand):
        """Eldeki kartların değerini hesaplar."""
        value = sum(cards[card] for card in hand)
        num_aces = hand.count('A')
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value

    def update_player_hand(self):
        """Oyuncunun elini günceller ve kartları gösterir."""
        for i in reversed(range(self.player_card_layout.count())):
            self.player_card_layout.itemAt(i).widget().setParent(None)

        for card in self.player_hand:
            card_label = QLabel(self)
            card_pixmap = QPixmap(f'cards/{card}.png')  # Kart resmi dosyasını yükle
            card_label.setPixmap(card_pixmap.scaled(100, 150, Qt.KeepAspectRatio))
            self.player_card_layout.addWidget(card_label)

    def update_dealer_hand(self, reveal=False):
        """Krupiyenin elini günceller ve kartları gösterir."""
        for i in reversed(range(self.dealer_card_layout.count())):
            self.dealer_card_layout.itemAt(i).widget().setParent(None)

        for i, card in enumerate(self.dealer_hand):
            card_label = QLabel(self)
            card_pixmap = QPixmap(f'cards/{card}.png')  # Kart resmi dosyasını yükle
            card_label.setPixmap(card_pixmap.scaled(100, 150, Qt.KeepAspectRatio))
            self.dealer_card_layout.addWidget(card_label)
        
        # Krupiyenin elinin toplamını gösterir
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        self.dealer_label.setText(f"Krupiye: {' '.join(self.dealer_hand)} ({dealer_value})")

    def start_game(self):
        """Oyunu başlatır ve bahis alır."""
        self.bet = self.bet_spinbox.value()
        self.odds = self.odds_spinbox.value()  # Kullanıcı tarafından belirlenen oran
        
        if self.bet > self.coins:
            QMessageBox.warning(self, 'Hata', 'Bahis, mevcut coin miktarınızı aşamaz.')
            return
        
        self.coins -= self.bet
        self.coins_label.setText(f"Mevcut Coin: {self.coins}")
        self.bet_label.setText(f"Bahis: {self.bet} (Oran: {self.odds}x)")
        
        self.deck = self.create_deck()
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        
        self.update_player_hand()
        self.update_dealer_hand()
        
        self.info_label.setText(f"Oyuncu: {self.calculate_hand_value(self.player_hand)}")
        
        self.hit_button.setEnabled(True)
        self.stand_button.setEnabled(True)
        self.start_button.setEnabled(False)

    def hit(self):
        """Oyuncu bir kart çeker."""
        self.player_hand.append(self.deck.pop())
        self.update_player_hand()
        player_value = self.calculate_hand_value(self.player_hand)
        self.info_label.setText(f"Oyuncu: {player_value}")
        if player_value > 21:
            self.show_result("Elini aştın! Krupiye kazandı.")
            self.stand_button.setEnabled(False)
            self.hit_button.setEnabled(False)

    def stand(self):
        """Oyuncu oyunu durdurur ve krupiyenin oyununu başlatır."""
        player_value = self.calculate_hand_value(self.player_hand)
        self.info_label.setText(f"Oyuncu: {player_value}")
        
        self.update_dealer_hand(reveal=True)
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        
        if dealer_value > 21 or player_value > dealer_value:
            self.show_result("Tebrikler, kazandınız!")
            self.coins += self.bet * self.odds
        elif player_value < dealer_value:
            self.show_result("Dealer kazandı.")
        else:
            self.show_result("Beraberlik.")
        
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)
        self.start_button.setEnabled(True)

    def show_result(self, message):
        """Sonucu gösterir ve oyunu bitirir."""
        QMessageBox.information(self, 'Sonuç', message)
        self.coins_label.setText(f"Mevcut Coin: {self.coins}")

    def change_difficulty(self, text):
        """Zorluk seviyesini değiştirir."""
        self.difficulty = text

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = BlackjackGame()
    game.show()
    sys.exit(app.exec_())
