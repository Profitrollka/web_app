"""Aded tag table and relationship with posts

Revision ID: 30d38b497198
Revises: 
Create Date: 2022-05-19 21:05:33.535067

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '30d38b497198'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('tag_name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('tag_id')
    )
    op.create_table('post_tags',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.post_id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.tag_id'], ),
    sa.PrimaryKeyConstraint('post_id', 'tag_id')
    )
    op.alter_column('post', 'created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.drop_table('post_tags')
    op.drop_table('tag')
    # ### end Alembic commands ###
