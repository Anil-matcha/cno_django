from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import User_Profile, Master_Profile, MenuItem
from .serializers import User_ProfileSerializer, MenuSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from gcm import GCM
from datetime import datetime
API_KEY_user = "AIzaSyB2D3W8RMet5egEeVtbGBrQyxLPkwNKlIg"
API_KEY_master = "AIzaSyCXCsforHSJERiXqw9XRtARkDFLtr2E3bc"
gcm_user = GCM(API_KEY_user)
gcm_master = GCM(API_KEY_master)

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
        
@csrf_exempt
def get_user(request, fbid):
    if request.method == 'GET':
        user = get_object_or_404(User, username=fbid)
        return JSONResponse({"username":user.first_name, "fb_id":user.username, "gcm_id":user.user_profile.gcm_id, "referral":user.user_profile.referral}, status=200)
        
@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = User.objects.create_user(username=data['fb_id'])
        user.first_name = data['username']
        user.user_profile.gcm_id = data['gcm_id']
        user.save()
        return JSONResponse("cool", status=200)
        
@csrf_exempt
def add_master(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        master = Master_Profile.objects.all()        
        if len(master) == 0:
            user = Master_Profile(gcm_id=data)
            user.save()
        else:
            master[0].gcm_id = data
            master[0].save()
        return JSONResponse("cool", status=200)
        
@csrf_exempt
def menu_list(request):
    """
    List all menu items
    """
    if request.method == 'GET':
        menu_list = MenuItem.objects.all()
        serializer = MenuSerializer(menu_list, many=True)
        return JSONResponse(serializer.data)

@csrf_exempt
def place_order(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        print data
        users = Master_Profile.objects.all()
        for user in users:
            print user.gcm_id
            data['date'] = str(datetime.now())
            response = gcm_master.plaintext_request(registration_id=user.gcm_id, data=data)
            return JSONResponse("order_placed", status=201)
            
@csrf_exempt
def accept_order(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        print data['gcm_id']
        response = gcm_user.plaintext_request(registration_id=data['gcm_id'], data={"accepted":"true"})
        return JSONResponse("order_placed", status=201)
            
@csrf_exempt
def update_gcm(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        users = User.objects.all().filter(username=data['fb_id'])
        for user in users:
            user.gcm_id = data['gcm_id']
            user.save()
        return JSONResponse("gcm_updated", status=200)