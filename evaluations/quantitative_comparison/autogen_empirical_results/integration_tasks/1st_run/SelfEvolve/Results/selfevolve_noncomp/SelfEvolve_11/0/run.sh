#
echo RUN.SH STARTING !#!#
export AUTOGEN_TESTBED_SETTING="Native"
echo "agbench version: 0.0.1a1" > timestamp.txt

# Create and activate the virtual environment
# This is called in a subprocess, and will not impact the parent
/home/aifahim/miniconda3/bin/python -m venv .agbench_venv
. .agbench_venv/bin/activate

# Run the global init script if it exists
if [ -f global_init.sh ] ; then
    . ./global_init.sh
fi

# Run the scenario init script if it exists
if [ -f scenario_init.sh ] ; then
    . ./scenario_init.sh
fi

# Run the scenario
pip install -r requirements.txt
echo SCENARIO.PY STARTING !#!#
start_time=$(date +%s)
timeout --preserve-status --kill-after 7230s 7200s python scenario.py
end_time=$(date +%s)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo SCENARIO.PY EXITED WITH CODE: $EXIT_CODE !#!#
else
    echo SCENARIO.PY COMPLETE !#!#
fi
elapsed_time=$((end_time - start_time))
echo "SCENARIO.PY RUNTIME: $elapsed_time !#!#"

# Clean up
if [ -d .cache ] ; then
    rm -Rf .cache
fi

if [ -d __pycache__ ] ; then
    rm -Rf __pycache__
fi

# Run the scenario finalize script if it exists
if [ -f scenario_finalize.sh ] ; then
    . ./scenario_finalize.sh
fi

# Run the global finalize script if it exists
if [ -f global_finalize.sh ] ; then
    . ./global_finalize.sh
fi

# We don't need to deactivate the venv because it's
# contained in the subprocess; but we should clean it up
if [ -d .agbench_venv ] ; then
    rm -Rf .agbench_venv
fi

echo RUN.SH COMPLETE !#!#
