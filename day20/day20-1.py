#!/usr/bin/python

import threading
# import resource
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

setDebug(False)
setDebug(True)
debug("debug is on")

puzzleNumber = "20"
partNumber = "1"

# initialize panic thread
panic_thread = PanicThread(
  threading.current_thread(),
  PanicThread.ONE_GIGABYTE,
  PanicThread.TEN_SECONDS)
panic_thread.start()

# start now, include file open in running time
start = datetime.now()

# get input lines
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input-1.txt", 'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input-2.txt", 'r')
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
# debug(f"rows: {nRows}, columns: {nColumns}")
# debug(f"{lines}")

print(f"# # # # # day{puzzleNumber}-{partNumber} # # # # #")

# # # # # # PUZZLE SOLUTION START # # # # # #

PULSE_VALUE_HIGH = "high"
PULSE_VALUE_LOW = "low"


class Pulse:
    def __init__(self, src: str, dest: str, value: str):
        self.src = src
        self.dest = dest
        self.value = value

    def __str__(self):
        return f"{self.src} -{pulse.value}-> {pulse.dest}"


pulses = []


class Module:
    def __init__(self, label: str, outputs: list[str]):
        self.label = label
        self.outputs = outputs
        self.inputs = []

    def __str__(self):
        sInputs = ""
        for inpt in self.inputs:
            sInputs += inpt + ","
        sOutputs = ""
        for output in self.outputs:
            sOutputs += output + ","
        return f"{self.label}:{sInputs}:{sOutputs}"

    def addInput(self, inputLabel: str):
        self.inputs.append(inputLabel)

    def receive(self, pulse: Pulse):
        raise Exception("receive() not implemented in base class Module")

    def send(self, pulseValue):
        for output in self.outputs:
            pulses.append(Pulse(self.label, output, pulseValue))


FLIP_FLOP_PREFIX = "%"
FLIP_FLOP_STATE_ON = "ON"
FLIP_FLOP_STATE_OFF = "OFF"


class FlipFlopModule(Module):
    def __init__(self, label: str, outputs: list[str]):
        super().__init__(label, outputs)
        self.state = FLIP_FLOP_STATE_OFF

    def __str__(self):
        return FLIP_FLOP_PREFIX + super().__str__() + ":" + self.state

    def receive(self, pulse: Pulse):
        if pulse.value == PULSE_VALUE_HIGH:
            return
        elif pulse.value == PULSE_VALUE_LOW:
            nextPulse = ""
            if self.state == FLIP_FLOP_STATE_OFF:
                self.state = FLIP_FLOP_STATE_ON
                nextPulse = PULSE_VALUE_HIGH
            elif self.state == FLIP_FLOP_STATE_ON:
                self.state = FLIP_FLOP_STATE_OFF
                nextPulse = PULSE_VALUE_LOW
            else:
                raise ValueError(f"invalid flip flop state, {self.state}")

            self.send(nextPulse)
        else:
            raise ValueError(f"invalid pulse value, {pulse.value}")


CONJUNCTION_PREFIX = "&"


class ConjunctionModule(Module):
    def __init__(self, label: str, outputs: list[str]):
        super().__init__(label, outputs)
        self.inputMemory = {}

    def __str__(self):
        sMemory = ""
        for mem in self.inputMemory.items():
            sMemory += str(mem) + ","
        return CONJUNCTION_PREFIX + super().__str__() + ":" + sMemory

    def addInput(self, inputLabel: str):
        super().addInput(inputLabel)
        self.inputMemory[inputLabel] = PULSE_VALUE_LOW

    def receive(self, pulse: Pulse):
        self.inputMemory[pulse.src] = pulse.value

        for memValue in self.inputMemory.values():
            if memValue == PULSE_VALUE_LOW:
                self.send(PULSE_VALUE_HIGH)
                return
        self.send(PULSE_VALUE_LOW)


BROADCASTER_KEY = "broadcaster"


class BroadcastModule(Module):
    def receive(self, pulse: Pulse):
        self.send(pulse.value)


OUTPUT_LABEL = "output"


class OutputModule(Module):
    def receive(self, pulse: Pulse):
        # print(f"OUTPUT: {pulse.value}")
        pass


modules = {}

modules[OUTPUT_LABEL] = OutputModule(OUTPUT_LABEL, [])

for line in lines:
    lineSplit = line.split(" ")

    outputs = lineSplit[2:]
    for i, output in enumerate(outputs):
        outputs[i] = output.replace(",", "")
        # debug(outputs[i])

    if lineSplit[0] == BROADCASTER_KEY:
        modules[BROADCASTER_KEY] = BroadcastModule(BROADCASTER_KEY, outputs)
    elif lineSplit[0][0] == FLIP_FLOP_PREFIX:
        label = lineSplit[0][1:]
        modules[label] = FlipFlopModule(label, outputs)
    elif lineSplit[0][0] == CONJUNCTION_PREFIX:
        label = lineSplit[0][1:]
        modules[label] = ConjunctionModule(label, outputs)
    else:
        raise Exception(f"Invalid prefix and/or label on line, {line}")

# set inputs
for module in modules.values():
    for output in module.outputs:
        if output in modules:
            modules[output].addInput(module.label)

# # # # #
for module in modules.values():
    debug(str(module))
# # # # # :


def pushButton():
    pulses.append(Pulse('button', BROADCASTER_KEY, PULSE_VALUE_LOW))


limitButtonPushes = 1000
nButtonPushes = 0
nLowPulses = 0
nHighPulses = 0

while nButtonPushes < limitButtonPushes:
    nButtonPushes += 1
    # debug(f"button push {nButtonPushes}")
    pushButton()
    while len(pulses) > 0:
        pulse = pulses[0]

        if pulse.value == PULSE_VALUE_HIGH:
            nHighPulses += 1
        elif pulse.value == PULSE_VALUE_LOW:
            nLowPulses += 1
        else:
            raise Exception(f"invalid pulse value, {pulse.value}")

        # debug(f"\t{pulse}")

        if pulse.dest in modules:
            modules[pulse.dest].receive(pulse)
        else:
            # debug(f"\t\toutput to non-existing module, {pulse.dest}")
            pass

        pulses = pulses[1:]

    # # # # #
    # for module in modules.values():
        # debug(str(module))
    # # # # # :

debug(f"nHighPulses = {nHighPulses}, nLowPulses = {nLowPulses}, product = {nLowPulses * nHighPulses}")

print(nLowPulses*nHighPulses)

# # # # # # PUZZLE SOLUTION END # # # # # # #

print(f"finished in {datetime.now() - start}")
# peakMemory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(f"peak memory: {peakMemory}")
panic_thread.end()
