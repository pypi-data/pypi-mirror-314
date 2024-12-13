from textual.widgets import DataTable
from rich.text import Text

class MageTable(DataTable):
    def __init__(self, editor, turns):
        super().__init__(id='mage_table')
        self.editor = editor
        self.turns = turns

    def on_mount(self):
        self.cursor_type = 'cell'
        self.zebra_stripes = True
        #self.fixed_columns = 1
        skill_union = set()
        for m in self.turns[len(self.turns) - 1].end_mages:
            for skill_level in m.skill_levels:
                if skill_level.name != '':
                    skill_union.add(skill_level.name)
        self.trained_skills = list(skill_union)
        self.trained_skills.sort()

        # self.add_column('Mage', key='Mage')
        for skill in self.trained_skills:
            self.add_column(skill, key=skill)
        for m1 in self.turns[0].start_mages:
            row = []
            # row.append(f'{m1.name} ({m1.id})')
            for skill in self.trained_skills:
                row.append('')
            self.add_row(*row, height=1, key=f'{m1.id}')
        self.update()

    def update(self):
        if hasattr(self, 'trained_skills'):
            widget = self.editor.query_one(f'#study_table')
            turn = widget.get_turn_num()
            for m1,m2 in zip(self.turns[turn].start_mages, self.turns[turn].end_mages):
                for skill in self.trained_skills:
                    d1 = m1.get_skill_level_and_days(skill)
                    d2 = m2.get_skill_level_and_days(skill)
                    if d2 != '0(0)':
                        if d1 == d2:
                            self.update_cell(str(m1.id), skill, f'{d1}', update_width=True)
                        else:
                            self.update_cell(str(m1.id), skill, Text(f'{d1}>{d2}', style='italic #1DAC23'), update_width=True)
                    else:
                        self.update_cell(str(m1.id), skill, f'')
            widget.on_data_table_cell_highlighted()

    def highlight(self, row, col, study):
        if study == 'TEACH' or study == '':
            self.cursor_type = 'row'
            self.move_cursor(row = row, column = 0, animate = True)
        else:
            self.cursor_type = 'cell'
            self.move_cursor(row = row, column = col, animate = True)
