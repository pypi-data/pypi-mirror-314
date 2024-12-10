""" send can messages and measure loop timing on Feather M4 CAN """

# pylint: disable=import-error
import time
import struct
import asyncio
import board
import canio
import digitalio

from common import can_init, check_bus_state

VERSION = "1.3.0"


led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()


can_bus = can_init()


async def send_messages() -> None:
    """send messages with counter value, wait for a response from BOB"""

    listener = can_bus.listen(matches=[canio.Match(id=0x02)], timeout=1.0)

    counter = 0

    while True:

        # time measurement
        start_time_ns = time.monotonic_ns()
        total_echo_time_ns = 0
        max_echo_time_ns = 0

        N_CYCLES = 1000

        for _ in range(N_CYCLES):
            # Send a message with the counter value
            counter += 1
            counter &= 0xFFFFFFFF
            message = canio.Message(id=0x01, data=struct.pack("<I", counter))
            can_bus.send(message)
            t_msg_sent = time.monotonic_ns()

            # Wait for a response from BOB
            msg = listener.receive()
            if msg is None:
                print("No response from BOB")
                led.value = True
                continue

            echo_time_ns = time.monotonic_ns() - t_msg_sent
            max_echo_time_ns = max(max_echo_time_ns, echo_time_ns)
            total_echo_time_ns += echo_time_ns

            bob_counter, _, _ = struct.unpack("<IBB", msg.data)
            if bob_counter != counter:
                print(f"Counter mismatch: {counter} != {bob_counter}")
                led.value = True
            else:
                led.value = False

            await asyncio.sleep(0)

        # time measurement
        elapsed_time_ns = time.monotonic_ns() - start_time_ns
        messages_per_second = (N_CYCLES * 1_000_000_000) / elapsed_time_ns
        avg_echo_time_ms = total_echo_time_ns / N_CYCLES / 1_000_000
        print(
            f"Messages per second: {messages_per_second:.1f}, avg echo time: {avg_echo_time_ms:.1f} ms, max echo time: {max_echo_time_ns / 1_000_000:.1f} ms"
        )


async def main() -> None:

    print(f"ALICE node version {VERSION}")

    await asyncio.gather(check_bus_state(can_bus), send_messages())


if __name__ == "__main__":

    asyncio.run(main())
