#!/bin/bash

# Start jupyter lab
jupyter lab --notebook-dir=/opt/notebooks --ip='*' --port=8888 --no-browser --allow-root --NotebookApp.token=''
