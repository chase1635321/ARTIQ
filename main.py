# Problems:
# After setting input/output, on/off doesn't work (Don't rebuild database???)
# led1 seems to be broken
# Comment and organize code
# DMA pulses (getting started docs)
# Build tcpdump parser
# Organize multiple folders
# Expand help menu

from artiq.experiment import *
import os
from tabulate import tabulate
import time
from tasks import *

class LED(EnvExperiment):
	
	def main(self):
		os.system("clear")
		print("[*] Loaded devices")
		self.get_modules()
		print("[*] Loaded tasks")
		print("[*] Type help for a help menu")

		while True:
			print(">> ", end="")
			cmd = input()

			if "run" in cmd:
				if cmd == "run":
					print("run {file.txt}")
				else:
					#try:
					#	with open(cmd.split(" ")[1]) as f:
					#		print("[+] Loaded module " + cmd.split(" ")[1])
					#		for line in f.readlines():
					#			print(" > " + line.strip("\n"))
					#	print("[?] Run this module? (y/n): ", end="")
					#	if input() == "n":
					#		pass
					#except:
					#	print("[!] File not found")
					#else:
						with open("modules/" + cmd.split(" ")[1]) as f:
							self.message("Starting " + cmd.split(" ")[1])
							for line in f.readlines():
								if "delay" in line:
									print("[*] Delaying for " + line.split(" ")[1].strip("\n") + " seconds")
									time.sleep(float(line.split(" ")[1]))
								elif "#" in line or line.strip("\n") == "":
									pass
								elif "pause" in line:
									print("[!] Pausing... (Press enter to continue)")
									input()
								else:
									#print("[*] Executing: " + line)
									self.cmd(line.strip("\n"))
							print("[-] Finished module")
			else:
				self.cmd(cmd)


# ==================== Command Parser ========================

	def cmd(self, cmd):
		if "test " in cmd:
			if cmd == "test":
				print("test {leds|ttl_outs|ttl_ins}")
			else:
				self.test(cmd[5:], self.parse_args(cmd[5:]))
		elif "synch" in cmd:
			temp = ""
			arr = []
			print("Enter multiple commands. To execute, type run, else type exit")
			while temp != "run" and temp != "exit":
				print("	>> ", end="")
				temp = input()
				arr.append(temp)
			arr.pop()
			print("Tasks: " + str(arr))
			if "run" in temp:
				for i in arr:
					self.cmd(i)
		elif "log" in cmd:
			print("[*] Printing log. Filtered out new connections, resetting RTIO, and idle kernel messages\n")
			os.system("artiq_coremgmt log | grep -v \"new connection\" | grep -v \"resetting\" | grep -v \"idle kernel\"")
		elif "system" in cmd:
			os.system(cmd[7:])
		elif "set" in cmd:
			if cmd == "set" or len(cmd.split(" ")) != 3:
				print("set {leds|ttl_outs|ttl_ins|device} {on|off}")
			else:
				self.set(cmd.split(" ")[1], self.parse_args(cmd.split(" ")[1]), cmd.split(" ")[2])
		elif "pulse" in cmd:
			if cmd == "pulse":
				print("pulse {device|ttl_outs|leds} {count in ms} {length in ms}")
			else:
				self.pulse(cmd, self.parse_args(cmd.split(" ")[1]))
		elif "test_input" in cmd:
			if cmd == "test_input":
				print("test_input {ttlX}")
			else:
				self.test_inputs(cmd[11:], self.parse_args(cmd[11:]), self.parse_args("ttl9"))
		elif "listen" in cmd:
			if cmd == "listen":
				print("listen {ttlX}")
			else:
				self.listen(cmd[7:], self.parse_args(cmd[7:]), self.parse_args("ttl9"))
		elif "list" in cmd:
			if "modules" in cmd:
				self.get_modules()
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
		elif cmd == "exit" or cmd == "q":
			exit()
		elif task_cmd(self, cmd):
			pass
		else:
			print("[!] Unknown command")

