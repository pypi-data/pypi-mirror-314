from textual.widgets import Input

class ValueInput(Input):
    def __init__(self, editor, header, callback, context):
        super().__init__(placeholder = header)
        self.editor = editor
        self.header = header
        self.callback = callback
        self.context = context

    def on_mount(self):
        pass

    def on_input_submitted(self, message: Input.Submitted):
        self.editor.value_entered(message.value, self.callback, self.context)
