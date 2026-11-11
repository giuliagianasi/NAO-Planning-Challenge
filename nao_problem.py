# -*- coding: utf-8 -*-
"""
IL PROBLEMA, scritto come negli esercizi del laboratorio (PourProblem, MC, U2):
una sottoclasse di Problem di search.py con actions, result, goal_test, path_cost e h.

Un NaoProblem e' UN TRATTO della coreografia: dalla fine di una posizione obbligatoria
all'inizio della successiva (la "A" tra Pi e Pi+1 nella slide della challenge).

STATO = (t, fatte)
    t      secondo della canzone in cui NAO torna libero
    fatte  tupla delle mosse fatte in questo tratto (l'ultima puo' essere la posizione
           obbligatoria finale: allora il tratto e' finito)
AZIONI = il nome di una mossa intermedia che ci sta nel tempo rimasto, oppure il nome della
         prossima posizione obbligatoria (che parte sempre al suo istante fisso)
GOAL   = la prossima posizione obbligatoria e' stata eseguita
COSTO  = secondi in cui NAO resta fermo + MOOD_PENALTY per ogni mossa fuori dal mood dell'atto
h(n)   = secondi di attesa sicuramente inevitabili: se nel tempo rimasto non ci sta nessuna
         mossa, NAO dovra' aspettare fino alla posizione obbligatoria (problema rilassato:
         h non sovrastima mai, quindi A* trova il tratto di costo minimo)
"""
import math

from search import Problem


class NaoMove:
    """Le informazioni di una mossa (come nel progetto FirenzeReggio)."""

    def __init__(self, file, duration, standing=False, tags=()):
        self.file = file            # file Python 2 in NaoMoves/
        self.duration = duration    # secondi misurati sul robot virtuale (misura_tempi.py)
        self.standing = standing    # True: NAO deve essere in piedi (camminate, rotazioni del piede)
        self.tags = tags            # "sapore" della mossa, confrontato con il mood dell'atto


class NaoProblem(Problem):

    def __init__(self, initial, goal, goal_time, moves, used, standing, acts,
                 beat, beat_offset, safety, mood_penalty):
        """initial = (t, ())       goal = nome della prossima posizione obbligatoria
        goal_time = istante della prossima posizione obbligatoria
        moves = dizionario {nome: NaoMove} delle mosse intermedie
        used = mosse gia' usate nei tratti precedenti (ognuna si usa una volta sola)
        standing = True se NAO in questo tratto e' in piedi"""
        super().__init__(initial, goal)
        self.goal_time = goal_time
        self.moves = moves
        self.used = used
        self.standing = standing
        self.acts = acts
        self.beat = beat
        self.beat_offset = beat_offset
        self.safety = safety
        self.mood_penalty = mood_penalty

    def __repr__(self):
        return "NaoProblem(-> %s)" % self.goal

    # ------------------------------------------------------------------ funzioni di aiuto
    def next_beat(self, t):
        """Primo battito della canzone a partire dall'istante t (le mosse partono a tempo)."""
        k = math.ceil((t - self.beat_offset - 0.001) / self.beat)
        return round(self.beat_offset + k * self.beat, 2)

    def slot(self, name):
        """Tempo che riserviamo a una mossa: la sua durata + il margine di sicurezza."""
        return self.moves[name].duration * self.safety

    def mood(self, t):
        """Il mood dell'atto in cui cade l'istante t."""
        mood = self.acts[0][2]
        for start, name, act_mood in self.acts:
            if start <= t + 0.01:
                mood = act_mood
        return mood

    def can_do(self, state, name):
        """Vincoli: mossa non ancora usata, compatibile con la postura, e ci sta nel tempo."""
        t, done = state
        move = self.moves[name]
        if name in done or name in self.used:
            return False
        if move.standing and not self.standing:
            return False
        return self.next_beat(t) + self.slot(name) <= self.goal_time

    # ------------------------------------------------------------------ il problema
    def actions(self, state):
        t, done = state
        if done and done[-1] == self.goal:      # tratto finito: nessuna azione
            return []
        return [name for name in self.moves if self.can_do(state, name)] + [self.goal]

    def result(self, state, action):
        t, done = state
        if action == self.goal:                 # la posizione obbligatoria parte al suo istante
            return (self.goal_time, done + (action,))
        start = self.next_beat(t)               # la mossa intermedia parte sul battito
        return (round(start + self.slot(action), 2), done + (action,))

    def goal_test(self, state):
        t, done = state
        return len(done) > 0 and done[-1] == self.goal

    def path_cost(self, c, state1, action, state2):
        t, done = state1
        if action == self.goal:                 # NAO aspetta ferma fino alla posizione obbligatoria
            return c + max(0, self.goal_time - t)
        start = self.next_beat(t)
        cost = c + (start - t)                  # attesa del battito
        if not set(self.moves[action].tags) & set(self.mood(start)):
            cost += self.mood_penalty           # mossa che non c'entra con l'atto
        return cost

    def h(self, node):
        t, done = node.state
        if self.goal_test(node.state):
            return 0
        if any(self.can_do(node.state, name) for name in self.moves):
            return 0                            # qualche mossa ci sta ancora: non so di piu'
        return max(0, self.goal_time - t)       # nessuna mossa ci sta: l'attesa e' inevitabile
