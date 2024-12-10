
# Embedded nodes

This folder contains code for testing can bus communication with physical devices.
The code is written in Circuitpython and will run on any compatible hardware that supports `canio`.

## How it works

1. **Alice** sens a message with id `0x01` and `uint32` counter value.
2. **Bob**
    - receives the message
    - checks that the counter values are consecutive (missing messages check)
    - replies with an echo message with id `0x02`, containing the counter and error counters.
3. **Alice**
    - waits for reply from Bob,
    - checks for correct counter value
    - measures echo times
    - sends a new message


* Both nodes continuously monitor bus state and errors
* Alice measures number of cycles per second


## Development

0. install `invoke`, `circup` and `rsync`
1. connect board, check with `invoke find-device`
2. init board `invoke init`
3. copy `alice.py` or `bob.py`  as `main.py` to CIRCUITPY drive
