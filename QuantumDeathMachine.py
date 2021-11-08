
from Adafruit_Thermal import *
from qiskit import QuantumCircuit, execute, Aer, IBMQ
import qiskit as q
from qiskit.tools.monitor import job_monitor, backend_overview
from qiskit.providers.ibmq import least_busy
import time
import warnings

warnings.filterwarnings("ignore")


DeathList = ["Bees","Sour milk","Natural Causes","Monsters from\nthe Deep","In space,\nAlone","In Sleep","Peacefully","Pooping","Furnace","Rollercoaster","Extreme cold","Bear","Heat death of\nthe universe","Goose attack","sneezing","Boat accident"]

provider = IBMQ.load_account() #load account from disk

qc = q.QuantumCircuit(4,4) #5 qubits 5 classical bits
qc.h(0)
qc.h(1)
qc.h(2)
qc.h(3)
#qc.h(4)
qc.measure([0, 1, 2, 3],[0, 1, 2, 3])

print("\nAll backends overview:\n")
backend_overview()

backend = least_busy(provider.backends(n_qubits=5, operational=True, simulator=False))
print("\nLeast busy 5-qubit backend:", backend.name())
#backend = provider.get_backend('ibmq_belem')

shots = 1
job = execute(qc, backend, shots=shots, memory=True)
job_monitor(job)
result = job.result()
dice=result.get_memory(qc)

print("Received qubits: " + dice[0])
print("Quantum dice roll result: " + str(int(dice[0],2)))
time.sleep(4)
printer = Adafruit_Thermal("/dev/serial0", 9600, timeout=5)
printer.wake()

print("Printing Result..")
printer.justify('C')
printer.feed(1)
printer.setSize('L')   # Set type size, accepts 'S', 'M', 'L'
#printer.println("---------------")
printer.setSize('M')
printer.println("This is how")
printer.setSize('L')
printer.println("YOU DIE")
import gfx.arrow as arrow
printer.printBitmap(arrow.width, arrow.height, arrow.data)
#printer.println("---------------")
printer.setSize("L")
#printer.justify('L')
#printer.feed(1)
printer.println("---------------")
#printer.println(DeathList[0])
printer.println(DeathList[(int(dice[0],2))])
printer.println("---------------")
#printer.println("Old Age,\nSurrounded by\nLoved Ones")
#printer.println("\uD83D\uDC80")
printer.feed(1)
printer.setSize("S")
printer.print("Your Qubits: ")
printer.println(dice)

printer.feed(3)

#testing
printer.sleep()      # Tell printer to sleep
#printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults
