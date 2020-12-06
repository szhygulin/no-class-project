indices = [96, 1587, 554, 5115, 2022, 390, 14240, 6966, 2174, 6403]
counter = 0
with open('network.txt', 'r') as f:
    for line in f:
        x = line.split('\t')
        if counter in indices:
            print(f"{counter}, {x[0]}")
        counter += 1
