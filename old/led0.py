from artiq.experiment import *
import time


class LED(EnvExperiment):
	def build(self):
		self.setattr_device("core")
		self.setattr_device("led0")

	@kernel
	def run(self):
		self.core.reset()
		self.core.break_realtime()
		i = 0
		while True:
			self.led0.pulse(.1*s)
			delay(.1*s)
			i = i+1
