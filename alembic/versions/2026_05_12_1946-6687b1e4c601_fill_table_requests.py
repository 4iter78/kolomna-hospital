"""fill table requests

Revision ID: 6687b1e4c601
Revises: e5ab770ca3b9
Create Date: 2026-05-12 19:46:21.755793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '6687b1e4c601'
down_revision: Union[str, Sequence[str], None] = 'e5ab770ca3b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        INSERT INTO requests (request_file) VALUES
            ('requests/req_001.pdf'),
            ('requests/req_002.pdf'),
            ('requests/req_003.docx'),
            ('requests/req_004.pdf'),
            ('requests/req_005.docx'),
            ('requests/req_006.pdf'),
            ('requests/req_007.pdf'),
            ('requests/req_008.docx'),
            ('requests/req_009.pdf'),
            ('requests/req_010.pdf');
    ''')


def downgrade() -> None:
    op.execute('''
        DELETE FROM requests
        WHERE request_file IN (
            'requests/req_001.pdf',
            'requests/req_002.pdf',
            'requests/req_003.docx',
            'requests/req_004.pdf',
            'requests/req_005.docx',
            'requests/req_006.pdf',
            'requests/req_007.pdf',
            'requests/req_008.docx',
            'requests/req_009.pdf',
            'requests/req_010.pdf'
        );
    ''')
