from datetime import datetime
import os

db.define_table('house',
                Field('title'),
                Field('tasks', 'json'),
                Field('rent', 'double'),
                Field('utilities','json'),
                Field('image', 'upload',),
                Field('date_posted', 'datetime'),
                Field('user1', 'string'),
                Field('user2', 'string'),
                Field('user3', 'string'),
                Field('user4', 'string'),
                Field('user5', 'string'),
                )

db.define_table('users',
                Field('name', 'text'),
                Field('first_name', 'text'),
                Field('last_name',  'text'),
                Field('house','text'),
                Field('rent','double'),
                Field('user_pic', 'upload'),
                )

#db.bboard.id.readable = False
#db.bboard.sold.writeable = False
#db.bboard.bbmessage.label = 'Message'
#db.bboard.name.default = get_first_name()
#db.bboard.user_id.default = auth.user_id
#db.bboard.email.requires = IS_EMAIL()
#db.bboard.category.requires = IS_IN_SET(CATEGORY)
#db.bboard.category.required = True

db.house.date_posted.default = datetime.utcnow()
#db.house.date_posted.writable = False
#db.house.rent.requires = IS_FLOAT_IN_RANGE(0, 100000.0, error_message='The rent should be in the range 0..100000')
#db.house.title.required = True
db.users.firstname = auth.user.first_name if auth.user else "Anonymous"
db.users.lastname = auth.user.last_name if auth.user else "Anonymous"
db.house.user1.default = auth.user.username if auth.user else ""
#db.house.user1.writable = False
db.house.user1.label = "Housemate 1"
db.house.user2.label = "Housemate 2"
db.house.user3.label = "Housemate 3"
db.house.user4.label = "Housemate 4"
db.house.user5.label = "Housemate 5"