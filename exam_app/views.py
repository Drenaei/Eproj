from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


# GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET

def index(request):
    return render(request, 'index.html')

def quotes_page(request):
    context={
        'user': User.objects.get(id = request.session['user_id']),
        'all_quotes': Quote.objects.all()
    }
    return render(request, 'quotes.html',context)

def logout(request):
    request.session.clear()
    return redirect('/')

def delete_quote(request, quote_id):
    delete_quote = Quote.objects.get(id=quote_id)
    delete_quote.delete()
    return redirect('/quotes')

def edit_acc(request, user_id):
    context={
        'the_user': User.objects.get(id=user_id)
    }
    return render(request, 'edit_acc.html', context)

def user_page(request, user_id):
    context={
        'user': User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'user_page.html', context)

def likes(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    users = User.objects.get(id = request.session['user_id'])
    if quote not in users.liked_quotes.all():
        quote.users_who_liked.add(users)
    else:
        quote.users_who_liked.remove(users)
    return redirect('/quotes')

# POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST 


def create_user(request):
    #make sure this is a post request
    if request.method == 'POST':
    #validate user input
        errors = User.objects.user_validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
    #secure user password
        user_pw = request.POST['pw']
        hash_pw = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        print(hash_pw)
    #create user
        new_user = User.objects.create(
            first_name = request.POST['f_n'],
            last_name = request.POST['l_n'], 
            email = request.POST['email'],
            password = hash_pw)
        request.session['user_id'] = new_user.id
        request.session['user_name'] = f"{new_user.first_name} {new_user.last_name}"
        return redirect('/quotes')
    return redirect('/')


def login(request):
    if request.method == 'POST':
        logged_user = User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user = logged_user[0]
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                request.session['user_name'] = f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/quotes')
            else:
                messages.error(request, "Password was incorrect.")
        else:
            messages.error(request, "Email was not found.")
    return redirect('/')

def add_quote(request):
    if request.method == 'POST':
    #validate the user input
        errors = Quote.objects.quote_validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/quotes')
    #create the quote
        new_quote = Quote.objects.create(
            author=request.POST['author'],
            quote=request.POST['quote'],
            created_by = User.objects.get(id = request.session['user_id']))
        return redirect('/quotes')
    return redirect('/quotes')


def edit_validate(request, user_id):
    if request.method == 'POST':
        errors = User.objects.edit_validator(request.POST)
        email_check = User.objects.filter(email = request.POST['email'])
        if email_check:
            errors['email_exists'] = "this email already exists"
            # messages.error(request, errors['email_exists'] )
        if errors:
            for error in errors:
                messages.error(request, errors[error])
        user_to_update = User.objects.get(id=user_id)
        user_to_update.first_name = request.POST['first']
        user_to_update.last_name = request.POST['last']
        user_to_update.email = request.POST['email']
        user_to_update.save()
        return redirect(f'/myaccount/{user_id}')
