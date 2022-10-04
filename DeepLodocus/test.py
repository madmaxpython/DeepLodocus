import pandas as pd

class animal:
    df = pd.DataFrame({'animal': [], 'me1': [], 'me2': []})
    def __init__(self, name, bana):
        self.name = name
        self.bana = bana
    def analyse(self):
        measurement = [self.name]
        measurement.append(self.bana*3)
        measurement.append(self.bana * 9)
        animal.df.loc[len(animal.df)] = measurement

class mouse

ani1 = animal('1TL', 3)
ani1.analyse()
ani2 = animal('2TR', 4)
ani2.analyse()

print(animal.df)

