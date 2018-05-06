from multiprocessing import Process, Queue
import PartsFactory
        
class MotorsController:
    def __init__(self,factory,queue):
        self.queue = queue
        self.factory = factory
        self.process = None
       
    def loop(self,partsFactory,queue):
        l_engine = partsFactory.getLeftEngine()
        r_engine = partsFactory.getRightEngine()
        servo = partsFactory.getServo()
        while True:
            if not queue.empty():
                command = queue.get()
                if command[0] == "f":
                    if command[1] > 100:
                        speed = 100
                    else:
                        speed = command[1]
                    l_engine.forward()
                    l_engine.changeSpeed(speed)
                    r_engine.forward()
                    r_engine.changeSpeed(speed)
                elif command[0] == "b":
                    if command[1] > 100:
                        speed = 100
                    else:
                        speed = command[1]
                    l_engine.backward()
                    l_engine.changeSpeed(speed)
                    r_engine.backward()
                    r_engine.changeSpeed(speed)
                elif command[0] == "s":
                    servo.update(command[1])
                elif command[0] == "q":
                    break

    def forward(self,speed):
        self.queue.put(("f",speed))
    
    def backward(self,speed):
        self.queue.put(("b",speed))

    def turn(self,angle):
        self.queue.put(("s",angle))
	    
    def start(self):
        self.process = Process(target=self.loop, args =(self.factory,self.queue))
        self.process.start()
        
    def stop(self):
       self.queue.put(("q",9))
       self.process.join()
