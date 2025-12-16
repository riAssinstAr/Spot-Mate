from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
from prompt_toolkit import prompt
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.formatted_text import ANSI
import shutil


def select_from_list(title, text, options):
    index = 0
    term_height = shutil.get_terminal_size().lines - 5
    offset = 0

    def render():
        nonlocal offset
        if index < offset:
            offset = index
        elif index >= offset + term_height:
            offset = index - term_height + 1

        fragments = [
            ("class:title", title + "\n"),
            ("class:text", text + "\n\n"),
        ]
        visible = options[offset : offset + term_height]

        for i, opt in enumerate(visible):
            real_i = offset + i
            if real_i == index:
                fragments.append(("class:selected", f"> {opt}\n"))
            else:
                fragments.append(("class:option", f"  {opt}\n"))

        return FormattedText(fragments)

    kb = KeyBindings()

    @kb.add("up")
    def _(_):
        nonlocal index
        index = (index - 1) % len(options)

    @kb.add("down")
    def _(_):
        nonlocal index
        index = (index + 1) % len(options)

    @kb.add("enter")
    def _(_):
        app.exit(result=options[index])

    @kb.add("escape")
    @kb.add("c-c")
    def _(_):
        app.exit(result=None)

    style = Style.from_dict({
        "title": "bold #F5D2D2",
        "text": "#F8F7BA",
        "option": "#BDE3C3",
        "selected": "bold #A3CCDA bg:#005f87",
    })

    control = FormattedTextControl(render)
    window = Window(content=control, wrap_lines=False)
    app = Application(layout=Layout(window), style=style, key_bindings=kb, full_screen=False)
    return app.run()


def confirm(message):
    while True:
        choice = input(f"{message} [y/n], this action cannot be undone: ").strip().lower()
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
