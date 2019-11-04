from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db import connection

from .models import *
from .forms import *

import json
import uuid
import os

def register(request):
    user_form = UserRegistrationForm()
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                    user_form.cleaned_data['password'])
            new_user.save()

            return redirect("/")
        else:
            render(request,
                  'registration/register.html',
                  {'user_form': user_form})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})

class AuthenticationUsernameBackend(object):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and user.check_password(password):
                return user
        return None

@login_required
def mapView(request):
    return render(request, 'map.html', {})

@login_required
def update_profile(request, pk):
    if not request.user.pk != pk: 
        return redirect('/')
    
    users = CustomUser.objects.all()
    user = get_object_or_404(CustomUser, pk=pk)

    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if request.POST.get('new_password') != "":
                user.set_password(request.POST.get('new_password'))
            user.save()
            return redirect('/map/')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'registration/update_profile.html', {'user_form': form})

@login_required
@csrf_exempt
def getGeoJson(request):
    # sql = '''SELECT row_to_json(fc)
    #     FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features
    #     FROM (SELECT 'Feature' As type, 
    #         ST_AsGeoJSON(data.geom)::json As geometry,
    #         (
    #             select row_to_json(t) 
    #             from (select data.id as id, data.speed As speed,
    #                 data.phone As phone,
    #                 data.digital_tv As digital_tv,
    #                 data.home_autom As home_autom,
    #                 data.url As url) t
    #         )
    #     As properties
    #     FROM data ) As f ) As fc;'''

    sql = '''SELECT row_to_json(fc)
        FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features
        FROM (SELECT 'Feature' As type, 
            ST_AsGeoJSON(data_detail.geom)::json As geometry,
            (
                select row_to_json(t) 
                from (select data_detail.id as id, data_detail.a_1 As a_1,
                    data_detail.a_2 As a_2,
                    data_detail.b_1 As b_1,
                    data_detail.b_2 As b_2,
                    data_detail.c_1 As c_1,
                    data_detail.c_2 As c_2,
                    data_detail.d_1 As d_1,
                    data_detail.d_2 As d_2,
                    data_detail.e_1 As e_1,
                    data_detail.e_2 As e_2) t
            )
        As properties
        FROM data_detail ) As f ) As fc;'''
    
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()

    return HttpResponse(json.dumps(row[0]), content_type='application/json')

@login_required
@csrf_exempt
def createItem(request):
    item_id = request.POST.get('data_id', '')
    print (request.POST.copy())
    if item_id == "":
        # sql = '''INSERT INTO data ("speed", "phone", "digital_tv", "home_autom", "url", "geom") 
        #     VALUES ('%s', '%s', '%s', '%s', '%s', ST_GeometryFromText('%s', 4326))''' % \
        #     (request.POST.get('speed'), request.POST.get('phone'), \
        #     request.POST.get('digital_tv'), request.POST.get('home_autom'), \
        #     request.POST.get('url'), request.POST.get('geometry'))

        sql = '''INSERT INTO data_detail ("a_1", "a_2", "b_1", "b_2", "c_1", "c_2", "d_1", "d_2", "e_1", "e_2", "geom") 
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', ST_GeometryFromText('%s', 4326))''' % \
            (request.POST.get('a_1'), request.POST.get('a_2'), \
            request.POST.get('b_1'), request.POST.get('b_2'), \
            request.POST.get('c_1'), request.POST.get('c_2'), \
            request.POST.get('d_1'), request.POST.get('d_2'), \
            request.POST.get('e_1'), request.POST.get('e_2'), \
            request.POST.get('geometry'))

        with connection.cursor() as cursor:
            cursor.execute(sql)
    else:
        data = request.POST.copy()
        item = get_object_or_404(DataDetailModel, pk=item_id)

        form = DataForm(data, instance=item)
        form.save()

    return HttpResponse("OK")

@login_required
@csrf_exempt
def removeItem(request):
    item_id = request.POST.get('data_id', '')
    DataDetailModel.objects.get(pk=item_id).delete()

    return HttpResponse("OK")

def getVal(body, key):
    try:
        return body[key]
    except:
        return ""

@login_required
@csrf_exempt
def upload(request):
    f = request.FILES['file']
    file_name = uuid.uuid4()
    cursor = connection.cursor()

    # save uploaded file in the server side
    with open('upload/%s.json' % file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    data = json.loads(open('upload/%s.json' % file_name, 'r').read().encode().decode('utf-8-sig'))
    for item in data['features']:
        lines = ""
        for polygon in item['geometry']['coordinates'][0]:
            lines = ", ".join(["%s %s" % (pt[0], pt[1]) for pt in polygon])
            break
        wkt = "MULTIPOLYGON (((%s)))" % lines

        # print (wkt)
        # sql = "SELECT * FROM data WHERE geom=ST_GeometryFromText('%s', 4326)" % wkt
        # cursor.execute(sql)
        # print (cursor.fetchone())

        item = item['properties']
        # sql = '''INSERT INTO data ("speed", "phone", "digital_tv", "home_autom", "url", "geom") 
        #     VALUES ('%s', '%s', '%s', '%s', '%s', ST_GeometryFromText('%s', 4326))''' % \
        #     (getVal(item, 'speed'), getVal(item, 'phone'), \
        #     getVal(item, 'digital_tv'), getVal(item, 'home_autom'), \
        #     getVal(item, 'url'), wkt)

        sql = '''INSERT INTO data_detail ("a_1", "a_2", "b_1", "b_2", "c_1", "c_2", "d_1", "d_2", "e_1", "e_2", "geom") 
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', ST_GeometryFromText('%s', 4326))''' % \
            (getVal(item, 'a_1'), getVal(item, 'a_2'), \
            getVal(item, 'b_1'), getVal(item, 'b_2'), \
            getVal(item, 'c_1'), getVal(item, 'c_2'), \
            getVal(item, 'd_1'), getVal(item, 'd_2'), \
            getVal(item, 'e_1'), getVal(item, 'e_2'), wkt)

        cursor.execute(sql)

    os.remove("upload/%s.json" % file_name)

    return HttpResponse("OK")