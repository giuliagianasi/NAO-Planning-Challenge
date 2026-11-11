# -*- coding: utf-8 -*-
"""
Misura quanto dura ogni posizione sul robot virtuale, lanciandola esattamente come fa main.py
(un processo Python 2 per ogni file). Due giri; i tempi vanno copiati in main.py.

    python misura_tempi.py 127.0.0.1 PORTA
"""
import subprocess
import sys
import time

from main import MANDATORY, MOVES, ENV2, python2, do_move

ip, port = sys.argv[1], int(sys.argv[2])
subprocess.run(python2("nao_tools.py", ip, port, "prepara"), env=ENV2)

files = dict((name, file) for name, file, start, duration in MANDATORY)
files.update((name, move.file) for name, move in MOVES.items())
# ordine "da coreografia": in piedi le intermedie, poi le posture fino a Crouch.
# Le rotazioni del piede per ultime: dopo di loro le posture sul simulatore diventano lentissime.
ORDER = ["StandInit", "Hello", "WipeForehead", "rotation_handgun_object", "right_arm",
         "double_movement", "arms_opening", "union_arms", "move_forward", "move_backward",
         "diagonal_left", "diagonal_right", "StandZero", "Stand", "Sit", "SitRelax", "Crouch",
         "StandInit", "rotation_foot_RLeg", "rotation_foot_LLeg"]

for giro in (1, 2):
    for name in ORDER:
        t = time.time()
        do_move(files[name], ip, port)
        print("giro %d  %-25s %6.2f s" % (giro, name, time.time() - t), flush=True)
print("fine")
