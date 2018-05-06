from multiprocessing import Process, Queue
from Config import FileConfigFactory, Config
import PartsFactory
import logging

class LEDSController:
    def __init__(self,factory,queue):
        self.queue = queue
        self.factory = factory
        self.process = None

    def loop(self,partsFactory,queue):
        leds = partsFactory.getLEDS()
        state = [0,0,0,0,0,0]
        while True:
            if not queue.empty():
                command = queue.get()
                if command[0] == "l":
                    state[command[1]] = 1
                elif command[0] == "d":
                    state[command[1]] = 0
                elif command[0] == "q":
                    break

            for i in range(len(state)):
                if state[i]:
                    leds.light_led(i)

    def lightGreen1(self):
	    self.light(3)

    def lightGreen2(self):
	    self.light(0)

    def lightGreen3(self):
	    self.light(4)

    def lightBlue(self):
	    self.light(1)

    def lightYellow(self):
	    self.light(2)

    def lightRed(self):
	    self.light(5)

    def downGreen1(self):
	    self.down(3)

    def downGreen2(self):
	    self.down(0)

    def downGreen3(self):
	    self.down(4)

    def downBlue(self):
	    self.down(1)

    def downYellow(self):
	    self.down(2)

    def downRed(self):
	    self.down(5)

    def light(self,num):
        logging.info("LED " + str(num) + ": on")
        self.queue.put(("l",num))
    
    def down(self,num):
        logging.info("LED " + str(num) + ": off")
        self.queue.put(("d",num))

    def start(self):
        self.process = Process(target=self.loop, args =(self.factory,self.queue))
        self.process.start()

    def stop(self):
       self.queue.put(("q",9))
       self.process.join()
