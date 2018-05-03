import RPi.GPIO as GPIO

class Engine:
    def __init__(self, in1_pin, in2_pin, enable_pin, name):
	self.in1_pin = in1_pin
        self.in2_pin = in2_pin
        self.enable_pin = enable_pin
	self.name = name

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(self.enable_pin, GPIO.OUT)
	GPIO.setup(self.in1_pin, GPIO.OUT)
	GPIO.setup(self.in2_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.enable_pin, 500)
        self.pwm.start(0)

    def forward(self):
	logging.info(self.name + ": forward")
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)
	GPIO.output(self.enable_pin, GPIO.HIGH)

    def backward(self):
	logging.info(self.name + ": backward")
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.HIGH)

    def changeSpeed(self,speed):
	logging.info(self.name + ": speed" + str(speed))
        self.pwm.ChangeDutyCycle(speed*10)

class Servo:
    def __init__(self,in_pin):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(in_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(in_pin, 100)
        self.pwm.start(0)

    def update(self,angle):
	logging.info("SERVO: angle " + str(angle))
        self.pwm.ChangeDutyCycle(float(angle) / 10.0 + 2.5)

class LED:
    def __init__(self,in1_pin,in2_pin,in3_pin):
        self.pins = [in1_pin,in2_pin,in3_pin]
        GPIO.setmode(GPIO.BOARD)

    pin_led_states = [
        [1, 0, -1],  # A
        [0, 1, -1],  # B
        [-1, 1, 0],  # C
        [-1, 0, 1],  # D
        [1, -1, 0],  # E
        [0, -1, 1]   # F
    ]

    def set_pin(self,pin_index, pin_state):
        if pin_state == -1:
            GPIO.setup(self.pins[pin_index], GPIO.IN)
        else:
            GPIO.setup(self.pins[pin_index], GPIO.OUT)
            GPIO.output(self.pins[pin_index], pin_state)

    def light_led(self,led_number):
        for pin_index, pin_state in enumerate(self.pin_led_states[led_number]):
            self.set_pin(pin_index, pin_state)
