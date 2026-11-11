# -*- coding: utf-8 -*-
# WipeForehead: animazione di Choregraphe (Choregraphe > Box libraries > Animations > Wipe Forehead), esportata in Python
# come fanno gli altri team. Si lancia come i file del corso: python2 WipeForehead.py IP PORTA. Angoli in radianti, mani da 0 (chiusa) a 1 (aperta).
from naoqi import ALProxy


def main(robotIP, port):
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.96, 1.68, 3.24, 3.88, 4.44, 5])
    keys.append([-0.026128, 0.427937, 0.308295, 0.111945, -0.013840, 0.061313])

    names.append("HeadYaw")
    times.append([0.96, 1.68, 3.24, 3.88, 4.44, 5])
    keys.append([-0.234747, -0.622838, -0.113551, -0.006178, -0.027646, -0.036861])

    names.append("LElbowRoll")
    times.append([0.8, 1.52, 3.08, 3.72, 4.28, 4.84])
    keys.append([-0.866661, -0.868197, -0.822190, -0.992447, -0.966371, -0.990928])

    names.append("LElbowYaw")
    times.append([0.8, 1.52, 3.08, 3.72, 4.28, 4.84])
    keys.append([-0.957261, -0.823795, -1.007875, -0.925042, -1.244123, -0.960333])

    names.append("LHand")
    times.append([1.52, 3.08, 3.72, 4.84])
    keys.append([0.132000, 0.132000, 0.132000, 0.132000])

    names.append("LShoulderPitch")
    times.append([0.8, 1.52, 3.08, 3.72, 4.28, 4.84])
    keys.append([0.863606, 0.858999, 0.888146, 0.929562, 1.017003, 0.977123])

    names.append("LShoulderRoll")
    times.append([0.8, 1.52, 3.08, 3.72, 4.28, 4.84])
    keys.append([0.286810, 0.230052, 0.202441, 0.406470, 0.360445, 0.319029])

    names.append("LWristYaw")
    times.append([1.52, 3.08, 3.72, 4.84])
    keys.append([0.386521, 0.386521, 0.386521, 0.386521])

    names.append("RElbowRoll")
    times.append([0.64, 1.36, 2.92, 3.56, 4.12, 4.68])
    keys.append([1.280932, 1.397520, 1.572385, 1.241051, 1.225710, 0.840673])

    names.append("RElbowYaw")
    times.append([0.64, 1.36, 2.92, 3.56, 4.12, 4.68])
    keys.append([-0.128893, -0.285361, -0.156504, 0.754680, 1.171936, 0.677991])

    names.append("RHand")
    times.append([1.36, 2.92, 3.56, 4.68])
    keys.append([0.167000, 0.166000, 0.167000, 0.166000])

    names.append("RShoulderPitch")
    times.append([0.64, 1.36, 2.92, 3.56, 4.12, 4.68])
    keys.append([0.076742, -0.595157, -0.866661, -0.613553, 0.584493, 0.882089])

    names.append("RShoulderRoll")
    times.append([0.64, 1.36, 2.92, 3.56, 4.12, 4.68])
    keys.append([-0.019984, -0.019984, -0.615176, -0.833011, -0.224013, -0.214798])

    names.append("RWristYaw")
    times.append([1.36, 2.92, 3.56, 4.68])
    keys.append([-0.058329, -0.052203, -0.067544, -0.038397])

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
