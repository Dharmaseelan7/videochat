from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
import random
import time
import json
from django.views.decorators.csrf import csrf_exempt

from .models import RoomMember
# Create your views here.


def getToken(request):
    appId = 'b3152a4366254c25abd274920d747fbf'
    appCertificate = '8919a4fd14704d389d58f0613bf36374'
    channelName = request.GET.get('channel')
    uid = random.randint(2, 230)
    expirationTimeInSeconds = 3600*24
    currentTimeStamp = time.time()
    role = 1
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    token = RtcTokenBuilder.buildTokenWithUid(
        appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token': token, 'uid': uid}, safe=False)


def lobby(request):
    return render(request, 'base/index.html')


def room(request):
    return render(request, 'base/room.html')


@csrf_exempt
def createUser(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name': data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name': member.name}, safe=False)


@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)
