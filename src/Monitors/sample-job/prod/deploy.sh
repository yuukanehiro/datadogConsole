#!/bin/sh

CURRENT=$(cd $(dirname $0);pwd)
cd $CURRENT

python3 ./CheckCpuUsage.py && \
python3 ./CheckDiskSpace.py && \
python3 ./CheckLoadAverage.py && \
python3 ./CheckMemoryFreeSpace.py && \
python3 ./CheckSwap.py && \
python3 ./CheckDatadogAgentStatus.py