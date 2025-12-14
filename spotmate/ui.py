from prompt_toolkit import prompt
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.formatted_text import ANSI

def select_from_list(title, text, options):
    index = 0

    def render():
        lines = [title, text, ""]
        for i, opt in enumerate(options):
            prefix = "> " if i == index else "  "
            lines.append(f"{prefix}{opt}")
        return ANSI("\n".join(lines))

    kb = KeyBindings()

    @kb.add("up")
    def _(_):
        nonlocal index
        index = (index - 1) % len(options)
        app.invalidate()

    @kb.add("down")
    def _(_):
        nonlocal index
        index = (index + 1) % len(options)
        app.invalidate()

    @kb.add("enter")
    def _(_):
        app.exit(result=options[index])

    @kb.add("escape")
    @kb.add("c-c")
    def _(_):
        app.exit(result=None)

    control = FormattedTextControl(render)
    window = Window(content=control)
    app = Application(layout=Layout(window), key_bindings=kb, full_screen=False)
    return app.run()


def confirm(message):
    while True:
        choice = input(f"{message} [y/n]: ").strip().lower()
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False


def choose_range(tracks):
    total = len(tracks)
    print(f"Playlist contains {total} tracks")

    start = prompt_int("Start index: ")
    end = prompt_int("End index: ")
    if (
        start is None
        or end is None
        or start < 1
        or end < 1
        or start > end
        or end > total
    ):
        print("Invalid range!")
        return None

    return tracks[start - 1 : end]


def prompt_int(message, allow_empty=False):
    while True:
        val = prompt(message).strip()
        if allow_empty and val == "":
            return None
        try:
            return int(val)
        except ValueError:
            print("Please enter a valid number!")
