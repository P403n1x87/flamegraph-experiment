This repository contains the code for the experiment presented in the paper
"On the Algebraic Properties of Flame Graphs".

## How to run the experiment

The experiment has been run with CPython 3.9 and Austin 3.4.1 (from the Snap
store) on Ubuntu 22.04. We recommend creating a virtual environment and
installing the dependencies with

~~~console
pip install -r requirements.txt`
~~~

The data can be collected by running the `collect_data.sh` bash script. The
samples will be saved in the `data` directory. The experiment can then be run
with

~~~console
python experiment.py
~~~

The output will contain the p-value and the Delta decomposition of the
difference of the average flame graph, with stacks filtered out as described in
the paper.

This is the result we obtained with a run of the experiment

~~~
p-value: 1.1102230246251565e-16

Δ+: {'<frozen importlib._bootstrap>:_find_and_load:1007;<frozen importlib._bootstrap>:_find_and_load_unlocked:986;<frozen importlib._bootstrap>:_load_unlocked:680;<frozen importlib._bootstrap_external>:exec_module:850;<frozen importlib._bootstrap>:_call_with_frames_removed:228;/usr/lib/python3.9/site.py:<module>:605;/usr/lib/python3.9/site.py:main:598;/usr/lib/python3.9/site.py:execsitecustomize:537;<frozen importlib._bootstrap>:_find_and_load:1007;<frozen importlib._bootstrap>:_find_and_load_unlocked:986;<frozen importlib._bootstrap>:_load_unlocked:680;<frozen importlib._bootstrap_external>:exec_module:850;<frozen importlib._bootstrap>:_call_with_frames_removed:228;sitecustomize.py:<module>:5': 100297.26}

Δ-: {'/usr/lib/python3.9/runpy.py:_run_module_as_main:197;/usr/lib/python3.9/runpy.py:_run_code:87;main.py:<module>:19;main.py:c:15;main.py:b:10;main.py:a:6': 50009.46000000002}
~~~
