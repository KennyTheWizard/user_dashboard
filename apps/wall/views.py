from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Message, Comment
from apps.users.models import User

# Create your views here.
def wall(request, wall_user_id):
    if not 'user_id' in request.session:
        return redirect(reverse('users:signin'))
    user_info = User.objects.filter(id=wall_user_id)
    if not user_info:
        return redirect(reverse('users:dashboard'))
    user_info = user_info[0]
    wall_messages = Message.objects.get_messages(wall_user_id)
    context = {
        'wall_user' : user_info,
        'wall_messages' : wall_messages,
    }
    return render(request, 'wall/wall.html', context=context)

def addmessage(request, wall_user_id):
    if request.method != 'POST':
        return redirect(reverse('wall:wall', kwargs={'wall_user_id':wall_user_id}))
    model_resp = Message.objects.add_message(
        wall_user_id, request.session['user_id'], request.POST)
    if not model_resp['status']:
        for tag, value in model_resp.items():
            messages.error(request, value)
    return redirect(reverse('wall:wall', kwargs={'wall_user_id':wall_user_id}))

def addcomment(request, wall_user_id, message_id):
    if request.method != 'POST':
        return redirect(reverse('wall:wall', kwargs={'wall_user_id':wall_user_id}))
    model_resp = Comment.objects.add_comment(
        message_id, request.session['user_id'], request.POST)
    if not model_resp['status']:
        for tag, value in model_resp.items():
            messages.error(request, value)
    return redirect(reverse('wall:wall', kwargs={'wall_user_id':wall_user_id}))
