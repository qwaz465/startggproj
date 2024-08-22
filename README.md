# jake project
### 8/21
#### got elo to "work" but it is not very good. however this is the first instance of a technically finished product especially if i figure out the rate limiting thing. Exciting stuff. Also implemented sorting for elo
### 8/05
#### have not looked into rate limit yet, testing using smaller set for now until i fix it. however, i did add the np array data structure to hold both game and set counts with a dictionary that maps player name to index in matrix where matrix[0,1] retrieves sets/games player 0 has over player 1. seems to be working fine with tests.
### 7/30
#### seeing that im getting rate limited, will look in to that
### 7/29
#### added functionality to extract players from sets, which seems to work however getting sets from setIDs seems to be broken because i get the following error on set 81 out of 114 (first set of the 2nd tournament in my list): "Traceback (most recent call last):
  #### File "<stdin>", line 2, in <module>
  #### File "<stdin>", line 9, in getPlayersAndScore
  #### KeyError: 'data'
#### and i do not know why it is happening, will ask in startgg discord to see if i can get help, also getting weird json errors on occasion