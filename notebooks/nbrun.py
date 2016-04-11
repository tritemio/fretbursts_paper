# Copyright (c) 2015 Antonino Ingargiola
# License: MIT

import os
import time
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


def run_notebook(notebook_name, nb_suffix='-out', out_path='.', timeout=3600,
                 **execute_kwargs):
    """Runs a notebook and saves the output in the same notebook.

    Arguments:
        notebook_name (string): name of the notebook to be executed.
        nb_suffix (string): suffix to append to the file name of the executed
            notebook.
        timeout (int): timeout in seconds after which the execution is aborted.
        execute_kwargs (dict): additional arguments passed to
            `ExecutePreprocessor`.
        out_path (string): folder where to save the output notebook.
    """
    timestamp_cell = "**Executed:** %s\n\n**Duration:** %d seconds."

    if str(notebook_name).endswith('.ipynb'):
        notebook_name = str(notebook_name)[:-len('.ipynb')]
    nb_name_input = notebook_name + '.ipynb'
    nb_name_output = notebook_name + '%s.ipynb' % nb_suffix
    nb_name_output = os.path.join(out_path, nb_name_output)
    print('- Executing: ', nb_name_input, flush=True)

    if execute_kwargs is None:
        execute_kwargs = {}
    ep = ExecutePreprocessor(timeout=timeout, **execute_kwargs)
    nb = nbformat.read(nb_name_input, as_version=4)

    start_time = time.time()
    try:
        # Execute the notebook
        ep.preprocess(nb, {'metadata': {'path': './'}})
    except:
        # Execution failed, print a message then raise.
        msg = 'Error executing the notebook "%s".\n\n' % notebook_name
        msg += 'See notebook "%s" for the traceback.' % nb_name_output
        print(msg)
        raise
    else:
        # On successful execution, add timestamping cell
        duration = time.time() - start_time
        timestamp_cell = timestamp_cell % (time.ctime(start_time), duration)
        nb['cells'].insert(0, nbformat.v4.new_markdown_cell(timestamp_cell))
    finally:
        # Save the notebook even when it raises an error
        nbformat.write(nb, nb_name_output)
        print('* Output: ', nb_name_output, flush=True)

if __name__ == '__main__':
    from pathlib import Path

    print('Executing notebooks in current folder ... ')
    pathlist = list(Path('.').glob('*.ipynb'))
    for nbpath in pathlist:
        if not nbpath.stem.endswith('-out'):
            print(flush=True)
            run_notebook(nbpath)
