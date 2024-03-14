from random import shuffle
from enum import Enum
from tqdm import tqdm

class PokerHand(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

def generate_packs(spots, figures):
    suits = ['heart', 'diamond', 'spade', 'club']

    spots_pack = [(spot, color) for spot in spots for color in suits]

    figures_pack = [(figure, color) for figure in figures for color in suits]

    return spots_pack, figures_pack

def draw_pack(pack):
    shuffle(pack)
    return pack[:5]

def evaluate_pack(pack):
    spots = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
    figures = ['jack', 'queen', 'king', 'as']
    spots_and_figures = spots + figures

    ranks = [card[0] for card in pack]
    suits = [card[1] for card in pack]

    rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}

    suit_counts = {suit: suits.count(suit) for suit in set(suits)}

    # ROYAL_FLUSH - impossible

    # STRAIGHT_FLUSH - 5 consecutive cards in same suit
    is_flush = any(count >= 5 for count in suit_counts.values())
    sorted_ranks = sorted(ranks, key=lambda x: spots_and_figures.index(x))
    is_straight = any(sorted_ranks == spots[i:i + 5] for i in range(len(spots) - 5 + 1))

    if is_flush and is_straight:
        return PokerHand.STRAIGHT_FLUSH

    # FOUR_OF_A_KIND
    if 4 in rank_counts.values():
        return PokerHand.FOUR_OF_A_KIND

    # FULL_HOUSE
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        return PokerHand.FULL_HOUSE

    # FLUSH - 5 cards in same suit
    if is_flush:
        return PokerHand.FLUSH

    # STRAIGHT - 5 consecutive cards
    if is_straight:
        return PokerHand.STRAIGHT

    # THREE_OF_A_KIND
    if 3 in rank_counts.values():
        return PokerHand.THREE_OF_A_KIND

    # TWO_PAIR
    if list(rank_counts.values()).count(2) == 2:
        return PokerHand.TWO_PAIR

    # PAIR
    if 2 in rank_counts.values():
        return PokerHand.PAIR

    # HIGH_CARD
    return PokerHand.HIGH_CARD

def judge(figures_score, spots_score):
    return figures_score.value >= spots_score.value

def test_straight():
    # Straight: Five consecutive cards of different suits
    pack = [('2', 'hearts'), ('3', 'clubs'), ('4', 'diamonds'), ('5', 'spades'), ('6', 'hearts')]
    assert evaluate_pack(pack) == PokerHand.STRAIGHT

def test_flush():
    # Flush: Five cards of the same suit
    pack = [('2', 'hearts'), ('6', 'hearts'), ('8', 'hearts'), ('10', 'hearts'), ('7', 'hearts')]
    assert evaluate_pack(pack) == PokerHand.FLUSH

def simulate(spots, figures):
    spots_pack, figure_pack = generate_packs(spots, figures, )
    number_of_games = 100000
    figures_wins = 0

    print("Number of cards in spots deck: " + str(len(spots_pack)))
    print("Number of cards in figure deck: " + str(len(figure_pack)))
    for i in tqdm(range(number_of_games)):
        spots_hand = draw_pack(spots_pack)
        figures_hand = draw_pack(figure_pack)
        if judge(evaluate_pack(figures_hand), evaluate_pack(spots_hand)):
            figures_wins += 1
    print("\nFigures winrate: " + str(round(figures_wins / number_of_games * 100, 2)) + "%")
    print("Spots winrate: " + str(round(100 - figures_wins / number_of_games * 100, 2)) + "%")

if __name__ == "__main__":
   simulate(['2', '3', '4', '5', '6', '7', '8', '9', '10'], ['jack', 'queen', 'king', 'as'])
   print("----------")
   simulate(['8', '9', '10'], ['jack', 'queen', 'king', 'as'])