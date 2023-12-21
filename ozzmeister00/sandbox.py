
differences = [[0, 3, 6, 9, 12, 15]]

# keep making a new list of differences between values as long as 
# some of the differences are not zero
steps = 0
while not all([i == 0 for i in differences[-1]]):
    newDifference = []
    for i, value in enumerate(differences[-1][:-1]):
        newDifference.append(differences[-1][i+1] - value)
    differences.append(newDifference)

print(differences)