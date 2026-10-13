"""PuzzleGraph — DAG builder for puzzle dependencies + solvability check."""

from __future__ import annotations

import random

import networkx as nx

from escape_room.models.puzzle_schema import Puzzle


class UnsolvableRoomError(RuntimeError):
    """Raised when the generated graph has no valid entry -> exit path."""


class PuzzleGraph:
    """Wraps a networkx DiGraph with escape-room semantics."""

    def __init__(self, rng: random.Random) -> None:
        self._rng = rng
        self._g: nx.DiGraph = nx.DiGraph()
        self.entry_id: str = ""
        self.exit_id: str = ""

    def link(self, puzzles: list[Puzzle], red_herring_ratio: float) -> None:
        if not puzzles:
            raise UnsolvableRoomError("no puzzles to link")
        for p in puzzles:
            self._g.add_node(p.puzzle_id, puzzle=p)

        # Linear spine guarantees solvability.
        for a, b in zip(puzzles, puzzles[1:]):
            self._g.add_edge(a.puzzle_id, b.puzzle_id)
            b.depends_on = sorted(set(b.depends_on) | {a.puzzle_id})

        # Random extra edges create branching without breaking the DAG.
        n_extra = max(1, int(len(puzzles) * red_herring_ratio))
        for _ in range(n_extra):
            i, j = sorted(self._rng.sample(range(len(puzzles)), 2))
            if not nx.has_path(self._g, puzzles[j].puzzle_id, puzzles[i].puzzle_id):
                self._g.add_edge(puzzles[i].puzzle_id, puzzles[j].puzzle_id)
                puzzles[j].depends_on = sorted(set(puzzles[j].depends_on) | {puzzles[i].puzzle_id})

        self.entry_id = puzzles[0].puzzle_id
        self.exit_id = puzzles[-1].puzzle_id
        if not nx.has_path(self._g, self.entry_id, self.exit_id):
            raise UnsolvableRoomError("entry cannot reach exit")

    def fingerprint(self) -> str:
        return nx.weisfeiler_lehman_graph_hash(self._g)

    def topological_order(self) -> list[str]:
        return list(nx.topological_sort(self._g))