sequence_2 = "TCCGTCAAGGCCCGACTTTCATCGCGGCCCATTCCATGCGCGGACCATACCGTCCTAATTCTTCGGTTATGTTTCCGATGTAGGAGTGAGCCTACCTGCC"
sequence_1 = "TTTGCGTCTTGATACCAATGAAAAACCTATGCACTTTGTACAGGGTGCCATCGGGTTTCTGAACTCTCAGATAGTGGGGATCCCGGGTAAAGACCTATAT"
match = 3
mismatch = -3
gap = 2

print("-" * 30)
print("Sequence 1:")
print("-" * 30)
print(sequence_1)

print("-" * 30)
print("Sequence 2:")
print("-" * 30)
print(sequence_2)

sequence_1 = '-'+sequence_1
sequence_2 = '-'+sequence_2

grid = [['_' for _ in range(len(sequence_2))] for _ in range(len(sequence_1))]


def print_grid():
  print('',end='\t')
  for w in sequence_2:
    print(w, end='\t')
  print('')
  for i,w in enumerate(sequence_1):
    print(w, end='\t')
    for j,_ in enumerate(sequence_2):
      print(grid[i][j], end='\t')
    print('')

def match_check(a,b):
  if a == b:
    return match
  return mismatch

step = 0

for i in range(len(grid[0])):
  grid[0][i] = step

for i in range(len(grid)):
  grid[i][0] = step

for i in range(1,len(sequence_1)):
  for j in range(1,len(sequence_2)):
    c_match = grid[i-1][j-1] + match_check(sequence_1[i], sequence_2[j])
    delete = grid[i-1][j] + gap
    insert = grid[i][j-1] + gap
    grid[i][j] = max(c_match, insert, delete, 0) 


alignment_A = ""
alignment_B = ""
max_i = len(sequence_1)-1
max_j = len(sequence_2)-1
max_value = float('-inf')

for i in range(len(grid)):
    a_row = grid[i]
    cur_max_value = max(a_row)
    if cur_max_value > max_value:
      j = a_row.index(cur_max_value)
      max_i = i
      max_j = j
      max_value = cur_max_value

i,j = max_i, max_j

while (i > 0 and j > 0 and grid[i][j] > 0):
  if (i > 0 and j > 0 and grid[i][j] == grid[i-1][j-1] + match_check(sequence_1[i], sequence_2[j])):
    alignment_A = sequence_1[i] + alignment_A
    alignment_B = sequence_2[j] + alignment_B
    i = i - 1
    j = j - 1
  elif i > 0 and grid[i][j] == grid[i-1][j] - gap:
    alignment_A = sequence_1[i] + alignment_A
    alignment_B = "-" + alignment_B
    i = i - 1
  else:
    alignment_A = "-" + alignment_A
    alignment_B = sequence_2[j] + alignment_B
    j = j - 1

res = 0
for w1,w2 in zip(alignment_A, alignment_B):
  res += match_check(w1, w2)

print("-" * 30)
print("Final alignment sequences:")
print("-" * 30)
print(alignment_B)
print(alignment_A)
print(f"Score is {res}")
