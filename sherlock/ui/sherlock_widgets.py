from random import randint

from rich.panel import Panel
from rich.color import Color
from rich.text import Text
from rich.table import Table
from rich.style import Style, StyleType
from rich.console import Console, ConsoleOptions, RenderableType
from textual.widgets import Header, Footer, FileClick, ScrollView, Placeholder
from textual.widget import Widget

from sherlock.ui.constants import SHERLOCK_COLORS

class SherlockHeader(Header):
    def __init__(self, *, tall: bool = True, style: StyleType = SHERLOCK_COLORS["PhthaloGreen"], clock: bool = True) -> None:
        super().__init__(tall=tall, style=style, clock=clock)

    def render(self) -> RenderableType:
        title =Text.assemble(("Sherlock Stream ", SHERLOCK_COLORS["SlimyGreen"]))# Text(self.full_title)
        header_table = Table.grid(padding=(0, 1), expand=True)
        header_table.style = self.style
        header_table.add_column(justify="left", ratio=0, width=8)
        header_table.add_column("title", justify="center", ratio=1)
        header_table.add_column("clock", justify="right", width=8)
        header_table.add_row(
            "🕵️", title, self.get_clock() if self.clock else ""
        )
        header: RenderableType
        header = Panel(header_table, style=self.style) if self.tall else header_table
        return header

class SherlockFooter(Footer):
    def __init__(self, *args, **kw) -> None:
        super().__init__(*args, **kw)

    def make_key_text(self) -> Text:
        """Create text containing all the keys."""
        text = Text(
            style=SHERLOCK_COLORS["PhthaloGreen"],
            no_wrap=True,
            overflow="ellipsis",
            justify="left",
            end="",
        )
        for binding in self.app.bindings.shown_keys:
            key_display = (
                binding.key.upper()
                if binding.key_display is None
                else binding.key_display
            )
            hovered = self.highlight_key == binding.key
            key_text = Text.assemble(
                (f" {key_display} ", "reverse" if hovered else "default on default"),
                f" {binding.description} ",
                meta={"@click": f"app.press('{binding.key}')", "key": binding.key},
            )
            text.append_text(key_text)
        return text

class LogListView(Widget):

    def render(self):
        table = Table(width=45, 
            style=SHERLOCK_COLORS["SlimyGreen"],
            header_style=SHERLOCK_COLORS["SlimyGreen"],
            show_header = False)

        for _ in range(2000):
            table.add_row(Text(f"FunctionCalled __init__.py {randint(100,999)}", style=SHERLOCK_COLORS["SlimyGreen"]))
        
       
        return table