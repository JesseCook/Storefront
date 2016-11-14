# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def email_to_name(email):
    """Returns a string corresponding to the user first and last names,
    given the user email."""
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])


def geolocation():
    row = ''
    return dict(row=row)


def search():
    search_key = request.vars.search_key
    search_option = request.vars.search_options
    rows = ''

    if search_key is '':
        redirect(URL('search'))
    elif search_key is not None:
        if search_option == 'user':
            rows = db(db.product.username.contains(search_key)).select()
        else:
            rows = db(db.product.name.contains(search_key)).select()


    num_of_result = len(rows)

    return dict(results=rows, search_key=search_key, num_of_result=num_of_result)


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.utcnow()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Hello World")
    products = None

    # Gets the list of all checklists for the user.
    products = db(db.product.status == True).select(
        orderby=~db.product.created_on, limitby=(0, 20)
    )

    return dict(message=T('Welcome to web2py!'), products=products, date=pretty_date, email_to_name=email_to_name)


    #stores = [
    #    dict(id=1,store_name="Target",store_uname="target"),
    #    dict(id=2,store_name="Safeway",store_uname="safeway"),
    #    dict(id=3,store_name="Baytree Bookstore",store_uname="ucsc")
    #]
    #return dict(message=T('Welcome to web2py!'),stores=stores,email_to_name=email_to_name)

def product():
    if db(db.category.id > 0).isempty():
        db.category.insert(name='Arts, Crafts & Sewing', description='Arts, Crafts & Sewing description')
        db.category.insert(name='Automotive Parts & Accessories', description='Automotive Parts & Accessories description')
        db.category.insert(name='Baby', description='Baby description')
        db.category.insert(name='Beauty & Personal Care', description='Beauty & personal care description')
        db.category.insert(name='Books', description='Books description')
        db.category.insert(name='CD & Vinyl', description='CD & Vinyl description')
        db.category.insert(name='Cell Phones & Accessories', description='Cell Phones & Accessories description')
        db.category.insert(name='Clothing, Shoes & Jewelry', description='Clothing Shoes & Jewelry description')
        db.category.insert(name='Computers', description='Computers description')
        db.category.insert(name='Game & Toys', description='Game description')
        db.category.insert(name='Electronics', description='Electronics description')
        db.category.insert(name='Grocery & Gourmet', description='Grocery Gourmet description')
        db.category.insert(name='Handmade', description='Handmade description')
        db.category.insert(name='Services', description='Services description')
        db.category.insert(name='Home & Kitchen', description=' description')
        db.category.insert(name='Luggage & Traveling Gear', description='Home & Traveling Gear description')
        db.category.insert(name='Music Instrument', description='Music Instrument description')
        db.category.insert(name='Office Products', description='Office Products description')
        db.category.insert(name='Pet Supplies', description='Pet Supplies description')
        db.category.insert(name='Software', description='Software description')
        db.category.insert(name='Vehicles', description='Vehicles description')
        db.category.insert(name='Wine', description='Wine description')
    form = None
    page_type = None
    product = None
    if request.args(0) is None:
        redirect(URL(args="add"))
    elif request.args(0) == "add":
        if auth.user_id is None:
            session.flash = T('Not logged in')
            redirect(URL('user', vars={'_next': URL('product', 'add')}))
        page_type = 'create'
        form = SQLFORM(db.product, showuser_id=False)
        form.add_button(T('Cancel'),URL('index'),_class='btn btn-warning')
    else:
        try:
            product = db(db.product.id == request.args(0)).select().first()
        except ValueError:
            session.flash = T('Invalid product id ' + request.args(0))
            redirect(URL('index'))
        if product is None:
            session.flash = T('Product #' + request.args(0) + ' does not exist')
            redirect(URL('default', 'index'))
        if product.user_id != auth.user_id:
            page_type = 'view'
            if not product.status:
                session.flash = T('Product no longer available')
                redirect(URL('index'))
        else:
            page_type = 'edit'
            form = SQLFORM(db.product, product, deletable=True, showid=False)
            form.add_button(T('Cancel'),URL('product', args=product.id),_class='btn btn-warning')
    if form is not None and form.process().accepted:
        if page_type == 'create':
            session.flash = T('Added product listing')
        elif page_type == 'edit':
            session.flash = T('Edited product listing')
        redirect(URL('product', args=form.vars.id))
    return dict(form=form, page_type=page_type, product=product)


def store():
    if request.args(0) is None:
        stores = db(db.auth_user).select(orderby=~db.auth_user.first_name)
        products = None
    else:
        store = request.args(0)
        try:
            stores = db(db.auth_user.id == store).select()
        except ValueError:
            session.flash = T('Store ' + store + ' undefined.')
            redirect(URL('default', 'store'))
        if stores.first() is None:
            session.flash = T('Store ' + store + ' not found.')
            redirect(URL('default', 'store'))
        else:
            products = db(db.product.user_id == store).select(orderby=~db.product.created_on)
    return dict(stores=stores,products=products)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


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
