# candbg tool


`candbg` is a simple tool that decodes canbus messages using a provided `dbc` file and shows them as a table.


    usage: candbg [-h] [-i INTERFACE] [-c CHANNEL] dbc_file

    candbg CLI

    positional arguments:
    dbc_file              Path to the DBC file

    options:
    -h, --help            show this help message and exit
    -i INTERFACE, --interface INTERFACE
                            Interface type (default: socketcan)
    -c CHANNEL, --channel CHANNEL
                            CAN channel (default: can0)



"screenshot":

    CAN Bus Monitor - Press 'q' to quit
    -----------------------------------
    [  9910] ID 0x0001: counter: {'counter': 25375238}
    [  9910] ID 0x0002: echo: {'counter': 25375238, 'count_errors': 0, 'bus_errors': 0}
