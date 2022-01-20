
def check(result, season):
  actual = [
    [('Adam', 'Shanley'), ('Chris S.', 'Jacy'), ('Chris T.', 'Paige'), ('Dillan', 'Coleysia'), ('Dre', 'Simone'), ('Ethan', 'Amber'), ('John', 'Ashleigh'), ('Joey', 'Brittany'), ('Ryan', 'Jessica'), ('Wes', 'Kayla')],
    [('Alex', 'Jasmine'), ('Anthony', 'Alexandria'), ('Brandon', 'Briana'), ('Curtis', 'Shelby'), ('Dario', 'Ashley'), ('Garland', 'Jessica'), ('John', 'Jenni'), ('Layton', 'Christina'), ('Layton', 'Tyler'), ('Nathan', 'Ellie'), ('Pratt', 'Paris')]
  ]
  tot = 0
  correct_guesses = []
  for p in result:
    if p in actual[season - 1]:
      tot += 1
      correct_guesses.append(p)
  print("\n Correct Guesses: %s, %s" %(tot, correct_guesses))

