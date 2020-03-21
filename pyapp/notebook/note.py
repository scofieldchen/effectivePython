import datetime as dt


# 新笔记的id
last_id = 0

class Note:
    """笔记，拥有备忘录(memo),标签(tag)等属性
    笔记存储在笔记本中，由笔记本创建和修改
    """
    def __init__(self, memo, tag=""):
        self.memo = memo
        self.tag = tag
        global last_id
        last_id += 1
        self.id = last_id
        self.creation_date = dt.datetime.now()

    def __str__(self):
        return f"{self.id} memo:{self.memo} tag:{self.tag}"


class NoteBook:
    """笔记本，提供公共接口操作笔记"""
    def __init__(self):
        self.notes = []

    def new_note(self, memo, tag=""):
        self.notes.append(Note(memo, tag))

    def search(self, filter):
        return [note for note in self.notes if filter in note.memo or \
            filter in note.tag]

    def modify_note(self, note_id, memo=None, tag=None):
        for note in self.notes:
            if str(note.id) == str(note_id):
                if memo is not None:
                    note.memo = memo
                if tag is not None:
                    note.tag = tag
                break
