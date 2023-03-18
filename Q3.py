from collections import OrderedDict
from Q1 import getvalue_pic, phazed_group_type, valid_run
from Q2 import phazed_phase_type
import itertools

def is_valid_player(play_type, last_player, player_id):
    """ Accepts a 3 element tuple containing play type, player ID of the 
    most recent player and the current Player ID as input and returns a boolean 
    value indicating whether the current player is eligible to play next as 
    output """
    
    # If card is picked up from the top of deck or discard pile in the play
    if play_type in (1, 2):
        # If the most recent player has Player ID of 0, 1 or 2
        if last_player in (0, 1, 2):
            valid_player = last_player + 1
        elif last_player == 3:
            valid_player = 0
       
        else:
            valid_player = None
        
        # If the current player ID is same as the expected next player's ID
        if player_id == valid_player:
            return True
        else:
            return False
        
    # If the play has play type of 3, 4 or 5    
    elif play_type in (3, 4, 5):        
        # If the most recent player has the same ID as the current player
        if last_player == player_id:
            valid_player = True
            return True
        else:
            valid_player = False
            return False
    else:
        valid_player = False
        return False
    
def addto_run_index(add_position_index, add_card, addto_group):
    """ Accepts a tuple containing position of single play to the table, name 
    of single play card and group to which the card is added to as input and 
    returns a boolean value indicating whether position of single play is valid 
    """
    
    addto_run_idx = bool
    
    # If card is being added to the start of the group 
    if add_position_index == 0:
        
        start_addto_group = addto_group
        start_addto_group.insert(0, add_card)
        start_addto_group_val = list(getvalue_pic(item[0]) for item in 
                                     start_addto_group)
        
        # Check if run of cards is valid 
        start_run = valid_run(start_addto_group_val)
        
        if start_run is True:
            addto_run_idx = True
        else:
            addto_run_idx = False
        start_addto_group.clear()
        
    # If card is added to the end of group    
    elif add_position_index == len(addto_group):
        end_addto_group = addto_group
        end_addto_group.append(add_card)
        end_addto_group_val = list(getvalue_pic(item[0]) for item in 
                                   end_addto_group)
        
        # Check if run of cards is valid
        end_run = valid_run(end_addto_group_val)
        if end_run is True:
            addto_run_idx = True
        else:
            addto_run_idx = False 
        end_addto_group.clear()
    return addto_run_idx

