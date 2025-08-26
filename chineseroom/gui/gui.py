import urwid
from chineseroom import seer


class ChineseRoomGUI:
    def __init__(self):
        self.palette = [
            ('bg', 'white', 'dark red'),
            ('text', 'black', 'white')
        ]
        self.messages = urwid.SimpleListWalker([])
        self.listbox = urwid.ListBox(self.messages)
        self.edit = urwid.Edit("You:\n")
        self.padded_edit = urwid.Filler(
            self.edit, valign='middle', top=1, bottom=1)

        self.frame = urwid.Frame(
            header=None,
            body=self.listbox,
            footer=urwid.Padding(self.padded_edit, left=2, right=2),
        )
        self.frame.focus_position = "footer"

        ats = urwid.AttrMap(urwid.SolidFill(" "), 'bg')
        self.screen = urwid.Overlay(self.frame, ats, align="center",
                                    width=70, valign="middle", height=20)

        self.loop = urwid.MainLoop(
            self.screen, palette=self.palette, unhandled_input=self.unhandled_input)

    def on_ask(self, button=None):
        question = self.edit.edit_text.strip()
        if question.lower() == "quit":
            raise urwid.ExitMainLoop()

        # update on message sent
        self.frame.footer = urwid.Padding(urwid.Text(
            "sending message..."), left=2, right=2)
        self.loop.draw_screen()

        # establish connection with the void
        client = seer.Seer()
        answer = client.ask(question)
        self.messages.append(urwid.Padding(urwid.Text(
            ("text", f"you:\n{question}\n")), left=2, right=2))
        self.messages.append(urwid.Padding(urwid.Text(
            ("text", f"chinese room:\n{answer}\n\n")), left=2, right=2))
        self.edit.edit_text = ""
        self.listbox.set_focus(len(self.messages) - 1)

        # restore input box
        self.frame.footer = urwid.Padding(self.padded_edit, left=2, right=2)
        self.frame.focus_position = "footer"
        self.loop.draw_screen()  # Redraw to update UI

    def unhandled_input(self, key):
        if key in {"q", "Q"}:
            raise urwid.ExitMainLoop()
        if key == "enter":
            self.on_ask()

    def run(self):
        self.loop.run()


if __name__ == "__main__":
    gui = ChineseRoomGUI()
    gui.run()
