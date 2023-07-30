import uuid
from django.shortcuts import render, redirect
from chat.models import Room, Message
from board.models import Board
from django.http import HttpResponse, JsonResponse
import json
from django.urls import reverse
from django.db.models import Q
from account.models import Account
from random import randint
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.shortcuts import get_object_or_404


@login_required(login_url='/login/')
def checkview(request, room, message, board_obj):
    if Board.objects.filter(slug=room).exists() and Room.objects.filter(Q(ad_fk=Board.objects.get(slug=room)), Q(participants__email=[request.user.email, board_obj.author.email])).exists():
        message = " ".join(message.splitlines()) # здесь, если пользователь ввёл многострочное сообщение, мы отправим его однострочным
        room_name = Room.objects.filter(Q(ad_fk=Board.objects.get(slug=room)), Q(participants__in=[request.user, board_obj.author]))[0]
        return redirect('/chat/'+room_name.name+'/?message='+message.replace("\n", "\t"))
    else:
        if Board.objects.filter(slug=room).exists():
            extra = str(uuid.uuid4()).replace('-','_')
            room_name = room + "_" + extra
            new_room = Room.objects.create(name=room_name, ad_fk = Board.objects.get(slug=room))
            new_room.participants.add(request.user, board_obj.author)
            new_room.save()

            message = " ".join(message.splitlines())

            return redirect('/chat/'+room_name+'/?message='+message.replace("\n", "\t"))
        else:
            return redirect('/')


@login_required(login_url='/login/')
def show_chats(request):
    my_rooms = Room.objects.filter(participants__in=[request.user])
    return render(request, 'chat/chats.html', {'my_rooms':my_rooms})

def get_last_msg(request):
    if request.is_ajax:
        room_id = request.GET.get('room_id')
        if Message.objects.filter(room=Room.objects.get(name=room_id)).exists():
            last_msg = Message.objects.filter(room=Room.objects.get(name=room_id)).last()
            last_msg = last_msg.value.replace('\\n','').replace('\n','')
        else:
            last_msg = '...'

        return JsonResponse(last_msg, safe=False)


@login_required(login_url='/login/')
def getMessages(request, room):
    try:
        last_msg = request.GET.get('last_msg', None)
        room_details = Room.objects.get(name=room)

        if Message.objects.filter(room=room_details.id).latest().value == last_msg:
            return HttpResponse(json.dumps('no_msgs'))
        else:
            messages = Message.objects.filter(room=room_details.id)
            messages_list = []
            for i in messages:
                messages_list.append(
                    {
                        'id': i.id, 
                        'value': i.value, 
                        'room_id': i.room.id, 
                        'date': i.date, 
                        'sender': i.sender.email
                    }
                )
            # return JsonResponse({"messages":list(messages.values())})
            return JsonResponse({"messages":messages_list})
    except:
        return redirect('chat:show_chats')


@login_required(login_url='/login/')
def room(request, room):
    if Room.objects.filter(name=room).exists():
        msg = ''
        if request.GET.get('message') != None:
            msg = request.GET.get('message')

        this_room = Room.objects.get(name=room)
        if request.user in this_room.participants.all(): # ищем другого участника чата  
            participants_list = []
            for usr in this_room.participants.all():
                if usr != request.user:
                    participants_list.append(usr)
            participant = participants_list[0]

            # Нужно ли показывать иконку "нанять работника"
            show_add_workers_icon = False
            workers_amount = 0
            if this_room.ad_fk.author == request.user:
                show_add_workers_icon = True
                board_obj = this_room.ad_fk
                if Board.objects.filter(Q(pk=board_obj.pk), Q(workers__in=[Account.objects.get(email=participant)])).exists():
                    show_add_workers_icon = False

                if board_obj.workers_amount != None:
                    workers_amount = board_obj.workers_amount-1 # делаем -1, чтобы человек, когда нажал на кнопку, получил сообщение "осталось колво-1 работников"
                else:
                    show_add_workers_icon = False

            context = {
                'this_user':request.user,
                'participant':participant,
                'room':this_room,
                'show_add_workers_icon':show_add_workers_icon,
                'workers_amount':workers_amount,
                'msg':msg,
            }

            return render(request, 'chat/room.html', context)
    return redirect('chat:show_chats')


@login_required(login_url='/login/')
def send(request):
    message = request.POST.get('message', None)
    sender = request.POST.get('sender', None)
    room_name = request.POST.get('room_name', None)

    sender = get_object_or_404(Account, email=sender)
    new_message = Message.objects.create(value=message, sender=sender, room=Room.objects.get(name=room_name))
    new_message.save()
    return HttpResponse('Message sent successfully')
    

@login_required(login_url='/login/')
def add_worker(request):
    room_name = request.POST.get('room_name', None)
    room_details = Room.objects.get(name=room_name)
    board_obj = room_details.ad_fk

    worker_filter = Message.objects.filter(room=room_details)[0]
    worker = ''
    data = ''

    if worker_filter.sender == request.user.email:
        worker = worker_filter.receiver
    else:
        worker = worker_filter.sender

    if Account.objects.get(email = worker) not in Board.objects.get(pk = board_obj.pk).workers.all():
        if board_obj.workers_amount > 0 :
            instance = Board.objects.filter(pk = board_obj.pk)

            instance.update(workers_amount = board_obj.workers_amount - 1)
            instance[0].workers.add(Account.objects.get(email = worker))
            data = 'added'
        else:
            data = 'expired'
            if request.user == board_obj.author:
                board_obj.status = 'archive'
                board_obj.save()
    else:
        data = 'added'
    return JsonResponse(data, safe=False)


@login_required(login_url='/login/')
def workers_list(request):
    board_obj = Board.objects.filter(author = request.user)

    if request.method == 'POST':
        worker = request.POST['worker']
        slug = request.POST['slug']
        obj = Board.objects.filter(slug=slug)

        if Account.objects.get(email = worker) in Board.objects.get(pk = obj[0].pk).workers.all():
            obj.update(workers_amount = obj[0].workers_amount + 1)
            obj[0].workers.remove(Account.objects.get(email = worker))

        return redirect('/chat/workers_list/')
    else:
        context = {
            'board_obj':board_obj,
        }
        return render(request, 'chat/workers_list.html', context)



# отвечает за переход по ссылке сразу к чату
@login_required(login_url='/login/')
def workers_list_a(request, slug):
    board_obj = Board.objects.get(slug=slug)

    return checkview(request, board_obj.slug, '', board_obj)


def search_chats(request):
    searchInput = request.GET.get('searchInput')

    if searchInput == '' or searchInput == ' ':
        rooms = Room.objects.filter(participants__in=[request.user])
    else:
        rooms = Room.objects.filter(Q(participants__in=[request.user]), Q(ad_fk__title__icontains=searchInput))

    adts = []
    participants = []
    last_msg = []
    for room in rooms:
        adts.append(room.ad_fk.title)
        
        msg = Message.objects.filter(room=room.id).latest()
        participants.append(msg.sender)
        last_msg.append(msg.value)

    context = {
        'rooms':list(rooms.values()),
        'adts':adts,
        'participants':participants,
        'last_msg':last_msg,
    }

    return JsonResponse(context)