def phazed_is_valid_play(play, player_id, table, turn_history, phase_status, 
                         hand, discard):
    """ Accepts a tuple containing several nested tuples within indicating play,
    player ID, table, turn history, phase status, hand and discard as input and
    returns a boolean value indicating if play is valid relative to the current 
    hand state as output """
    
    valid_play = bool
    
    # Find play type and content of the play
    play_type = play[0]
    play_type_details = play[1]
    
    # Define discard pile and phase status of each player
    discard_pile = discard
    player_phase = phase_status[player_id]
    
    # Create lists containing details of the last turn in turn history
    last_turn = list(turn_history[-1])
    last_player = last_turn[0]
    last_play = last_turn[1]
    last_play_pickup = last_play[0][0]
    last_play_info = list(last_play[-1])
    last_discarded = [item for item in last_turn[1] if item[0] == 5]
    last_play_type = last_play_info[0]

    # Check validity of the play
    # If play type is 3, 4 or 5
    if turn_history == [] and play_type in (3, 4, 5):
        valid_play = False
   
    # Check if current player ID matches the expected player ID of next turn
    if turn_history != [] and is_valid_player(play_type, last_player, 
                                              player_id):
        valid_play = True
    else:
        valid_play = False
   
    # If play type is 1 
    if play_type == 1:
        
        # Check if first play was played by Player 0
        if turn_history == [] and player_id == 0:
            valid_play = True
            
        # Check if the play type of the last turn is 5
        elif turn_history != [] and last_play_type == 5:
            valid_play = True
        else:
            valid_play = False

    # If play type is 2 
    if play_type == 2:
        
        pile_pickupcard = play_type_details
       
        # Check if the recently discarded card was picked up again by player 
        if turn_history != [] and (last_discarded != [] or discard_pile != [])\
            and last_discarded[0][1] == pile_pickupcard:
            valid_play = True
                
        elif (turn_history == [] and player_id == 0) and discard_pile != [] \
            and pile_pickupcard == discard_pile:
            valid_play = True
        else:
            valid_play = False 
    
    # If play type is 3
    if play_type == 3:
        
        # If current player is the last player of the play
        # And picked up a card from the deck or discard pile
        # Then did not place a phase to the table from hand
        if last_player == player_id and last_play_pickup in (1, 2) and \
            last_play_type != 3:
            
            phase_fromq2 = phazed_phase_type(play_type_details[1])
            
            # Check if current phase played by the player is in order with
            # previous phase played           
            if (play_type_details[0] == player_phase + 1) and \
                (phase_fromq2[0] == play_type_details[0]):
                
                # Find all cards played by the player to the phase
                phase_cards = list(itertools.chain.from_iterable
                                   (play_type_details[1]))
                
                # If all cards played in the phase is from player's hand 
                if (all(cards in hand for cards in phase_cards)):
                    valid_play = True
                else:
                    valid_play = False
            else:
                valid_play = False
        else:
            valid_play = False

    # If play type is 4 
    if play_type == 4:
        
        # If previous plays for the player exist
        if last_turn != [] and last_player == player_id:
            
            # Find single card placed to a phase on the table
            add_card = play_type_details[0]
            
            # If play types of player is in order
            # And single card from player's hand was placed on the table 
            if last_play_pickup in (1, 2) and last_play_type in (1, 2, 3, 4) \
                and (add_card in hand):
                
                # Find details of card placed to phase on table
                add_card_name = add_card[0]
                add_card_colour = list(set('Red' if col in ('D', 'H') else 
                                           'Black' for col in add_card))
                add_card_colour = add_card_colour[0]
                add_card_suit = add_card[1]
                add_card_value = getvalue_pic(add_card[0])
                
                # Find position of phase that the card is being placed to 
                add_position_player_id = play_type_details[1][0]
                add_position_group = play_type_details[1][1] 
                add_position_index = play_type_details[1][2]
                
                # Compile details of group to which card is placed
                target_table_info = table[add_position_player_id]
                addto_phase = target_table_info[0]
                addto_group = target_table_info[1][add_position_group]
                length_addtogroup = len(addto_group)
                col_addtogroup_naturals = list('Red' if col in ('D', 'H') else
                                               'Black' for col in addto_group 
                                               if addto_group[0] != 'A')
                col_addtogroup_nat = list(OrderedDict.fromkeys
                                          (col_addtogroup_naturals))
                col_addtogroup_nat = col_addtogroup_nat[0]
                suit_addtogroup_naturals = list(sym[1] for sym in addto_group 
                                                if sym[0][0] != 'A')
                suit_addtogroup_nat = list(OrderedDict.fromkeys
                                           (suit_addtogroup_naturals))
                suit_addtogroup_nat = suit_addtogroup_nat[0]
                values_addtogroup_naturals = list(getvalue_pic(item[0]) for 
                                                  item in addto_group if 
                                                  item[0] != 'A')
                values_addtogroup_nat = list(OrderedDict.fromkeys
                                             (values_addtogroup_naturals))
                values_addtogroup_nat = values_addtogroup_nat[0]
                
                start_addto_run_idx = bool
                end_addto_run_idx  = bool
                
                # If card is added to a group of phase 7 having a run of cards 
                if (addto_phase == 7 and add_position_group == 0) and \
                    length_addtogroup <13:
                    
                    # Check if card added is a wild card (Ace)
                    if (add_card_name != 'A' and add_card_colour == 
                        col_addtogroup_naturals):
                        
                        # If card is added to the start of run
                        if add_position_index == 0:
                            start_addto_run_idx = addto_run_index(0, add_card, 
                                                                  addto_group)
                        # If card is added to end of run     
                        elif add_position_index == length_addtogroup:
                            end_addto_run_idx = addto_run_index
                            (length_addtogroup, add_card, addto_group)
                        
                        # If index of card being added exists
                        if start_addto_run_idx is True or end_addto_run_idx is\
                            True:
                            valid_play = True
                        else:
                            valid_play = False
                            
                    # If card added is a Wild card
                    elif add_card_name == 'A':
                        valid_play = True
                        
                # If card is added to a group of phase 5 having a run of cards   
                elif addto_phase == 5 and length_addtogroup <13:
                    
                    # If card added is not a Wild card
                    if add_card_name != 'A':
                        
                        # If card is being added to the start of the run 
                        if add_position_index == 0:
                            start_addto_run_idx = addto_run_index(0, add_card, 
                                                                  addto_group)
                            
                        # If card is being added to the end of the run    
                        elif add_position_index == length_addtogroup:
                            end_addto_run_idx = addto_run_index
                            (length_addtogroup, add_card, addto_group)
                            
                        # If index of card being added exists    
                        if start_addto_run_idx is True or end_addto_run_idx \
                            is True or add_card_name == 'A':
                            valid_play = True
                        else:
                            valid_play = False
                            
                    # If card being added is a Wild card 
                    elif add_card_name == 'A':
                        valid_play = True
                        
                # Check for valid index position in case of card added to other
                # types of groups of varying phases
                elif addto_phase in (1, 2, 4) or (addto_phase == 7 and 
                                                  add_position_group == 1):
                    
                    if add_position_index >= 0 and add_position_index <= \
                        length_addtogroup and length_addtogroup < 17:
                        
                        # If card added is a Wild Card
                        if add_card_name != 'A':
                        
                            if addto_phase == 1 or addto_phase == 4 or \
                                (addto_phase == 7 and add_position_group == 1):
                                
                                # Check if the card added is the same value 
                                if values_addtogroup_nat == add_card_value:
                                    valid_play = True
                                else:
                                    valid_play = False
                                    
                            # If card is added to a group of cards of phase 2 
                            if addto_phase == 2:
                                
                                # Check if card added is of the same suit
                                if suit_addtogroup_nat == add_card_suit:
                                    valid_play = True
                                else:
                                    valid_play = False
                                    
                            # If card is added to a group of cards of phase 5
                            if addto_phase == 5:
                                
                                # Check if card added is of the same colour
                                if col_addtogroup_nat == add_card_colour:
                                    valid_play = True
                                else:
                                    valid_play = False
                                    
                        # If the card added is a Wild card
                        elif add_card_name == 'A':
                            valid_play = True
                            
                    # If added card's index is out of range 
                    elif add_position_index > length_addtogroup:
                        valid_play = False
                        
                # If card is being added to a group of cards with phase 3 or 6
                elif addto_phase in (3, 6) and (add_position_index >= 0 and 
                                                add_position_index <= 
                                                length_addtogroup):
                    sumup = 0
                    values_addtogroup = list(getvalue_pic(item[0]) for item 
                                             in addto_group)
                    sum_values_addtogroup = list(itertools.accumulate
                                                 (values_addtogroup,))
                    sumup = sum_values_addtogroup[-1]
                    
                    # If card is added to a 34-accumulation of the same colour
                    if addto_phase == 6:
                        col_sumup = bool
                        
                        # If card added is same colour as accumulation cards
                        if col_addtogroup_nat == add_card_colour:
                            col_sumup = True
                        else:
                            col_sumup = False
                            valid_play = False    
                            
                    # If card is added to a group of cards of phase 3
                    # Or if card is added to group of same colour cards
                    if addto_phase == 3 or col_sumup is True:
                        
                        # Check if card added is not the only card left in hand
                        if len(hand)>1:    
                            
                            # Check if single play results in full accumulation
                            # Or results in value lesser than lowest value  
                            if sumup < 55 and (sumup + add_card_value) <= 55:
                                valid_play = True
                            elif sumup > 55 and (sumup + add_card_value) <= 68:
                                valid_play = True
                            elif sumup > 68 and (sumup + add_card_value) <= 76:
                                valid_play = True
                            elif sumup > 76 and (sumup + add_card_value) <= 81:
                                valid_play = True
                            elif sumup > 81 and (sumup + add_card_value) <= 84:
                                valid_play = True
                            elif sumup > 84 and (sumup + add_card_value) <= 86:
                                valid_play = True
                            elif sumup > 86 and (sumup + add_card_value) <= 87:
                                valid_play = True
                            else:
                                valid_play = False
                                
                        # If card added is the last card left in hand        
                        elif len(hand) == 1:
                            
                            # Check if single play results in full accumulation
                            # Or results in value lesser than lowest value  
                            if sumup < 55 and (sumup + add_card_value) == 55:
                                valid_play = True
                            elif sumup > 55 and (sumup + add_card_value) == 68:
                                valid_play = True
                            elif sumup > 68 and (sumup + add_card_value) == 76:
                                valid_play = True
                            elif sumup > 76 and (sumup + add_card_value) == 81:
                                valid_play = True
                            elif sumup > 81 and (sumup + add_card_value) == 84:
                                valid_play = True
                            elif sumup > 84 and (sumup + add_card_value) == 86:
                                valid_play = True
                            elif sumup > 86 and (sumup + add_card_value) == 87:
                                valid_play = True
                            else:
                                valid_play = False
            else:
                valid_play = False
        else:
            valid_play = False
    
    # If play type is 5
    if play_type == 5:
        
        # Find which card is to be discarded
        cardto_discard = play_type_details
        
        # If the current player is the last player 
        # If the card to be discarded is in player's hand 
        if last_player == player_id and last_play_pickup in (1, 2) and \
            cardto_discard in hand:
            
            # If card to discard is not the last card left in hand
            if len(hand) > 1 and last_play_type != 5:
                valid_play = True
                
            # If card to discard is the last card left in hand     
            elif len(hand) == 1 and last_play_type == 4:
                accu_end_sumup = 0
                accu_end_playerid = last_play_info[1][1][0]
                accu_end_group_idx = last_play_info[1][1][1]
                accu_end_group = table[accu_end_playerid][1]
                [accu_end_group_idx]
                accu_end_group = list(item for item in accu_end_group)
                accu_end_values = list(getvalue_pic(val[0]) for val in 
                                       accu_end_group)
                accu_end_sum_values = list(itertools.accumulate
                                           (accu_end_values,))
                accu_end_sumup = accu_end_sum_values[-1]
                
                # If value of cards add up to 55,68,76,81,84,86 or 87
                if accu_end_sumup in (55, 68, 76, 81, 84, 86, 87):
                    valid_play = True           
                else:
                    valid_play = False
        else:
            valid_play = False
            
    return valid_play


