import itertools
from collections import OrderedDict

# Defining Validity of group
valid_group_type = ['Valid']
invalid_group = bool
group_ctype_n2 = bool

def query_list_build(query_group):
    """ Accepts a list of cards as input and returns a list indicating the 
    colour and value of each card as output """
    
    query_list = []
    val = 0
    colour = 0
    
    # Finds the value of each card in the list by identifying its first element
    for items in query_group:
        if items[:-1] == 'A':
            val = 1
        elif items[:-1] == '0':
            val = 10
        elif items[:-1]   == 'J':
            val = 11
        elif items[:-1]   == 'Q':
            val = 12
        elif items[:-1]   == 'K':
            val = 13
        else:
            val = int(items[:-1]) 
            
        # Finds the colour of each card in the list using its first letter   
        if items[1:2] in ('C', 'S'):
            colour = 'Black'
        elif items[1:2] in ('D', 'H'):
            colour = 'Red'
        
        query_list.append((('%s%s' % (items[:-1], items[1:2])), colour, val))
        
    # Create a list containing details of colour and value of each card
    query_list = [list(elem) for elem in query_list]
    return query_list

def getvalue_pic(card):
    """ Accepts a string containing a card name as input and returns its value
    in integer form as output """
    
    val = 0
    
    # Finds the value of the card using its first element
    if card == 'A':
        val = 1
    elif card == '0':
        val = 10
    elif card  == 'J':
        val = 11
    elif card  == 'Q':
        val = 12
    elif card == 'K':
        val = 13
    else:
        val = int(card)
        
    return(val)

def getnames(card):
    """ Accepts a value in integer form as input and returns the possible card 
    name matching the value as a string as output """
    
    # Find first element of card name using its value
    if card == '1' or card == 1:
        card_name = 'A'
    elif card == '10' or card == 10:
        card_name =  '0'
    elif card == '11' or card == 11:
        card_name = 'J'
    elif card == '12'or card == 12:
        card_name = 'Q'
    elif card == '13' or card == 13:
        card_name = 'K'
    else:
        card_name = str(card)

    return card_name

def valid_run(run_values):
    """ Accepts a list containing the first element of each card in the list as 
    input and returns whether the cards constitute a valid run in the form of 
    boolean value as output """
    
    # Find the position of each card in the list corresponding to card value
    card_position = list(i for i, k in enumerate(run_values) if k !=1)
    card_val = list(x for x in run_values if x !=1)

    valid_run = bool
    tally = 0
    gap = 0
    card1_val = 0
    card2_val = 0
    card1_val = card_val[0]
    
    for index, element in enumerate(run_values):        
        tally += 1   
        
        # Check if card is in correct position in list corresponding to value
        if index > card_position[0] and tally < (len(run_values) + 1):
            card2_val = run_values[index]
            
            # Define expected value of card succeeding the current card in list
            if card2_val == 1:
                card1_val = card1_val + 1
                
            else:
                
                # If current card is of lower value than next card in list
                if card1_val < card2_val:
                    # Find gap in value between two successive cards in list
                    gap = (card2_val - card1_val) - 1
                    
                    # Find validity of run
                    if gap > 1:
                        valid_run = False
                        break
                    else:
                        valid_run = True
                        card1_val = card2_val
                        
                elif card1_val > card2_val:
                    if card1_val == 13 and card2_val == 2:
                        valid_run = True
                    else:
                        valid_run = False
                        break
                        
                elif card1_val == card2_val:
                    valid_run = False
                    break
                    
    return valid_run

