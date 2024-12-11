class Subject(object):
    def __init__(self):
        self.listens = []

    def add_listen(self, listen):
        self.listens.append(listen)

    def remove_listen(self, listen):
        self.listens.remove(listen)

    def notify_listens(self, message, **kwargs):
        pass


class Listen(object):
    def on_message(self, message):
        pass


class TagListen(Listen):
    def __init__(self):
        self._tag = 0

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value
        self._tag_changed()

    def _tag_changed(self):
        if self.tag == -1:
            print(f"资源缺失")


# 创建一个全局的监听器
tag_listener = TagListen()
