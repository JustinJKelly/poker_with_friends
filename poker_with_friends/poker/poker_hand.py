import copy

rankings = ["royal_flush","straight_flush","quads", "full_house", "flush","straight","three_of_a_kind",
    "two_pair","pair","high_card"]

cards = ['2_of_hearts','3_of_hearts','4_of_hearts','5_of_hearts','6_of_hearts','7_of_hearts','8_of_hearts','9_of_hearts','10_of_hearts','jack_of_hearts','queen_of_hearts','king_of_hearts','ace_of_hearts',
'2_of_clubs','3_of_clubs','4_of_clubs','5_of_clubs','6_of_clubs','7_of_clubs','8_of_clubs','9_of_clubs','10_of_clubs','jack_of_clubs','queen_of_clubs','king_of_clubs','ace_of_clubs',
'2_of_spades','3_of_spades','4_of_spades','5_of_spades','6_of_spades','7_of_spades','8_of_spades','9_of_spades','10_of_spades','jack_of_spades','queen_of_spades','king_of_spades','ace_of_spades',
'2_of_diamonds','3_of_diamonds','4_of_diamonds','5_of_diamonds','6_of_diamonds','7_of_diamonds','8_of_diamonds','9_of_diamonds','10_of_diamonds','jack_of_diamonds','queen_of_diamonds','king_of_diamonds','ace_of_diamonds']

card_highs = ["2","3","4","5","6","7","8","9","10","jack","queen","king","ace"]


#checkHands(player1,player1_cards,player2,player2_cards,flop_cards,turn_card_river_card)
#Poker winning hand logic
def checkHands(player1,player1_cards,player2,player2_cards,flop_cards,turn_card,river_card):
    #my hand
    player1_cards = player1_cards + flop_cards + [turn_card,river_card] #['queen_of_hearts','queen_of_spades','6_of_hearts','4_of_hearts','2_of_hearts','ace_of_clubs','7_of_diamonds']
    #print(player1_cards)
    player1_hand = getHand(player1_cards)
    
    if "two_pair" in player1_hand or "quads" in player1_hand:
        player1_hand = get_other_high_cards(1, player1_hand, player1_cards)
    elif "pair" in player1_hand:
        player1_hand = get_other_high_cards(3, player1_hand, player1_cards)
    elif "three_of_a_kind" in player1_hand:
        player1_hand = get_other_high_cards(2, player1_hand, player1_cards)
        
    print(player1, ":",player1_hand)
    
    player2_cards = player2_cards + flop_cards + [turn_card,river_card] #['queen_of_hearts','queen_of_spades','6_of_hearts','4_of_hearts','2_of_hearts','ace_of_clubs','7_of_diamonds']
    player2_hand = getHand(player2_cards)
    #print(player2_cards)
    
    if "two_pair" in player2_hand or "quads" in player2_hand:
        player2_hand = get_other_high_cards(1, player2_hand, player2_cards)
    elif "pair" in player2_hand:
        player2_hand = get_other_high_cards(3, player2_hand, player2_cards)
    elif "three_of_a_kind" in player2_hand:
        player2_hand = get_other_high_cards(2, player2_hand, player2_cards)
        
    print(player2,":",player2_hand)

    player1_hand_strength = rankings.index(player1_hand[0])
    player2_hand_strength = rankings.index(player2_hand[0])
    
    if player1_hand_strength < player2_hand_strength:
        return [player1,player1_hand[0],player1_hand,player2_hand]
    elif player1_hand_strength == player2_hand_strength:
        return findWinner(player1_hand,player2_hand,player1,player2)
    else:
        return [player2,player2_hand[0],player1_hand,player2_hand]


