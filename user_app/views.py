from django.shortcuts import render, redirect
from .models import User, Quote
import bcrypt
from django.contrib import messages
from django.db.models import Count



def index(request):
    return render(request, "index.html")

def create_user(request):
    if request.method == "POST":
        errors = User.objects.create_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password=pw_hash,
            )
            request.session['user_id'] = user.id 
            return redirect('/quotes')
    return redirect('/')

def main_page(request):
    if 'user_id' not in request.session: 
        return redirect('/')
    context={
        'current_user' : User.objects.get(id=request.session['user_id']),
        'all_quotes': Quote.objects.all(),
    }
    return render(request, "main_page.html", context)

def login(request):
    if request.method == "POST":
        user_with_email = User.objects.filter(email = request.POST['email']) 
        if user_with_email:
            user = user_with_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id 
                return redirect('/quotes')
        messages.error(request, "Email or password are not correct.")
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def add_quote(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        errors = Quote.objects.create_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/quotes')
        else:
            quote = Quote.objects.create(
                author = request.POST['author'],
                content = request.POST['quote'],
                posted_by = User.objects.get(id = request.session['user_id'])
            )
            messages.success(request, "You successfully created a quote!")
            return redirect('/quotes')
    return redirect('/quotes')

def like_quote(request, quote_id):
    if 'user_id' not in request.session: 
        return redirect('/')
    if request.method == "POST":
        current_user = User.objects.get(id = request.session['user_id'])
        one_quote = Quote.objects.get(id = quote_id)
        current_user.quotes_liked.add(one_quote)
    return redirect('/quotes')

def unlike_quote(request, quote_id):
    if 'user_id' not in request.session: 
        return redirect('/')
    if request.method == "POST":
        current_user = User.objects.get(id = request.session['user_id'])
        one_quote = Quote.objects.get(id = quote_id)
        current_user.quotes_liked.remove(one_quote)
    return redirect('/quotes')

def user_quotes(request, user_id):
    if 'user_id' not in request.session: 
        return redirect('/')
    context={
        'current_user' : User.objects.get(id = request.session['user_id']),
        'all_quotes': Quote.objects.all(),
    }
    return render(request, "user_quotes.html", context)

def edit_account(request, user_id):
    if 'user_id' not in request.session: 
        return redirect('/')
    context={
        'current_user' : User.objects.get(id = request.session['user_id']),
    }
    return render(request, "edit_account.html", context)

def update_account(request, user_id):
    if 'user_id' not in request.session: 
        return redirect('/')
    if request.method =="POST":
        errors = User.objects.edit_validator(request.POST, user_id)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/myaccount/{user_id}/edit')
        else:
            current_user = User.objects.get(id=user_id)
            current_user.first_name=request.POST['first_name']
            current_user.last_name=request.POST['last_name']
            current_user.email=request.POST['email']
            current_user.save()
            messages.success(request, "You successfully updated your account.")
    return redirect(f'/myaccount/{user_id}/edit')      

def delete_quote(request, quote_id):
    if 'user_id' not in request.session: 
        return redirect('/')
    quote_with_id = Quote.objects.filter(id = quote_id) 
    if len(quote_with_id) == 0: 
        return redirect('/quotes')
    if request.method == "POST":
        delete_quote = Quote.objects.get(id=quote_id)
        if delete_quote.posted_by.id == request.session['user_id']:
            delete_quote.delete()
    return redirect('/quotes')