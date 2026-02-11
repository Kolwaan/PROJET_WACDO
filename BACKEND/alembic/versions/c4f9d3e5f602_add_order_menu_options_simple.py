"""add_order_menu_options_table

Revision ID: c4f9d3e5f602
Revises: 8c7e7ad1a714
Create Date: 2026-02-11 10:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4f9d3e5f602'
down_revision: Union[str, Sequence[str], None] = '8c7e7ad1a714'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Créer la table order_menu_options pour stocker les options choisies pour chaque menu
    # Options = frites/potatoes + boisson
    op.create_table(
        'order_menu_options',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('menu_id', sa.Integer(), nullable=False),
        sa.Column('option_product_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], ),
        sa.ForeignKeyConstraint(['option_product_id'], ['products.id'], ),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Créer des index pour améliorer les performances
    op.create_index('ix_order_menu_options_order_id', 'order_menu_options', ['order_id'])
    op.create_index('ix_order_menu_options_menu_id', 'order_menu_options', ['menu_id'])


def downgrade() -> None:
    # Supprimer les index
    op.drop_index('ix_order_menu_options_menu_id', table_name='order_menu_options')
    op.drop_index('ix_order_menu_options_order_id', table_name='order_menu_options')
    
    # Supprimer la table
    op.drop_table('order_menu_options')