def findWinner(player1_hand,player2_hand,player1,player2):
    
    if player1_hand[0] == "high_card":
        player1Hand = player1_hand[1:]
        player2Hand = player2_hand[1:]
    
        #player1Hand.sort(key=comparefunction2,reverse=True)
        #player2Hand.sort(key=comparefunction2,reverse=True)
        
        for i in range(0,len(player1Hand)):
            n1 = player1Hand[i].find("_")
            sub1 = player1Hand[i][0:n1]
            
            n2 = player2Hand[i].find("_")
            sub2 = player2Hand[i][0:n2]
            
            
            if card_highs.index(sub1) > card_highs.index(sub2):
                return [player1,player1_hand[0],player1_hand,player2_hand]
            elif card_highs.index(sub1) < card_highs.index(sub2):
                return [player2,player2_hand[0],player1_hand,player2_hand]
        
        return ["both",player1_hand[0],player1_hand,player2_hand]
    
    elif player1_hand[0] == "pair":
        
        player1Hand = player1_hand[2:]
        player2Hand = player2_hand[2:]
        
        n1 = player1_hand[1].find("_")
        sub1 = player1_hand[1][0:n1]
        
        n2 = player2_hand[1].find("_")
        sub2 = player2_hand[1][0:n2]
        
        if card_highs.index(sub1) > card_highs.index(sub2):
            return [player1,player1_hand[0],player1_hand,player2_hand]
        elif card_highs.index(sub1) < card_highs.index(sub2):
            return [player2,player2_hand[0],player1_hand,player2_hand]
        
        
        for i in range(0,len(player1Hand)):
            n1 = player1Hand[i].find("_")
            sub1 = player1Hand[i][0:n1]
            
            n2 = player2Hand[i].find("_")
            sub2 = player2Hand[i][0:n2]
            
            
            if card_highs.index(sub1) > card_highs.index(sub2):
                return [player1,player1_hand[0],player1_hand,player2_hand]
            elif card_highs.index(sub1) < card_highs.index(sub2):
                return [player2,player2_hand[0],player1_hand,player2_hand]
            
        return ["both",player2_hand[0],player1_hand,player2_hand]
    
    elif player1_hand[0] == "two_pair":
        
        #player1Hand = player1_hand[4:]
        #player2Hand = player2_hand[4:]
        
        #check the pair values
        n1 = player1_hand[1].find("_")
        sub1 = player1_hand[1][0:n1]
        
        n2 = player2_hand[1].find("_")
        sub2 = player2_hand[1][0:n2]
        
        if card_highs.index(sub1) > card_highs.index(sub2):
            return [player1,player1_hand[0],player1_hand,player2_hand]
        elif card_highs.index(sub1) < card_highs.index(sub2):
            return [player2,player2_hand[0],player1_hand,player2_hand]
        
        n1 = player1_hand[3].find("_")
        sub1 = player1_hand[3][0:n1]
        
        n2 = player2_hand[3].find("_")
        sub2 = player2_hand[3][0:n2]
        
        if card_highs.index(sub1) > card_highs.index(sub2):
            return [player1,player1_hand[0],player1_hand,player2_hand]
        elif card_highs.index(sub1) < card_highs.index(sub2):
            return [player2,player2_hand[0],player1_hand,player2_hand]
        
        #check last high card
        n1 = player1_hand[4].find("_")
        sub1 = player1_hand[4][0:n1]
        
        n2 = player2_hand[4].find("_")
        sub2 = player2_hand[4][0:n2]
        
        
        if card_highs.index(sub1) > card_highs.index(sub2):
            return [player1,player1_hand[0],player1_hand,player2_hand]
        elif card_highs.index(sub1) < card_highs.index(sub2):
            return [player2,player2_hand[0],player1_hand,player2_hand]
            
        return ["both",player2_hand[0],player1_hand,player2_hand]
    
    elif player1_hand[0] == "straight" or player1_hand[0] == "straight_flush" or player1_hand[0] == "flush":
        n1 = player1_hand[1].find("_")
        sub1 = player1_hand[1][0:n1]
        
        n2 = player2_hand[1].find("_")
        sub2 = player2_hand[1][0:n2]
        
        if card_highs.index(sub1) > card_highs.index(sub2):
            return [player1,player1_hand[0],player1_hand,player2_hand]
        elif card_highs.index(sub1) < card_highs.index(sub2):
            return [player2,player2_hand[0],player1_hand,player2_hand]
        
        return ["both",player2_hand[0],player1_hand,player2_hand]
    
    elif player1_hand[0] == "three_of_a_kind":
        n1 = player1_hand[1].find("_")
        sub1 = player1_hand[1][0:n1]
        
        n2 = player2_hand[1].find("_")
        sub2 = player2_hand[1][0:n2]
        
        if card_highs.index(sub1) > card_highs.index(sub2):
            return [player1,player1_hand[0],player1_hand,player2_hand]
        elif card_highs.index(sub1) < card_highs.index(sub2):
            return [player2,player2_hand[0],player1_hand,player2_hand]
        
        
        player1Hand = player1_hand[3:]
        player2Hand = player2_hand[3:]
        for i in range(0,len(player1Hand)):
            n1 = player1Hand[i].find("_")
            sub1 = player1Hand[i][0:n1]
            
            n2 = player2Hand[i].find("_")
            sub2 = player2Hand[i][0:n2]
            
            
            if card_highs.index(sub1) > card_highs.index(sub2):
                return [player1,player1_hand[0],player1_hand,player2_hand]
            elif card_highs.index(sub1) < card_highs.index(sub2):
                return [player2,player2_hand[0],player1_hand,player2_hand]
        
        return ["both",player2_hand[0],player1_hand,player2_hand]
        
    elif player1_hand[0] == "quads":
        n1 = player1_hand[1].find("_")
        sub1 = player1_hand[1][0:n1]
        
        n2 = player2_hand[1].find("_")
        sub2 = player2_hand[1][0:n2]
        
        if card_highs.index(sub1) > card_highs.index(sub2):
            return [player1,player1_hand[0],player1_hand,player2_hand]
        elif card_highs.index(sub1) < card_highs.index(sub2):
            return [player2,player2_hand[0],player1_hand,player2_hand]
        
        
        '''player1Hand = player1_hand[4:]
        player2Hand = player2_hand[4:]
        for i in range(0,len(player1Hand)):
            n1 = player1Hand[i].find("_")
            sub1 = player1Hand[i][0:n1]
            
            n2 = player2Hand[i].find("_")
            sub2 = player2Hand[i][0:n2]
            
            
            if card_highs.index(sub1) > card_highs.index(sub2):
                return [player1,player1_hand[0],player1_hand,player2_hand]
            elif card_highs.index(sub1) < card_highs.index(sub2):
                return [player2,player2_hand[0],player1_hand,player2_hand]'''
        
        #return ["both",player2_hand[0],player1_hand,player2_hand]
    
    elif player1_hand[0] == "full_house":
        
        n1 = player1_hand[1].find("_")
        sub1 = player1_hand[1][0:n1]
        
        n2 = player2_hand[1].find("_")
        sub2 = player2_hand[1][0:n2]
        
        if card_highs.index(sub1) > card_highs.index(sub2):
            return [player1,player1_hand[0],player1_hand,player2_hand]
        elif card_highs.index(sub1) < card_highs.index(sub2):
            return [player2,player2_hand[0],player1_hand,player2_hand]
        
        n1 = player1_hand[3].find("_")
        sub1 = player1_hand[3][0:n1]
        
        n2 = player2_hand[3].find("_")
        sub2 = player2_hand[3][0:n2]
        
        if card_highs.index(sub1) > card_highs.index(sub2):
            return [player1,player1_hand[0],player1_hand,player2_hand]
        elif card_highs.index(sub1) < card_highs.index(sub2):
            return [player2,player2_hand[0],player1_hand,player2_hand]
    
        return ["both",player2_hand[0],player1_hand,player2_hand]
        
        


