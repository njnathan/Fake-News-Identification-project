import random

with open('inputs/UseCase15Test.csv', 'r') as r, open('inputs/UseCase15TestShuffled.csv', 'w') as w:
    data = r.readlines()
    header, rows = data[0], data[1:]
    random.shuffle(rows)
    rows = '\n'.join([row.strip() for row in rows])
    w.write(header + rows)

with open('inputs/UseCase15Train.csv', 'r') as r, open('inputs/UseCase15TrainShuffled.csv', 'w') as w:
    data = r.readlines()
    header, rows = data[0], data[1:]
    random.shuffle(rows)
    rows = '\n'.join([row.strip() for row in rows])
    w.write(header + rows)