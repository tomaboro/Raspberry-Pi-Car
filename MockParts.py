import logging

class MockEngine:
    def __init__(self,name):
        self.name = name

    def forward(self):
	logging.info(self.name + ": forward (M)")

    def backward(self):
        logging.info(self.name + ": backward")

    def changeSpeed(self,speed):
        logging.info(self.name + ": speed " + str(speed))

class MockServo:
    def update(self,angle):
        logging.info("SERVO: angle " + str(angle))

class MockLED:
    def light_led(self,led_number):
	pass
