from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import User, Wish
from django.contrib import messages
import bcrypt

# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        new_user = User.objects.create(first_name=first_name, last_name=last_name,
                                       email=email, password_hash=pw_hash)
        request.session['uid'] = new_user.id
        return redirect('/wishes')


def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password_hash.encode()):
                request.session['uid'] = logged_user.id
                return redirect('/wishes')
        messages.error(request, "Login failed. Try again")
        return redirect('/')


def logout(request):
    del request.session['uid']
    return redirect('/')


def home(request):
    if 'uid' in request.session:
        user = User.objects.get(id=request.session['uid'])
        context = {
            'user': user,
            'wishes': user.wishes.filter(granted=False).order_by('-created_at'),
            'granted_wishes': Wish.objects.filter(granted=True).order_by('-created_at')
        }
        return render(request, 'home.html', context)
    else:
        return redirect('/')


def new_wish(request):
    if 'uid' not in request.session:
        return redirect('/')
    return render(request, 'new_wish.html')


def create_wish(request):
    if request.method == "POST":
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/wishes/new')
        user = User.objects.get(id=request.session['uid'])
        print(request.POST)
        Wish.objects.create(
            wish=request.POST['wish'], description=request.POST['description'], user=user)
        return redirect('/wishes')


def edit_wish(request, wish_id):
    if 'uid' not in request.session:
        return redirect('/')
    wish_to_edit = Wish.objects.filter(id=wish_id)
    if not wish_to_edit:
        return redirect('/wishes')
    context = {
        'wish': wish_to_edit[0]
    }
    return render(request, 'edit_wish.html', context)


def update_wish(request, wish_id):
    if request.method == "POST":
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/wishes/edit/{wish_id}')
        wish_to_update = Wish.objects.get(id=wish_id)
        wish_to_update.wish = request.POST['wish']
        wish_to_update.description = request.POST['description']
        wish_to_update.save()
        return redirect('/wishes')


def delete_wish(request, wish_id):
    if 'uid' not in request.session:
        return redirect('/')
    wish = Wish.objects.filter(id=wish_id)
    if not wish:
        print("no wish")
        return redirect('/wishes')
    user = User.objects.get(id=request.session['uid'])
    wish.delete()
    return redirect('/wishes')


def grant_wish(request, wish_id):
    if 'uid' not in request.session:
        return redirect('/')
    wish = Wish.objects.get(id=wish_id)
    wish.granted = True
    wish.save()
    return redirect('/wishes')


def like_wish(request, wish_id):
    if 'uid' not in request.session:
        return redirect('/')
    wish = Wish.objects.get(id=wish_id)
    user = User.objects.get(id=request.session['uid'])
    wish.likers.add(user)
    return redirect('/wishes')


def stats_wish(request):
    if 'uid' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['uid'])
    context = {
        "all_granted_wishes": Wish.objects.filter(granted=True),
        'user': user,
        'granted_wishes': user.wishes.all().filter(granted=True),
        'pending_wishes': user.wishes.all().filter(granted=False)
    }
    return render(request, 'stats.html', context)
