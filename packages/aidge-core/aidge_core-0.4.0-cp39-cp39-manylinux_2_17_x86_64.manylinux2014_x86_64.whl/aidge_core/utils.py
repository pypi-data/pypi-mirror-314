"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import queue
import threading
import subprocess
import pathlib
from typing import List


def template_docstring(template_keyword, text_to_replace):
    """Method to template docstring

    :param template: Template keyword to replace, in the documentation you template word must be between `{` `}`
    :type template: str
    :param text_to_replace: Text to replace your template with.
    :type text_to_replace: str
    """

    def dec(func):
        if "{" + template_keyword + "}" not in func.__doc__:
            raise RuntimeError(
                f"The function {func.__name__} docstring does not contain the template keyword: {template_keyword}."
            )
        func.__doc__ = func.__doc__.replace(
            "{" + template_keyword + "}", text_to_replace
        )
        return func

    return dec




def run_command(command: List[str], cwd: pathlib.Path = None):
    """
    This function has the job to run a command and return stdout and stderr that are not shown
    by subprocess.check_call / call.
    If the subprocess returns smthg else than 0, it will raise an error.
    Arg:
        command : written with the same syntax as subprocess.call
        cwd : path from where the command must be called

    Call example:
    ```python
        try:
            for std_line in run_command(
                [
                    "cmake",
                    str(self.EXPORT_PATH.absolute()),
                    "-DPYBIND=1",
                    f"-DCMAKE_INSTALL_PREFIX:PATH={install_path}",
                ],
                cwd=str(self.BUILD_DIR),
            ):
                print(std_line, end="")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}\nFailed to configure export.")
    ```
    """
    process = subprocess.Popen(
        command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    stdout_queue = queue.Queue()
    stderr_queue = queue.Queue()

    def enqueue_output(stream, queue_to_append):
        for line in iter(stream.readline, ""):
            queue_to_append.put(line)
        stream.close()

    stdout_thread = threading.Thread(
        target=enqueue_output, args=(process.stdout, stdout_queue)
    )
    stderr_thread = threading.Thread(
        target=enqueue_output, args=(process.stderr, stderr_queue)
    )
    stdout_thread.start()
    stderr_thread.start()

    while (
        stdout_thread.is_alive()
        or stderr_thread.is_alive()
        or not stdout_queue.empty()
        or not stderr_queue.empty()
    ):
        try:
            stdout_line = stdout_queue.get_nowait()
            yield stdout_line
        except queue.Empty:
            pass

        try:
            stderr_line = stderr_queue.get_nowait()
            yield stderr_line
        except queue.Empty:
            pass

    return_code = process.wait()
    if return_code != 0:
        raise subprocess.CalledProcessError(return_code, command)
