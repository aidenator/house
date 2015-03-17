#By Aiden Hoopes and Mark Manguray for CMPS 183 Winter 2015
import logging
from datetime import datetime
from datetime import date 
from calendar import monthrange

def index():
    message = ''
    listofhouses = ""
    logger.info("Username is = %r" % auth.user)

    if auth.user == None:
        redirect(URL('default', 'user', args = ['login']))

    return dict()

@auth.requires_login()
def house():
    users = []
    thehouse = None
    this_username = auth.user.username
    user_db = db(db.user_list.person == auth.user).select()

    if( len(user_db) == 0 ):
        db.user_list.insert(person = auth.user)


    this_user = db(db.user_list.person == auth.user).select().first()
    this_pic = this_user.pic if this_user.pic != None else ""

    if this_user.house != None:
        this_house = this_user.house
        housemates = db(db.user_list.house == this_house).select()
        house_task_list = this_house.house_task_list
    else:
        this_house = None
        housemates = None
        house_task_list = None

    #SETTINGS TAB CODE ---------------------
    record = db(db.user_list.person == auth.user).select().first()
    settingsform = SQLFORM(db.user_list, 
                           record = record,
                           upload=URL('download'),
                           )

    if settingsform.process().accepted:
        response.flash = "User settings saved!"
        redirect(URL('default', 'house'))

    elif settingsform.errors:
        response.flash = 'form has errors'

    #TASK TAB CODE --------------------------

    #PARENT TASK CODE
    parent_task_form = SQLFORM(db.task_list)
    if parent_task_form.process(session=None, formname='taskForm').accepted:
        new_task = db(db.task_list.id == parent_task_form.vars.id)
        new_task.update(task_list_name = parent_task_form.vars.task_list_name)

        thehouse = db(db.house.id == this_house).select().first()

        this_house_task_list = thehouse.house_task_list
        logger.info("tasklist is = %r" % this_house_task_list)

        if this_house_task_list == None:
            this_house_task_list = [parent_task_form.vars.id]
            logger.info("NEW tasklist is = %r" % this_house_task_list)
        else:
            this_house_task_list.append(parent_task_form.vars.id)

        db.house.update_or_insert(db.house.id == thehouse.id, house_task_list = this_house_task_list)

        logger.info("thehouse is = %r" % thehouse)
        response.flash = 'form accepted'
        redirect(URL('default', 'house'))
    elif parent_task_form.errors:
        response.flash = 'form has errors'

    #CHILD TASK CODE
    child_task_form = SQLFORM(db.task)
    if house_task_list != None:
        for task_list in house_task_list:
            tl = db(db.task_list.id == task_list).select().first()
            logger.info('tl is %r' %tl)

            if child_task_form.process(session=None, formname='child'+str(tl.id) ).accepted:
                new_tltask = db(db.task.id == child_task_form.vars.id)
                new_tltask.update(title = child_task_form.vars.title,
                                description = child_task_form.vars.description)
                new_tasks = tl.tasks
                if new_tasks == None:
                    new_tasks = [child_task_form.vars.id]
                else:
                    new_tasks.append(child_task_form.vars.id)

                db.task_list.update_or_insert(db.task_list.id == tl.id, tasks = new_tasks)

                redirect(URL('default', 'house'))

            elif child_task_form.errors:
                response.flash = 'form has errors'

        pass

    #Here I find how many days are in the current month and subtract it from today's day number
    #This will let me know how many days are left until rent is due
    today = date.today()
    today_day  = int( today.strftime('%d') ) # 3
    today_month= int( today.strftime('%m') ) # 16
    today_year = int( today.strftime('%Y') ) # 2015

    month_range = monthrange(today_year, today_month) #monthrange(2015, 3) = (1,31)
    rent_due = month_range[1] - today_day

    return dict(today = today_string(), 
                pic = this_pic, users=housemates, 
                thehouse = this_house, 
                settingsform = settingsform, 
                house_task_list = house_task_list,
                rent_due = rent_due
                )

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@auth.requires_login()
def add_house():
    creating = request.vars.action == 'create'
    joining = request.vars.action == 'join'
    join_house_id = request.vars.houseID
    joinform = ""

    #JOINING FORM CODE ----------------------------------------------
    logger.info("MADE IT HERE.")

    if joining and join_house_id != None:
        join_house = db(db.house.id == join_house_id).select().first()
        db.user_list.update_or_insert(db.user_list.person == auth.user, house=join_house)
        session.flash = 'House Joined!'
        redirect(URL('default', 'house'))

    elif joining and join_house_id == None:
        record = db(db.user_list.person == auth.user).select().first()
        joinform = SQLFORM(db.user_list,
                           record = record,
                           fields=['house'],
                          )
        if joinform.process().accepted:
            response.flash = "Joined house successfully!"
            redirect(URL('default','house'))
        elif joinform.errors:
            response.flash = 'form has errors'
            """checkhouse = db(db.house.id == joinform.vars.house).select()

            if len(checkhouse) <= 0:
                response.flash = "This house doesn't exist. You can create it though."
                redirect(URL('default','house'))

            db.user_list.update(db.user_list.person == auth.user, house = joinform.vars.house)"""


    #CREATING FORM CODE  --------------------------------------------
    form = SQLFORM( db.house,
                    fields=['title', 'image'],
                    upload=URL('download'),                          
                    )

    form.add_button('Go Back', URL('default', 'index'))

    if form.process().accepted:
        check = db(db.house.title == form.vars.title).select()
        new_houseID = db.house.insert(title=form.vars.title, image=form.vars.image)
        new_house = db(db.house.id == new_houseID).select().first()

        #Check if person is in Users DB, if so, update their house info, if not, add them with their new house
        db.user_list.update_or_insert(db.user_list.person == auth.user, house=new_house)
        session.flash = 'House Created!'

        redirect(URL('default', 'house'))

    elif form.errors:
        response.flash = 'form has errors'

    return dict(creating = creating, joining = joining, form = form, joinform = joinform)

