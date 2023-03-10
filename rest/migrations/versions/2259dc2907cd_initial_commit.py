"""Initial commit

Revision ID: 2259dc2907cd
Revises: 
Create Date: 2023-03-07 21:48:52.465293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2259dc2907cd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('todo', sa.String(), nullable=True))
        batch_op.drop_column('text')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('text', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('todo')

    # ### end Alembic commands ###