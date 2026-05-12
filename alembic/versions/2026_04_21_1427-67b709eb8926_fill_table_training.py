"""fill table training

Revision ID: 67b709eb8926
Revises: 52012fb52346
Create Date: 2026-04-21 14:27:26.385754

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '67b709eb8926'
down_revision: Union[str, Sequence[str], None] = '52012fb52346'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        INSERT INTO training (name, special_type_id) VALUES
            ('Работа с аппаратом МРТ: базовый курс',       (SELECT id FROM special_type WHERE name ='МРТ')),
            ('Работа с аппаратом МРТ: продвинутый курс',   (SELECT id FROM special_type WHERE name ='МРТ')),
            ('Рентген-диагностика: основы',                (SELECT id FROM special_type WHERE name ='Рентген')),
            ('Рентген-диагностика: интерпретация снимков', (SELECT id FROM special_type WHERE name ='Рентген')),
            ('Флюорография: техника проведения',           (SELECT id FROM special_type WHERE name ='Флюорография')),
            ('Флюорография: безопасность и дозиметрия',    (SELECT id FROM special_type WHERE name ='Флюорография'));
    ''')
    pass

def downgrade() -> None:
    op.execute('''
        DELETE FROM training WHERE name IN ('Работа с аппаратом МРТ: базовый курс',
            'Работа с аппаратом МРТ: продвинутый курс',
            'Рентген-диагностика: основы',
            'Рентген-диагностика: интерпретация снимков',
            'Флюорография: техника проведения',
            'Флюорография: безопасность и дозиметрия');
    ''')
    pass
