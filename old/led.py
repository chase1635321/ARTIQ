from artiq.experiment import *
import time


class LED(EnvExperiment):
	def build(self):
		self.setattr_device("core")
		self.setattr_device("ttl0")

	@kernel
	def run(self):
		self.core.reset()
		self.core.break_realtime()
		i = 0
		while True:
			self.ttl0.pulse(2*ms)
			delay(2*ms)
			i = i+1

