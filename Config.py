import ConfigParser

class FileConfigFactory:
    def __init__(self,path):
        conf = ConfigParser.ConfigParser()
        conf.read(path)
        self.config = Config(conf.getint("Left Engine","in_1_pin"), conf.getint("Left Engine","in_2_pin"), conf.getint("Left Engine","enable_pin"), conf.getint("Right Engine","in_1_pin"), conf.getint("Right Engine","in_2_pin"), conf.getint("Right Engine","enable_pin"), conf.getint("Servo","in_1_pin"), conf.getint("LEDS","in_1_pin"), conf.getint("LEDS","in_2_pin"), conf.getint("LEDS","in_3_pin"))

    def getConfig(self):
        return self.config

class DefaultConfigFactory:
    def __init__(self):
        self.config = Config(12,16,18,11,7,13,22,15,32,29)

class Config:
    def __init__(self,l_engine_in_1_pin, l_engine_in_2_pin, l_engine_enable_pin, r_engine_in_1_pin, r_engine_in_2_pin, r_engine_enable_pin, servo_in_pin, leds_in_1_pin, leds_in_2_pin, leds_in_3_pin) :
        self.l_engine_in_1_pin = l_engine_in_1_pin
        self.l_engine_in_2_pin = l_engine_in_2_pin
        self.l_engine_enable_pin = l_engine_enable_pin
        self.r_engine_in_1_pin = r_engine_in_1_pin
        self.r_engine_in_2_pin = r_engine_in_2_pin
        self.r_engine_enable_pin = r_engine_enable_pin
        self.servo_in_pin = servo_in_pin
        self.leds_in_1_pin = leds_in_1_pin
        self.leds_in_2_pin = leds_in_2_pin
        self.leds_in_3_pin = leds_in_3_pin

    def validate(self):
        return true

