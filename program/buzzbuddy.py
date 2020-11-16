import os
import subprocess
import time
import sys
import beepy
from console.utils import wait_key
import easygui

def begin_read(qtext):
    return subprocess.Popen(["say", "-r", str(rate), qtext])

total = 0

rate = 200
qs = 20


qtexts = []
answers = []


os.environ['TK_SILENCE_DEPRECATION'] = '1'

packetfn = easygui.fileopenbox(filetypes=["*.docx"])
if packetfn == None:
    sys.exit()


os.system("./program/docx2txt.pl " + packetfn +  " tmp/packet.txt")
packet = open("tmp/packet.txt").read()


paras = packet.split("\n")


looking_for = 1
for para in paras:
    slooking = str(looking_for)
    if para[:len(slooking)] == slooking:
        qtexts.append(para)
        looking_for += 1
    if para[:len("ANSWER")] == "ANSWER":
        answers.append(para)


    if len(paras) == qs and len(answers) == qs:
        break


for i, qtext in enumerate(qtexts):
    p = begin_read(qtext)

    wait_key()

    p.kill()
    beepy.beep()

    print("Press space again to reveal answer")

    wait_key()
    print(answers[i])
    print("press y if right, n if not, q to quit",)

    k = wait_key()

    if k == "q":
        sys.exit()

    elif k == "y":
        total += 1

    print("Total", total)
    time.sleep(1)
