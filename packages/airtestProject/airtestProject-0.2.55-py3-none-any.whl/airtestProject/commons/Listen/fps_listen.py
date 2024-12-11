from airtestProject.commons.Listen.listen import Subject, Listen


class ApmSubject(Subject):
    def __init__(self):
        super().__init__()

    def notify_listens(self, msg, apm_type=None):
        for i in self.listens:
            i.on_message(msg, apm_type)


class ApmListen(Listen):

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_message(self, msg, apm_type=None):
        self.callback(msg, apm_type)


globalApmSubject = ApmSubject()
