# -*- coding: utf-8 -*-
"""
Piccoli comandi per il robot, in Python 2 come i file in NaoMoves/ (NAOqi funziona solo con Python 2).

    python2 nao_tools.py IP PORTA prepara        sveglia NAO, lo porta in StandInit, occhi spenti
    python2 nao_tools.py IP PORTA eyes 0x00E5FF  cambia il colore degli occhi
"""
import sys
from naoqi import ALProxy

robotIP, port, command = sys.argv[1], int(sys.argv[2]), sys.argv[3]

if command == "prepara":
    ALProxy("ALMotion", robotIP, port).wakeUp()
    posture = ALProxy("ALRobotPosture", robotIP, port)
    posture.setMaxTryNumber(3)
    posture.goToPosture("StandInit", 0.6)
    posture.setMaxTryNumber(1)   # sul robot virtuale altrimenti le posture ritentano e diventano lentissime
    ALProxy("ALLeds", robotIP, port).fadeRGB("FaceLeds", 0x000000, 0.3)
elif command == "eyes":
    ALProxy("ALLeds", robotIP, port).fadeRGB("FaceLeds", int(sys.argv[4], 16), 1.0)
