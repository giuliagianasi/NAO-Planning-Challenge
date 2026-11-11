# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import threading
import time

from search import *
from reporting import path_actions, report
from nao_problem import NaoMove, NaoProblem

HERE = os.path.dirname(os.path.abspath(__file__))

# =============================================================================== CANZONE
SONG = os.path.join(HERE, "music", "son_of_flynn.wav")
SONG_DURATION = 95.3        # secondi (limite della challenge: 2 minuti)
BEAT = 0.4245               # secondi tra due battiti (141 BPM)
BEAT_OFFSET = 0.38          # istante del primo battito

# Atti della storia: (inizio, nome, mood, colore degli occhi). Il mood sono i tag preferiti.
ACTS = [
    (0.00,  "I - Il Rifugio",    ("calm",),            "0x00E5FF"),
    (18.21, "II - I Giochi",     ("disc", "public"),   "0x00E5FF"),
    (31.79, "III - Light Cycle", ("space", "robotic"), "0x40FFFF"),
    (45.38, "IV - Battaglia",    ("disc", "power"),    "0xFF6A00"),
    (58.96, "V - Il Portale",    ("dance", "public"),  "0xFFFFFF"),
    (77.64, "VI - Ritorno",      ("calm",),            "0x00E5FF"),
]

# =============================================================================== POSIZIONI
# Posizioni obbligatorie: (nome, file in NaoMoves/, istante fisso sulla musica, durata misurata).
# Prima lo stato iniziale StandInit, poi P1..P6, infine il goal Crouch.
MANDATORY = [
    ("StandInit",    "14-StandInit.py",   0.00, 2.0),
    ("Hello",        "Hello.py",         18.21, 8.0),   # saluta sull'ingresso del basso
    ("StandZero",    "15-StandZero.py",  32.64, 2.4),   # dopo il colpo d'orchestra: braccia avanti, il manubrio
    ("WipeForehead", "WipeForehead.py",  47.08, 8.8),   # fine della corsa: si asciuga la fronte
    ("Stand",        "11-Stand.py",      56.41, 2.0),   # si ricompone per la battaglia
    ("Sit",          "16-Sit.py",        65.33, 9.0),   # sulla soglia del portale si siede...
    ("SitRelax",     "17-SitRelax.py",   75.09, 11.2),  # ...si rilassa...
    ("Crouch",       "6-Crouch.py",      86.98, 10.0),  # ...e si spegne in ginocchio sul finale
]
SITTING = ("Sit", "SitRelax", "Crouch")   # dopo queste NAO non e' in piedi

# Posizioni intermedie: i file del corso. Durate misurate sul robot virtuale con misura_tempi.py
# (valore piu' alto di 2 prove; camminate +1 s: dopo un'altra mossa NAO ci mette di piu' a partire).
MOVES = {
    "rotation_handgun_object": NaoMove("1-Rotation_handgun_object.py", 5.5, False, ("disc",)),
    "right_arm":               NaoMove("2-Right_arm.py",              16.3, False, ("disc", "power")),
    "double_movement":         NaoMove("3-Double_movement.py",        10.0, False, ("power", "robotic")),
    "arms_opening":            NaoMove("4-Arms_opening.py",           13.5, False, ("calm",)),
    "union_arms":              NaoMove("5-Union_arms.py",             13.7, False, ("calm",)),
    "move_forward":            NaoMove("7-Move_forward.py",            7.5, True,  ("space",)),
    "move_backward":           NaoMove("8-Move_backward.py",           6.0, True,  ("space",)),
    "diagonal_left":           NaoMove("9-Diagonal_left.py",           5.3, True,  ("space",)),
    "diagonal_right":          NaoMove("10-Diagonal_right.py",         5.4, True,  ("space",)),
    "rotation_foot_RLeg":      NaoMove("12-Rotation_foot_RLeg.py",    38.3, True,  ("robotic", "calm")),
    "rotation_foot_LLeg":      NaoMove("13-Rotation_foot_LLeg.py",    69.0, True,  ("robotic", "calm")),
}

MIN_INTERMEDIATE = 5   # regola della challenge
SAFETY = 1.05          # ogni mossa occupa il 5% di tempo in piu' (margine per il simulatore)
MOOD_PENALTY = 1.0     # costo (in secondi) di una mossa che non c'entra con l'atto


# =============================================================================== 1. PIANIFICAZIONE
def make_problem(i, used):
    """Il NaoProblem del tratto i: dalla posizione obbligatoria i alla i+1."""
    name, file, start, duration = MANDATORY[i]
    next_name, next_file, next_start, next_duration = MANDATORY[i + 1]
    free_at = round(start + duration * SAFETY, 2)          # quando NAO torna libero
    standing = name not in SITTING
    acts = [(a_start, a_name, a_mood) for a_start, a_name, a_mood, eyes in ACTS]
    return NaoProblem((free_at, ()), next_name, next_start, MOVES, used, standing, acts,
                      BEAT, BEAT_OFFSET, SAFETY, MOOD_PENALTY)


