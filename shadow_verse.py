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
                if card.name == "Dshift":
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
            self.__hand.append(TokenSpell())


class Deck:
    def __init__(self):
        cards = \
            [Snipe(),Snipe(),Snipe(),
            Experiment(),Experiment(),
            Insight(),Insight(),Insight(),
            Knowledge(),
            Owl(),Owl(),Owl(),
            Missile(),Missile(),Missile(),
            Blast(),Blast(),Blast(),
            Glow(),Glow(),Glow(),
            Assault(),Assault(),Assault(),
            Concentration(),Concentration(),Concentration(),
            Fate(),Fate(),Fate(),
            Embrace(),Embrace(),
            Dshift(),Dshift(),Dshift(),
            F(),F(),F(),
            F(),F()]
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


class Snipe(Card):
    def __init__(self):
        super().__init__("Snipe", 1, 0, 0, 0)


class Experiment(Card):
    def __init__(self):
        super().__init__("Experiment", 1, 0, 0, 0)


class Insight(Card):
    def __init__(self):
        super().__init__("Insight", 1, 0, 1, 0)


class Knowledge(Card):
    def __init__(self):
        super().__init__("Knowledge", 1, 0, 0, 1)


class Owl(Card):
    def __init__(self):
        super().__init__("Owl", 2, 2, 0, 0, is_spell=False)


class Missile(Card):
    def __init__(self):
        super().__init__("Missile", 2, 0, 1, 0)


class Blast(Card):
    def __init__(self):
        super().__init__("Blast", 2, 0, 0, 0)


class Glow(Card):
    def __init__(self):
        super().__init__("Glow", 2, 0, 1, 0)


class Assault(Card):
    def __init__(self):
        super().__init__("Assault", 2, 0, 0, 1)


class Concentration(Card):
    def __init__(self):
        super().__init__("Concentration", 3, 0, 2, 0)


class Fate(Card):
    def __init__(self):
        super().__init__("Fate", 5, 0, 2, 0, reducible=True)


class Embrace(Card):
    def __init__(self):
        super().__init__("Embrace", 8, 0, 0, 0, reducible=True)


class Dshift(Card):
    def __init__(self):
        super().__init__("Dshift", 20, 0, 0, 0, reducible=True)


class F(Card):
    def __init__(self):
        super().__init__("F", 1, 0, 0, 0, reducible=False, is_spell=False)


class TokenSpell(Card):
    def __init__(self):
        super().__init__("TokenSpell", 1, 0, 0, 0)
