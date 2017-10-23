from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import User

USER_LEVELS = {
    '1' : 'normal',
    '2' : 'admin',
}
# Create your views here.
def index(request):
    if 'user_id' in request.session:
        return redirect(reverse('users:dashboard'))
    return render(request, 'users/index.html')

def login(request):
    if request.method == 'POST':
        model_resp = User.objects.validate_login(request.POST)
        if model_resp['status']:
            request.session['user_id'] = model_resp['id']
            return redirect(reverse('users:dashboard'))
        for errortag, content in model_resp.items():
            messages.error(request, content, extra_tags=errortag)
    return redirect(reverse('users:signin'))

def signin(request):
    if 'user_id' in request.session:
        return redirect(reverse('users:dashboard'))
    return render(request, 'users/signin.html')

def create(request):
    if request.method == 'POST':
        all_users = User.objects.all()
        if all_users:
            user_level = 1
        else:
            user_level = 9
        model_resp = User.objects.validate_registration(request.POST, user_level)
        if model_resp['status']:
            if not 'user_id' in request.session:
                request.session['user_id'] = model_resp['id']
            return redirect(reverse('users:dashboard'))
        for errortag, content in model_resp.items():
            messages.error(request, content, extra_tags=errortag)
        if 'user_id' in request.session:
            return redirect(reverse('users:new'))
    return redirect(reverse('users:register'))

def register(request):
    if 'user_id' in request.session:
        return redirect(reverse('users:dashboard'))
    return render(request, 'users/register.html')

def edit(request, user_id):
    if not 'user_id' in request.session:
        return redirect(reverse('users:signin'))

    the_user = User.objects.get_user(request.session['user_id'])
    if the_user.user_level == 1:
        #print(request.session['user_id'], user_id)
        if str(request.session['user_id']) != user_id:
            #print('doing this')
            return redirect(reverse('users:edit', kwargs={'user_id' : request.session['user_id']}))
    context = {
        'edit_user' : User.objects.get_user(user_id),
        #'user_level_name' : USER_LEVELS[the_user.user_level],
        'user_level' : the_user.user_level
    }
    return render(request, 'users/edit.html', context=context)

def update(request, user_id):
    if request.method != 'POST':
        return redirect(reverse('users:edit', kwargs={'user_id' : user_id}))
    model_resp = User.objects.edit_user(user_id, request.POST)
    if model_resp['status']:
        return redirect(reverse('users:dashboard'))
    for errortag, content in model_resp.items():
        messages.error(request, content, extra_tags=errortag)
    return redirect(reverse('users:edit', kwargs={'user_id' : user_id}))

def dashboard(request):
    if not 'user_id' in request.session:
        return redirect('users:signin')
    the_users = User.objects.all()
    curr_user = User.objects.get_user(request.session['user_id'])
    context = {
        'all_users' : the_users,
        #'user_level_name' : USER_LEVELS[curr_user.user_level],
        'user_level' : curr_user.user_level
    }
    return render(request, 'users/dashboard.html', context=context)

def logout(request):
    request.session.clear()
    return redirect(reverse('users:index'))

def new(request):
    if 'user_id' in request.session:
        if User.objects.check_admin(request.session['user_id']):
            return render(request, 'users/register.html')
    return redirect(reverse('users:register'))

def delete(request, user_id):
    if 'user_id' in request.session:
        if User.objects.check_admin(request.session['user_id']):
            context = {
                'del_user' : User.objects.get_user(user_id)
            }
        return render(request, 'users/delete.html', context)
    return redirect(reverse('users:register'))

def destroy(request, user_id):
    if request.method == 'POST':
        User.objects.delete_user(user_id)
        messages.success(request, "User {} deleted".format(user_id))
    return redirect(reverse('users:dashboard'))
