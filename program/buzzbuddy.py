import os
import subprocess
import time
import sys
import beepy
from console.utils import wait_key
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import json
import random
import html
import re


print("*** BUZZBUDDY ***")
print()

def begin_read(qtext):
    return subprocess.Popen(["say", "-r", str(rate), qtext])

total = 0

rate = 170
qs = 20

qtexts = []
answers = []

MODE_WORD_DOC = 1
MODE_JSON = 2
mode = MODE_JSON

jfile = "easycollege.json"

if mode == MODE_WORD_DOC:
    os.environ['TK_SILENCE_DEPRECATION'] = '1'

    Tk().withdraw()
    packetfn = askopenfilename(filetypes=(("Word Documents", "*.docx"),))
    if packetfn == None:
        sys.exit()

    try:
        open(packetfn)
    except:
        sys.exit(0)


    subprocess.Popen(["./program/docx2txt.pl", packetfn, "tmp/packet.txt"]).wait()
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

elif mode == MODE_JSON:
    print("Asking", qs, "random questions from file", jfile)
    print("PRESS SPACE TO BUZZ")
    print()
    full_qs = json.load(open("questions/" + jfile))["data"]["tossups"]
    selected = random.choices(full_qs, k=qs)
    for i, s in enumerate(selected):
        qtexts.append("Question " + str(i + 1) + ". " + s["text"])
        answers.append(s["answer"])






for i, qtext in enumerate(qtexts):
    print("Question", i+1)
    p = begin_read(qtext)

    wait_key()

    print("BUZZ")
    p.kill()
    beepy.beep()

    print("Press space again to reveal answer")

    wait_key()

    print("ANSWER: " + html.unescape(re.sub('<[^<]+?>', '', answers[i])))
    print("press y if right, n if not, q to quit",)

    k = wait_key()

    if k == "q":
        sys.exit()

    elif k == "y":
        total += 1

    print("Total: " + str(total) + "/" + str(i + 1))
    print()
    time.sleep(1)
