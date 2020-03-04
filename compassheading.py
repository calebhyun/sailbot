import py_qmc5883l
from time import sleep
sensor = py_qmc5883l.QMC5883L()

while True:
	m = sensor.get_magnet()
	print(sensor.get_bearing())
	sleep(.5)
