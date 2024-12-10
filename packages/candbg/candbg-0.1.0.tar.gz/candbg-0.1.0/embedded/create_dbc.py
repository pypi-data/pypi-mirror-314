#!/usr/bin/env python3
""" create dbc file for candbg """

from cantools.database import Database, Message, Signal, dump_file


def byte_def_to_size(struct_byte_def: str) -> int:
    """convert byte definition to number of bytes"""
    symbols = {"<": 0, "B": 1, "H": 2, "I": 4}
    return sum([symbols[s] for s in struct_byte_def])


# --------------create message definition----------------

db = Database()

# counter message
counter_message = Message(
    frame_id=0x01,
    length=4,
    name="counter",
    signals=[
        Signal(
            name="counter",
            start=0,
            length=32,
        )
    ],
)

# echo message
echo_message = Message(
    frame_id=0x02,
    length=6,
    name="echo",
    signals=[
        Signal(
            name="counter",
            start=0,
            length=32,
        ),
        Signal(
            name="count_errors",
            start=32,
            length=8,
        ),
        Signal(
            name="bus_errors",
            start=40,
            length=8,
        ),
    ],
)


db.messages.append(counter_message)
db.messages.append(echo_message)

dump_file(db, "ping_pong.dbc")