def phazed_group_type(group):
    """ Accepts a list containing a group of cards as input and returns a 
    sorted list of integers indicating card combination types as output """

    global valid_group_type
    query_group = group[:]

    # Check if there are atleast 3 and maximum 11 cards in the list
    if len(query_group) not in range(3, 12):
        valid_group_type = []       
        return valid_group_type
    
    # Check if there are more than 8 cards and if all of them are the same 
    elif len(query_group)>8 and len(set(query_group)) == 1:
        # Group of cards are invalid
        valid_group_type = []
        return valid_group_type
    
    # Create a list containing information of each card
    query_list = query_list_build(query_group)
    
    # List of card names
    qcard_names = list(x[0][0] for x in query_list)
    # Lists of colours and values of each card in group
    qcard_values = list(v[2] for v in query_list)
    # Amount of cards in list
    qcards_n = len(query_list)

    # Group is valid if there are atleast 2 cards
    if len(qcard_names) >= 2:
        group_ctype_n2 = True
    else:
        group_ctype_n2 = False
        valid_group_type = []
        return valid_group_type
    
    # Create lists from query_list excluding Wild Cards  
    naturals_names = list(name[0][0] for name in query_list if name[0][0] != 
                          'A')
    naturals_suits = list(name[0][1] for name in query_list if name[0][0] != 
                          'A')
    naturals_colours = list(name[1] for name in query_list if name[0][0] != 
                            'A')

    # Create lists of unique cards from the lists of Non-Wild Cards
    naturals_names_unique = list(OrderedDict.fromkeys(naturals_names))
    naturals_suits_unique = list(OrderedDict.fromkeys(naturals_suits))
    naturals_colours_unique = list(OrderedDict.fromkeys(naturals_colours))
    
    def group_1_3(query_group):
        """ Accepts a list containing a group of cards as input and returns 
        their group number if they belong to groups 1 and/or 3 as list of 
        integers as output """
        
        group_ctype1 = []

        # If there are minimum 2 cards and maximum 5 cards in list
        # If there is atleast one unique Non-Wild Card in list        
        if group_ctype_n2 is True and qcards_n in range(3, 5) and \
            len(naturals_names_unique) == 1:
            # If there are 3 cards
            if qcards_n == 3:
                group_ctype1.append(1)
            # If there are 4 cards    
            elif qcards_n == 4:
                group_ctype1.append(3)
        else:
            group_ctype1 = []

        return group_ctype1
    
    def group_2(query_group):
        """ Accepts a list containing a group of cards as input and returns 
        their group number if they belong to group 2 as list of 
        integer as output """
        
        group_ctype2 = []
        # If there are 7 cards and all of them belong to the same suit
        if group_ctype_n2 is True and qcards_n == 7 and \
            len(naturals_suits_unique) == 1:
            group_ctype2.append(2)
        else:
            group_ctype2 = []
        return group_ctype2

    def group_4(query_group):
        """ Accepts a list containing a group of cards as input and returns 
        their group number if they belong to group 4 as list of 
        integer as output """
        
        group_ctype4 = []
        run8 = bool
        
        # If there are 8 cards and no Wild cards in list
        if group_ctype_n2 is True and len(query_list) == 8 and \
            len(naturals_names_unique) == len(naturals_names):
            run_values = qcard_values
            run8 = valid_run(run_values)
            
            # If cards constitute a run of cards
            if run8 is True:
                group_ctype4.append(4)
            else:
                group_ctype4 = []
                
        else:
            group_ctype4 = []   
            
        return group_ctype4
    
    def group_5(query_group):
        """ Accepts a list containing a group of cards as input and returns 
        their group number if they belong to group 5 as list of 
        integer as output """        
        
        group_ctype5 = []
        run4 = bool
        
        # If there exactly 4 Non-Wild Cards of the same colour
        if group_ctype_n2 is True and len(query_list) == 4 and \
            len(naturals_names_unique) == len(naturals_names) and \
            len(naturals_colours_unique) == 1:
            
            run_values = qcard_values
            run4 = valid_run(run_values)
            
            # If the group of cards constitute a valid run
            if run4 is True:
                group_ctype5.append(5)
            else:
                group_ctype5 = []
        else:
            group_ctype5 = []  
            
        return group_ctype5
    
    def group_6(query_group):
        """ Accepts a list containing a group of cards as input and returns 
        their group number if they belong to group 6 as list of 
        integer as output """       
        
        group_ctype6 = []
        
        # Find sum of values of cards in list
        sumup = list(itertools.accumulate(qcard_values,))
        
        # If cards form an accumulation of 34
        if sumup[-1] == 34:
            group_ctype6.append(6)
        else:
            group_ctype6 = []
            
        return group_ctype6
    
    def group_7(query_group):
        """ Accepts a list containing a group of cards as input and returns 
        their group number if they belong to group 7 as list of 
        integer as output """   
        
        group_ctype7 = []
        
        # If all cards are of the same colour
        if len(naturals_colours_unique) == 1:
            # Find sum of values of cards in list
            sumup = list(itertools.accumulate(qcard_values,))
            # If cards form an accumulation of 34
            if sumup[-1] == 34:
                group_ctype7.append(7)
            else:
                group_ctype7 = []
                
        else:
            group_ctype7 = []
            
        return group_ctype7

    # Create a list of integers indicating card combination types of the cards 
    consolidate = group_1_3(query_group) + group_2(query_group) + \
        group_4(query_group) + group_5(query_group) + group_6(query_group) + \
        group_7(query_group)
    consolidate = sorted(dict.fromkeys(consolidate))
    valid_group_type = consolidate
    return valid_group_type


if __name__ == '__main__':
    # Example calls to the function.
    print(phazed_group_type(['2C', '2S', '2H']))
    print(phazed_group_type(['2C', '2C', '4C', 'KC', '9C', 'AH', 'JC']))
    print(phazed_group_type(['4H', '4S', 'AC', '4C']))
    print(phazed_group_type(['4H', '5S', 'AC', '7C', '8H', 'AH', '0S', 'JC']))
    print(phazed_group_type(['4H', '5D', 'AC', '7H']))
    print(phazed_group_type(['KS', '0D', '8C', '3S']))
    print(phazed_group_type(['KS', '0C', '8C', '3S']))
    print(phazed_group_type(['2C', '2C', '4C', 'KC', '9C', 'AS', '3C']))
    print(phazed_group_type(['4H', '5D', '7C', 'AC']))
