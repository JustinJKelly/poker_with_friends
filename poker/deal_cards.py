import random

# A function to generate a random permutation of arr[] 
def randomize (arr, n): 
    # Start from the last element and swap one by one. We don't 
    # need to run for the first element that's why i > 0 
    for i in range(n-1,0,-1): 
        # Pick a random index from 0 to i 
        j = random.randint(0,i+1) 
  
        # Swap arr[i] with the element at random index 
        arr[i],arr[j] = arr[j],arr[i] 
    return arr 

def deal_cards(num_players):
    cards = ['2_of_hearts','3_of_hearts','4_of_hearts','5_of_hearts','6_of_hearts','7_of_hearts','8_of_hearts','9_of_hearts','10_of_hearts','jack_of_hearts','queen_of_hearts','king_of_hearts','ace_of_hearts',
             '2_of_clubs','3_of_clubs','4_of_clubs','5_of_clubs','6_of_clubs','7_of_clubs','8_of_clubs','9_of_clubs','10_of_clubs','jack_of_clubs','queen_of_clubs','king_of_clubs','ace_of_clubs',
             '2_of_spades','3_of_spades','4_of_spades','5_of_spades','6_of_spades','7_of_spades','8_of_spades','9_of_spades','10_of_spades','jack_of_spades','queen_of_spades','king_of_spades','ace_of_spades',
             '2_of_diamonds','3_of_diamonds','4_of_diamonds','5_of_diamonds','6_of_diamonds','7_of_diamonds','8_of_diamonds','9_of_diamonds','10_of_diamonds','jack_of_diamonds','queen_of_diamonds','king_of_diamonds','ace_of_diamonds']
    
    #cards = randomize(cards,len(cards))
    random.shuffle(cards)
    hand_cards = cards[:9]
    print(hand_cards)
    
    return hand_cards
    