if __name__ == '__main__':
    # Example calls to the function.
    print(phazed_is_valid_play((3, (1, [['2S', '2S', '2C'],
        ['AS', '5S', '5S']])), 0, [(None, []), (None, []),
        (None, []), (None, [])], [(0, [(2, 'JS')])],
        [0, 0, 0, 0], ['AS', '2S', '2S', '2C', '5S', '5S',
                       '7S', '8S', '9S', '0S', 'JS'], None))
    print(phazed_is_valid_play((4, ('KC', (1, 0, 0))),
        1, [(None, []), (2, [['2S', '2S', 'AS', '5S',
        '5S', '7S', 'JS']]), (None, []), (None, [])],
        [(0, [(2, 'JS'), (5, 'JS')]), (1, [(1, 'XX'),
        (3, (2, [['2S', '2S', 'AS', '5S', '5S', '7S', 'JS']]))])],
        [0, 2, 0, 0], ['5D', '0S', 'JS', 'KC'], 'JS'))
    print(phazed_is_valid_play((5, 'JS'), 1, [(None, []),
        (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']]),
        (None, []), (None, [])], [(0, [(2, 'JS'),
        (5, 'JS')]), (1, [(1, 'XX'), (3, (1, [['2S', '2S',
        '2C'], ['AS', '5S', '5S']]))])], [0, 1, 0, 0],
        ['AD', '8S', '9S', '0S', 'JS'], 'JS'))
