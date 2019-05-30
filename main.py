from artiq.experiment import *
import os
from tabulate import tabulate
import time

class LED(EnvExperiment):

	def main(self):
		while True:
			print(">> ", end="")
			cmd = input()

			if "procedure" in cmd:
				if cmd == "procedure":
					print("procedure {file.txt}")
				else:
					print("[+] Loading procedure " + cmd.split(" ")[1])
					with open(cmd.split(" ")[1]) as f:
						for line in f.readlines():
							print("	> " + line.strip("\n"))
					print("[?] Are you sure you want to continue? (y/n): ", end="")
					if input() == "n":
						pass
					else:
						with open(cmd.split(" ")[1]) as f:
							self.message("Starting procedure")
							for line in f.readlines():
								if "delay" in line:
									print("[*] Delaying for " + line.split(" ")[1].strip("\n") + " seconds")
									time.sleep(float(line.split(" ")[1]))
								else:
									print("[*] Executing: " + line)
									self.cmd(line.strip("\n"))
							print("[-] Finished procedure")
			else:
				self.cmd(cmd)


	def cmd(self, cmd):
		if "test" in cmd:
			if cmd == "test":
				print("test {leds|ttl_outs|ttl_ins}")
			else:
				self.test(cmd[5:], self.parse_args(cmd[5:]))
		elif "set" in cmd:
			if cmd == "set" or len(cmd.split(" ")) != 3:
				print("set {leds|ttl_outs|ttl_ins} {on|off}")
			else:
				self.set(cmd.split(" ")[1], self.parse_args(cmd.split(" ")[1]), cmd.split(" ")[2])
		elif "pulse" in cmd:
			if cmd == "pulse":
				print("pulse {device|ttl_outs|leds} {count in ms} {length in ms}")
			else:
				self.pulse(cmd, self.parse_args(cmd.split(" ")[1]))
		elif "listen" in cmd:
			if cmd == "listen":
				print("listen {ttlX}")
			else:
				self.listen(cmd[7:], self.parse_args(cmd[7:]))
		elif "list" in cmd:
			if "leds" in cmd or "all" in cmd:
				print(tabulate(self.leds, headers=["Name", "Device"], tablefmt="orgtbl"))
				print("")
			if "outs" in cmd or "all" in cmd:
				print(tabulate(self.ttl_outs, headers=["Name", "Device"], tablefmt="orgtbl"))
				print("")
			if "ins" in cmd or "all" in cmd:
				print(tabulate(self.ttl_ins, headers=["Name", "Device"], tablefmt="orgtbl"))
				print("")
			if cmd == "list":
				print("Syntax: list {all|leds|ttl_outs|ttl_ins}")
		elif cmd == "help":
			self.print_help()
		elif cmd == "clear":
			os.system("clear")
		elif cmd == "exit":
			exit()
		else:
			print("Unknown command")

# ==================== Commands ========================

	def pulse(self, cmd, devices):
		if devices == None:
			print("Invalid device")
		else:
			arr = cmd.split(" ")
			for name, dev in devices:
				print("[*] Sending " + str(arr[2]) + " pulses of length " + str(arr[3]) + " ms to device " + name)
				self.pulse_device(dev, int(arr[2]), int(arr[3]))

	def listen(self, cmd, devices): # NOT DONE
		name, dev = devices[0]
		print("Listening on device " + name)
		for i in range(10):
			self.listen_dev(dev)
			print("Gate changed!!!")

	def read(self, cmd, devices): # NOT DONE
		if devices == None:
			print("Invalid device")
		else:
			print("[+] Reading " + str(len(devices)) + " voltages")
			for name, dev in devices:
				val = 0
				val = read_dev(dev)
				print("[*] Voltage of " + name + " is " + str(val))

	def set(self, cmd, devices, state):
		if devices == None:
			print("Invalid device")
		else:
			print("[+] Setting " + str(len(devices)) + " devices")
			if state == "on" or state == "off":
				for name,  dev in devices:
					print("[*] Setting " + name + " to state " + state)
					self.set_device_onoff(dev, state == "on")
			elif state == "input" or state == "output":
				print("Found output or input")
				for name, dev in devices:
					print("[*] Setting " + name + " to an " + state)
					try:
						self.set_device_inout(dev, state == "input")
					except:
						print("[!] Cannot set device")
				self.build()
				

	def test(self, cmd, devices):
		if devices == None:
			print("Invalid device")
		else:
			print("[+] Starting test on " + str(len(devices)) + " devices")
			for name, dev in devices:
				print("[*] Flashing: {}".format(name))
				self.test_device(dev)

# ==================== Kernel ========================

	@kernel
	def listen_dev(self, dev): # NOT DONE
		self.core.break_realtime()
		return dev.gate_both(1*ms)

	@kernel
	def read_dev(self, dev): # NOT DONE
		self.core.break_realtime()

	@kernel
	def set_device_onoff(self, dev, to_on):
		self.core.break_realtime()
		if to_on:
			dev.on()
		else:
			dev.off()

	@kernel
	def set_device_inout(self, dev, to_input):
		self.core.break_realtime()
		if to_input:
			dev.input()
		else:
			dev.output()

	@kernel
	def test_device(self, dev):
		self.core.break_realtime()
		for i in range(20):
			dev.pulse(10*ms)
			delay(50*ms)

	@kernel
	def pulse_device(self, dev, count, length):
		self.core.break_realtime()
		for i in range(count):
			dev.pulse(length*ms)
			delay(length*ms)

# ==================== Utility ========================

	def parse_args(self, cmd):
		if cmd == "leds":
			return self.leds
		elif cmd == "ttl_outs":
			return self.ttl_outs
		elif cmd == "ttl_ins":
			return self.ttl_ins
		else:
			for name, dev in self.leds + self.ttl_outs + self.ttl_ins:
				if cmd == name:
					return [(name, dev)]
			return None

	def print_help(self):
		print("List devices: list {all|leds|ttl_outs|ttl_ins|device}")
		print("Test devices: test {leds|ttl_outs|device}")
		print("Set devices: set {leds|ttl_outs|device} {on|off|input|output}")
		print("pulse {device|ttl_outs|leds} {count in ms} {length in ms}")
		print("Listen: listen {device}")
		print("Other: help, clear, exit")

	def build(self):
		self.setattr_device("core")

		self.leds = dict()
		self.ttl_outs = dict()
		self.ttl_ins = dict()

		dbb = self.get_device_db()
		for name, desc in dbb.items():
			if isinstance(desc, dict) and desc["type"] == "local":
				module, cls = desc["module"], desc["class"]
				if (module, cls) == ("artiq.coredevice.ttl", "TTLOut"):
					dev = self.get_device(name)
					if "led" in name:
						self.leds[name] = dev
					else:
						self.ttl_outs[name] = dev
				elif (module, cls) == ("artiq.coredevice.ttl", "TTLInOut"):
					self.ttl_ins[name] = self.get_device(name)

		self.leds = sorted(self.leds.items(), key=lambda x: x[1].channel)
		self.ttl_outs = sorted(self.ttl_outs.items(), key=lambda x: x[1].channel)
		self.ttl_ins = sorted(self.ttl_ins.items(), key=lambda x: x[1].channel)
		print("[!] Built database")


	def message(self, s):
		print("*"*30 + " " + s + " " + "*"*30)
	
	def run(self):
		try:
			self.core.reset()
			self.main()
		except RTIOUnderflow:
			print("[!] RTIOUnderflow")
			exit()
		except KeyboardInterrupt:
			print("\n[!] Keyboard Interrupt")
			exit()
