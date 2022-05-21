"""Changed tag table

Revision ID: bbc2067de334
Revises: 2c6377cf6892
Create Date: 2022-05-21 12:29:13.989111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbc2067de334'
down_revision = '2c6377cf6892'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('tag_tag_name_key', 'tag', type_='unique')
    op.create_index(op.f('ix_tag_tag_name'), 'tag', ['tag_name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tag_tag_name'), table_name='tag')
    op.create_unique_constraint('tag_tag_name_key', 'tag', ['tag_name'])
    # ### end Alembic commands ###
