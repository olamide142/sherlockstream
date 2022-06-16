from textual.app import App
from textual.widget import Widget
from textual.reactive import Reactive
from rich.console import RenderableType
from rich.padding import Padding
from rich.align import Align
from rich.panel import Panel
from rich.text import Text

class Letter(Widget):

    label = Reactive("")

    def render(self) -> RenderableType:
        return Text(
            Align.center(Text(text=self.label), vertical="middle"),
            (0, 1),
            style="white on rgb(73,72,80)",
        )

class MainApp(App):

    async def on_mount(self) -> None:
        letter = Letter()
        letter.label = "A"
        await self.view.dock(letter)

MainApp.run(title="DeepWordle")