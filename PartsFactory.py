import Config
import MockParts
import Parts

class PartsFactory:
    def __init__(self, config):
        self.config = config

    def getLeftEngine(self):
        return Parts.Engine(self.config.l_engine_in_1_pin, self.config.l_engine_in_2_pin, self.config.l_engine_enable_pin,"LEFT ENGINE")

    def getRightEngine(self):
        return Parts.Engine(self.config.r_engine_in_1_pin, self.config.r_engine_in_2_pin, self.config.r_engine_enable_pin,"RIGHT ENGINE")

    def getServo(self):
        return Parts.Servo(self.config.servo_in_pin)

    def getLEDS(self):
        return Parts.LED(self.config.leds_in_1_pin, self.config.leds_in_2_pin, self.config.leds_in_3_pin)

class MockPartsFactory:
    def getLeftEngine(self):
        return MockParts.MockEngine("LEFT ENGINE")

    def getRightEngine(self):
        return MockParts.MockEngine("RIGHT ENGINE")

    def getServo(self):
        return MockParts.MockServo()

    def getLEDS(self):
        return MockParts.MockLED()
