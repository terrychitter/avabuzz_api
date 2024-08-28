"""Initial migration

Revision ID: f0c2f3d12784
Revises: 
Create Date: 2024-08-18 21:40:47.921990

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f0c2f3d12784'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_reactions')
    op.drop_table('post_reaction_types')
    with op.batch_alter_table('user_followers', schema=None) as batch_op:
        batch_op.drop_index('followee_user_id')
        batch_op.drop_index('idx_followee_user_id')
        batch_op.drop_index('idx_follower_user_id')

    op.drop_table('user_followers')
    op.drop_table('post_comment_likes')
    with op.batch_alter_table('user_groups', schema=None) as batch_op:
        batch_op.drop_index('idx_owner_id')
        batch_op.drop_index('idx_public_group_id')
        batch_op.drop_index('public_group_id')

    op.drop_table('user_groups')
    op.drop_table('post_categories')
    with op.batch_alter_table('user_public_id_sequence', schema=None) as batch_op:
        batch_op.drop_index('current_value')

    op.drop_table('user_public_id_sequence')
    op.drop_table('group_stats')
    op.drop_table('user_private_id_sequence')
    op.drop_table('post_reaction_counts')
    op.drop_table('post_hashtags')
    op.drop_table('post_media')
    with op.batch_alter_table('blocked_users', schema=None) as batch_op:
        batch_op.drop_index('blocker_id')
        batch_op.drop_index('idx_blocked_id')
        batch_op.drop_index('idx_blocker_id')

    op.drop_table('blocked_users')
    with op.batch_alter_table('user_group_members', schema=None) as batch_op:
        batch_op.drop_index('idx_group_member_role')
        batch_op.drop_index('user_id')

    op.drop_table('user_group_members')
    with op.batch_alter_table('giveaways', schema=None) as batch_op:
        batch_op.drop_index('unq_giveaways_event_id')

    op.drop_table('giveaways')
    with op.batch_alter_table('event_participants', schema=None) as batch_op:
        batch_op.drop_index('unq_event_participants_group_id')
        batch_op.drop_index('unq_event_participants_group_id_0')
        batch_op.drop_index('unq_event_participants_user_id')
        batch_op.drop_index('unq_event_participants_user_id_0')

    op.drop_table('event_participants')
    op.drop_table('posts')
    with op.batch_alter_table('hashtags', schema=None) as batch_op:
        batch_op.drop_index('hashtag_name')
        batch_op.drop_index('hashtag_name_2')

    op.drop_table('hashtags')
    op.drop_table('post_comments')
    with op.batch_alter_table('group_followers', schema=None) as batch_op:
        batch_op.drop_index('idx_group_followers_group_id')

    op.drop_table('group_followers')
    with op.batch_alter_table('giveaway_winners', schema=None) as batch_op:
        batch_op.drop_index('unq_giveaway_winners_group_id')
        batch_op.drop_index('unq_giveaway_winners_user_id')

    op.drop_table('giveaway_winners')
    with op.batch_alter_table('group_profile_accessories', schema=None) as batch_op:
        batch_op.drop_index('idx_active_badge_id')
        batch_op.drop_index('idx_active_banner_id')

    op.drop_table('group_profile_accessories')
    with op.batch_alter_table('post_events', schema=None) as batch_op:
        batch_op.drop_index('unq_post_events_post_id')

    op.drop_table('post_events')
    op.drop_table('post_comment_like_counts')
    with op.batch_alter_table('owned_accessories', schema=None) as batch_op:
        batch_op.alter_column('created_at',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
        batch_op.drop_index('idx_accessory_id')
        batch_op.drop_index('idx_group_id')
        batch_op.drop_index('idx_user_id')
        batch_op.drop_index('user_id')
        batch_op.drop_constraint('owned_accessories_ibfk_3', type_='foreignkey')
        batch_op.drop_constraint('owned_accessories_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('owned_accessories_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['private_user_id'])
        batch_op.create_foreign_key(None, 'profile_accessories', ['accessory_id'], ['accessory_id'])
        batch_op.drop_column('group_id')

    with op.batch_alter_table('profile_accessories', schema=None) as batch_op:
        batch_op.alter_column('available',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False,
               existing_server_default=sa.text("'1'"))
        batch_op.alter_column('default_accessory',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False,
               existing_server_default=sa.text("'0'"))
        batch_op.alter_column('owner_count',
               existing_type=mysql.INTEGER(),
               nullable=False,
               existing_server_default=sa.text("'0'"))
        batch_op.alter_column('created_at',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
        batch_op.drop_index('idx_available')
        batch_op.drop_index('idx_ownership_type')
        batch_op.drop_index('idx_profile_accessory_type')
        batch_op.drop_index('idx_profile_type')

    with op.batch_alter_table('user_profile_accessories', schema=None) as batch_op:
        batch_op.alter_column('active_banner_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('active_profile_picture_border_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('active_badge_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.drop_index('idx_active_banner_id')
        batch_op.drop_index('idx_active_profile_picture_border_id')
        batch_op.drop_constraint('user_profile_accessories_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('user_profile_accessories_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('user_profile_accessories_ibfk_3', type_='foreignkey')
        batch_op.create_foreign_key(None, 'owned_accessories', ['active_banner_id'], ['owned_accessory_id'])
        batch_op.create_foreign_key(None, 'owned_accessories', ['active_profile_picture_border_id'], ['owned_accessory_id'])
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['private_user_id'])
        batch_op.create_foreign_key(None, 'owned_accessories', ['active_badge_id'], ['owned_accessory_id'])

    with op.batch_alter_table('user_stats', schema=None) as batch_op:
        batch_op.alter_column('follower_count',
               existing_type=mysql.INTEGER(),
               nullable=False,
               existing_server_default=sa.text('(0)'))
        batch_op.alter_column('following_count',
               existing_type=mysql.INTEGER(),
               nullable=False,
               existing_server_default=sa.text('(0)'))
        batch_op.alter_column('post_count',
               existing_type=mysql.INTEGER(),
               nullable=False,
               existing_server_default=sa.text('(0)'))
        batch_op.drop_constraint('fk_user_stats_users', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['private_user_id'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('profile_picture_url',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True,
               existing_server_default=sa.text("'https://placehold.co/400'"))
        batch_op.alter_column('gender',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True,
               existing_server_default=sa.text("'None'"))
        batch_op.alter_column('country',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True,
               existing_server_default=sa.text("'None'"))
        batch_op.alter_column('orientation',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True,
               existing_server_default=sa.text("'None'"))
        batch_op.alter_column('user_type',
               existing_type=mysql.ENUM('user', 'moderator', 'admin'),
               type_=sa.Enum('user', 'admin', 'moderator', name='usertype'),
               existing_nullable=False,
               existing_server_default=sa.text("'user'"))
        batch_op.alter_column('created_at',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
        batch_op.drop_index('gender_id')
        batch_op.drop_index('idx_active')
        batch_op.drop_index('idx_created_at')
        batch_op.drop_index('idx_email')
        batch_op.drop_index('idx_username')
        batch_op.drop_index('orientation_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index('orientation_id', ['orientation'], unique=False)
        batch_op.create_index('idx_username', ['username'], unique=False)
        batch_op.create_index('idx_email', ['email'], unique=False)
        batch_op.create_index('idx_created_at', ['created_at'], unique=False)
        batch_op.create_index('idx_active', ['active'], unique=False)
        batch_op.create_index('gender_id', ['gender'], unique=False)
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
        batch_op.alter_column('user_type',
               existing_type=sa.Enum('user', 'admin', 'moderator', name='usertype'),
               type_=mysql.ENUM('user', 'moderator', 'admin'),
               existing_nullable=False,
               existing_server_default=sa.text("'user'"))
        batch_op.alter_column('orientation',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False,
               existing_server_default=sa.text("'None'"))
        batch_op.alter_column('country',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False,
               existing_server_default=sa.text("'None'"))
        batch_op.alter_column('gender',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False,
               existing_server_default=sa.text("'None'"))
        batch_op.alter_column('profile_picture_url',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False,
               existing_server_default=sa.text("'https://placehold.co/400'"))

    with op.batch_alter_table('user_stats', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('fk_user_stats_users', 'users', ['user_id'], ['private_user_id'], onupdate='CASCADE', ondelete='CASCADE')
        batch_op.alter_column('post_count',
               existing_type=mysql.INTEGER(),
               nullable=True,
               existing_server_default=sa.text('(0)'))
        batch_op.alter_column('following_count',
               existing_type=mysql.INTEGER(),
               nullable=True,
               existing_server_default=sa.text('(0)'))
        batch_op.alter_column('follower_count',
               existing_type=mysql.INTEGER(),
               nullable=True,
               existing_server_default=sa.text('(0)'))

    with op.batch_alter_table('user_profile_accessories', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('user_profile_accessories_ibfk_3', 'owned_accessories', ['active_profile_picture_border_id'], ['owned_accessory_id'], ondelete='SET NULL')
        batch_op.create_foreign_key('user_profile_accessories_ibfk_2', 'owned_accessories', ['active_banner_id'], ['owned_accessory_id'], ondelete='SET NULL')
        batch_op.create_foreign_key('user_profile_accessories_ibfk_1', 'users', ['user_id'], ['private_user_id'], ondelete='CASCADE')
        batch_op.create_index('idx_active_profile_picture_border_id', ['active_profile_picture_border_id'], unique=False)
        batch_op.create_index('idx_active_banner_id', ['active_banner_id'], unique=False)
        batch_op.alter_column('active_badge_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.alter_column('active_profile_picture_border_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.alter_column('active_banner_id',
               existing_type=mysql.INTEGER(),
               nullable=True)

    with op.batch_alter_table('profile_accessories', schema=None) as batch_op:
        batch_op.create_index('idx_profile_type', ['profile_type'], unique=False)
        batch_op.create_index('idx_profile_accessory_type', ['profile_accessory_type'], unique=False)
        batch_op.create_index('idx_ownership_type', ['ownership_type'], unique=False)
        batch_op.create_index('idx_available', ['available'], unique=False)
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
        batch_op.alter_column('owner_count',
               existing_type=mysql.INTEGER(),
               nullable=True,
               existing_server_default=sa.text("'0'"))
        batch_op.alter_column('default_accessory',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True,
               existing_server_default=sa.text("'0'"))
        batch_op.alter_column('available',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True,
               existing_server_default=sa.text("'1'"))

    with op.batch_alter_table('owned_accessories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('group_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('owned_accessories_ibfk_2', 'user_groups', ['group_id'], ['private_group_id'], ondelete='CASCADE')
        batch_op.create_foreign_key('owned_accessories_ibfk_1', 'users', ['user_id'], ['private_user_id'], ondelete='CASCADE')
        batch_op.create_foreign_key('owned_accessories_ibfk_3', 'profile_accessories', ['accessory_id'], ['accessory_id'], ondelete='CASCADE')
        batch_op.create_index('user_id', ['user_id', 'group_id', 'accessory_id'], unique=True)
        batch_op.create_index('idx_user_id', ['user_id'], unique=False)
        batch_op.create_index('idx_group_id', ['group_id'], unique=False)
        batch_op.create_index('idx_accessory_id', ['accessory_id'], unique=False)
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    op.create_table('post_comment_like_counts',
    sa.Column('post_comment_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('post_comment_like_count', mysql.INTEGER(), server_default=sa.text("'0'"), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['post_comment_id'], ['post_comments.post_comment_id'], name='post_comment_like_counts_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_comment_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('post_events',
    sa.Column('post_event_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('event_name', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('event_description', mysql.MEDIUMTEXT(), nullable=True),
    sa.Column('start_date', mysql.DATETIME(), server_default=sa.text('(now())'), nullable=False),
    sa.Column('end_date', sa.DATE(), nullable=False),
    sa.Column('event_type', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('post_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.post_id'], name='fk_post_events_posts'),
    sa.PrimaryKeyConstraint('post_event_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('post_events', schema=None) as batch_op:
        batch_op.create_index('unq_post_events_post_id', ['post_id'], unique=True)

    op.create_table('group_profile_accessories',
    sa.Column('group_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('active_banner_id', mysql.INTEGER(), server_default=sa.text("'4'"), autoincrement=False, nullable=True),
    sa.Column('active_badge_id', mysql.INTEGER(), server_default=sa.text("'5'"), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['active_badge_id'], ['owned_accessories.owned_accessory_id'], name='group_profile_accessories_ibfk_3', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['active_banner_id'], ['owned_accessories.owned_accessory_id'], name='group_profile_accessories_ibfk_2', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['group_id'], ['user_groups.private_group_id'], name='group_profile_accessories_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('group_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('group_profile_accessories', schema=None) as batch_op:
        batch_op.create_index('idx_active_banner_id', ['active_banner_id'], unique=False)
        batch_op.create_index('idx_active_badge_id', ['active_badge_id'], unique=False)

    op.create_table('giveaway_winners',
    sa.Column('giveaway_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('group_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['giveaway_id'], ['giveaways.giveaway_id'], name='fk_giveaway_winners_giveaways', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['group_id'], ['event_participants.group_id'], name='fk_giveaway_winners_event_participants_0', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['event_participants.user_id'], name='fk_giveaway_winners_event_participants', onupdate='CASCADE', ondelete='CASCADE'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('giveaway_winners', schema=None) as batch_op:
        batch_op.create_index('unq_giveaway_winners_user_id', ['user_id', 'giveaway_id'], unique=True)
        batch_op.create_index('unq_giveaway_winners_group_id', ['group_id', 'giveaway_id'], unique=True)

    op.create_table('group_followers',
    sa.Column('group_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', mysql.VARCHAR(length=10), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['user_groups.private_group_id'], name='fk_group_followers_user_groups', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.private_user_id'], name='fk_group_followers_users', onupdate='CASCADE', ondelete='CASCADE'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('group_followers', schema=None) as batch_op:
        batch_op.create_index('idx_group_followers_group_id', ['group_id', 'user_id'], unique=False)

    op.create_table('post_comments',
    sa.Column('post_comment_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('post_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', mysql.VARCHAR(length=10), nullable=False),
    sa.Column('post_comment_text', mysql.TEXT(), nullable=False),
    sa.Column('post_comment_status', mysql.ENUM('NORMAL', 'HIDEEN', 'FLAGGED'), nullable=True),
    sa.Column('parent_post_comment_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['parent_post_comment_id'], ['post_comments.post_comment_id'], name='post_comments_ibfk_3', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['post_id'], ['posts.post_id'], name='post_comments_ibfk_1', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.private_user_id'], name='post_comments_ibfk_2', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_comment_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('hashtags',
    sa.Column('hashtag_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('hashtag_name', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('views', mysql.INTEGER(), server_default=sa.text('(0)'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('hashtag_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('hashtags', schema=None) as batch_op:
        batch_op.create_index('hashtag_name_2', ['hashtag_name'], unique=False)
        batch_op.create_index('hashtag_name', ['hashtag_name'], unique=True)

    op.create_table('posts',
    sa.Column('post_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('post_caption', mysql.TEXT(), nullable=True),
    sa.Column('post_type', mysql.VARCHAR(length=20), server_default=sa.text("'post'"), nullable=True),
    sa.Column('post_category_id', mysql.INTEGER(), server_default=sa.text("'1'"), autoincrement=False, nullable=True),
    sa.Column('user_id', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('group_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('view_count', mysql.INTEGER(), server_default=sa.text("'0'"), autoincrement=False, nullable=True),
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.CheckConstraint('((`user_id` is not null) or (`group_id` is not null))', name='posts_chk_1'),
    sa.ForeignKeyConstraint(['group_id'], ['user_groups.private_group_id'], name='posts_ibfk_2', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['post_category_id'], ['post_categories.post_category_id'], name='posts_ibfk_3', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['users.private_user_id'], name='posts_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('event_participants',
    sa.Column('event_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('group_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['post_events.post_event_id'], name='fk_event_participants_post_events', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['group_id'], ['user_groups.private_group_id'], name='fk_event_participants_user_groups', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.private_user_id'], name='fk_event_participants_users', onupdate='CASCADE', ondelete='CASCADE'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('event_participants', schema=None) as batch_op:
        batch_op.create_index('unq_event_participants_user_id_0', ['user_id'], unique=True)
        batch_op.create_index('unq_event_participants_user_id', ['user_id', 'event_id'], unique=True)
        batch_op.create_index('unq_event_participants_group_id_0', ['group_id'], unique=True)
        batch_op.create_index('unq_event_participants_group_id', ['group_id', 'event_id'], unique=True)

    op.create_table('giveaways',
    sa.Column('giveaway_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('giveaway_status', mysql.ENUM('Not Started', 'Running', 'Ended'), server_default=sa.text("'Not Started'"), nullable=False),
    sa.Column('event_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['post_events.post_event_id'], name='fk_giveaways_post_events', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('giveaway_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('giveaways', schema=None) as batch_op:
        batch_op.create_index('unq_giveaways_event_id', ['event_id'], unique=True)

    op.create_table('user_group_members',
    sa.Column('membership_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', mysql.VARCHAR(length=10), nullable=False),
    sa.Column('group_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('group_member_role', mysql.ENUM('owner', 'admin', 'member'), server_default=sa.text("'member'"), nullable=True),
    sa.Column('joined_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['user_groups.private_group_id'], name='user_group_members_ibfk_2', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.private_user_id'], name='user_group_members_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('membership_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('user_group_members', schema=None) as batch_op:
        batch_op.create_index('user_id', ['user_id', 'group_id'], unique=True)
        batch_op.create_index('idx_group_member_role', ['group_member_role'], unique=False)

    op.create_table('blocked_users',
    sa.Column('blocked_users_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('blocker_id', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('blocked_id', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('blocked_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['blocked_id'], ['users.private_user_id'], name='blocked_users_ibfk_2', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['blocker_id'], ['users.private_user_id'], name='blocked_users_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('blocked_users_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('blocked_users', schema=None) as batch_op:
        batch_op.create_index('idx_blocker_id', ['blocker_id'], unique=False)
        batch_op.create_index('idx_blocked_id', ['blocked_id'], unique=False)
        batch_op.create_index('blocker_id', ['blocker_id', 'blocked_id'], unique=True)

    op.create_table('post_media',
    sa.Column('post_media_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('post_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('media_url', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('media_type', mysql.VARCHAR(length=50), server_default=sa.text("'IMAGE'"), nullable=True),
    sa.Column('media_size_bytes', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('media_order', mysql.INTEGER(), server_default=sa.text("'1'"), autoincrement=False, nullable=True),
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.post_id'], name='post_media_ibfk_1', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_media_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('post_hashtags',
    sa.Column('post_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('hashtag_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['hashtag_id'], ['hashtags.hashtag_id'], name='post_hashtags_ibfk_2', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['post_id'], ['posts.post_id'], name='post_hashtags_ibfk_1', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_id', 'hashtag_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('post_reaction_counts',
    sa.Column('post_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('post_reaction_type', mysql.VARCHAR(length=20), server_default=sa.text('(0)'), nullable=False),
    sa.Column('reaction_count', mysql.INTEGER(), server_default=sa.text('(0)'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.post_id'], name='fk_post_reaction_counts_posts'),
    sa.ForeignKeyConstraint(['post_reaction_type'], ['post_reaction_types.post_reaction_type'], name='fk_post_reaction_counts_post_reaction_types'),
    sa.PrimaryKeyConstraint('post_reaction_type', 'post_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('user_private_id_sequence',
    sa.Column('id', mysql.VARCHAR(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('group_stats',
    sa.Column('group_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('post_count', mysql.INTEGER(), server_default=sa.text('(0)'), autoincrement=False, nullable=False),
    sa.Column('follower_count', mysql.INTEGER(), server_default=sa.text('(0)'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['user_groups.private_group_id'], name='fk_group_stats_user_groups', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('group_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('user_public_id_sequence',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('current_value', mysql.CHAR(length=7), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('user_public_id_sequence', schema=None) as batch_op:
        batch_op.create_index('current_value', ['current_value'], unique=True)

    op.create_table('post_categories',
    sa.Column('post_category_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('post_category_name', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('post_category_description', mysql.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('post_category_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('user_groups',
    sa.Column('private_group_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('public_group_id', mysql.VARCHAR(length=10), nullable=False),
    sa.Column('group_name', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('group_description', mysql.TEXT(), nullable=True),
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('owner_id', mysql.VARCHAR(length=10), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.private_user_id'], name='user_groups_ibfk_1', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('private_group_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('user_groups', schema=None) as batch_op:
        batch_op.create_index('public_group_id', ['public_group_id'], unique=True)
        batch_op.create_index('idx_public_group_id', ['public_group_id'], unique=False)
        batch_op.create_index('idx_owner_id', ['owner_id'], unique=False)

    op.create_table('post_comment_likes',
    sa.Column('post_comment_like_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('post_comment_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', mysql.VARCHAR(length=10), nullable=False),
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['post_comment_id'], ['post_comments.post_comment_id'], name='post_comment_likes_ibfk_1', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.private_user_id'], name='post_comment_likes_ibfk_2', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_comment_like_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('user_followers',
    sa.Column('follow_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('followee_user_id', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('follower_user_id', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('followed_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['followee_user_id'], ['users.private_user_id'], name='user_followers_ibfk_1', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['follower_user_id'], ['users.private_user_id'], name='user_followers_ibfk_2', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('follow_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('user_followers', schema=None) as batch_op:
        batch_op.create_index('idx_follower_user_id', ['follower_user_id'], unique=False)
        batch_op.create_index('idx_followee_user_id', ['followee_user_id'], unique=False)
        batch_op.create_index('followee_user_id', ['followee_user_id', 'follower_user_id'], unique=True)

    op.create_table('post_reaction_types',
    sa.Column('post_reaction_type', mysql.VARCHAR(length=20), nullable=False),
    sa.PrimaryKeyConstraint('post_reaction_type'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('post_reactions',
    sa.Column('post_reaction_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('post_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', mysql.VARCHAR(length=10), nullable=False),
    sa.Column('post_reaction_type', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.post_id'], name='post_reactions_ibfk_1', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['post_reaction_type'], ['post_reaction_types.post_reaction_type'], name='post_reactions_ibfk_3', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.private_user_id'], name='post_reactions_ibfk_2', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_reaction_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###