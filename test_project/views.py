from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
import jwt, urllib.parse, urllib.request, json, bcrypt
from datetime import datetime, timedelta

from . import utils, validators
from .forms import LoginForm, RegistrationForm, TokenExpiredForm, ForgotPasswordForm, ResetPasswordForm, GroupForm, PostForm, ReplayForm, NotesForm
from .models import User, Group, Post, PostFiles, ChatRoom, Roles, Replay
from django.core.exceptions import ValidationError


# Create your views here.


def index(request):
    if request.session.get('user', None):
        return redirect('dashboard')
    else:
        return redirect('login')


def dashboard(request):
    email = request.session.get('user', None)
    user = get_object_or_404(User, email=email)

    if request.method == 'POST':
        group_form = GroupForm(request.POST)
        group_form.owner = user
        if group_form.is_valid():
            group_form.save()

    else:
        group_form = GroupForm()


    users = User.objects.all()
    groups = Group.objects.filter(users=user)

    return render(request, 'dashboard.html', {
        'user': user,
        'users': users,
        'groups': groups,
        'group_form': group_form,
        'chat': ChatRoom.objects.all()
    })


def groups(request):
    email = request.session.get('user', None)
    groups = Group.objects.all()
    user = get_object_or_404(User, email=email)
    return render(request, 'groups.html', {
        'groups': groups,
        'user': user,
        'chat': ChatRoom.objects.all()
    })

def group(request, id):
    group = Group.objects.get(id=id)
    email = request.session.get('user', None)
    user = get_object_or_404(User, email=email)
    time_threshold = datetime.now() - timedelta(minutes=3)
    my_posts = Post.objects.filter(owner=user, created_at__gte=time_threshold).order_by('-created_at')
    my_replays = Replay.objects.filter(subject=user, created_at__gte=time_threshold).order_by('-created_at')
    replay_form = ReplayForm()
    post_form = PostForm()
    group_form = GroupForm(initial={
        'name': group.name,
        'description': group.description,
        'users': group.users
    })



    if request.method == "POST":

        #replay
        id_subject = request.POST.get('subject', None)


        #pinned
        post_id = request.POST.get('post_id', None)

        #new post
        group_id = request.POST.get('group', None)

        if post_id is not None:
            pinned = request.POST.get('pinned', False)
            if pinned == 'on':
                pinned = True
            post = Post.objects.get(id=post_id)
            post.pinned = pinned
            post.save()
            return render(request, 'group.html', {
                'group': group,
                'user': user,
                'post_form': PostForm(),
                'replay_form': replay_form,
                'group_form': group_form
            })

        elif id_subject is not None:
            file = request.FILES.get('file', None)
            replay = ReplayForm(request.POST)
            if replay.is_valid():
                if len(my_replays) == 0:
                    replay = replay.save()
                    replay.file = file
                    replay.save()
                    post = replay.post
                    post.replays.add(replay)
                    post.save()
                else:
                    messages.add_message(request, messages.WARNING, 'You must wait 3 minutes since the last replay')


            return render(request, 'group.html', {
                'group': group,
                'user': user,
                'post_form': PostForm(),
                'replay_form': replay_form,
                'group_form': group_form
            })

        else:
            post_form = PostForm(request.POST)
            file = request.FILES.get('file', None)
            if post_form.is_valid():
                if len(my_posts) == 0:
                    post = post_form.save()
                    post.file = file
                    post.save()
                    group.posts.add(post)
                    group.save()
                else:
                    messages.add_message(request, messages.WARNING, 'You must wait 3 minutes since the last post')

            else:
                print("post not valid")
        return render(request, 'group.html', {
            'group': group,
            'user': user,
            'post_form': post_form,
            'replay_form': replay_form,
            'group_form': group_form
        })
    return render(request, 'group.html', {
        'group': group,
        'user': user,
        'post_form': post_form,
        'replay_form': replay_form,
        'group_form': group_form
    })

def users(request):
    email = request.session.get('user', None)
    user = get_object_or_404(User, email=email)
    users = User.objects.all()
    return render(request, 'users.html', {
        'users': users,
        'user': user,
        'chat': ChatRoom.objects.all()
    })

