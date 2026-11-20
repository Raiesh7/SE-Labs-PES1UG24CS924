"""Hostel room allocation demonstration application."""
# pylint: disable=invalid-name

import html
import logging
import random
from flask import Flask, request
import yaml


rooms = {}
allocations = {}
waitlist = []
app = Flask(__name__)

CONFIG = """
blocks:
  A: {gender: M, rooms: 3, capacity: 2, fee: 4000}
  B: {gender: F, rooms: 2, capacity: 3, fee: 3500}
"""


def load_config(text=CONFIG):
    """Load room configuration and reset hostel state."""
    rooms.clear()
    allocations.clear()
    waitlist.clear()
    config = yaml.safe_load(text)

    for block, info in config["blocks"].items():
        for room_number in range(1, info["rooms"] + 1):
            room_id = f"{block}{room_number}"
            rooms[room_id] = {
                "gender": info["gender"],
                "capacity": info["capacity"],
                "fee": info["fee"],
                "occupants": [],
            }
    return config


def allocate_room(student_id, name, gender, year, preferred=None):
    """Allocate a compatible room to a student."""
    if not isinstance(year, int) or isinstance(year, bool):
        return None

    if student_id in allocations:
        vacate_room(student_id)

    candidates = list(preferred or [])
    candidates.extend(
        room_id for room_id in rooms if room_id not in candidates
    )

    for room_id in candidates:
        room = rooms.get(room_id)
        if room is None:
            continue
        if room["gender"] != gender:
            continue
        if len(room["occupants"]) >= room["capacity"]:
            continue
        room["occupants"].append(student_id)
        allocations[student_id] = {
            "name": name,
            "room": room_id,
            "year": year,
        }
        return room_id

    if student_id not in waitlist:
        waitlist.append(student_id)
    return None


def vacate_room(student_id):
    """Remove a student from both the allocation and room occupant list."""
    allocation = allocations.pop(student_id, None)
    if allocation is None:
        return False

    room = rooms.get(allocation["room"])
    if room is not None and student_id in room["occupants"]:
        room["occupants"].remove(student_id)
    return True


def monthly_fee(student_id, days_stayed):
    """Calculate monthly-equivalent hostel fees."""
    allocation = allocations.get(student_id)
    if allocation is None:
        raise KeyError(f"Unknown student ID: {student_id}")
    if not isinstance(days_stayed, int) or days_stayed < 0:
        raise ValueError("days_stayed must be a non-negative integer")

    room = rooms[allocation["room"]]
    months = days_stayed // 30
    return months * room["fee"]


def priority_order(students):
    """Return students ordered from most senior to least senior."""
    return sorted(students, key=lambda student: student["year"], reverse=True)


def room_lottery(student_ids):
    """Randomize student IDs for a room lottery."""
    return random.SystemRandom().sample(list(student_ids), len(student_ids))


def vacant_beds():
    """Count every unoccupied bed across all rooms."""
    return sum(
        room["capacity"] - len(room["occupants"])
        for room in rooms.values()
    )


def connect_warden_db():
    """Return a mock Warden database connection status."""
    return sqlite_connect(
        host="localhost",
        user="warden",
        password=None,
    )


def sqlite_connect(host, user, password):
    """Build a read-only connection descriptor without exposing credentials."""
    del host, user
    if password:
        raise ValueError("Password material must not be passed in this demo")
    return {"connected": False, "mode": "credential-free demo"}


def start_remote_log_config():
    """Disable network logging for a secure local demonstration."""
    logging.disable(logging.CRITICAL)
    return {"enabled": False, "reason": "Remote logging disabled"}


@app.route("/room")
def room_lookup():
    """Render an escaped room lookup response."""
    student_id = request.args.get("id", "")
    allocation = allocations.get(student_id)
    return (
        "<h1>Room lookup</h1>"
        f"<p>Student: {html.escape(student_id)}</p>"
        f"<p>Allocation: {html.escape(str(allocation))}</p>"
    )


def run_portal():
    """Start the Flask portal in production-safe mode."""
    app.run(debug=False)


# Backward-compatible names used by the original assignment.
loadConfig = load_config
allocateRoom = allocate_room
vacateRoom = vacate_room
monthlyFee = monthly_fee
priorityOrder = priority_order
roomLottery = room_lottery
vacantBeds = vacant_beds
connectWardenDb = connect_warden_db
startRemoteLogConfig = start_remote_log_config
roomLookup = room_lookup
runPortal = run_portal


def main():
    """Demonstrate the hostel allocation operations."""
    load_config()
    print("Rooms:", list(rooms))
    print("S1 ->", allocate_room("S1", "Arjun", "M", 1))
    print("S2 ->", allocate_room("S2", "Kabir", "M", 2))
    print("S3 ->", allocate_room("S3", "Rohan", "M", 3))
    print("S4 (female) ->", allocate_room("S4", "Diya", "F", 1))
    print("S1 again ->", allocate_room("S1", "Arjun", "M", 1))
    print("S5 year '2' ->", allocate_room("S5", "Vikram", "M", "2"))
    print("Occupants of A1:", rooms["A1"]["occupants"])
    vacate_room("S2")
    print("Occupants of A1 after S2 left:", rooms["A1"]["occupants"])
    print("Fee for S1, 45 days:", monthly_fee("S1", 45))
    print(
        "Priority (senior first):",
        [student["year"] for student in priority_order(
            [{"year": 1}, {"year": 4}, {"year": 2}]
        )],
    )
    print("Lottery:", room_lottery(["S6", "S7", "S8"]))
    print("Vacant beds:", vacant_beds())
    print("Warden DB:", connect_warden_db())
    print("Waitlist:", waitlist)


if __name__ == "__main__":
    main()
