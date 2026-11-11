NAO PLANNING CHALLENGE 2026/27 - Fondamenti di Intelligenza Artificiale (UniBo)
==============================================================================

Nome del team : Il Figlio di Flynn
Partecipanti  : NOME COGNOME   - nome.cognome@studio.unibo.it   - matricola 0000000000
                NOME COGNOME   - nome.cognome@studio.unibo.it   - matricola 0000000000
Repository    : https://github.com/<UTENTE-GITHUB>/NAO-SonOfFlynn

Canzone       : Daft Punk - "The Son of Flynn" (TRON: Legacy), 1:35 (< 2 minuti)
Tema          : un programma entra nella Griglia di TRON: si risveglia, saluta i "programmi"
                (il pubblico), corre sulla Griglia, combatte, raggiunge il portale e si spegne.


LIBRERIE NECESSARIE
-------------------
- Python 3 con numpy (pip install -r requirements.txt): serve a search.py e utils.py del
  laboratorio (AIMA), con cui si pianifica la coreografia.
- Python 2.7 con NAOqi: esegue le posizioni (cartella NaoMoves/), come i file del corso.
    * Windows: quello dentro Choregraphe 2.8 (C:\Program Files (x86)\Softbank Robotics\
      Choregraphe Suite 2.8), main.py lo trova da solo.
    * VM del corso (NaoUbuntu): il comando python2 con NAOqi gia' installato.
- Musica sul PC: winsound (Windows, incluso in Python), afplay (macOS), aplay (Linux).


COME TESTARE SUL NAO SIMULATO
-----------------------------
1. Aprire Choregraphe con il robot virtuale NAO
   (Edit > Preferences > Virtual Robot > Robot model = NAO H25, Motor speed 100%).
   Nella stessa finestra si legge la porta: "NAOqi state: Running on port XXXXX".
2. Lanciare:
     Windows:     avvia_windows.bat XXXXX        (oppure doppio click e scrivere la porta)
     VM / Linux:  python3 main.py 127.0.0.1 XXXXX
3. main.py stampa il piano trovato da A*, porta NAO in StandInit, fa partire la canzone sul PC
   e la coreografia nella finestra 3D di Choregraphe.
   Solo il piano, senza robot:              python3 main.py --solo-piano
   Confronto tra strategie (reporting.py):  python3 main.py --report
   Senza musica:                            aggiungere --no-music
   Il robot simulato non puo' riprodurre musica: la canzone (music/son_of_flynn.wav) la
   suona il PC.


ALGORITMO A (nao_problem.py + astar_search di search.py)
---------------------------------------------------------
Come negli esercizi del laboratorio, il problema e' una sottoclasse di Problem (NaoProblem)
risolta con astar_search. Stato iniziale StandInit (0 s), le 6 posizioni obbligatorie
P1..P6 (Hello, StandZero, WipeForehead, Stand, Sit, SitRelax) e il goal Crouch hanno ordine e
istante fissi, scelti sulla musica (MANDATORY in main.py). Per ogni tratto tra due posizioni
obbligatorie si crea un NaoProblem e lo si risolve con A*:
  - stato  = (secondo in cui NAO torna libero, mosse fatte nel tratto)
  - azioni = una posizione intermedia non ancora usata, compatibile (camminate e rotazioni
             del piede solo in piedi), che parte sul battito della canzone e finisce prima della
             prossima obbligatoria; oppure la prossima posizione obbligatoria
  - goal   = la prossima posizione obbligatoria e' stata eseguita
  - costo  = secondi in cui NAO resta fermo + 1 per ogni mossa che non c'entra con il "mood"
             dell'atto della canzone (path_cost)
  - h      = secondi di attesa inevitabili: se nel tempo rimasto non ci sta nessuna mossa, NAO
             dovra' aspettare fino alla posizione obbligatoria. h non sovrastima mai
             (euristica ammissibile), quindi A* trova il tratto di costo minimo.
Alla fine si controlla il vincolo globale: almeno 5 posizioni intermedie.
Incompatibilita' trovata sul simulatore: da Sit il robot si sdraia per tornare in piedi, quindi
le posture sedute stanno alla fine.

Piano attuale: union_arms, rotation_handgun_object, diagonal_right, diagonal_left, move_backward.


POSIZIONI (cartella NaoMoves/)
------------------------------
- 1-17: i file del corso (RobotPositions), eseguiti come script Python 2:
  python2 NaoMoves/<file>.py IP PORTA. Come gli altri team abbiamo commentato le frasi
  (ttsProxy.say) e la pausa time.sleep(1) che le segue; nelle posture 6, 11, 14-17 la
  velocita' di goToPosture e' 1.0 invece di 0.5 (altrimenti Sit, SitRelax e Crouch durerebbero
  circa 50 s su 95).
- Hello.py e WipeForehead.py: animazioni di Choregraphe esportate in Python.
- Le durate in main.py (MOVES, MANDATORY) sono misurate sul robot virtuale con
  python3 misura_tempi.py 127.0.0.1 PORTA (ogni file lanciato come in main.py).


STRUTTURA
---------
  main.py              dati della coreografia, pianificazione (A*) ed esecuzione
  nao_problem.py       classe NaoProblem (sottoclasse di Problem) e classe NaoMove
  search.py, utils.py  libreria AIMA usata in laboratorio (non modificata)
  reporting.py         path_actions e report del laboratorio (non modificato)
  nao_tools.py         Python 2: prepara il robot e cambia il colore degli occhi
  misura_tempi.py      misura la durata di ogni posizione sul robot virtuale
  avvia_windows.bat    lancia main.py su Windows
  NaoMoves/            i file delle posizioni (Python 2)
  music/               la canzone


SINCRONIZZAZIONE
----------------
t0 = istante in cui parte la canzone. Ogni posizione aspetta il proprio secondo della canzone
(orologio reale) e poi viene eseguita; se una mossa finisce dopo, la successiva parte subito e
il ritardo viene stampato, senza accumularsi. Gli occhi cambiano colore a ogni atto.
