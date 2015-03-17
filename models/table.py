from datetime import datetime
import os

#### USE db.tablename.drop() to fully get rid of a table

db.define_table('house',
                Field('title'),
                Field('rent', 'double'),
                Field('image', 'upload'),
                Field('house_task_list', 'list:reference task_list')
                )

db.define_table('user_list',
                Field('person', db.auth_user),
                Field('house', db.house),
                Field('rent','double'),
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

db.define_table('task',
                Field('title'),
                Field('description', 'text'),
                )

db.define_table('task_list',
                Field('task_list_name'),
                Field('tasks', 'list:reference task'),
                )

db.task_list

#db.bboard.id.readable = False
#db.bboard.sold.writeable = False
#db.bboard.bbmessage.label = 'Message'
#db.bboard.name.default = get_first_name()
#db.bboard.user_id.default = auth.user_id
#db.bboard.email.requires = IS_EMAIL()
#db.bboard.category.requires = IS_IN_SET(CATEGORY)
#db.bboard.category.required = True

db.user_list.rent.requires = IS_FLOAT_IN_RANGE(0, 100000.0, error_message='The rent should be in the range 0..100000')
db.house.rent.requires = IS_FLOAT_IN_RANGE(0, 100000.0, error_message='The rent should be in the range 0..100000')
db.house.title.required = True
db.user_list.id.readable = False
db.user_list.person.writable = False
db.user_list.house.label = 'House ID'
db.user_list.rent.label = 'Your rent'
db.user_list.rent.default = 0
db.house.rent.default = 0
