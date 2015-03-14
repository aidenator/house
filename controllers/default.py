#By Aiden Hoopes and Mark Manguray for CMPS 183 Winter 2015
import logging
from datetime import datetime
from datetime import date 

def index():
    message = ''
    listofhouses = ""
    logger.info("Username is = %r" % auth.user)

    if auth.user == None:
        redirect(URL('default', 'user', args = ['login']))

    return dict()

@auth.requires_login()
def house():
    ##response.flash = T(datetime_convert())
    peopledb = db(db.users.name == auth.user.username).select() #See if they're registered in users db yet
    if( len(peopledb) == 0 ):
        db.users.insert(name=auth.user.username) #If not, insert them

    peopledb = db(db.users.name == auth.user.username).select().first() # The relevant user we need
    listofhouses = ""
    listofhouses = db(db.house.title == peopledb.house).select().first() if peopledb.house != None else None
    '''if len(listofhouses) > 0:
        for h in listofhouses:
            logger.info("Listofhouses: %r" % h)'''
    pic = peopledb.user_pic if peopledb.user_pic != None else ""
    users = db(db.users.house == listofhouses.title).select()
    #pic = pic.image
    house_name = request.args(0) or ''
    return dict(today = today_string(), listofhouses = listofhouses, pic = pic, users=users)

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

def index2():
    return dict()

@auth.requires_login()
def add_house():
    creating = request.vars.action == 'create'
    joining = request.vars.action == 'join'

    form = SQLFORM.factory(db.house,
                           fields=['title', 'image'],                          
                           )
    form.add_button('Go Back', URL('default', 'index'))
    if form.process().accepted:
        check = db(db.house.title == form.vars.title).select()
        if(len(check) > 0): #Check if house exists, if so, skip making it and redirect
            session.flash = "House already exists!"
            redirect(URL('default','house'))
        db.house.insert(title=form.vars.title, image=form.vars.image)
        db(db.users.name == auth.user.username).update(house=form.vars.title)
        db.groups.update_or_insert(housename=form.vars.title, username=auth.user.username)
        session.flash = 'House Created!'
        redirect(URL('default', 'house'))
    elif form.errors:
        response.flash = 'form has errors'

    return dict(creating = creating, joining = joining, form = form)

def people():
    username = request.args(0) #request the username of the person
    if username == None: #In case someone doesn't include a name in the URL
        redirect(URL('default', 'index')) 
    person = db(db.auth_user.username == username).select().first() #Find that person in the user database using the username
    if person == None:
        session.flash = 'test'
        redirect(URL('default','index'))
        return dict(person = None, house_list= [])
    house_list = ''
    house_list = db(db.users.name == person.username).select(orderby=db.users.name)
    if len(house_list) > 0:
        for h in house_list:
            logger.info("house_list: %r" % h)
    return dict(person = person, house_list = house_list)

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