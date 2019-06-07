from artiq.experiment import *

# This function is run on build()

def tasks_build(self):
	self.setattr_device("ttl9")

# This function is triggered when a command is run

def task_cmd(self, cmd):
	if cmd == "task1":
		print("[*] Running task1")
		task1(self)
	else:
		return False
	return True
	
@kernel
def task1(self):
	self.core.break_realtime()
	for i in range(30):
		with parallel:
			self.led0.pulse(2*ms)
			self.ttl9.pulse(4*ms)
		delay(30*ms)


# This function is triggered by the "help" command
def tasks_help():
	print("task1")
