# NAO-Planning-Challenge
AI planning project for generating a robotic choreography for the NAO humanoid robot, developed for the Fundamentals of Artificial Intelligence course at the University of Bologna.

Nome del team : NAOgraphy
Partecipanti  : Giulia Gianasi  - giulia.gianasi@studio.unibo.it
                Francesco Imperato  - francesco.imperato2@studio.unibo.it
Repository    : https://github.com/giuliagianasi/NAO-Planning-Challenge.git
Canzone       : Daft Punk - "The Son of Flynn" (TRON: Legacy), 1:35 (< 2 minuti)

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


