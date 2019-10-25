from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView
from django.contrib import messages
import bcrypt

def login(request):
    return render(request, 'login.html')

def processlogin(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    else:
        user = User.objects.get(username=request.POST['username'])
        request.session['userid'] = user.id
        return redirect('/')


def register(request):
    return render(request, 'register.html')

def processregister(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        safepassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(first_name=first_name, last_name=last_name, username=username, password=safepassword.decode(), admin=False)
        request.session['userid'] = user.id
        return redirect('/')

def main(request):
    context = {
        'posts': Post.objects.all
    }
    return render(request, 'main.html', context)

def userpage(request):
    if request.session['userid']:
        user = User.objects.get(id=request.session['userid'])
        user_comments = user.comments.all()
        user_posts = user.posts.all()
        user_favorites = user.favorite_posts.all()
        context = {
            'user': user,
            'user_comments': user_comments,
            'user_posts': user_posts,
            'user_favorites': user_favorites,
        }
        return render(request, 'userpage.html', context)
    else:
        return redirect('/')

def postpage(request, postid):
    user = ''
    if request.session.get('userid'):
        user = User.objects.get(id=request.session['userid'])
    post = Post.objects.get(id=postid)
    comments = post.comments.all()
    index = 0
    context = {
        'post': post,
        'comments': comments,
        'index': index,
        'user': user
    }
    return render(request, 'postpage.html', context)

def createpostpage(request):
    if request.session.get('userid'):
        return render(request, 'createpost.html')
    else:
        return redirect('/')

def processpost(request):
    errors = Post.objects.post_validator(request.POST, request.FILES)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/createpost')
    else:
        user = User.objects.get(id=request.session['userid'])
        title = request.POST['title']
        desc = request.POST['desc']
        image = request.FILES['image']
        Post.objects.create(title=title, desc=desc, image=image, likes=0, dislikes=0, user=user)
        return redirect('/')

def processcommentonpage(request, postid):
    user = User.objects.get(id=request.session['userid'])
    post = Post.objects.get(id=postid)
    content = request.POST['comment']
    comment = Comment.objects.create(content=content, post=post, user=user, likes=0, dislikes=0)
    return redirect('/post/' + str(post.id))

def logout(request):
    del request.session['userid']
    return redirect('/')

def favorite(request, postid):
    user = User.objects.get(id=request.session['userid'])
    post = Post.objects.get(id=postid)
    user.favorite_posts.add(post)
    return redirect('/post/' + str(postid))

def unfavorite(request, postid):
    user = User.objects.get(id=request.session['userid'])
    post = Post.objects.get(id=postid)
    user.favorite_posts.remove(post)
    return redirect('/post/' + str(postid))

def delete(request, postid):
    post = Post.objects.get(id=postid)
    post.delete()
    return redirect('/')