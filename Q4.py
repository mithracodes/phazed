def phazed_score(hand):
    """ Accepts a list of cards that the current player holds in their hand in 
    the form of a 2-element string as input and returns the score for the hand 
    in the form of a non-negative integer as output """
    
    score = 0
    
    # Create a dictionary with values for each card based on its first element
    values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, 
              "0": 10, "J": 11, "Q": 12, "K": 13, "A": 25}
    
    if hand != []:        
        # Find first element of each card in list 
        first_val = [i[0] for i in hand]
        
        # Find corresponding value of card and add to total score 
        for val in first_val:
            if val in values.keys():
                score = score + int(values[val])
        return score
    return 0
  
    
if __name__ == '__main__':
    # Example calls to the function.
    print(phazed_score(['9D', '9S', '9D', '0D', '0S', '0D']))
    print(phazed_score(['2D', '9S', 'AD', '0D']))
    print(phazed_score([]))
