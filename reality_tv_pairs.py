import csv
import guess_checker

weeks = 8
n = 2
suspected_pairs = []
confirmed_pairs = []

# Read the CSV into an array of arrays, one for each week.
# Each week's array holds two values: an array of couples (represented by
# tuples) and the number of "correct" couples for that week.
all_lists_of_couples_by_week = [[[], 0] for i in range(weeks)]
season = "season%d.csv" %(n)
with open(season) as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  for i, row in enumerate(reader):
    if row[0] == "Correct Matches":
      for j in range(1,weeks+1):
        all_lists_of_couples_by_week[j-1][1] = int(row[j])
    else:
      for j in range(1,weeks+1):
        all_lists_of_couples_by_week[j-1][0].append((row[0], row[j]))

# Add a third number to each list, representing the total number of possible 
# matches for that week (this will be reduced by 1 for every confirmed couple
# that appears in that week's correct couple count).
for week_list in all_lists_of_couples_by_week:
  week_list.append(len(week_list[0]))

# Initialize some useful variables for later
all_confirmed_pairs = confirmed_pairs + suspected_pairs
all_couples_lists = [list_of_couples[0] for list_of_couples in all_lists_of_couples_by_week]
all_couples = [item for sublist in all_couples_lists for item in sublist]
all_people = set([item for sublist in all_couples for item in sublist])
couples_dictionary = {}

# Remove couples that are confirmed from consideration by our algorithm. We
# remove 1 from the score of confirmed couples AND from the total possible number
# of couples for that week.
for week in all_lists_of_couples_by_week:
  for couple in week[0]:
    if couple in all_confirmed_pairs:
      week[1] -= 1
      week[2] -= 1

# For each couple not in a confirmed pair, give them a score calculated by
# subtracting the possible couple count from the correct couple count divided by 2.
# This means that for a week where half the couples (5) are correct, those couples 
# get +0. If 4 couples are correct, each couple gets -1, if 6 couples are correct
# each couple gets +1, etc. This scoring system rewards couples that were matched during 
# successful weeks while penalizing couples matched during unsuccessful weeks.
for week in all_lists_of_couples_by_week:
  for couple in week[0]:
    if couple not in all_confirmed_pairs:
      if couple in couples_dictionary:
        couples_dictionary[couple] += (week[1] - week[2] / 2)
      else:
        couples_dictionary[couple] = (week[1] - week[2] / 2)

# More variable initialization for sorting
sorted_couples_with_value = sorted(couples_dictionary.items(), key = lambda x: -x[1])
sorted_couples = [couple[0] for couple in sorted_couples_with_value]
people_in_pairs = [p for p in all_confirmed_pairs]
all_people = [p for p in all_people if p not in people_in_pairs]
all_speculative_pairs = []

# After scoring all the pairs, greedily choose the best pairs until no more 
# pairs remain.
for couple in sorted_couples:
  if (couple[0] in all_people) and (couple[1] in all_people):
    all_speculative_pairs.append(couple)
    all_people.remove(couple[0])
    all_people.remove(couple[1])

result = all_speculative_pairs + all_confirmed_pairs

guess_checker.check(result, n)