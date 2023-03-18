from Q1 import phazed_group_type

def phazed_phase_type(*phase):
    """ Accepts a list containing lists of cards as input and returns a sorted 
    list of integers indicating the type(s) of the combinations of card groups 
    contained in phase as output """
    
    # List containing lists of cards
    phase_group = next(iter(phase), [])
    
    valid_phase_type = []
    
    # Create a list containing all the cards 
    total_cards = len(list(i for sublist in phase_group for i in sublist))
    
    # Check if there are atleast 4 and atmost 11 total cards
    if total_cards > 11 or total_cards < 4 or phase_group == []:
        valid_phase_type = []
        return valid_phase_type
    else:
        group_type = []
        phase_type = []
        
        for sublist in phase_group:
            # Find group type of each sublist of cards in the list
            group_type = phazed_group_type(sublist)
            phase_type.append(group_type)
        
        # Create list containing group types of each sublist of cards in list
        flat_group_type = list(j for sublist in phase_type for j in sublist)
      
        consolidate = []
        # Find phase type of list using group type of sublists of cards     
        if flat_group_type.count(1) == 2:
            consolidate.append(1)
        if flat_group_type.count(2) == 1: 
            consolidate.append(2)
        if flat_group_type.count(6) == 2: 
            consolidate.append(3)
        if flat_group_type.count(3) == 2: 
            consolidate.append(4)
        if flat_group_type.count(4) == 1: 
            consolidate.append(5)
        if flat_group_type.count(7) == 2: 
            consolidate.append(6)
        if flat_group_type.count(3) == 1 and flat_group_type.count(5) == 1: 
            consolidate.append(7)
      
    consolidate = sorted(dict.fromkeys(consolidate))
    valid_phase_type = consolidate
    return valid_phase_type


if __name__ == '__main__':
    # Example calls to the function.
    print(phazed_phase_type([['2C', '2S', '2H'], ['7H', '7C', 'AH']]))
    print(phazed_phase_type([['2C', '2C', '4C', 'KC', '9C', 'AH', 'JC']]))
    print(phazed_phase_type([['2C', 'KH', 'QS', '7H'],
                             ['3H', '7S', '0D', 'KD', 'AD']]))
    print(phazed_phase_type([['4H', '4S', 'AC', '4C'],
                             ['7H', '7C', 'AH', 'AC']]))
    print(phazed_phase_type([['4H', '5S', 'AC', '7C',
                              '8H', 'AH', '0S', 'JC']]))
    print(phazed_phase_type([['2C', 'KC', 'QS', '7C'],
                             ['3H', '7H', '0D', 'KD', 'AD']]))
    print(phazed_phase_type([['4H', '5D', 'AC', '7H'],
                             ['7H', '7C', 'AH', 'AS']]))
    print(phazed_phase_type([['4H', '5D', '7C', 'AC'], ['AC', 'AS', 'AS']]))
