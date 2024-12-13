from textual.widgets import Static, Footer, Input
from textual.validation import Validator, ValidationResult
from textual.app import ComposeResult
from textual.suggester import SuggestFromList

from Skill import *

skill_names = []
for skill in Skill.all_skills:
    skill_names.append(skill.name)
skill_names.append('TEACH')

class SkillValidator(Validator):
    def validate(self, value:str) -> ValidationResult:
        for skill_name in skill_names:
            if skill_name.lower().startswith(value.lower()):
                return self.success()
        return self.failure()

class PromptInput(Input):
    def __init__(self, editor, placeholder, suggester, validate_on, validators):
        super().__init__(placeholder = placeholder, suggester = suggester, validate_on = validate_on, validators = validators, id = f'prompt_input')
        self.editor = editor

    def on_input_changed(self, message: Input.Changed) -> None:
        if message.validation_result.is_valid == False:
            self.action_delete_left()

    def on_input_submitted(self, message: Input.Submitted) -> None:
        for skill_name in skill_names:
            if skill_name.lower() == (message.value.lower()):
                widget = self.editor.query_one(f'#study_table')
                if widget.can_update(message.value.upper()):
                    widget.update(message.value.upper())
                    self.clear()
                    widget.focus()

    def on_focus(self) -> None:
        pass

class Prompt(Static):
    def __init__(self, id, editor):
        super().__init__(id = id)
        self.editor = editor

    def compose(self) -> ComposeResult:
        yield PromptInput(self.editor,
                          placeholder="Type something...", 
                          suggester=SuggestFromList(skill_names, case_sensitive=False),
                          validate_on=['changed'],
                          validators=SkillValidator(skill_names))
        yield Footer()
