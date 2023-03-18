from Q1 import phazed_group_type, query_list_build, getvalue_pic, getnames, \
    valid_run 
from Q2 import phazed_phase_type
from Q3 import phazed_is_valid_play, is_valid_player, addto_run_index
from collections import OrderedDict
import itertools

def phazed_play(player_id, table, turn_history, phase_status, hand, discard):
    """ Accepts a 6-element tuple containing details of player ID, table, turn
    history, phase status, hand and discard as input and returns a 2-tuple 
    describing the single play the player wishes to make, made up of player
    ID and associated play content as output """
    
    # Find cards in discard pile and amount of cards in hand 
    discard_pile = discard
    length_hand_cards = len(hand)

    player_to_playid = 0
    player_to_playcontent = ''
    playid = 0
    playcontent = []
    
    # Check if player is the first to play, middle or last to play

    # If turn history is empty, player picks up card from deck or discard pile
    if turn_history == []:
        playid = 1
        playcontent = None

    # If discard pile is empty, player is to discard a card
    if discard_pile is None or discard_pile == []:
        playid = 5
        playcontent = hand[-1]

    # If there is only 1 card left in hand, player is to discard it
    if length_hand_cards == 1:
        playid = 5
        playcontent = hand[-1]

    # If there is more than 1 card left in hand, collect details of last turn     
    if length_hand_cards > 1 and discard_pile != [] and turn_history != []:
        last_turn = list(turn_history[-1])
        last_player = last_turn[0]
        last_play_list = last_turn[1]    
        last_playdetails = list(last_play_list[-1])
        last_play_type = last_playdetails[0]
        
        # Define name to player_id as "player"
        player = player_id

        # If there are no cards put by player on table, phase is not completed
        if table[player][0] is None:
            player_turn_phase_completed = False
        else:
            player_turn_phase_completed = True

        # If player is not the last one to play
        if last_player != player:
            
            # Check if pile pick up could benefit for phase completion
            # If player has completed a phase 
            if player_turn_phase_completed is True:
                playid = 1
                playcontent = None
                play_handcard = hand
                
                # Find details about cards in player's hand 
                query_list = query_list_build(play_handcard)
                qcard_naturals = list(n[0] for n in query_list if n[0][0] != 
                                      'A')
            else:
                playid = 2
                playcontent = discard_pile
                pile_pickup = discard_pile

                # Evaluate hand cards, discard pile to match phase to play
                play_handcard = hand
                play_handcard.append(pile_pickup)

                # Find details about cards in player's hand
                query_list = query_list_build(play_handcard)
                qcard_naturals = list(n[0] for n in query_list if n[0][0] != 
                                      'A')
                
        
        def play4_5(table, pile_pickup):
            """ Accepts 2 lists containing information about cards in table 
            and discard pile as input and returns play ID and play content
            as output """

            valid_addto_play4 = bool
            addto_playcontent4 = []
            group_no = -1
            playid = 0
            playcontent = []

            for player in table:

                # If player 0 did not play a phase 
                if player[0] is not None:
                    for phase_group in player[1]:
                        group_no += 1

                        # Find last card of the group to be added
                        addto_last_index = len(phase_group)
                        play = tuple((4, (pile_pickup, (player[0], (group_no), 
                                                        addto_last_index))))
                        addto_playcontent4 = tuple((play, player, table, 
                                                    turn_history, phase_status, 
                                                    play_handcard, 
                                                    discard_pile))
                        valid_addto_play4 = phazed_is_valid_play(play, player, 
                                                                 table, 
                                                                 turn_history, 
                                                                 phase_status, 
                                                                 play_handcard, 
                                                                 discard_pile)
                        
                        # Check if addition of card to group is valid
                        if valid_addto_play4 is True:
                            break

            if valid_addto_play4 is True:
                playid = 4
                playcontent = addto_playcontent4[0]
            else:
                playid = 5
                playcontent = pile_pickup
            return playid, playcontent
        
        play_handcard = hand

        # Find details of cards in player's hand 
        query_list = query_list_build(play_handcard)
        qcard_naturals= list(n[0] for n in query_list if n[0][0] != 'A')

        # If player is the last one to play 
        if last_player == player:

            # If player picked card from deck or discard pile
            # And has not completed a phase yet
            if last_play_type in (1, 2) and player_turn_phase_completed is\
                False:
                
                # If there is less than 2 non-Wild cards 
                if len(qcard_naturals) < 2:
                    playid = 5
                    playcontent = pile_pickup

                # If there is more than 2 non-Wild cards    
                elif len(qcard_naturals) > 2: 
                    playid = 5
                    playcontent = qcard_naturals[-1]     

            # If player picked card from deck or discard pile
            # And has already completed a phase                       
            elif last_play_type in (1, 2) and player_turn_phase_completed is \
                True:
                playid, playcontent = play4_5(table, pile_pickup)

            elif last_play_type == 3:
                playid, playcontent = play4_5(table, pile_pickup)

            elif last_play_type == 4:
                playid = 5
                playcontent = pile_pickup      

    player_to_playid = playid
    player_to_playcontent = playcontent
    
    return player_to_playid, player_to_playcontent 
  
    
if __name__ == '__main__':
    # Example call to the function.
    print(phazed_play(1, [(None, []), (5, [['2C', '3H', '4D', 'AD', '6S', '7C',
      '8S', '9H', '0S', 'JS']]), (None, []), (None, [])], [(0, [(2, 'JS'),
      (5, 'JS')]), (1, [(2, 'JS'), (3, (5, [['2C', '3H', '4D', 'AD', '6S',
      '7C', '8S', '9H']])), (4, ('0S', (1, 0, 8))), (4, ('JS',
      (1, 0, 9)))])], [0, 5, 0, 0], ['5D'], '7H'))