def get_other_high_cards(cards_needed, current_hand, possible_cards):
    for card in current_hand:
        if card in possible_cards:
            possible_cards.remove(card)
        
    possible_cards.sort(key=comparefunction2,reverse=True)
    for i in range(0,cards_needed):
        current_hand.append(possible_cards[i])
        
    return current_hand

def getHand(cards_left):
    #cards_left = ['2_of_hearts','3_of_hearts','4_of_hearts','5_of_hearts','6_of_hearts','7_of_hearts','8_of_hearts']
    royal_flush = checkRoyalFlush(cards_left)
    if royal_flush != None:
        return royal_flush

    #print("not royal")
    straight_flush = checkStraightFlush(cards_left)
    if straight_flush != None:
        return straight_flush

    #print("not straight flush")
    quads = checkQuads(cards_left)
    if quads != None:
        return quads

    #print("not quads")
    full_house = checkFullHouse(cards_left)
    if full_house != None:
        return full_house

    #print("not full house")
    flush = checkFlush(cards_left)
    if flush != None:
        return flush

    #print("not flush")
    straight = checkStraight(cards_left)
    if straight != None:
        return straight

    #print("not straight")
    three_of_a_kind = checkThreeOfAKind(cards_left)
    if three_of_a_kind != None:
        return three_of_a_kind

    #print("not ToK")
    two_pair = checkTwoPair(cards_left)
    if two_pair != None:
        return two_pair

    #print("not two pair")
    one_pair = checkOnePair(cards_left)
    if one_pair != None:
        return one_pair

    #print("not pair")
    high_card = checkHighCard(cards_left)
    if high_card != None:
        return high_card

    #print("high card")    

