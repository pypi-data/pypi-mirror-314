""" receive can messages and measure loop timing on Feather M4 CAN """

# pylint: disable=import-error

import asyncio
import struct

import board
import canio
import digitalio

from common import can_init, check_bus_state

VERSION = "1.2.0"

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()


can_bus = can_init()


async def echo_messages() -> None:

    # match counter messages
    can_listener = can_bus.listen(matches=[canio.Match(id=0x01)], timeout=2.0)

    count_errors = 0

    msg = can_listener.receive()
    if msg is None:
        raise ValueError("No counter message received")

    prev_counter = struct.unpack("<I", msg.data)[0]

    while True:

        msg = can_listener.receive()
        if msg is None:
            print("No counter message received")
            led.value = True
            continue

        counter = struct.unpack("<I", msg.data)[0]

        led.value = False

        # check for consecutive counter values, ignore wrap-around
        if counter != prev_counter + 1 and counter > prev_counter:
            count_errors += 1

        prev_counter = counter

        nr_bus_errors = can_bus.receive_error_count + can_bus.transmit_error_count

        # Send an echo message
        can_bus.send(
            canio.Message(
                id=0x02,
                data=struct.pack(
                    "<IBB", counter, count_errors & 0xFF, nr_bus_errors & 0xFF
                ),
            )
        )
        await asyncio.sleep(0)


async def main() -> None:
    """main function"""

    print(f"BOB node version: {VERSION}")
    await asyncio.gather(check_bus_state(can_bus), echo_messages())


if __name__ == "__main__":
    asyncio.run(main())
