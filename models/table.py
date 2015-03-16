from datetime import datetime
import os

#### USE db.tablename.drop() to fully get rid of a table

db.define_table('house',
                Field('title'),
                Field('rent', 'double'),
                Field('image', 'upload'),
                )

db.define_table('users',
                Field('name', 'text'),
                Field('first_name', 'text'),
                Field('last_name',  'text'),
                Field('house','text'),
                Field('rent','double'),
                Field('user_pic', 'upload'),
                )

db.define_table('user_list',
                Field('person', db.auth_user),
                Field('house', db.house),
                Field('pic', 'upload'),
                )

db.define_table('conversation',
                Field('subject'),
                Field('recent_post', 'datetime'),
                Field('house', db.house)
                )

db.define_table('conversation_message',
                Field('conversation_text', 'text'),
                Field('date_posted', 'datetime'),
                Field('person_posting', db.auth_user),
                Field('conversation_id', db.conversation)
                )

#db.bboard.id.readable = False
#db.bboard.sold.writeable = False
#db.bboard.bbmessage.label = 'Message'
#db.bboard.name.default = get_first_name()
#db.bboard.user_id.default = auth.user_id
#db.bboard.email.requires = IS_EMAIL()
#db.bboard.category.requires = IS_IN_SET(CATEGORY)
#db.bboard.category.required = True

#db.house.rent.requires = IS_FLOAT_IN_RANGE(0, 100000.0, error_message='The rent should be in the range 0..100000')
#db.house.title.required = True
db.users.firstname = auth.user.first_name if auth.user else "Anonymous"
db.users.lastname = auth.user.last_name if auth.user else "Anonymous"

db.house.rent.readable = db.house.rent.writable = False
