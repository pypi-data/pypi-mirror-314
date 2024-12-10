#!/usr/bin/env python3
# type: ignore
# pylint: disable=no-member
"""
 Inspect and decode CAN messages with curses-based display

 Copyright (c) 2023-2024 ROX Automation - Jev Kuznetsov
"""
import collections
import curses
from pathlib import Path
from typing import Dict, NamedTuple

import can
from cantools.database import load_file as load_dbc

TIMEOUT = 1.0
HEADER_ROWS = 2  # Number of rows used for header


class MessageStats(NamedTuple):
    count: int
    last_message: str
    last_display: str = ""  # Track the last displayed string
    display_line: int = -1  # Line number where this message is displayed


class CANMonitor:
    def __init__(self, stdscr, bus: can.Bus, dbc_file: Path) -> None:
        self.stdscr = stdscr
        self.message_stats: Dict[int, MessageStats] = collections.defaultdict(
            lambda: MessageStats(0, "", "", -1)
        )
        self.bus = bus
        self.dbc = load_dbc(dbc_file)
        self.header_drawn = False
        self.next_available_line = HEADER_ROWS  # Start after header

        # Configure curses
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_YELLOW, -1)
        self.stdscr.nodelay(1)
        curses.curs_set(0)  # Hide the cursor

    def get_display_line(self, msg_id: int) -> int:
        """Get or assign a display line for a message ID"""
        stats = self.message_stats[msg_id]
        if stats.display_line == -1:
            # Assign next available line
            line = self.next_available_line
            self.next_available_line += 1
            # Update the message stats with the assigned line
            self.message_stats[msg_id] = MessageStats(
                stats.count, stats.last_message, stats.last_display, line
            )
            return line
        return stats.display_line

    def update_display(self):
        # Draw header only once
        if not self.header_drawn:
            header = "CAN Bus Monitor - Press 'q' to quit"
            self.stdscr.addstr(0, 0, header, curses.A_BOLD)
            self.stdscr.addstr(1, 0, "-" * len(header))
            self.header_drawn = True

        # Display messages
        for msg_id, stats in self.message_stats.items():
            line = f"[{stats.count:6d}] ID 0x{msg_id:04x}: {stats.last_message}"

            # Only update if line has changed
            if line != stats.last_display:
                try:
                    display_line = self.get_display_line(msg_id)
                    if display_line >= curses.LINES - 1:  # Skip if beyond screen
                        continue

                    self.stdscr.move(display_line, 0)
                    self.stdscr.clrtoeol()  # Clear current line
                    self.stdscr.addstr(display_line, 0, line[: curses.COLS - 1])
                    # Update the stored display
                    self.message_stats[msg_id] = MessageStats(
                        stats.count, stats.last_message, line, display_line
                    )
                except curses.error:
                    pass

        self.stdscr.refresh()

    def process_message(self, msg):
        if msg is None:
            return

        msg_id = msg.arbitration_id

        # Prepare message display string
        if msg.is_remote_frame:
            db_msg = self.dbc.get_message_by_frame_id(msg_id)
            display_str = f"RTR: {db_msg.name}"
        else:
            try:
                db_msg = self.dbc.get_message_by_frame_id(msg_id)
                decoded = db_msg.decode(msg.data)
                display_str = f"{db_msg.name}: {decoded}"
            except KeyError:
                display_str = f"{msg_id} Raw: {msg.data.hex(' ')}"

        # Update statistics while preserving the display line
        current_stats = self.message_stats[msg_id]
        self.message_stats[msg_id] = MessageStats(
            count=current_stats.count + 1,
            last_message=display_str,
            last_display=current_stats.last_display,
            display_line=current_stats.display_line,
        )

    def run(self):

        try:
            while True:
                # Check for quit command
                try:
                    key = self.stdscr.getch()
                    if key == ord("q"):
                        break
                except curses.error:
                    pass

                # Process CAN message
                msg = self.bus.recv(TIMEOUT)
                self.process_message(msg)
                self.update_display()

        finally:
            self.bus.shutdown()


def main(dbc_file: Path, interface: str = "socketcan", channel: str = "can0"):
    """Main function"""
    canbus = can.Bus(channel, interface)
    curses.wrapper(lambda stdscr: CANMonitor(stdscr, canbus, dbc_file).run())
