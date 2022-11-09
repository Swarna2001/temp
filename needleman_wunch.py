# Input sequences
sequence_2 = "TCCGTCAAGGCCCGACTTTCATCGCGGCCCATTCCATGCGCGGACCATACCGTCCTAATTCTTCGGTTATGTTTCCGATGTAGGAGTGAGCCTACCTGCC"
sequence_1 = "TTTGCGTCTTGATACCAATGAAAAACCTATGCACTTTGTACAGGGTGCCATCGGGTTTCTGAACTCTCAGATAGTGGGGATCCCGGGTAAAGACCTATAT"

# Scores for match, mismatch and gap penalty
match = 1
mismatch = -1
gap = -1

print("-" * 30)
print("Sequence 1:")
print("-" * 30)
print(sequence_1)

print("-" * 30)
print("Sequence 2:")
print("-" * 30)
print(sequence_2)

# Appending a start '_' for computation
sequence_1 = '-'+sequence_1
sequence_2 = '-'+sequence_2

# The grid variable is the matrix that stores all the computations
grid = [['_' for _ in range(len(sequence_2))] for _ in range(len(sequence_1))]

# Helper function to print the grid
def display_grid():
  print('',end='\t')
  for w in sequence_2:
    print(w, end='\t')
  print('')
  for i,w in enumerate(sequence_1):
    print(w, end='\t')
    for j,_ in enumerate(grid):
      print(grid[i][j], end='\t')
    print('')

# Given two values a and b, this function identfies if they are a match or not
def match_check(a,b):
  if a == b:
    return match
  return mismatch

# Initializing the '_' entries of the grid as 0
step = 0

for i in range(len(grid[0])):
  grid[0][i] = step
  step += gap

step = 0

for i in range(len(grid)):
  grid[i][0] = step
  step += gap


# Moving across every entry in the grid, in row-wise fashion
# We compute the scores for match, mismatch and gap for each cell
# Then, the maximum score is taken and filled in the grid
for i in range(1,len(sequence_1)):
  
  for j in range(1,len(sequence_2)):
    match_score = grid[i-1][j-1] + match_check(sequence_1[i], sequence_2[j])
    delete_score = grid[i-1][j] + gap
    insert_score = grid[i][j-1] + gap
    grid[i][j] = max(match_score, insert_score, delete_score) 
  

# Backtracking to get the aligned sequences
# While backtracking, we find the parent cell that gave us the maximum score and store it
alignment_A = ""
alignment_B = ""
i = len(sequence_1)-1
j = len(sequence_2)-1
while (i > 0 or j > 0):
  if (i > 0 and j > 0 and grid[i][j] == grid[i-1][j-1] + match_check(sequence_1[i], sequence_2[j])):
    alignment_A = sequence_1[i] + alignment_A
    alignment_B = sequence_2[j] + alignment_B
    i = i - 1
    j = j - 1
  elif i > 0 and grid[i][j] == grid[i-1][j] + gap:
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
