# phazed

This is my submission for ***Assignment 2 of COMP10001 Foundations of Computing in Sem 1 2021***. The program involves an implementation of the game 'Phazed' which is a variant of Phase 10, which is in turn a variant of rummy.

## Overview

Phazed is a 4-player game that requires players to complete a series of “phases” by placing specific combinations of cards on the table. The game consists of several “hands,” with each player dealt 10 cards from a 104-card deck. 

During a hand, players take turns drawing cards from the deck or picking up the top card from the discard pile. Once a player has the necessary cards to complete a phase, they can place them on the table and add any remaining cards to any existing groups (either their own or those of other players). The hand ends when one of the following happens: (1) a player places all of their cards on the table; (2) the deck runs out; or (3) each player has played 50 times. 

At this point, players tally up penalty points based on the cards remaining in their hand. The game continues across multiple hands until either: (1) a player has completed all of their phases, in which case they win (or the player(s) with the lowest point score win, in the case of a tie); or (2) 20 hands have been completed, in which case the player(s) with the lowest point score win.

## Project Questions 

### Question 1

The function `phazed_group_type` takes a single argument, group, which is a list of 2-character strings representing a group of cards. Each string in the list represents a card with the value drawn from `234567890JQKA` followed by the suit drawn from `SHDC`. For example, `['2C', '2S', '2H']` represents a group of three cards, made up of the Two of Clubs, the Two of Spades, and the Two of Hearts.

The function returns a sorted list of integers indicating card combination types as specified below. If the `group` argument does not correspond to any valid card combination, the function returns an empty list.

1. A **set of three cards of the same value**:
The set may include Wilds, but must include at least two "natural" cards (i.e. non-Wild cards), which define the value. Note that the sequence of the cards is not significant for this group type.

2. A **set of seven cards of the same suit**:
The set may include Wilds, but must include at least two "natural" cards (i.e. non-Wild card), which define the suit. Note that the sequence of the cards is not significant for this group type.

3. A **set of four cards of the same value**:
The set may include Wilds, but must include at least two "natural" cards (i.e. non-Wild cards), which define the value. Note that the sequence of the cards is not significant for this group type.

4. A **run of eight cards**:
The card combination may include Wilds, but must include at least two "natural" cards (i.e. non-Wild cards). Note that the sequence of the cards is significant for this group type.

5. A **run of four cards of the same colour**:
The card combination may include Wilds, but must include at least two "natural" cards (i.e. non-Wild cards), which define the colour. Note that the sequence of the cards is significant for this group type.

6. A **34-accumulation of cards**:
An accumulation of cards totaling 34 in value. Note that for accumulations, Aces do not function as Wilds and simply take the value 1.

7. A **34-accumulation of cards of the same colour**:
An accumulation of cards of the same colour totaling 34 in value. Note that for accumulations, Aces do not function as Wilds and simply take the value 1.

Example calls to the function are:

```powershell
>>> phazed_group_type(['2C', '2C', '4C', 'KC', '9C', 'AH', 'JC'])
[2]
>>> phazed_group_type(['KS', '0C', '8C', '3S'])
[6, 7]
>>> phazed_group_type(['2C', '2C', '4C', 'KC', '9C', 'AS', '3C'])
[2, 6, 7]
>>> phazed_group_type(['4H', '5D', '7C', 'AC'])
[]
```

### Question 2

The `phazed_phase_type` function takes a single argument, phase, which is a combination of card groups represented as a list of lists of cards. Each card is a 2-character string with the value (drawn from `234567890JQKA`) followed by the suit (drawn from `SHDC`). The function returns a sorted list composed of integers, each integer indicating the type(s) of the combinations of card groups contained in phase, as described below. If phase is an invalid combination, the function returns an empty list.

1. Two sets of **three cards of the same value**
2. One set of **7 cards of the same suit**
3. Two **34-accumulations**
4. Two sets of **four cards of the same value**
5. One **run of eight cards**
6. Two 34-accumulations of the **same colour**
7. A run of **four cards of the same colour** and a set of **four cards of the same value**

Note that each set may include Wilds, but must include at least two *natural" cards (i.e. non-Wild cards), which define the value/suit/colour. Note also that the sequence of the cards is significant for some group types, and the sequence of the two groups is significant for group type 7.

Example calls to the function are:

```powershell
>>> phazed_phase_type([['2C', 'KH', 'QS', '7H'], ['3H', '7S', '0D', 'KD', 'AD']])
[3]
>>> phazed_phase_type([['2C', 'KC', 'QS', '7C'], ['3H', '7H', '0D', 'KD', 'AD']])
[3, 6]
>>> phazed_phase_type([['4H', '5D', '7C', 'AC'], ['AC', 'AS', 'AS']])
[]
```

### Question 3

