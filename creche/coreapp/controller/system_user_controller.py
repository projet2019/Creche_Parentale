#!  /usr/bin/env python
# encoding: utf-8
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author Nadia
## nadia@gmail.com/joel@gmail.com
##

from coreapp.controller.base_controller import BaseController
from coreapp.service.system_user_service import SystemUserService
from coreapp.service.principal_service import PrincipalService, PRINCIPAL_ROLE
from coreapp.util.app_util import json_encode
from coreapp.util.export_util import ExportUtil
from django.http import HttpResponse

class SystemUserController(BaseController):
    pass

def loginAudit(request):
    #TO-DO check if this user has a valid session
    controller = SystemUserController()
    
    try:
        service = SystemUserService()

        result = service.loginAudit(request.POST)

    except Exception as e:
        result = controller.handleException(e)

    return HttpResponse(json_encode(result),
                       content_type="application/json")
                       
def list(request):
    #TO-DO check if this user has a valid session
    controller = SystemUserController()
    
    try:
        service = SystemUserService()

        result = service.list(request.POST)

    except Exception as e:
        result = controller.handleException(e)

    return HttpResponse(json_encode(result),
                       content_type="application/json")

def listExport(request):
    #TO-DO check if this user has a valid session
    controller = SystemUserController()

    try:
        service = SystemUserService()

        headers, records = service.listExport(request.GET)

        return ExportUtil.export(headers, records, request.GET['exportType'])

    except Exception as e:
        result = controller.handleException(e)

    return HttpResponse(json_encode(result),
                       content_type="application/json")

def list_principals(request):
    # TO-DO check if this user has a valid session
    controller = SystemUserController()

    try:
        service = PrincipalService()

        result = service.list(request.POST)

    except Exception as e:
        result = controller.handleException(e)

    return HttpResponse(json_encode(result),
                        content_type="application/json")

def userLoggedOn(request):
    #TO-DO check if this user has a valid session
    controller = SystemUserController()

    try:
        service = SystemUserService()

        user = service.userLoggedOn(request.session, request.POST)
        result = {'success': True, 'data' : user}
    except Exception as e:
        result = controller.handleException(e)

    return HttpResponse(json_encode(result),
                       content_type="application/json")


def saveUser(request):
    #TO-DO check if this user has a valid session
    controller = SystemUserController()

    try:
        service = SystemUserService()

        service.save(request.POST)
            
        result = {'success': True, 'message' : 'User details successfully updated. You can now login into the platform.'}

    except Exception as e:
        result = controller.handleException(e)

    return HttpResponse(json_encode(result),
                       content_type="application/json")


def passwordForget(request):
    #TO-DO check if this user has a valid session
    controller = SystemUserController()

    try:
        service = SystemUserService()

        service.passwordForget(request.POST)
            
        result = {'success': True, 'message' : 'The password reset instructions have been sent to your email address.'}

    except Exception as e:
        result = controller.handleException(e)

    return HttpResponse(json_encode(result),
                       content_type="application/json")

def passwordChange(request):
    #TO-DO check if this user has a valid session
    controller = SystemUserController()

    try:
        service = SystemUserService()

        service.passwordChange(request.POST)
            
        result = {'success': True, 'message' : 'You have changed your password successfully.'}

    except Exception as e:
        result = controller.handleException(e)

    return HttpResponse(json_encode(result),
                       content_type="application/json")


def savePrincipal(request):
    # TO-DO check if this user has a valid session
    controller = SystemUserController()

    try:
        service = PrincipalService()
        service.save_principal(request.POST)
        result = {'success': True, 'message': 'Principal details successfully saved. You can now view it.'}

    except Exception as e:
        result = controller.handleException(e)

    return HttpResponse(json_encode(result),
                        content_type="application/json")


    