def checkRoyalFlush(cards_left):
    
    cards_left.sort(key=comparefunction2,reverse=True)
    cards_left.sort(key=comparefunction)
    royal_flushes = [ ['ace_of_diamonds','king_of_diamonds', 'queen_of_diamonds', 'jack_of_diamonds', '10_of_diamonds'],
                         ['ace_of_club','king_of_clubs', 'queen_of_clubs', 'jack_of_clubs', '10_of_clubs'],
                         ['ace_of_hearts','king_of_hearts', 'queen_of_hearts', 'jack_of_hearts', '10_of_hearts'],
                         ['ace_of_spades','king_of_spades', 'queen_of_spades', 'jack_of_spades', '10_of_spades']
                        ]

    for i in range(0,3):
        if cards_left[i:i+5] in royal_flushes:
            hand = ["royal_flush"]
            hand += cards_left[i:i+5]
            return hand

    return None


def checkStraightFlush(cards_left):
    #print(cards_left)
    cards_left.sort(key=comparefunction2,reverse=True)
    cards_left.sort(key=comparefunction)
    #print("straightflush sort",cards_left)

    for i in range(0,len(cards_left)-4):
        n1 = cards_left[i].find("_")
        sub1 = cards_left[i][0:n1]
        suit1 = cards_left[i][n1:]
        for j in range(i+1,i+5):
            n2 = cards_left[j].find("_")
            sub2 = cards_left[j][0:n2]
            suit2 = cards_left[j][n2:]
            #print("straight:",card_highs.index(sub2), ' ',card_highs.index(sub1))
            
            if (card_highs.index(sub1) - card_highs.index(sub2)) != 1 or suit1 != suit2:
                break
            elif i+4 == j:
                hand = ["straight_flush"]
                hand += cards_left[i:i+5]
                return hand
            else:
                sub1 = sub2
                suit1 = suit2

    return None

def checkQuads(cards_left):

    cards_left.sort(key=comparefunction2)
    #print(cards_left)
    for i in range(0,4):
        if cards_left[i][0] == cards_left[i+3][0]:
            #print(cards_left[i][0], " ", cards_left[i+3][0])
            
            hand = ["quads"]
            hand += cards_left[i:i+4]
            return hand

    return None

def checkFullHouse(cards_left):
    
    copy_cards = copy.deepcopy(cards_left)
    copy_cards.sort(key=comparefunction2,reverse=True)
    three_kind = checkThreeOfAKindForFullHouse(copy_cards)
    
    if three_kind != None:
        for i in range(0,7):
            if copy_cards[i][0] == three_kind[0][0]:
                del copy_cards[i:i+3]
                break
    else:
        return None

    pair = checkOnePairForTwoPair(copy_cards)

    if pair != None:
        hand = ["full_house"]
        hand += three_kind 
        hand += pair
        #print("HFRIHF")
        return hand

    return None


def checkFlush(cards_left):
    cards_left.sort(key=comparefunction2,reverse=True)
    cards_left.sort(key=comparefunction)
    #print(cards_left)

    for i in range(0,3):
        n1 = cards_left[i].find("_")
        n2 = cards_left[i+4].find("_")
        if cards_left[i][n1:len(cards_left[i])] == cards_left[i+4][n2:len(cards_left[i+4])]:
            hand = ["flush"]
            return hand + cards_left[i:i+5]

    return None

