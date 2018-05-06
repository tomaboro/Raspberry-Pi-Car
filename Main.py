from Config import FileConfigFactory
from Config import Config
from MotorsController import MotorsController
from LEDSController import LEDSController
import PartsFactory
import argparse
from time import sleep
from multiprocessing import Queue, Process
import logging

parser = argparse.ArgumentParser(description='App for controling remote car based on RaspberryPi')

# Optional argument
parser.add_argument('--config_path', help='Path to config file')
parser.add_argument('--mode', help='Controller mode. Possible options are: keyboard, raw and camera')
parser.add_argument('--mock_parts', action='store_true',  help='Use Mock parts instead of real one')
parser.add_argument('--log_to_file',  help='Path to a file where program will save its log')
parser.add_argument('--console_log_lvl', help='logging level')

args = parser.parse_args()

if args.config_path is not None:
    config = FileConfigFactory(args.config_path).getConfig()
else:
    config = FileConfigFactory("./default_config.ini").getConfig()
if args.mock_parts is not None:
    factory = PartsFactory.MockPartsFactory()
else:
    factory = PartsFactory.PartsFactory(config)
if args.console_log_lvl is not None:
    log_lvl = args.log_lvl.upper()
else:
    log_lvl = 'DEBUG'.upper()
if args.log_to_file is not None:
    logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s',filename=args.log_to_file,level=log_lvl)
else:
    logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s',level=log_lvl)
    
motorsQueue = Queue()
ledsQueue = Queue()

motorsController = MotorsController(factory,motorsQueue)
ledsController = LEDSController(factory,ledsQueue)

motorsController.start()
ledsController.start()

def raw_contorller():
    while True:
        line = raw_input('Enter command: ')
        command = line.split()
        if command[0] == "engines":
            if command[1] == "forward":
                motorsController.forward(int(command[2]))
            elif command[1] == "backward":
                motorsController.backward(int(command[2]))
        elif command[0] == "servo":
                motorsController.turn(float(command[1]))
        elif command[0] == "led":
                if command[1] == "light":
                    ledsController.light(int(command[2]))
                elif command == "down":
                    ledsController.down(int(command[2]))
        elif command[0] == "sleep":
            sleep(float(command[1]))
        elif command[0] == "quit":
            break;

def keyboard_controller():
    import keyboard
    leftTime = 0
    rightTime = 0
    speedTime = 0
    breakingTime = 0

    def getSpeed(upTime,downTime):
        if downTime <= 0:
            speed = upTime / 60
            if speed > 100:
                return 100
            else:
                return speed
        elif downTime <= 1000:
            return 0
        else:
            speed = (downTime-1000) / 60
            if speed > 100:
                return 100
            else:
                return speed

    def getAngle(leftTime,rightTime):
        return 90*(rightTime - leftTime)/5000

    while True: 
	interval_ms = 500
	interval_s = interval_ms / 1000
        try: 
            if keyboard.is_pressed(103): #UP 
                speedTime = speedTime + interval_ms
            else:
                if speed > 0:
                    speedTime = speedTime - interval_ms

            if keyboard.is_pressed(105): #LEFT
                leftTime = leftTime + interval_ms
            else:
                if leftTime > 0:
                    leftTime = leftTime - interval_ms

            if keyboard.is_pressed(106): #RIGHT
                rightTime = rightTime + interval_ms
            else:
                if rightTime > 0: 
                    rightTime = rightTime - interval_ms

            if keyboard.is_pressed(108): #DOWN
                breakingTime = breakingTime + interval_ms
            else:
                if breakingTime > 0:
                    brakingTime = breakingTime - interval_ms

            if keyboard.is_pressed('q'): #q
                break

            speed = getSpeed(speedTime,breakingTime)
            angle = getAngle(leftTime,rightTime)

            if speed < 0:
                motorsController.backward(speed)
                ledsController.lightYellow()
            else:
                motorsController.forward(speed)
                ledsController.downYellow()
                if speed < 50:
                    ledsController.lightGreen1()
                    ledsController.downGreen2()
                    ledsController.downGreen3()
                elif speed < 75:
                    ledsController.lightGreen1()
                    ledsController.lightGreen2()
                    ledsController.downGreen3()
                elif speed < 90:
                    ledsController.lightGreen1()
                    ledsController.lightGreen2()
                    ledsController.lightGreen3()
            motorsController.turn(angle)

            sleep(0.5)
            pass
        except:
            pass

def camera_controller():
    print "TO DO"

if args.mode == "raw":
    raw_contorller()
elif args.mode == "camera":
    camera_controller()
elif args.mode == "keyboard":
    keyboard_controller()

motorsController.stop()
ledsController.stop()
