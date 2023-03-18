from Q1 import phazed_group_type, query_list_build, getvalue_pic, getnames, \
    valid_run 
from Q2 import phazed_phase_type
from Q3 import phazed_is_valid_play, is_valid_player, addto_run_index
from collections import OrderedDict
import itertools
   
def phazed_bonus(player_id, table, turn_history, phase_status, hand, discard):
    """ Accepts a 6-element tuple containing details of player ID, table, turn
    history, phase status, hand and discard as input and returns a 2-tuple 
    describing the single play the player wishes to make, made up of player
    ID and associated play content as output """
    
    # Find cards in discard pile and amount of cards in hand 
    hand_cards = hand    
    pile_topcard = discard
    length_hand_cards = len(hand)
    playid = 0
    playcontent = []
    
    def throw_card(hand):
        
        playid = 0
        playcontent = ''
        skip_card = 'zz'
        if skip_card in hand:
            playid = 6
            playcontent = 3
        else:
            playid = 5
            playcontent = hand[0]
        return playid, playcontent

    # Check if player is the first to play, middle or last to play
    # If turn history is empty, player picks up card from deck or discard pile
    if turn_history == []:
        playid = 1
        playcontent = None

    # If discard pile is empty, player is to discard a card
    if pile_topcard is None or pile_topcard == []:
        # play 5 or 6
        playid, playcontent = throw_card(hand)     

    # If there is only 1 card left in hand, player is to discard it
    if length_hand_cards == 1:
        playid, playcontent = throw_card(hand)

    # If there is more than 1 card left in hand, collect details of last turn     
    if length_hand_cards > 1 and pile_topcard != [] and turn_history != []:
        last_turn = list(turn_history[-1])
        last_player = last_turn[0]
        last_play_list = last_turn[1]    
        last_playdetails = list(last_play_list[-1])
        last_play_type = last_playdetails[0]
        
        # Define name to player_id as "player"
        player = player_id
        
        
        # check if our player has completed the phase in that turn
        
        if last_player == player_id and (last_play_type == 3 or last_play_type 
                                         == 4):
            player_turn_phase_completed = True
        else:
            player_turn_phase_completed = False

        # First play of the player turn
        if last_player != player:
            playid = 1
            playcontent = None
       
                        
        def play4_5(table, add_card):
            """ Accepts 2 lists containing information about cards in table 
            and discard pile as input and returns play ID and play content
            as output """

            valid_addto_play4 = bool
            group_no = -1
            playid = 0
            playcontent = []
            # check for any phases displayed  by players on the table
            for player in table:
                # ignore those who have not got any phase                
                if player[0] is not None:
                    # collect details of the group if displayed by players
                    for phase_group in player[1]:
                        group_no += 1
                        # Find last card postion of the group to be added
                        addto_last_index = len(phase_group)
                        play = tuple((4, (add_card, (player[0], (group_no), 
                                                        addto_last_index))))

                        valid_addto_play4 = phazed_is_valid_play(play, player, 
                                                                 table, 
                                                                 turn_history, 
                                                                 phase_status, 
                                                                 hand_cards, 
                                                                 pile_topcard)
                        
                        # Check if addition of card to group is valid
                        if valid_addto_play4 is True:
                            break

            if valid_addto_play4 is True:
                playid = 4
                playcontent = play[0]
            else:
                playid, playcontent = throw_card(hand)
            return playid, playcontent
       
        # If the play is continuous play after play 1
        if last_player == player:

            # If player picked card from deck or discard pile
            # And has not completed a phase yet
            if last_play_type in (1, 2) and player_turn_phase_completed is\
                False:
                # assuming no phase to display
                playid, playcontent = throw_card(hand)

            # If player picked card from deck or discard pile
            # And has already completed a phase                       
            elif last_play_type in (1, 2) and player_turn_phase_completed is \
                True:
                non_skip_cards = list(item for item in hand_cards if item[0] != 
                                      'z')
                add_card = non_skip_cards[0]
                playid, playcontent = play4_5(table, add_card)

            elif last_play_type == 3:
                playid, playcontent = throw_card(hand)

            elif last_play_type == 4:
                playid, playcontent = throw_card(hand)     

    player_to_playid = playid
    player_to_playcontent = playcontent
    
    return player_to_playid, player_to_playcontent


if __name__ == '__main__':
    # Example call to the function.
    print(phazed_bonus(2, [(None, []), (None, []), (None, []), (None, [])],
        [(0, [(2, 'JS'), (6, 1)])],
        [(False, False, False, False, False, False, False),
         (False, False, False, False, False, False, False),
         (False, False, False, False, False, False, False),
         (False, False, False, False, False, False, False)],
        ['5D', '3H', '0C', '2H', '2C', '7H', 'KS', 'AS', 'KH', 'JC'], 'ZZ'))  
