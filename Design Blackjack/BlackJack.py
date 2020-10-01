import random


suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
         'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return '%s of %s' % (self.rank, self.suit)


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_content = ''
        for card in self.deck:
            deck_content += '\n' + card.__str__()
        return 'The Deck contains:' + deck_content

    def shuffle(self):
        random.shuffle(self.deck)


class Player:
    def __init__(self, dealer=False):
        self.type_of_player = 'Dealer' if dealer else 'Player'
        self.hand = []
        self.hand_value = 0
        self.no_of_aces = 0

    def add_card_in_hand(self, curr_card):
        self.hand.append(curr_card)
        self.hand_value += values[curr_card.rank]
        if curr_card.rank == 'Ace':
            self.no_of_aces += 1

    def display_current_hand(self):
        print("\n%s's hand: " % self.type_of_player)
        for card in self.hand:
            print(card.__str__())

    def adjust_for_ace(self):
        while self.hand_value > 21 and self.no_of_aces:
            self.hand_value -= 10
            self.no_of_aces -= 1

    def hit_or_stand(self, game):
        while self.hand_value < 21:
            hit_or_stand = input("\nDo you want to Hit or Stand (h/s)?: ")
            if hit_or_stand == 'h':
                game.draw_card(self)
                self.adjust_for_ace()
                self.display_current_hand()
                print("Player's hand value: %d" % self.hand_value)
            elif hit_or_stand == 's':
                print("\nPlayer stands!\nPlayer's hand value: %d" % self.hand_value)
                break


class BlackJackGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

    def deal_cards(self, player):
        current_card = self.deck.deck.pop()
        player.add_card_in_hand(current_card)
        player.add_card_in_hand(current_card)
        player.adjust_for_ace()

    def draw_card(self, player):
        current_card = self.deck.deck.pop()
        player.add_card_in_hand(current_card)

    def play_game(self):
        dealer = Player(dealer=True)
        player = Player()
        self.deal_cards(dealer)
        self.deal_cards(player)
        print("\nDealer's hand: ")
        print(dealer.hand[0].__str__(), '\n2nd card hidden!')

        player.display_current_hand()
        print('Player\'s hand value: %d' % player.hand_value)
        player.hit_or_stand(self)

        if player.hand_value == 21:
            print('Player Wins!')
            return
        elif player.hand_value > 21:
            print('Player busted! Dealer Wins')
            return

        dealer.display_current_hand()
        print('Dealer\'s hand value: %d' % dealer.hand_value)
        while dealer.hand_value < 17:
            self.draw_card(dealer)
            dealer.adjust_for_ace()
            dealer.display_current_hand()
            print("Dealer's hand value: %d" % dealer.hand_value)

        print('---------------------------------------------------')
        player_hand_value = player.hand_value
        dealer_hand_value = dealer.hand_value
        print('Player\'s final hand value: %d' % player_hand_value)
        print('Dealer\'s final hand value: %d' % dealer_hand_value)
        if dealer.hand_value == 21:
            print('Dealer Wins!')
            return
        elif dealer.hand_value > 21:
            print('Dealer Busted! Player Wins!')
            return
        elif dealer_hand_value > player_hand_value:
            print('Dealer Wins!')
        elif dealer_hand_value == player_hand_value:
            print("It's a Tie!!! No one Wins!")
        else:
            print('Player Wins!')


while 1:
    black_jack = BlackJackGame()
    black_jack.play_game()
    play_again = input('Do you want to play again (y/n)? ')
    if play_again != 'y':
        break
