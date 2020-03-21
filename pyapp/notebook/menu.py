import sys

from note import Note, NoteBook


class Menu:
    """命令行交互菜单，提供选项让用户操作笔记"""
    def __init__(self):
        self.nb = NoteBook()
        self.choices = {
            "1": self.add_note,
            "2": self.display_notes,
            "3": self.search,
            "4": self.modify_note,
            "5": self.exit_app
        }
        
    def display_options(self):
        print("""
Interactive Menu:

1. add note
2. display notes
3. search
4. modify note
5. quit
""")

    def run(self):
        while True:
            self.display_options()
            choice = input("enter your option: ")
            try:
                self.choices[choice]()
            except KeyError:
                print("not valid option")

    def add_note(self):
        memo = input("memo: ")
        tag = input("tag: ")
        self.nb.new_note(memo, tag)
    
    def display_notes(self):
        for note in self.nb.notes:
            print(note)

    def search(self):
        filter = input("filter: ")
        notes = self.nb.search(filter)
        for note in notes:
            print(note)

    def modify_note(self):
        note_id = int(input("note id: "))
        memo = input("new memo: ")
        tag = input("new tag: ")
        if memo and tag:
            self.nb.modify_note(note_id, memo, tag)

    def exit_app(self):
        print("quit notebook app")
        sys.exit(0)


if __name__ == "__main__":
    menu = Menu()
    menu.run()