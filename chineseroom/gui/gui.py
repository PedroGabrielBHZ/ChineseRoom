import urwid
from chineseroom import gemini_client


palette = [
    ('bg', 'dark red', 'dark red'),
    ('text', 'black', 'white')
]

messages = urwid.SimpleListWalker([])
listbox = urwid.ListBox(messages)
edit = urwid.Edit("You:\n")
padded_edit = urwid.Filler(edit, valign='middle', top=1, bottom=1)


def on_ask(button):
    question = edit.edit_text.strip()
    if question.lower() == "quit":
        raise urwid.ExitMainLoop()
    # Show sending message
    frame.footer = urwid.Padding(urwid.Text(
        "sending message..."), left=2, right=2)
    loop.draw_screen()  # Force redraw to show the message

    client = gemini_client.GeminiClient()
    answer = client.ask(question)
    messages.append(urwid.Padding(urwid.Text(
        ("text", f"you:\n{question}\n")), left=2, right=2))
    messages.append(urwid.Padding(urwid.Text(
        ("text", f"chinese room:\n{answer}\n\n")), left=2, right=2))
    edit.edit_text = ""  # Clear input
    listbox.set_focus(len(messages) - 1)  # Scroll to bottom

    # Restore input box
    frame.footer = urwid.Padding(padded_edit, left=2, right=2)
    frame.focus_position = "footer"
    loop.draw_screen()  # Redraw to update UI


def unhandled_input(key):
    if key in {"q", "Q"}:
        raise urwid.ExitMainLoop()
    if key == "enter":
        on_ask(None)


frame = urwid.Frame(
    header=None,
    body=listbox,
    footer=urwid.Padding(padded_edit, left=2, right=2),
)

frame.focus_position = "footer"

ats = urwid.AttrMap(urwid.SolidFill(" "), 'bg')
screen = urwid.Overlay(frame, ats, align="center",
                       width=70, valign="middle", height=20)

loop = urwid.MainLoop(screen, palette=palette, unhandled_input=unhandled_input)
loop.run()
