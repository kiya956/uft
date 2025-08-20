"""handle send command to host"""

import logging
import os
import signal
import subprocess as Subprocess

from universal_flash.err import FAILED, SUCCESS



# pylint: disable=R1732
def syscmd(
    message="",
    timeout=300,
    as_user=False,
):
    """send command to host system"""
    try:
        if as_user:
            escaped_message = message.replace('"', '\\"')
            message = f'su ubuntu -c "{escaped_message}"'

        p = Subprocess.Popen(
            message,
            shell=True,
            start_new_session=True,  # We need a session, then it can pass down signal
            text=True,
            close_fds=True,
        )
        p.communicate(timeout=timeout)  # waits & reaps

        if p.returncode != 0:
            print(f"command {message} failed (rc={p.returncode})")
            return FAILED

    except Subprocess.TimeoutExpired:
        print(f"command {message} timeout, timeout={timeout}")
        try:
            os.killpg(
                p.pid, signal.SIGTERM
            )  # Politely signal the process to terminate
        except ProcessLookupError:
            pass

        try:
            p.communicate(timeout=3)  # reap
        except Subprocess.TimeoutExpired:
            try:
                # failed to terminate
                # Need to nuclear it
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            p.communicate()  # reap

        return FAILED

    return SUCCESS