The function `phazed_is_valid_play` checks whether the given play is valid based on the current state of the hand. The function takes the arguments `play`, `player_id`, `table`, `turn_history`, `phase_status`, `hand`, and `discard`, and returns `True` if the play is valid and `False` otherwise.

#### Arguments

- `play`: A 2-tuple indicating the play type and the content of the play.
* `player_id`: An integer between 0 and 3 inclusive, indicating the ID of the player attempting the play.
+ `table`: A 4-element list of phase plays for each of Players 0—3, respectively.
- `turn_history`: A list of all turns in the hand to date, in sequence of play.
* `phase_status`: A 4-element list indicating the phases that each of Players 0—3, respectively, have achieved in the game.
+ `hand`: The list of cards that the current player holds in their hand.
- `discard`: The top card of the discard stack or None.

#### Returns
`True` if play is valid relative to the current hand state, and `False` otherwise.

#### Conditions for Valid Play

1. If the play is a ***pick-up play*** from the deck or discard pile, the player must not have already picked up a card in their turn.
2. If the play is a ***phase play***, the player must have the specified phase in their hand and the phase played must be valid.
3. If the play is a ***single card play***, the player must have the specified card in their hand and the position they are attempting to play it must be valid.
4. If the play is a ***discard play***, the player must have the specified card in their hand.

Example calls to the function are:

```powershell
>>> phazed_is_valid_play((3, (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']])), 0, [(None, []), (None, []), (None, []), (None, [])], [(0, [(2, 'JS')])], [0, 0, 0, 0], ['AS', '2S', '2S', '2C', '5S', '5S', '7S', '8S', '9S', '0S', 'JS'], None)
True
>>> phazed_is_valid_play((4, ('KC', (1, 0, 0))), 1, [(None, []), (2, [['2S', '2S', 'AS', '5S', '5S', '7S', 'JS']]), (None, []), (None, [])], [(0, [(2, 'JS'), (5, 'JS')]), (1, [(1, 'XX'), (3, (2, [['2S', '2S', 'AS', '5S', '5S', '7S', 'JS']]))])], [0, 2, 0, 0], ['5D', '0S', 'JS', 'KC'], 'JS')
False
>>> phazed_is_valid_play((5, 'JS'), 1, [(None, []), (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']]), (None, []), (None, [])], [(0, [(2, 'JS'), (5, 'JS')]), (1, [(1, 'XX'), (3, (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']]))])], [0, 1, 0, 0], ['AD', '8S', '9S', '0S', 'JS'], 'JS')
True
```

### Question 4

The `phazed_score` function takes a single argument `hand`, which is a list of cards that the current player holds in their hand. Each card in the hand is represented as a 2-element string.

The function returns the score for the `hand` (assuming the game has ended, and the player is left with the cards in `hand`) as a non-negative integer.

Example calls to the function are:

```powershell
>>> phazed_score(['9D', '9S', '9D', '0D', '0S', '0D'])
57
>>> phazed_score(['2D', '9S', 'AD', '0D'])
46
>>> phazed_score([])
0
```

### Question 5

The function `phazed_play` takes the following arguments:

- `player_id`: An integer between 0 and 3 indicating the ID of the player attempting the play.
* `table`: A 4-element list of phase plays for each of Players 0—3, respectively.
+ `turn_history`: A list of all turns in the hand to date, in sequence of play.
- `phase_status`: A 4-element list indicating the phases that each of Players 0—3, respectively, have achieved in the game.
* `hand`: The list of cards that the current player holds in their hand.
+ `discard`: The top card of the discard stack.

The function returns a *2-tuple* describing the single play your player wishes to make, made up of a *play ID* and associated *play content*:

1. Pick up a card from the top of the deck at the start of the player's turn. In this case, the play content is set to None (i.e. `(1, None)`).
2. Pick up a card from the top of the discard pile at the start of the player's turn, with the play content taking the value of discard (e.g. `(2, '2C')`).
3. Place a phase to the table from the player's hand, with the play type being the 2-tuple of the phase ID (see Q2) and phase (e.g. `(3, (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']]))`).
4. Place a single card from the player's hand to a phase on the table, with the play type being a 2-tuple made up of the card the player is attempting to play, and the position they are attempting to play it in.
5. Discard a single card from the player's hand, and in doing so, end the turn (e.g. `(5, 'JS')` indicates that a Jack of Spades is to be discarded).

An example call to the function is:

```powershell
>>> print(phazed_play(1, [(None, []), (5, [['2C', '3H', '4D', 'AD', '6S', '7C', '8S', '9H', '0S', 'JS']]), (None, []), (None, [])], [(0, [(2, 'JS'), (5, 'JS')]), (1, [(2, 'JS'), (3, (5, [['2C', '3H', '4D', 'AD', '6S', '7C', '8S', '9H']])), (4, ('0S', (1, 0, 8))), (4, ('JS', (1, 0, 9)))])], [0, 5, 0, 0], ['5D'], None))
(5, '5D')
```

#### Question 6


