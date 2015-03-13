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
    listofhouses = ""
    listofhouses = db(db.users.name == auth.user.username).select(orderby=db.users.name)
    logger.info("List of houses: %r" % listofhouses)
    house_name = request.args(0) or ''
    return dict(today = today_string(), listofhouses = listofhouses)

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
    db.auth_user.first_name.widget = lambda f,v: SQLFORM.widgets.string.widget(f, v,
    _placeholder='First Name')
    db.auth_user.last_name.widget = lambda f,v: SQLFORM.widgets.string.widget(f, v,
    _placeholder='Last Name')
    db.auth_user.email.widget = lambda f,v: SQLFORM.widgets.string.widget(f, v,
    _placeholder='Email Address')
    db.auth_user.username.widget = lambda f,v: SQLFORM.widgets.string.widget(f, v,
    _placeholder='Username')
    db.auth_user.password.widget = lambda f,v: SQLFORM.widgets.password.widget(f, v,
    _placeholder='Password')

    return dict(form=auth())

def index2():
    return dict()

@auth.requires_login()
def add_house():
    creating = request.vars.action == 'create'
    joining = request.vars.action == 'join'

    form = SQLFORM.factory(db.house,
                           fields=['title','user1','user2','user3','user4','user5','image'],
                           )
    form.add_button('Go Back', URL('default', 'index'))
    if form.process().accepted:
        session.flash = 'House Created!'
        db.house.insert(title=form.vars.title, user1=form.vars.user1, user2=form.vars.user2, user3=form.vars.user3, user4=form.vars.user4, user5=form.vars.user5, image=form.vars.image)
        redirect(URL('default', 'house'))
    elif form.errors:
        response.flash = 'form has errors'

    return dict(creating = creating, joining = joining, form = form)

def people():
    username = request.args(0) #request the username of the person
    if username == None: #In case someone doesn't include a name in the URL
        redirect(URL('default', 'index')) 
    person = db(db.auth_user.username == username).select().first() #Find that person in the user database using the username
    house_list = ''
    house_list = db(db.users.name == person.username).select(orderby=db.users.name)

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