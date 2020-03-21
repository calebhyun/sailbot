import time
import py_qmc5883l
from time import sleep
sensor = py_qmc5883l.QMC5883L()
sensor.calibration = [[1.013535132361361, -0.008522647106776193, -1016.2116244340472],[-0.008522647106776138, 1.005366442807312, -1293.387118453363], [0.0, 0.0, 1.0]]
sensor.declination = 15.5
m = sensor.get_magnet()
while True:
	#m = sensor.get_magnet()
	print(sensor.get_bearing())
	print(time.time())
	#sleep(.5)