def make_plan():
    """Risolve un tratto alla volta con A*. Restituisce la lista (istante, nome, file)."""
    for (a, _, _, _), (b, _, _, _) in zip(MANDATORY, MANDATORY[1:]):
        if a == "Sit" and b not in SITTING:
            raise RuntimeError("Da Sit il robot virtuale si sdraia per rialzarsi: metti %s dopo" % b)

    name, file, start, duration = MANDATORY[0]
    plan = [(start, name, file)]
    used = ()
    total_cost = 0
    print("ALGORITMO A: astar_search su ogni tratto tra due posizioni obbligatorie\n")
    for i in range(len(MANDATORY) - 1):
        problem = make_problem(i, used)
        node = astar_search(problem)
        if node is None:
            raise RuntimeError("Tratto %d: nessuna soluzione" % (i + 1))
        actions = path_actions(node)
        t = problem.initial[0]
        for action in actions:                              # ricostruisco gli istanti di partenza
            if action == problem.goal:
                plan.append((problem.goal_time, action, MANDATORY[i + 1][1]))
            else:
                t = problem.next_beat(t)
                plan.append((t, action, MOVES[action].file))
                t = round(t + problem.slot(action), 2)
                used = used + (action,)
        total_cost += node.path_cost
        print("Tratto %d  %-12s -> %-12s costo %5.2f   %s" % (
            i + 1, MANDATORY[i][0], problem.goal, node.path_cost, ", ".join(actions[:-1]) or "-"))

    intermediate = [name for t, name, file in plan if name in MOVES]
    print("\n  inizio  posizione")
    for t, name, file in plan:
        print("%7.2fs  %s%s" % (t, name, "" if name in MOVES else "  *"))
    print("\n* = obbligatoria.  Intermedie: %d (%s).  Costo totale: %.2f"
          % (len(intermediate), ", ".join(intermediate), total_cost))
    if len(intermediate) < MIN_INTERMEDIATE:
        raise RuntimeError("Solo %d posizioni intermedie: ne servono almeno %d"
                           % (len(intermediate), MIN_INTERMEDIATE))
    return plan


# =============================================================================== 2. ESECUZIONE
# Python 2 con NAOqi: su Windows quello dentro Choregraphe, sulla VM del corso "python2".
CHOREGRAPHE = r"C:\Program Files (x86)\Softbank Robotics\Choregraphe Suite 2.8"
if sys.platform == "win32":
    PYTHON2 = os.path.join(CHOREGRAPHE, "bin", "python.exe")
    ENV2 = dict(os.environ,
                PATH=os.path.join(CHOREGRAPHE, "bin") + ";" + os.environ.get("PATH", ""),
                PYTHONHOME=os.path.join(CHOREGRAPHE, "lib", "python2.7"),
                PYTHONPATH=os.path.join(CHOREGRAPHE, "lib") + ";" +
                           os.path.join(CHOREGRAPHE, "lib", "python2.7", "Lib"))
else:
    PYTHON2 = "python2"
    ENV2 = None


def python2(script, *args):
    """La riga di comando per lanciare uno script Python 2 con NAOqi."""
    return [PYTHON2, os.path.join(HERE, script)] + [str(a) for a in args]


def do_move(file, ip, port):
    """Esegue una posizione e aspetta che finisca."""
    subprocess.run(python2(os.path.join("NaoMoves", file), ip, port), env=ENV2)


def play_music():
    if sys.platform == "win32":
        import winsound
        winsound.PlaySound(SONG, winsound.SND_FILENAME | winsound.SND_ASYNC)
    elif sys.platform == "darwin":
        subprocess.Popen(["afplay", SONG])
    else:
        subprocess.Popen(["aplay", "-q", SONG])


def stop_music():
    if sys.platform == "win32":
        import winsound
        winsound.PlaySound(None, 0)


def eyes(ip, port, t0):
    """In parallelo alle mosse: colore degli occhi a ogni atto, spenti alla fine."""
    events = [(start, color) for start, name, mood, color in ACTS] + [(SONG_DURATION - 4.5, "0x000000")]
    for t, color in events:
        time.sleep(max(0, t0 + t - time.time()))
        subprocess.Popen(python2("nao_tools.py", ip, port, "eyes", color), env=ENV2)


def perform(plan, ip, port, music=True):
    print("\nPreparazione: NAO si sveglia e va in StandInit...")
    subprocess.run(python2("nao_tools.py", ip, port, "prepara"), env=ENV2)
    if music:
        play_music()
    t0 = time.time()                                 # t0 = istante in cui parte la canzone
    threading.Thread(target=eyes, args=(ip, port, t0), daemon=True).start()
    try:
        for start, name, file in plan:               # ogni posizione aspetta il SUO secondo
            time.sleep(max(0, t0 + start - time.time()))
            late = time.time() - t0 - start
            print("[%6.2fs] %-25s %s" % (time.time() - t0, name,
                                         "(in ritardo di %.1fs)" % late if late > 0.3 else ""))
            do_move(file, ip, port)
        time.sleep(max(0, t0 + SONG_DURATION - time.time()))
        print("Fine! (%.1fs)" % (time.time() - t0))
    finally:
        stop_music()


def compare_searchers():
    """Come negli esercizi del laboratorio: report() di reporting.py su tutti i tratti."""
    problems, used = [], ()
    for i in range(len(MANDATORY) - 1):
        problem = make_problem(i, used)
        problems.append(problem)
        node = astar_search(problem)
        used = used + tuple(a for a in path_actions(node) if a in MOVES)
    report([astar_search, uniform_cost_search, breadth_first_graph_search], problems)


if __name__ == "__main__":
    if "--report" in sys.argv:
        compare_searchers()
        sys.exit()
    plan = make_plan()
    if "--solo-piano" in sys.argv:
        sys.exit()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ip = args[0] if len(args) > 0 else "127.0.0.1"
    port = int(args[1]) if len(args) > 1 else 9559
    perform(plan, ip, port, music="--no-music" not in sys.argv)
