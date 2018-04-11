import random


class Play:
    def __init__(self):
        self.__hand = []
        self.__deck = Deck()
        self.__pp = 0
        self.__tyoetu_used = False

    def first_draw(self):
        for i in range(5):
            card = self.__deck.draw()
            if card == None:
                break
            self.__hand.append(card)

    def get_hand(self):
        return sorted(self.__hand, key=lambda c: c.cost)

    def run_turn(self):
        self.__pp += 1
        self.__draw()
        self.__play_cards()
        return not self.__deck.is_empty() and not self.__tyoetu_used

    def __draw(self):
        card = self.__deck.draw()
        if card is not None and len(self.__hand) < 9:
            self.__hand.append(card)

    def __play_cards(self):
        self.__hand = sorted(self.__hand, key=lambda c: (not c.is_spell, c.cost))
        pp_tmp = self.__pp
        for card in self.__hand[:]:
            if pp_tmp >= card.cost:
                pp_tmp -= card.cost
                self.__hand.remove(card)
                self.__play_card(card)
                if card.name == "STyoetu":
                    print("Tyoetu is used in turn %d." % self.__pp)
                    self.__tyoetu_used = True

    def __play_card(self, play_card):
        reduce_cost = 0
        if play_card.is_spell:
            reduce_cost += 1
        reduce_cost += play_card.sp_boost
        for card in self.__hand:
            card.reduce_cost(reduce_cost)
        for i in range(play_card.draw):
            self.__draw()
        for i in range(play_card.draw_spell):
            self.__hand.append(S())


class Deck:
    def __init__(self):
        cards = \
            [SAngele(), SAngele(), SAngele(),
             SJikken(), SJikken(),
             STie(), STie(), STie(),
             SMaria(),
             FOwl(), FOwl(), FOwl(),
             SMissile(), SMissile(), SMissile(),
             SBlast(), SBlast(), SBlast(),
             SNiji(), SNiji(), SNiji(),
             SGorem(), SGorem(), SGorem(),
             SSeisin(), SSeisin(), SSeisin(),
             SUnmei(), SUnmei(), SUnmei(),
             SAkugeki(), SAkugeki(),
             STyoetu(), STyoetu(), STyoetu(),
             F(), F(), F(), F(), F()]
        random.shuffle(cards)
        self.__cards = cards

    def draw(self):
        if len(self.__cards) == 0:
            return None
        return self.__cards.pop(0)

    def is_empty(self):
        if len(self.__cards) == 0:
            return True
        return False


class Card:
    def __init__(self, name, cost, sp_boost, draw, draw_spell, reducible=False, is_spell=True):
        self.name = name
        self.cost = cost
        self.sp_boost = sp_boost
        self.draw = draw
        self.draw_spell = draw_spell
        self.reducible = reducible
        self.is_spell = is_spell

    def reduce_cost(self, val):
        if self.reducible:
            self.cost -= val
        if self.cost < 0:
            self.cost = 0


class SAngele(Card):
    def __init__(self):
        super().__init__("SAngle", 1, 0, 0, 0)


class SJikken(Card):
    def __init__(self):
        super().__init__("SJikken", 1, 0, 0, 0)


class STie(Card):
    def __init__(self):
        super().__init__("STie", 1, 0, 1, 0)


class SMaria(Card):
    def __init__(self):
        super().__init__("SMaria", 1, 0, 0, 1)


class FOwl(Card):
    def __init__(self):
        super().__init__("SOwl", 2, 2, 0, 0, is_spell=False)


class SMissile(Card):
    def __init__(self):
        super().__init__("SMissile", 2, 0, 1, 0)


class SBlast(Card):
    def __init__(self):
        super().__init__("SBurst", 2, 0, 0, 0)


class SNiji(Card):
    def __init__(self):
        super().__init__("SNiji", 2, 0, 1, 0)


class SGorem(Card):
    def __init__(self):
        super().__init__("SGorem", 2, 0, 0, 1)


class SSeisin(Card):
    def __init__(self):
        super().__init__("SSeisin", 3, 0, 2, 0)


class SUnmei(Card):
    def __init__(self):
        super().__init__("SUnmei", 5, 0, 2, 0, reducible=True)


class SAkugeki(Card):
    def __init__(self):
        super().__init__("SAkugeki", 8, 0, 0, 0, reducible=True)


class STyoetu(Card):
    def __init__(self):
        super().__init__("STyoetu", 20, 0, 0, 0, reducible=True)


class F(Card):
    def __init__(self):
        super().__init__("F", 1, 0, 0, 0, reducible=False, is_spell=False)


class S(Card):
    def __init__(self):
        super().__init__("S", 1, 0, 0, 0)

