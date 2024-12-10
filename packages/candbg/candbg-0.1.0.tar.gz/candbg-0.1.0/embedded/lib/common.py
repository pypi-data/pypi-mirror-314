# pylint: disable=import-error

import asyncio
import board
import canio
import digitalio
import neopixel


def can_init() -> canio.CAN:
    """initialize the CAN bus"""
    # If the CAN transceiver has a standby pin, bring it out of standby mode
    if hasattr(board, "CAN_STANDBY"):
        standby = digitalio.DigitalInOut(board.CAN_STANDBY)
        standby.switch_to_output(False)

    # If the CAN transceiver is powered by a boost converter, turn on its supply
    if hasattr(board, "BOOST_ENABLE"):
        boost_enable = digitalio.DigitalInOut(board.BOOST_ENABLE)
        boost_enable.switch_to_output(True)

    # Use this line if your board has dedicated CAN pins. (Feather M4 CAN and Feather STM32F405)
    return canio.CAN(
        rx=board.CAN_RX, tx=board.CAN_TX, baudrate=500_000, auto_restart=True
    )


async def check_bus_state(bus: canio.CAN, delay: float = 2.0) -> None:
    """check & report errors and set neopixel color"""

    px = neopixel.NeoPixel(board.NEOPIXEL, 1)
    px.brightness = 0.1
    px.fill((0, 0, 255))

    while True:
        bus_state = bus.state
        print(
            f"Bus state: {bus_state} rx_errors: {bus.receive_error_count}, tx_errors: {bus.transmit_error_count}"
        )
        if bus_state != canio.BusState.ERROR_ACTIVE:
            px.fill((255, 0, 0))
        else:
            px.fill((0, 255, 0))

        await asyncio.sleep(delay)
