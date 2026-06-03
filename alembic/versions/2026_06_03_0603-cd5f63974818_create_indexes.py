"""create indexes

Revision ID: cd5f63974818
Revises: d78f2970ccdd
Create Date: 2026-06-03 06:03:58.984320

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'cd5f63974818'
down_revision: Union[str, Sequence[str], None] = 'd78f2970ccdd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        -- users
        CREATE INDEX idx_users_user_role_id ON users (user_role_id);
        CREATE UNIQUE INDEX uq_users_login ON users(login);
        
        -- entities
        CREATE UNIQUE INDEX uq_entities_code ON entities (code);
        
        -- role_permissions
        CREATE INDEX idx_role_permissions_role_id ON role_permissions (role_id);
        CREATE INDEX idx_role_permissions_entity_id ON role_permissions (entity_id);
        CREATE UNIQUE INDEX uq_role_permissions_role_entity ON role_permissions (role_id, entity_id);
        
        -- delivery_items
        CREATE INDEX idx_delivery_items_stock_delivery_id
        ON delivery_items(stock_delivery_id);
        CREATE INDEX idx_delivery_items_material_id
        ON delivery_items(medical_material_id);
        
        -- issue_items
        CREATE INDEX idx_issue_items_issue_id ON issue_items(material_issue_id);
        CREATE INDEX idx_issue_items_material_id ON issue_items(medical_material_id);
        
        -- stock_deliveries
        CREATE INDEX idx_stock_deliveries_supplier_id ON stock_deliveries(supplier_id);
        CREATE INDEX idx_stock_deliveries_delivery_date ON stock_deliveries(delivery_date);
        
        -- material_issues
        CREATE INDEX idx_material_issues_department_id ON material_issues(department_id);
        CREATE INDEX idx_material_issues_from_user_id ON material_issues(from_user_id);
        CREATE INDEX idx_material_issues_to_user_id ON material_issues(to_user_id);
        CREATE INDEX idx_material_issues_issue_date ON material_issues(issue_date);
        
        -- material_operations
        CREATE INDEX idx_material_operations_material_id ON material_operations(medical_material_id);
        CREATE INDEX idx_material_operations_department_id ON material_operations(department_id);
        CREATE INDEX idx_material_operations_user_id ON material_operations(current_user_id);
        CREATE INDEX idx_material_operations_date ON material_operations(operation_date);
        
        -- department_to_user
        CREATE INDEX idx_department_to_user_department_id ON department_to_user(department_id);
        CREATE INDEX idx_department_to_user_user_id ON department_to_user(user_id);
    ''')


def downgrade() -> None:
    """Downgrade schema."""
    # users
    op.drop_index('idx_users_user_role_id', table_name='users')

    # entities
    op.drop_index('uq_entities_code', table_name='entities')

    # role_permissions
    op.drop_index('idx_role_permissions_role_id', table_name='role_permissions')
    op.drop_index('idx_role_permissions_entity_id', table_name='role_permissions')
    op.drop_index('uq_role_permissions_role_entity', table_name='role_permissions')

    # delivery_items
    op.drop_index('idx_delivery_items_stock_delivery_id', table_name='delivery_items')
    op.drop_index('idx_delivery_items_material_id', table_name='delivery_items')

    # issue_items
    op.drop_index('idx_issue_items_issue_id', table_name='issue_items')
    op.drop_index('idx_issue_items_material_id', table_name='issue_items')

    # stock_deliveries
    op.drop_index('idx_stock_deliveries_supplier_id', table_name='stock_deliveries')
    op.drop_index('idx_stock_deliveries_delivery_date', table_name='stock_deliveries')

    # material_issues
    op.drop_index('idx_material_issues_department_id', table_name='material_issues')
    op.drop_index('idx_material_issues_from_user_id', table_name='material_issues')
    op.drop_index('idx_material_issues_to_user_id', table_name='material_issues')
    op.drop_index('idx_material_issues_issue_date', table_name='material_issues')

    # material_operations
    op.drop_index('idx_material_operations_material_id', table_name='material_operations')
    op.drop_index('idx_material_operations_department_id', table_name='material_operations')
    op.drop_index('idx_material_operations_user_id', table_name='material_operations')
    op.drop_index('idx_material_operations_date', table_name='material_operations')

    # department_to_user
    op.drop_index('idx_department_to_user_department_id', table_name='department_to_user')
    op.drop_index('idx_department_to_user_user_id', table_name='department_to_user')
