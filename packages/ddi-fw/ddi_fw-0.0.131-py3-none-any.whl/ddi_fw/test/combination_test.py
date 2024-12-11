import itertools

l = ['e1','e2','e3','e4','e5']
all_combinations = []
for i in range(2, len(l) + 1):
    all_combinations.extend(list(itertools.combinations(l, i)))

print(all_combinations)

for combination in all_combinations:
    combination_descriptor = '-'.join(combination)
    print(combination_descriptor)