"""initial version : K.Draziotis 25-4-2016
    
   = Tested in Python 3 =
   
   Find a function best_hand(hand) where hand consists from five cards (TODO: for seven cards)
   and returns the best hand
   
   We use the following formalism for cards :
   for Aces we use A
   for Kings we use K
   for Queens we use Q
   for 10 we use T
   for Jacks we use J
   and for suits h(hurt),d(diamont),c(club),s(spade)
   We give the following grades to the hands :
    1- One Pair
    2- Two Pair
    3- Three of a Kind
    4- Straight
    5- Flush (Tie : in case with the same three cards the higher pair wins)
    6- Full House
    7- Four of a Kind (Tie : the highest card wins)
    8- Straight Flush
   We do not consider High cards (ToDo)
   For instance a hand is represented by AsKsQsJsTs (straight flush)
   
   We shall make a function best_hand(hand), which takes a hand and returns the 
   best hand. So we need some functions, kinds(hand), which shall compute if a hand
   is two of a kind, two_pairs, three of a kind,four of kind. A function
   staright(hand),flush(hand),full_house(hand) and straight_flush(hand).
   All the functions return also the grade of the hand.
   
   TEST : 
   
   In:hand ='As Ah Ac 4s 5s'.split()
   In:straight_flush(hand)  
   Out: False
   
   In:kinds(hand)
   Out:('three aces', 3) #the second parameter is the grade of the hand
   
   In:hand ='2s 3s 2c 2h 3c'.split()
   In:best_hand(hand)   
   Out:('full house : three twos and a pair of threes', 6)
   
   In:hand ='2s 3s 4s 5s 6s'.split()
   In:best_hand(hand)
   Out:('straight flush with high card sixes', 8)
   """


import collections
allranks = '2 3 4 5 6 7 8 9 T J Q K A'.split()
suits ='h d c s'.split()
aDict = {'2':'twos','3':'threes','4':'fours','5':'fives',
         '6':'sixes','7':'sevens','8':'eights','9':'nines',
         '10':'tens','11':'jacks','12':'queens','13':'kings','14':'aces'}

bDict = {'s':'Spades','c':'Clubs','h':'Hurts','d':'Diamonds' }


import itertools
#we generate all the cards
cards = []
for element in itertools.product(allranks,suits):
    cards.append("".join(element))


def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def flush(hand):
    "Returns flush, if all the cards have the same suit."
    suits = [s for r,s in hand]
    if len(set(suits)) == 1:
        return 'flush of' + ' ' + bDict[suits[0]],5
    return False
        
def straight(hand):
    """Return a message starigh with high card 'something', if the ordered
    ranks form a 5-card straight."""
    ranks = card_ranks(hand)
    if (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5:
        return 'straight with high card' + ' ' + str(ranks[0]),4
    return False

def kinds(hand):
    "this function will return the best hand between 4 of kind, three of a kind,two pairs,one pair"
    ranks = card_ranks(hand)
    
    ### four of a kind
    n = 4
    A = [item for item, count in collections.Counter(ranks).items() if count == n]
    if A!=[]:
        return "four"+" "+ aDict[str(A[0])],7
    
    ### three of a kind
    n = 3
    A = [item for item, count in collections.Counter(ranks).items() if count == n]
    if A!=[]:
        return "three" + " " + aDict[str(A[0])],3
    
    ### two_pairs
    n = 2
    A = [item for item, count in collections.Counter(ranks).items() if count == n]
    if A!=[] and len(A)==2:
        return "two pairs of" + ' ' + aDict[str(A[0])] + ' ' + 'and' + ' ' +  aDict[str(A[1])],2
    
    ### two of a kind:one pair
    n = 2
    A = [item for item, count in collections.Counter(ranks).items() if count == n]
    if A!=[] and len(A)==1:
        return "one pair of" + " " + aDict[str(A[0])],1     
    return False

def full_house(hand):
    "Return full house, if there are both three of kind and one pair"
    ranks = card_ranks(hand)
    if kinds(hand)!=False:
        if kinds(hand)[1]==3:
            B = [item for item, count in collections.Counter(ranks).items() if count == 3]
            A = [item for item, count in collections.Counter(ranks).items() if count == 2]
            if A!=[] and len(A)==1:
                 return "full house : three" + " " +  aDict[str(B[0])] + " " + "and a pair of" + " " + aDict[str(A[0])],6
    return False

def straight_flush(hand):
    "Return straight flush"
    ranks = card_ranks(hand)
    if straight(hand)!=False:
        if flush(hand)!=False:
             return "straight flush with high card"+ " " + aDict[str(ranks[0])],8
    return False

def best_hand(hand):
    #we use the fact that function kinds(hand) returns the best hand
    if straight_flush(hand)==False and flush(hand)==False and straight(hand)==False and full_house(hand)==False:
        if kinds(hand)!=False:
            return kinds(hand)
    if full_house(hand)!=False:
        return full_house(hand)
        
    #straight flush is the best hand
    if straight_flush(hand)!=False:
         return straight_flush(hand)
    #if the hand is flush and not straight flush we do not have to consider other case
    if flush(hand)!=False:
        return flush(hand)
    #if the hand is not flush,straight flush,and kinds(hand) then it will be straight
    if straight(hand)!=False:
        return straight(hand)       
        

