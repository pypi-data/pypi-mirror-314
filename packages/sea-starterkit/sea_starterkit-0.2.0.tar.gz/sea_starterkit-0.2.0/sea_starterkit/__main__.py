"""
A module to designed to perform package installations, and verification of install,
in preparation for the StructuralPython "Python for Structural Engineers" ("pfse")
course.
"""

import importlib.util
import importlib
import pathlib
import platform
import psutil
import subprocess
import time
import warnings
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, track
from rich.markdown import Markdown
from rich.text import Text

console = Console()


def check_installs():
    """
    Runs various mini-scripts to validate that certain packages
    are installed correctly. Offers suggestions for remediation if not.
    """
    header = Markdown("# Python for Structural Engineers ('PfSE') _Accelerated_")
    addl_installs = Markdown("## Installing additional package for Linux...")
    addl_installs.style = "yellow"
    console.print(header)
    console.print(addl_installs)

    ipyk_install = Markdown("## Installing pfse Jupyter kernel...")
    ipyk_install.style = "yellow"
    install_pfse_kernel()
    validating = Markdown("## Validating installed packages...")
    validating.style = "yellow"
    console.print(validating)

    funcs = [
        check_streamlit,
        check_numpy,
        check_shapely,
        check_sectionproperties,
        check_openpyxl,
    ]
    msgs = []
    for func in track(funcs):
        msg = func()
        if msg is not None:
            msgs.append(msg)
        time.sleep(0.2)

    if len(msgs) != 0:
        for msg in msgs:
            if msg is not None:
                console.print(msg)
        notify = Markdown("# Inconsistencies encoutered")
        notify.style = "red"
        instructions = Markdown(
            "### Please use Ctrl-Shift-C to copy the above error messages and email them to connor@structuralpython.com"
        )
        instructions.style = "red"
        console.print(notify)
        console.print(instructions)
    else:
        verified = Markdown("# PfSE installation seems ok")
        verified.style = "green"
        close_windows = Markdown(
            "## You can now close any windows that have opened as a result of the test."
        )
        close_windows.style = "green"
        console.print(verified)
        console.print(close_windows)


def check_streamlit():
    st_file = pathlib.Path(__file__).parent / "streamlit_test.py"
    try:
        proc = subprocess.Popen(
            ["streamlit", "run", str(st_file)],
            stdout=subprocess.PIPE
        )
        # proc.communicate("\n")
        time.sleep(4)
        proc.kill()

    except Exception as err:
        err_msg = Text("Streamlit did not run properly.")
        for err_arg in err.args:
            err_msg.append("\t" + err_arg + "\n")
        err_msg.stylize("bold magenta")
        return err_msg


def check_numpy():
    try:
        import numpy as np
    except Exception as err:
        err_msgs = Text("\nnumpy did not import properly:\n")
        for err_arg in err.args:
            err_msgs.append("\t" + err_arg + "\n")
        err_msgs.stylize("bold green")
        return err_msgs
    

def check_pandas():
    try:
        import pandas as pd
    except Exception as err:
        err_msgs = Text("\nnumpy did not import properly:\n")
        for err_arg in err.args:
            err_msgs.append("\t" + err_arg + "\n")
        err_msgs.stylize("bold green")
        return err_msgs


def check_shapely():
    try:
        from shapely import Polygon
    except Exception as err:
        err_msgs = Text("\nshapely did not import properly:\n")
        for err_arg in err.args:
            err_msgs.append("\t" + err_arg + "\n")
        err_msgs.stylize("bold cyan")
        return err_msgs


def check_sectionproperties():
    try:
        import sectionproperties.pre.library.primitive_sections as sections
        from sectionproperties.analysis.section import Section

        geometry = sections.circular_section(d=50, n=64)
        geometry.create_mesh(mesh_sizes=[2.5])
    except Exception as err:
        err_msgs = Text("\nsectionproperties example did not run properly:\n")
        for err_arg in err.args:
            err_msgs.append("\t" + err_arg + "\n")
        err_msgs.stylize("bold cyan")
        return err_msgs


def check_openpyxl():
    try:
        from openpyxl import Workbook

        wb = Workbook()
        dest_filename = "empty_book.xlsx"
        saved_file = pathlib.Path.home() / dest_filename
        wb.save(filename=saved_file)
        if not saved_file.exists():
            raise Exception(f"No file found: {saved_file}")
        else:
            saved_file.unlink()
    except Exception as err:
        err_msgs = Text("\nopenpyxl example did not run properly:\n")
        for err_arg in err.args:
            err_msgs.append("\t" + err_arg + "\n")
        err_msgs.stylize("bold yellow")
        return err_msgs

def install_pfse_kernel():
    proc = subprocess.Popen(
        ["python", "-m", "ipykernel", "install", "--user", "--name", "pfse", "--display-name", "Python 3 (pfse)"],
        stdout=subprocess.PIPE,
        text=True,
    )
    msg = Text("PfSE Jupyter Kernel Installed Successfully")
    msg.stylize("bold green")
    console.print(msg)

if __name__ == "__main__":
    install_pfse_kernel()
    check_installs()
