#!/usr/bin/env python3

import random
import secrets
import config
import subprocess, shlex
from sys import exit
import os
from os import path
import signal
# https://stackoverflow.com/questions/19447603/how-to-kill-a-python-child-process-created-with-subprocess-check-output-when-t/19448096#19448096
import ctypes
from pathlib import Path
import time
import datetime

libc = ctypes.CDLL("libc.so.6")


def set_pdeathsig(sig=signal.SIGTERM):
    def callable():
        return libc.prctl(1, sig)

    return callable


THUNDERBIRD_PROFILE_PATH = config.thunderbird_profile
GNUPG_PROFILE_PATH = config.gnupg_profile
CANARY = "95DAFBDA41D7E9C71D28D6A2.canary"

def start_recording(pid):
    cmd = f"ffmpeg -loglevel quiet -f alsa -i pulse -f x11grab -r 30 -s {config.resolution} -i :0.0 -acodec mp3 -vcodec libx264 -preset ultrafast -qp 1 recordings/{pid}.mkv"
    # cmd = f"ffmpeg -loglevel quiet -nostdin -f alsa -i pulse -f x11grab -r 30 -s 1920x1080 -i :0.0 -acodec mp3 -vcodec libx264 -preset ultrafast -qp 1 recordings/{pid}.mkv"
    # cmd = f"ffmpeg -f alsa -i pulse -f x11grab -r 30 -s 1920x1080 -i :0.0 -acodec mp3 -vcodec libx264 -preset ultrafast -qp 1 recordings/{pid}.mkv"
    # cmd = f"ffmpeg -f alsa -i pulse -f x11grab -r 30 -s 1920x1080 -i :0.0 -acodec pcm_s16le -vcodec libx264 -threads 0 {pid}.mkv"

    args = shlex.split(cmd)
    stdout = open("/dev/null")
    stderr = open("/dev/null")
    ffmpeg = subprocess.Popen(args, stdout=stdout, stderr=stderr, preexec_fn=set_pdeathsig(signal.SIGTERM))
    return ffmpeg


def stop_recording(ffmpeg):
    ffmpeg.terminate()


def firefox(url):
    my_env = os.environ.copy()
    my_env["LANG"] = "EN"

    stdout = open("/dev/null")
    stderr = open("/dev/null")
    subprocess.run(["firefox", url], stdout=stdout, stderr=stderr, env=my_env,
                   preexec_fn=set_pdeathsig(signal.SIGTERM))


def thunderbird(sid):
    if sid == "4":
        reset_profile("with_wkd")
    else:
        reset_profile("without_wkd")

    my_env = os.environ.copy()
    my_env["LANG"] = "EN"

    handler = imap(sid)

    stdout = open("/dev/null")
    stderr = open("/dev/null")
    subprocess.run("thunderbird", stdout=stdout, stderr=stderr, env=my_env,
                   preexec_fn=set_pdeathsig(signal.SIGTERM))

    handler.terminate()


def imap(sid):
    cmd = f"./fake_imap_server testcases/{sid}.eml"
    args = shlex.split(cmd)

    stdout = open("/dev/null")
    stderr = open("/dev/null")
    imap = subprocess.Popen(args, stdout=stdout, stderr=stderr,
                            preexec_fn=set_pdeathsig(signal.SIGTERM))
    return imap


def reset_profile(which):
    def remove_folder(path):
        path = Path(path)

        if not path.exists():
            return

        if not path.is_dir():
            raise Exception(f"{path} is a file. Expected directory.")

        if (path / Path(CANARY)).exists():
            subprocess.run(["rm", "-rf", str(path)])
        else:
            raise Exception(f"{path} exists, but has no canary. Won't delete.")

    def copy_folder(src, dst):
        src = Path(src)
        dst = Path(dst)

        if not src.exists():
            raise Exception(f"{src} does not exist.")

        if not src.is_dir():
            raise Exception(f"{src} is a file. Expected directory.")

        if dst.exists():
            raise Exception(f"{dst} exists. Won't copy over it.")

        subprocess.run(["cp", "-r", str(src), str(dst)])

    def reset_thunderbird_profile():
        remove_folder(THUNDERBIRD_PROFILE_PATH)
        copy_folder("thunderbird_genesis", THUNDERBIRD_PROFILE_PATH)

    def reset_gnupg_profile(which):
        remove_folder(GNUPG_PROFILE_PATH)

        if which == "without_wkd":
            copy_folder("gnupg_genesis", GNUPG_PROFILE_PATH)
        elif which == "with_wkd":
            copy_folder("gnupg_genesis_wkd", GNUPG_PROFILE_PATH)
        else:
            raise Exception('Wrong argument "which"')

    reset_thunderbird_profile()
    reset_gnupg_profile(which)


def selfcheck():
    if not THUNDERBIRD_PROFILE_PATH:
        raise Exception("Please tell me where your .thunderbird profile is in `config.py`.")

    if path.exists(THUNDERBIRD_PROFILE_PATH):
        if not path.exists(THUNDERBIRD_PROFILE_PATH + "/95DAFBDA41D7E9C71D28D6A2.canary"):
            raise Exception("No canary found in .thunderbird profile folder. Ask for advice or delete that folder yourself.")

    if not GNUPG_PROFILE_PATH:
        raise Exception("Please tell me where your .gnupg profile is in `config.py`.")

    if path.exists(GNUPG_PROFILE_PATH):
        if not path.exists(GNUPG_PROFILE_PATH + "/95DAFBDA41D7E9C71D28D6A2.canary"):
            raise Exception("No canary found in .gnupg profile folder. Ask for advice or delete that folder yourself.")

    if not config.resolution:
        raise Exception("Please tell me your display resolution in `config.py`")

    reset_profile("without_wkd")
    reset_profile("with_wkd")

    return True


if __name__ == "__main__":
    selfcheck()

    from sys import argv

    if len(argv) != 2:
        print("USAGE:\n\rpython run_study.py <first name of tester>")
        exit(1)

    name = argv[1].lower()

    pid = name[0] + name[-1] + secrets.token_hex(3)
    sids = [
        0, 1, 2, 3, 4, 5, 6, 7
    ]
    random.shuffle(sids)
    sids = "".join(map(lambda sid: str(sid), sids))

    base = "https://www.soscisurvey.de/email-study/"
    consent = f"?q=Congress-Consent&pid={pid}&eorder={sids}&scheme=openpgp"
    pre_questions = f"?q=Congress-PreQuestions&pid={pid}"

    # Step 0
    print("Close all Thunderbird and Firefox windows")
    print("")
    print("[press enter to continue]")

    input("")

    print(f"Hello, {pid}!")

    # Step 1
    firefox(base + consent)

    # Step 2
    firefox(base + pre_questions)

    print("[!] starting recording...")
    try:
        ffmpeg_handler = start_recording(pid)
    except Exception as e:
        print(e)
        exit(1)

    head = sids[:-1]
    tail = sids[-1]

    for (i, sid) in enumerate(head):
        thunderbird(sid)
        email = f"?q=Congress-Emails&pid={pid}&eid={sid}&mailnr={i}"
        firefox(base + email)

    post_questions = f"?q=Congress-PostQuestions&pid={pid}&eid={tail}"
    thunderbird(tail)
    firefox(base + post_questions)


    stop_recording(ffmpeg_handler)
    time.sleep(5)
    open("final.txt", "at").write(f"{pid},{name},openpgp,\"{datetime.datetime.now()}\"\n")
    print("goodbye")
