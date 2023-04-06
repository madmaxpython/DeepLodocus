from main import Experiment, Mouse

exp = Experiment('/Users/maximeteixeira/Desktop/Datas')


exp.load_animal(Mouse)


exp.area_definition(calibration=True, zone_name=['lines', 'dots'])

exp.analyze(distance = True)

#8076.913557