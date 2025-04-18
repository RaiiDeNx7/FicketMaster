"""Add price to Event model

Revision ID: 755b4f1f4ce7
Revises: 
Create Date: 2025-04-16 15:27:58.633627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '755b4f1f4ce7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', sa.Float(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_column('price')

    # ### end Alembic commands ###
