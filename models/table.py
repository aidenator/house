from datetime import datetime

def get_first_name():
    name = 'Nobody'
    if auth.user:
        name = auth.user.first_name
    return name

db.define_table('house',
                Field('users', 'json'),
                Field('title', 'text'),
                Field('tasks', 'json'),
                Field('rent', 'double'),
                Field('utilities','json'),
                Field('image', 'upload'),
                Field('date_posted', 'datetime'),
                )

db.define_table('users',
                Field('name', 'text'),
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
db.house.date_posted.writable = False
db.house.rent.requires = IS_FLOAT_IN_RANGE(0, 100000.0, error_message='The rent should be in the range 0..100000')
db.house.title.required = True
