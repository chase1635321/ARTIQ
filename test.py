from artiq.experiment import *

class Tutorial(EnvExperiment):
	def build(self):
		self.setattr_device("core")
		self.setattr_device("ttl0")
		self.setattr_device("ttl0") # ?
		self.setattr_device("ttl9")
		#for i in range(8):
		#	self.setattr_device("suservo0_ch{}".format(i))

	@kernel
	def run(self):
		self.core.reset()
		self.ttl0.output() # ?
		for i in range(30):
			delay(30*ms)
			self.ttl0.pulse(30*ms) # ?
			self.ttl9.pulse(30*ms)