#sort by suit
def comparefunction(a):
    n1 = a.find("_")
    return a[n1:len(a)]


def checkStraight(cards_left):
    cards_left.sort(key=comparefunction2, reverse=True)
    #print("Look here",cards_left)
    
    cards_copy = copy.deepcopy(cards_left)
    for i in range(0,len(cards_copy)-1):
        n1 = cards_copy[i].find("_")
        sub1 = cards_copy[i][0:n1]
        
        n2 = cards_copy[i+1].find("_")
        sub2 = cards_copy[i+1][0:n2]
        if sub1 == sub2:
            del cards_copy[i+1]
            break

    #print("BUEHBDUEHNDIU", cards_copy)
    for i in range(0,len(cards_copy)-4):
        n1 = cards_copy[i].find("_")
        sub1 = cards_copy[i][0:n1]
        for j in range(i+1,i+5):
            n2 = cards_copy[j].find("_")
            sub2 = cards_copy[j][0:n2]
            #print("straight:",card_highs.index(sub2), ' ',card_highs.index(sub1))
            
            if (card_highs.index(sub1) - card_highs.index(sub2)) != 1:
                break
            elif i+4 == j:
                hand = ["straight"]
                return hand + cards_copy[i:j+1]
            else:
                sub1 = sub2

    return None


def checkThreeOfAKind(cards_left):
    cards_left.sort(key=comparefunction2)

    for i in range(0,5):
        if cards_left[i][0] == cards_left[i+2][0]:
            hand = ["three_of_a_kind"]
            return hand + cards_left[i:i+3]

def checkThreeOfAKindForFullHouse(cards_left):
    cards_left.sort(key=comparefunction2,reverse=True)

    for i in range(0,5):
        if cards_left[i][0] == cards_left[i+2][0]:
            return cards_left[i:i+3]

def checkTwoPair(cards_left):
    cards_left.sort(key=comparefunction2)
    #print("knhdied", cards_left)
    copy_cards = copy.deepcopy(cards_left)

    found_pair = checkOnePairForTwoPair(copy_cards)
    #print(found_pair)
    if found_pair != None:
        for i in range (0, len(copy_cards)-1):
            if copy_cards[i][0] == found_pair[0][0]:
                del copy_cards[i:i+2]
                break
    else:
        return None

    #print("rc:",copy_cards)
    found_other_pair = checkOnePairForTwoPair(copy_cards)
    if found_other_pair != None:
        hand = ["two_pair"]
        hand += found_pair 
        hand += found_other_pair
        return hand

    return None


def checkOnePair(cards_left):
    cards_left.sort(key=comparefunction2)
    #print("hihdied",cards_left)

    for i in range(0, len(cards_left)-1):
        if cards_left[i][0] == cards_left[i+1][0]:
            return ["pair", cards_left[i], cards_left[i+1]]

    return None

def checkOnePairForTwoPair(cards_left):
    cards_left.sort(key=comparefunction2,reverse=True)
    #print(cards_left)

    for i in range(0, len(cards_left)-1):
        if cards_left[i][0] == cards_left[i+1][0]:
            #print("pair!")
            return [cards_left[i],cards_left[i+1]]

    return None

#sort by card high
def comparefunction2(a):
    n1 = a.find("_")
    #print("n1:",n1)
    sub1 = a[0:n1]
    #print("sub1:",sub1)
    
    #print("card:",sub1[0:n1])
    
    return card_highs.index(sub1)


def checkHighCard(cards_left):
    cards_left.sort(key=comparefunction2, reverse=True)
    return ["high_card"] + cards_left[0:5]


if __name__ == "__main__":
    #print(getHand(['3_of_clubs', '7_of_spades','queen_of_diamonds','10_of_spades', 'jack_of_spades', '4_of_hearts', '9_of_spades']))
    print(checkHands("player1",['8_of_clubs', 'ace_of_spades'],"player2",['ace_of_clubs','8_of_spades'],['ace_of_hearts', '8_of_diamonds', '8_of_hearts'],"ace_of_diamonds","9_of_spades"))