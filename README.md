# ARTIQ

This is a terminal interface for the Advanced Real-Time Infrastructure for Quantum physics (ARTIQ). 

## Basics

The core code is contained in main.py. To start the interface, run

```
user@user:~$ conda activate artiq
(artiq) user@user:~$ artiq_run main.py
[*] Loaded devices
[*] Found modules:
 > test.m
 > pulse.m
[*] Loaded tasks
[*] Type help for a help menu
>> 
```

The core features include: a set of commands for directly interacting with I/O, a tasks.py file for custom user function, and modules for defining sets of commands to run.

To list possible commands, use the `help` command.

```
>> help
list {all|leds|ttl_outs|ttl_ins|device|modules}
test {leds|ttl_outs|device}
set {leds|ttl_outs|device} {on|off|input|output}
pulse {device|ttl_outs|leds} {count in ms} {length in ms}
listen {device}
run {file.txt}
system {bash command}
log
help, clear, exit
task1
>> 
```

The script should automatically detect different I/O. To list these, use the `list` command.

```
>> list all
| Name   | Device                                                 |
|--------+--------------------------------------------------------|
| led0   | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac783e400> |
| led1   | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78653c8> |

| Name                  | Device                                                 |
|-----------------------+--------------------------------------------------------|
| ttl4                  | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78650f0> |
| ttl5                  | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac7865208> |
| ttl6                  | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78650b8> |
| ttl7                  | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78f5f60> |
| ttl8                  | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78f5eb8> |
| ttl9                  | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78f5940> |
| ttl10                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78651d0> |
| ttl11                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac7865080> |
| ttl12                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac7865278> |
| ttl13                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78f5f98> |
| ttl14                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac7865390> |

| Name   | Device                                                   |
|--------+----------------------------------------------------------|
| ttl0   | <artiq.coredevice.ttl.TTLInOut object at 0x7f4ac783ef98> |
| ttl1   | <artiq.coredevice.ttl.TTLInOut object at 0x7f4ac78f59b0> |
| ttl2   | <artiq.coredevice.ttl.TTLInOut object at 0x7f4ac7865160> |
| ttl3   | <artiq.coredevice.ttl.TTLInOut object at 0x7f4ac78654a8> |

>> 
```

## Input and Output

There are several commands for interacting with output, the simplest of which is `set`

```
>> set led0 on
[*] Setting led0 to state on
>> 
```

We can check which other outputs are avaliable

```
>> list ttl_outs
| Name                  | Device                                                 |
|-----------------------+--------------------------------------------------------|
| ttl4                  | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78650f0> |
| ttl5                  | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac7865208> |
| ttl6                  | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78650b8> |
| ttl7                  | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78f5f60> |
| ttl8                  | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78f5eb8> |
| ttl9                  | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78f5940> |
| ttl10                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78651d0> |
| ttl11                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac7865080> |
| ttl12                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac7865278> |
| ttl13                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78f5f98> |
| ttl14                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac7865390> |
| ttl15                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78f5978> |
| ttl16                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78f5ef0> |
| ttl17                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac7865400> |
| ttl18                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac7865240> |
| ttl19                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac7865470> |
| ttl20                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78654e0> |
| ttl21                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78f52b0> |
| ttl22                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac7865320> |
| ttl23                 | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac7865358> |
| ttl_novogorny0_cnv    | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78f5fd0> |
| ttl_urukul0_io_update | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac7865128> |
| ttl_urukul0_sw0       | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78f5f28> |
| ttl_urukul0_sw1       | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78652e8> |
| ttl_urukul0_sw2       | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78652b0> |
| ttl_urukul0_sw3       | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac7865438> |
| ttl_urukul1_io_update | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac78f5e80> |
| ttl_zotino0_ldac      | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac7865048> |
| ttl_zotino0_clr       | <artiq.coredevice.ttl.TTLOut object at 0x7f4ac7865198> |

>> 

```

The same command can be used with ttl_outs.

```
>> set ttl9 on
[*] Setting ttl9 to state on
>> 
```

It can also be used with groups of devices.

```
>> set leds off
[*] Setting led0 to state off
[*] Setting led1 to state off
>> set ttl_outs off
[*] Setting ttl4 to state off
[*] Setting ttl5 to state off
[*] Setting ttl6 to state off
[*] Setting ttl7 to state off
[*] Setting ttl8 to state off
[*] Setting ttl9 to state off
[*] Setting ttl10 to state off
[*] Setting ttl11 to state off
[*] Setting ttl12 to state off
[*] Setting ttl13 to state off
[*] Setting ttl14 to state off
[*] Setting ttl15 to state off
[*] Setting ttl16 to state off
[*] Setting ttl17 to state off
[*] Setting ttl18 to state off
[*] Setting ttl19 to state off
[*] Setting ttl20 to state off
[*] Setting ttl21 to state off
[*] Setting ttl22 to state off
[*] Setting ttl23 to state off
[*] Setting ttl_novogorny0_cnv to state off
[*] Setting ttl_urukul0_io_update to state off
[*] Setting ttl_urukul0_sw0 to state off
[*] Setting ttl_urukul0_sw1 to state off
[*] Setting ttl_urukul0_sw2 to state off
[*] Setting ttl_urukul0_sw3 to state off
[*] Setting ttl_urukul1_io_update to state off
[*] Setting ttl_zotino0_ldac to state off
[*] Setting ttl_zotino0_clr to state off
>> 
```
