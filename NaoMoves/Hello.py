# -*- coding: utf-8 -*-
# Hello: animazione di Choregraphe (Choregraphe > Box libraries > Animations > Hello), esportata in Python
# come fanno gli altri team. Si lancia come i file del corso: python2 Hello.py IP PORTA. Angoli in radianti, mani da 0 (chiusa) a 1 (aperta).
from naoqi import ALProxy


def main(robotIP, port):
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.8, 1.56, 2.24, 2.8, 3.48, 4.6])
    keys.append([0.296025, -0.170309, -0.340584, -0.059865, -0.193330, -0.010786])

    names.append("HeadYaw")
    times.append([0.8, 1.56, 2.24, 2.8, 3.48, 4.6])
    keys.append([-0.135036, -0.351335, -0.415755, -0.418827, -0.520073, -0.375874])

    names.append("LElbowRoll")
    times.append([0.72, 1.48, 2.16, 2.72, 3.4, 4.52])
    keys.append([-1.379020, -1.290043, -1.182670, -1.248626, -1.319207, -1.184206])

    names.append("LElbowYaw")
    times.append([0.72, 1.48, 2.16, 2.72, 3.4, 4.52])
    keys.append([-0.803864, -0.691883, -0.679596, -0.610569, -0.753232, -0.670398])

    names.append("LHand")
    times.append([1.48, 4.52])
    keys.append([0.238000, 0.240000])

    names.append("LShoulderPitch")
    times.append([0.72, 1.48, 2.16, 2.72, 3.4, 4.52])
    keys.append([1.118232, 0.928026, 0.940296, 0.862070, 0.897344, 0.842121])

    names.append("LShoulderRoll")
    times.append([0.72, 1.48, 2.16, 2.72, 3.4, 4.52])
    keys.append([0.363517, 0.226998, 0.203977, 0.217782, 0.248465, 0.226998])

    names.append("LWristYaw")
    times.append([1.48, 4.52])
    keys.append([0.147219, 0.119607])

    names.append("RElbowRoll")
    times.append([0.64, 1.4, 1.68, 2.08, 2.4, 2.64, 3.04, 3.32, 3.72, 4.44])
    keys.append([1.385233, 0.242409, 0.349066, 0.934257, 0.680678, 0.191986, 0.261799, 0.707207, 1.019272, 1.265591])

    names.append("RElbowYaw")
    times.append([0.64, 1.4, 2.08, 2.64, 3.32, 3.72, 4.44])
    keys.append([-0.312972, 0.564474, 0.391128, 0.348176, 0.381930, 0.977384, 0.826780])

    names.append("RHand")
    times.append([1.4, 3.32, 4.44])
    keys.append([0.853000, 0.855000, 0.425000])

    names.append("RShoulderPitch")
    times.append([0.64, 1.4, 2.08, 2.64, 3.32, 4.44])
    keys.append([0.247016, -1.171936, -1.089103, -1.260913, -1.148915, 1.020145])

    names.append("RShoulderRoll")
    times.append([0.64, 1.4, 2.08, 2.64, 3.32, 4.44])
    keys.append([-0.242409, -0.954189, -0.460243, -0.960333, -0.328314, -0.250088])

    names.append("RWristYaw")
    times.append([1.4, 3.32, 4.44])
    keys.append([-0.312972, -0.303775, 0.182509])

    motionProxy = ALProxy("ALMotion", robotIP, port)
    motionProxy.angleInterpolation(names, keys, times, True)


if __name__ == "__main__":
    import sys
    robotIP = "127.0.0.1"
    port = 9559  # Insert NAO port
    if len(sys.argv) <= 1:
        print("(robotIP default: 127.0.0.1)")
    elif len(sys.argv) <= 2:
        robotIP = sys.argv[1]
    else:
        port = int(sys.argv[2])
        robotIP = sys.argv[1]
    main(robotIP, port)
