"""RoomSolver — produces a human-readable walkthrough for QA + hint tuning."""

from __future__ import annotations

from escape_room.models.room_schema import RoomBundle


class RoomSolver:
    """Walks the dependency DAG and emits one line per required action."""

    def __init__(self, room: RoomBundle) -> None:
        self._room = room
        self._by_id = {p.puzzle_id: p for p in room.puzzles}

    def walkthrough(self) -> list[str]:
        order = self._topological_order()
        steps: list[str] = []
        for pid in order:
            p = self._by_id[pid]
            tag = " [red herring]" if p.is_red_herring else ""
            steps.append(f"{p.title}{tag}: {p.solution}")
        return steps

    def _topological_order(self) -> list[str]:
        indeg = {p.puzzle_id: len(p.depends_on) for p in self._room.puzzles}
        ready = [pid for pid, d in indeg.items() if d == 0]
        out: list[str] = []
        while ready:
            pid = ready.pop(0)
            out.append(pid)
            for q in self._room.puzzles:
                if pid in q.depends_on:
                    indeg[q.puzzle_id] -= 1
                    if indeg[q.puzzle_id] == 0:
                        ready.append(q.puzzle_id)
        if len(out) != len(self._room.puzzles):
            raise RuntimeError("cycle detected — room is unsolvable")
        return out