# ==================== Commands ========================

	def pulse(self, cmd, devices):
		if devices == None:
			print("Invalid device")
		else:
			#print("[+] Gathered " + str(len(devices)) + " devices")
			arr = cmd.split(" ")
			for name, dev in devices:
				print("[*] Sending " + str(arr[2]) + " pulses of length " + str(arr[3]) + " ms to device " + name)
				self.pulse_device(dev, int(arr[2]), int(arr[3]))


	def read(self, cmd, devices): # NOT DONE
		if devices == None:
			print("[!] Invalid device")
		else:
			print("[+] Gathered " + str(len(devices)) + " devices")
			for name, dev in devices:
				val = 0
				val = read_dev(dev)
				print("[*] Voltage of " + name + " is " + str(val))

	def set(self, cmd, devices, state):
		if devices == None:
			print("[!] Invalid device")
		else:
			#print("[+] Gathered " + str(len(devices)) + " devices")
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
			else:
				print("[!] Invalid state")
				

	def test(self, cmd, devices):
		if devices == None:
			print("[!] Invalid device")
		else:
			print("[+] Gathered " + str(len(devices)) + " devices")
			for name, dev in devices:
				print("[*] Flashing: {}".format(name))
				self.test_device(dev)

	def test_inputs(self, cmd, devices, output):
		outname, outdev = output[0]
		for name, dev in devices:
			print("[*] Listening on " + name + " while pulsing on " + outname)
			print("[!] Pausing... (Press enter when ready)", end='')
			input()
			print("[*] Input success: " + str(self.test_input(dev, outdev)))
			
	def listen(self, cmd, devices, output): # NOT DONE
		if devices == None or output == None:
			print("[!] Invalid device")
		else:
			print("[+] Gathered " + str(len(devices)) + " devices")
			for name, dev in devices:
				outname, outdev = output[0]
				print("[*] Listening on device " + name)
				#print("[*] Returned: " + str(self.listen_dev(dev, outdev)))
				temp = self.listen_dev(dev, outdev)
				if temp == 0:
					print("[!] Timed out")
				else:
					print("[*] Input detected")

# ==================== Kernel ========================

	@kernel
	def test_input(self, ttl_in, ttl_out):
		n = 42
		self.core.break_realtime()
		with parallel:
			ttl_in.gate_rising(1*ms)
			with sequential:
				delay(50*us)
				for _ in range(n):
					ttl_out.pulse(2*us)
					delay(2*us)
		return ttl_in.count(now_mu()) == n

	@kernel
	def listen_dev(self, dev, ttl_out): # NOT DONE
		self.core.break_realtime()
		for i in range(100):
			with parallel:
				dev.gate_rising(1*ms)
				with sequential:
					delay(50*us)
					for _ in range(50):
						ttl_out.pulse(2*us)
						delay(2*us)
			temp = dev.count(now_mu())
			if temp > 0:
				return temp
			delay(100*ms)
		return dev.count(now_mu())

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
		elif cmd == "all":
			return self.leds + self.ttl_outs + self.ttl_ins
		else:
			for name, dev in self.leds + self.ttl_outs + self.ttl_ins:
				if cmd == name:
					return [(name, dev)]
			return None

	def print_help(self):
		print("list {all|leds|ttl_outs|ttl_ins|device|modules}")
		print("test {leds|ttl_outs|device}")
		print("set {leds|ttl_outs|device} {on|off|input|output}")
		print("pulse {device|ttl_outs|leds} {count in ms} {length in ms}")
		print("listen {device}")
		print("run {file.txt}")
		print("system {bash command}")
		print("log")
		print("help, clear, exit")
		tasks_help()

	def get_modules(self):
		print("[*] Found modules:")
		for root, dirs, files in os.walk(os.getcwd()):
			for file in files:
				if file.endswith(".m"):
					print(" > " + file)


	def build(self):
		self.setattr_device("core")
		#self.core.reset()
		self.setattr_device("led0")
		self.setattr_device("ttl0")
		self.setattr_device("ttl1")

		tasks_build(self)

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
		print("")
		print("*"*30 + " " + s + " " + "*"*30)
		print("")
	
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

