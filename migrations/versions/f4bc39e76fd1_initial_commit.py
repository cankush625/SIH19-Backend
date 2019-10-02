"""Initial commit

Revision ID: f4bc39e76fd1
Revises: 
Create Date: 2019-03-02 15:53:12.136502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4bc39e76fd1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('phone_number', sa.String(length=20), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('role', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_email'), 'admin', ['email'], unique=True)
    op.create_index(op.f('ix_admin_phone_number'), 'admin', ['phone_number'], unique=True)
    op.create_table('website',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('url', sa.String(length=150), nullable=False),
    sa.Column('http_status_code', sa.Integer(), nullable=True),
    sa.Column('message_sent', sa.Boolean(), nullable=True),
    sa.Column('remark', sa.String(length=200), nullable=False),
    sa.Column('approved', sa.Boolean(), nullable=True),
    sa.Column('verification_doc_url', sa.String(), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_website_url'), 'website', ['url'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_website_url'), table_name='website')
    op.drop_table('website')
    op.drop_index(op.f('ix_admin_phone_number'), table_name='admin')
    op.drop_index(op.f('ix_admin_email'), table_name='admin')
    op.drop_table('admin')
    # ### end Alembic commands ###