def people():
    username = request.args(0) #request the username of the person
    if username == None: #In case someone doesn't include a name in the URL
        redirect(URL('default', 'index'))

    selector = db(db.auth_user.username == username).select().first()

    user = db(db.user_list.person == selector).select().first()
    house = db(db.house.id == user.house).select().first()

    return dict(user=user, house = house)

#We never got around to fully implementing this feature :(
@auth.requires_login()
def inbox():
    this_user = db(db.user_list.person == auth.user).select().first() # this_user refers to the current user in user_list
    this_house = db(db.house.id == this_user.house).select().first() # this_house refers to the current house this_user is in

    if this_house == None:
        session.flash = 'Make or Join A House First!'
        redirect(URL('default', 'house'))

    conversation_list = db(db.conversation.house == this_house).select(orderby=~db.conversation.recent_post)

    form = ''
    if request.vars.action == 'start':
        this_time = datetime.utcnow()
        form = SQLFORM.factory( Field('subject'),
                                Field('text_message', 'text')
                                )
        if form.process().accepted:
            new_convoID = db.conversation.insert(   subject = form.vars.subject,
                                                    recent_post = this_time,
                                                    house = this_house
                                                    )
            db.conversation_message.insert( conversation_text = form.vars.text_message,
                                            date_posted = this_time,
                                            person_posting = auth.user,
                                            conversation_id = new_convoID
                                            )
            redirect(URL('default', 'inbox'))

    

    return dict(today = today_string(), form = form, conversation_list = conversation_list, this_user = this_user)

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login()
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)


def today_string():
    today = date.today()
    today_format = today.strftime('Today is %B %d, %Y')
    return today_format

def new_conversation():
    new_convoID = db.conversation.insert(member1 = auth.user)
    return new_convoID

def taskForm():
    form = SQLFORM.factory( Field('auth_user', 'list:reference auth_user'),
                          )
    return form
