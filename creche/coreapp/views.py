#!  /usr/bin/env python
# encoding: utf-8
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author Nadia
## nadia@gmail.com/joel@gmail.com
##

from django.shortcuts import render
from django.views.generic import TemplateView
from coreapp.controller.login_controller import authenticate, user_logout, get_module
from coreapp.controller.system_user_controller import list_principals, PRINCIPAL_ROLE, saveUser as user_save, passwordForget as password_forget, passwordChange as password_change, list as list_users, savePrincipal
from coreapp.controller.bill_controller import list as list_bills, saveComponent,saveActivity, ACTIVITY_CATEGORY, list_activities, list_components
from coreapp.controller.parent_controller import list_parents, list_children, saveChild, saveParent, saveParentChild, GENDER, CHILD_CLASSES, PARENT_CHILD_RELATION
from coreapp.controller.report_controller import get_principal, list_reports, saveDailyChildReport
from simplejson import loads
from django.template.defaultfilters import register
from creche import settings
import datetime

@register.filter(name='dict_key')
def dict_key(d, k):
    '''Returns the given key from a dictionary.'''
    v = d[k]
    if type(v) == list and type(v[0]) == dict:
        v = ' , '.join([ '-'.join([ '%s' % x[q] for q in x.keys()]) for x in v])
    return v

@register.filter(name='dict_cols')
def dict_cols(d):
    '''Returns the given key from a dictionary.'''
    if d is None or d == []: return []
    if type(d) == list: d = d[0]
    return d.keys()

def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


@register.filter(name='title')
def make_title(d):
    '''Returns the given key from a dictionary.'''
    if d is None: return ''
    if type(d) == str:
        d = d.title().replace('_', ' ')
    return d

# Create your views here.

class HomePageView(TemplateView):
    def index(self, request, **kwargs):
        return render(request, 'index.html', context=None)

def home(request, **kwargs):
    return render(request, 'index.html', context=None)

def login(request, **kwargs):
    if  request.POST:
        response = loads(authenticate(request).content.decode())
        response.update({"privileges" : [ eval(m) for m in request.session["allowed_modules"] ] })
        if response.get("success") is True:
            return render(request, 'dashboard.html', context=response)
        else:
            return render(request, 'signin.html', context=response)
    return render(request, 'signin.html', context=None)

def logout(request, **kwargs):
    response = user_logout(request).content
    print(response)
    return render(request, 'signin.html', context=loads(response.decode()))

def forgotpass(request, **kwargs):
    if request.POST:
        response = password_forget(request).content
        print(response)
        return render(request, 'forgot.html', context=loads(response.decode()))
    return render(request, 'forgot.html', context=None)

def signup(request, **kwargs):
    if request.POST:
        response = user_save(request).content
        print(response)
        return render(request, 'signup.html', context=loads(response.decode()))
    return render(request, 'signup.html', context=None)

def dashboard(request, **kwargs):
    return render(request, 'dashboard.html', context={"privileges" : [ eval(m) for m in request.session["allowed_modules"] ] })

def users(request, **kwargs):
    users = loads(list_users(request).content.decode())
    principals = loads(list_principals(request).content.decode())
    for i, elem in enumerate(principals['records']):
        created = elem['date_created'][0:10]
        principals['records'][i]['date_created'] = created
    data = {"mdl": get_module('/user'),
            'cols': ["id", "mail", "status", "password", "full_name", "description", "can_use_admin"],
            'users': users, "roles" : PRINCIPAL_ROLE, "principals": principals}

    if request.POST and request.POST.get('form_name') == 'principal':
        print("ADD PRINCIPAL", request.POST)
        principal = savePrincipal(request)
        data.update({"principal": loads(principal.content.decode())})
    # print( data)
    return render(request, 'user_management.html', context = data)

def childreport(request, **kwargs):
    principal = get_principal(request)
    children  = list_children(request)
    td = datetime.date.today()
    hrs =  [dt.strftime('%H:%M') for dt in
            datetime_range(datetime.datetime(td.year, td.month, td.day, 0, 0), datetime.datetime.now(),
            datetime.timedelta(minutes=5))]

    data = {"setup": settings.APPLICATION_SETTINGS['common'],
            "accueillante": loads(principal.content.decode()), "children": loads(children.content.decode()),
            "day": td, "hours": hrs, 'services': CHILD_CLASSES}
    print(data)
    return render(request, 'daily_report.html', context=data)


def bills(request, **kwargs):
    bills = loads(list_bills(request).content.decode())
    activitiess = loads(list_activities(request).content.decode())
    components = loads(list_components(request).content.decode())
    data = {"mdl": get_module('/bill'), "activity_categories": ACTIVITY_CATEGORY,
            'cols': ["id", "bill_no"],
            'bills': bills, "components": components, "activities": activitiess}
    if request.POST and request.POST.get('form_name') == 'patisserie':
        print("ADD PATISSERIE", request.POST)
        component = saveComponent(request)
        data.update({"component": loads(component.content.decode()) })

    if request.POST and request.POST.get('form_name') == 'activity':
        print("ADD ACTIVITY", request.POST)
        activity = saveActivity(request)
        data.update({"activity": loads(activity.content.decode())})


    print(data)
    return render(request, 'bill_management.html', context=data)


def parents(request, **kwargs):
    parents = loads(list_parents(request).content.decode())
    children = loads(list_children(request).content.decode())
    for i, elem in enumerate(parents['records']):
        created = elem['date_created'][0:10]
        parents['records'][i]['date_created'] = created
    data = {"mdl": get_module('/parent'), "relationship": PARENT_CHILD_RELATION,
            'cols': ["id", "bill_no"], 'groups': CHILD_CLASSES, 'genders': GENDER,
            "parents": parents, "children": children}
    if request.POST and request.POST.get('form_name') == 'parent_child':
        print("ADD PARENT AND CHILD", request.POST)
        parent_child = saveParentChild(request)
        data.update({ "parent_child": loads(parent_child.content.decode()) })

    if request.POST and request.POST.get('form_name') == 'parent':
        print("ADD PARENT", request.POST)
        parent = saveParent(request)
        data.update({"parent": loads(parent.content.decode())})

    # print(data)
    return render(request, 'parent_management.html', context=data)


def children(request, **kwargs):
    children = loads(list_children(request).content.decode())
    data = {"mdl": get_module('/child'), "genders": GENDER, 'groups': CHILD_CLASSES,
            'cols': ["id", "bill_no"],
            'bills': bills, "children": children}
    if request.POST and request.POST.get('form_name') == 'patisserie':
        print("ADD PATISSERIE", request.POST)
        component = saveComponent(request)
        data.update({"component": loads(component.content.decode())})

    if request.POST and request.POST.get('form_name') == 'activity':
        print("ADD ACTIVITY", request.POST)
        activity = saveActivity(request)
        data.update({"activity": loads(activity.content.decode())})

    print(data)
    return render(request, 'bill_management.html', context=data)



