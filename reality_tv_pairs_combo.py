import math
import itertools
import sys
import csv
from itertools import permutations
import guess_checker

weeks = 6
n = 2
suspected_pairs = []
confirmed_pairs = []

# Read the CSV into an array of arrays, one for each week.
# Each week's array holds two values: an array of couples (represented by
# tuples) and the number of "correct" couples for that week.
# Additionally, store the members into list_1 and list_2 for permuting later.
list_1 = []
list_2 = []
all_lists_of_couples_by_week = [[[], 0] for i in range(weeks)]
season = "season%d.csv" %(n)
with open(season) as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  for i, row in enumerate(reader):
    if row[0] == "Correct Matches":
      for j in range(1,weeks+1):
        all_lists_of_couples_by_week[j-1][1] = int(row[j])
    else:
      list_1.append(row[0])
      list_2.append(row[1])
      for j in range(1,weeks+1):
        all_lists_of_couples_by_week[j-1][0].append((row[0], row[j]))

all_confirmed_pairs = confirmed_pairs + suspected_pairs

def intersection(lst1, lst2):
  return list(set(lst1) & (set(lst2)))

# Exclude couples in confirmed pairs 
for couple in all_confirmed_pairs:
  if couple[0] in list_1:
    list_1.remove(couple[0])
  if couple[1] in list_2:
    list_2.remove(couple[1])

for week in all_lists_of_couples_by_week:
  for couple in week[0][:]:
    if couple in all_confirmed_pairs:
      week[1] -= 1
      week[0].remove(couple)

# Create empty list to store the combinations
unique_combinations = []
 
# Getting all permutations of list_1 with length of list_2
permut = itertools.permutations(list_2, len(list_2))

# Initialize some variables
possible_combinations = []
attempts = 0
total_attempts = math.factorial(len(list_2))

# Iterate over all combinations
for comb in permut:
  attempts += 1.0
  if (attempts % 10000 == 0):
    i = (attempts / total_attempts) * 100
    sys.stdout.write('[%d%%] complete\r'%i )
    sys.stdout.flush()
  zipped = zip(list_1, comb)
  works = True
  for week in all_lists_of_couples_by_week:
    if len(intersection(week[0], zipped)) != week[1]:
      works = False
      break
  if works == True:
    possible_combinations.append(zipped)

print("Found %s possible combinations" %(len(possible_combinations)))
index = 1
actual_pairs = possible_combinations[0]
pair_count = {}
for pc in possible_combinations:
  # print("%s." %(index))
  # print(pc)
  actual_pairs = intersection(actual_pairs, pc)
  index += 1
print("Confirmed pairs:")
print(actual_pairs + confirmed_pairs)

# Caculate the number of times each pair appears across all possible combinations
for pc in possible_combinations:
  for pair in pc:
    if pair in pair_count:
      pair_count[pair] += 1
    else:
      pair_count[pair] = 1

# Choose the possible combination that contains the most commonly seen pairs
best = 0
result = None
for pc in possible_combinations:
  score = 0
  for p in pc:
    score += pair_count[p]
  if score > best:
    result = pc


print("Best guess:")
print(possible_combinations[0])
result = possible_combinations[0] + all_confirmed_pairs
guess_checker.check(result, n)
