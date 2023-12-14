''' panic_thread.py
IMPORTANT: don't forget to call PanicThread.end() or the execution will not finish until a threshold is passed!

Please note that this script uses the psutil library to monitor memory usage, and the threading library to handle the panic thread. If you haven’t installed psutil, you can do so using pip: pip install psutil.

This script continuously checks if the time or memory threshold is exceeded, and if so, it exits the script. You can adjust the MEMORY_THRESHOLD and TIME_THRESHOLD variables to suit your needs.

Please note that this is a simple example and might not work for complex multi-threaded applications. Also, abruptly exiting a script with os._exit(1) might not be the best approach in a real-world application as it could lead to resources not being cleaned up properly. It’s generally better to have a graceful shutdown process. This script is just to give you an idea of how you could implement a ‘panic’ thread. Always remember to handle resources and errors properly in your scripts.
'''

import os
import time
import threading
import psutil

class PanicThread:
  ONE_MEGABYTE = 1000000
  ONE_HUNDRED_MEGABYTES = 100000000
  FIVE_HUNDRED_MEGABYTES = 500000000
  ONE_GIGABYTE = 1000000000
  TWO_GIGABYTES = 2000000000
  FOUR_GIGABYTES = 4000000000

  TEN_SECONDS = 10
  ONE_MINUTE = 60
  TWO_MINUTES = 120
  FOUR_MINUTES = 240

  def __init__(self, calling_thread, memory_threshold=ONE_MEGABYTE, time_threshold=TEN_SECONDS):
    self.calling_thread = calling_thread
    self.memory_threshold = memory_threshold
    self.time_threshold = time_threshold
    self.process = psutil.Process(os.getpid())
    self.running = True

  def panic(self):
    start_time = time.time()
    while self.running:
      # Check if the calling thread is still alive
      if not self.calling_thread.is_alive():
        # print("PANIC! The calling thread has ended. Ending the panic thread.")
        break

      # Check the time elapsed
      elapsed_time = time.time() - start_time
      if elapsed_time > self.time_threshold:
        print(f"\nPANIC! Time threshold, {self.time_threshold}, exceeded: {elapsed_time} seconds")
        os._exit(1)

      # Check the memory usage
      memory_usage = self.process.memory_info().rss
      if memory_usage > self.memory_threshold:
        print(f"\nPANIC! Memory threshold, {self.memory_threshold}, exceeded: {memory_usage} bytes")
        os._exit(1)

      # Sleep for a while
      time.sleep(0.1)

  def start(self):
    self.thread = threading.Thread(target=self.panic)
    self.thread.start()

  def end(self):
    self.running = False
    self.thread.join()

''' usage example:
from panic_thread import PanicThread

# Create a PanicThread instance with custom thresholds
panic_thread = PanicThread(
  threading.current_thread(), 
  PanicThread.ONE_GIGABYTE, 
  PanicThread.ONE_MINUTE)

# Start the panic thread
panic_thread.start()

# Rest of the script goes here
while True:
    pass

# End the panic thread when the script has ended normally
panic_thread.end()
'''
