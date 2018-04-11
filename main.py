from shadow_verse import *

play = Play()
play.first_draw()

while True:
    print("[Hand]\nName\tCost")
    for card in play.get_hand():
        print(card.name + "\t" + str(card.cost))
    print("\n")
    if not play.run_turn():
        break
