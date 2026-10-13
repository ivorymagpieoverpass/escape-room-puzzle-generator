"""Typer CLI — the operator's front door to the generator."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from escape_room.config.loader import load_config
from escape_room.core.room_builder import RoomBuilder
from escape_room.handlers.export_handler import ExportHandler
from escape_room.utils.logging import get_logger

app = typer.Typer(
    name="erpg",
    help="AI escape room & puzzle generator.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()
log = get_logger(__name__)


@app.command()
def generate(
    theme: str = typer.Option("abandoned-lab", help="Room theme key."),
    difficulty: int = typer.Option(3, min=1, max=10, help="1=easy, 10=brutal."),
    seed: int = typer.Option(6767, help="Deterministic RNG seed."),
    out: Optional[Path] = typer.Option(None, help="Output bundle path."),
    config: Path = typer.Option(Path("config/default.toml"), help="Config file."),
) -> None:
    """Generate a single room bundle from a theme + seed."""
    cfg = load_config(config)
    builder = RoomBuilder(cfg)
    room = builder.build(theme=theme, difficulty=difficulty, seed=seed)
    dest = out or cfg.paths.output_dir / f"{room.room_id}.json"
    ExportHandler(cfg).write_room(room, dest)
    console.print(f"[green]room built[/] -> {dest}")
    console.print(f"  puzzles: {len(room.puzzles)}  hints: {room.total_hints}")


@app.command()
def solve(room_path: Path) -> None:
    """Print a solution walkthrough for a generated room."""
    from escape_room.core.solver import RoomSolver

    cfg = load_config(Path("config/default.toml"))
    room = ExportHandler(cfg).read_room(room_path)
    walkthrough = RoomSolver(room).walkthrough()
    for i, step in enumerate(walkthrough, 1):
        console.print(f"{i:>2}. {step}")


@app.command()
def validate(room_path: Path) -> None:
    """Validate a room bundle against the schema."""
    from escape_room.models.room_schema import RoomBundle

    cfg = load_config(Path("config/default.toml"))
    room = ExportHandler(cfg).read_room(room_path)
    RoomBundle.model_validate(room.model_dump())
    console.print(f"[green]ok[/] {room.room_id} validates")


if __name__ == "__main__":
    app()