def notes(request):
    email = request.session.get('user', None)
    groups = Group.objects.all()
    user = get_object_or_404(User, email=email)

    if request.method == 'POST':
        notes_form = NotesForm(request.POST)
        if notes_form.is_valid():
            notes_form.save()
    else:
        notes_form = NotesForm()
    return render(request, 'notes.html', {
        'user': user,
        'chat': ChatRoom.objects.all(),
        'notes': Roles.objects.all(),
        'notes_form': notes_form
    })

def delete_notes(request, id):
    Roles.objects.get(id=id).delete()
    return redirect('notes')


def edit_user(request, id):
    return HttpResponse('edit')

def delete_user(request, id):
    return HttpResponse('delete')

def approve_disapprove_user(request, id, action):
    user = User.objects.get(id=id)
    user.approved = action == 'approve'
    user.save()
    return render(request, 'user.html', {
        'user': user,
        'action': action
    })

def user(request, id):
    user = User.objects.get(id=id)

    return render(request, 'user.html', {
        'user': user
    })


def profile(request):
    user = User.objects.get(email=request.session.get('user'))
    return render(request, 'profile.html', {
        'user': user,
        'chat': ChatRoom.objects.all()
    })


def logout(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    return redirect('login')


def activate_email(request, token):
    token = urllib.parse.unquote(token)
    try:
        payload = jwt.decode(token, utils.CONSTANTS.get('JWT_SECRET'), algorithms=['HS256']).get('payload')
        email = payload.get('email')
        user = get_object_or_404(User, email=email)
        user.email_verified = True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Your email is confirmed')
        return redirect('login')
    except jwt.ExpiredSignatureError:
        if request.method == 'POST':
            form = TokenExpiredForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                user = get_object_or_404(User, email=email)

                payload = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                }

                utils.send_confirm_email(payload, email)
                messages.add_message(request, messages.INFO, 'New token is sended to your email')
                return redirect('login')


        else:
            form = TokenExpiredForm()
        return render(request, 'token_expired.html', {
            'form': form
        })
    except:
        return HttpResponse("Bad request 400", status=400)


def login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid() and form.is_logged_in():
            request.session['user'] = form.cleaned_data.get('email')
            return redirect('index')
        else:
            messages.add_message(request, messages.WARNING, 'Wrong email/password')

    else:
        form = LoginForm()



    return render(request, 'login.html', {
        'form': form
    })


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': '6Lfjp2QUAAAAAJkoc0D3K2ZWPhZ_KfB3UPwpLyn_',
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode('utf-8')
        req = urllib.request.Request(url, data)
        response = urllib.request.urlopen(req)
        result = json.load(response)
        ''' End reCAPTCHA validation '''

        if result['success']:

            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'You are successfully registered, please check email')
                return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, 'Please check recaptcha')

    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {
        'form': form
    })


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            payload = {
                'email': email
            }
            utils.send_reset_password_email(payload, email)
            messages.add_message(request, messages.INFO, 'Check your email to reset the password')
            return redirect('login')

    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot_password.html', {
        'form': form
    })


def reset_password(request, token):
    token = urllib.parse.unquote(token)
    try:
        payload = jwt.decode(token, utils.CONSTANTS.get('JWT_SECRET'), algorithms=['HS256']).get('payload')
        email = payload.get('email')
        user = get_object_or_404(User, email=email)

        if user:
            if request.method == 'POST':
                form = ResetPasswordForm(request.POST)
                if form.is_valid() and form.change_password(email=email):
                    messages.add_message(request, messages.SUCCESS, 'Password is successfully changed')
                    return redirect('login')
            else:
                form = ResetPasswordForm()

            return render(request, 'reset_password.html', {
                'form': form
            })
        else:
            return redirect('login')
    except jwt.ExpiredSignatureError:
        messages.add_message(request, messages.WARNING, 'Token has expired, send new token')
        return redirect('forgot_password')
    except:
        return HttpResponse("Bad request 400", status=400)
