#By Aiden Hoopes and Mark Manguray for CMPS 183 Winter 2015
import logging
from datetime import datetime
from datetime import date 

def index():
    message = ''
    listofhouses = ""
    logger.info("Username is = %r" % auth.user)
    #Checks for User Login and House Membership
    if auth.user == None:
        message = "Please login to create, view, or join a house!"
    else:
        listofhouses = db(db.users.name == auth.user).select(orderby=db.users.name)
        if len(listofhouses) == 0:
            message = "Create a house or ask someone to let you into theirs!" 

    return dict(message=message, listofhouses=listofhouses)

def house():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    ##response.flash = T(datetime_convert())
    house_name = request.args(0) or ''
    return dict(today = today_string())


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
    _placeholder='Person')
    db.auth_user.last_name.widget = lambda f,v: SQLFORM.widgets.string.widget(f, v,
    _placeholder='Personson')
    db.auth_user.email.widget = lambda f,v: SQLFORM.widgets.string.widget(f, v,
    _placeholder='example@email.com')
    db.auth_user.username.widget = lambda f,v: SQLFORM.widgets.string.widget(f, v,
    _placeholder='Blahblah')
    db.auth_user.password.widget = lambda f,v: SQLFORM.widgets.password.widget(f, v,
    _placeholder='6-12 alphanumeric characters')

    return dict(form=auth())


def index2():

    return dict()

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