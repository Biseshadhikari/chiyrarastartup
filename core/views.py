from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login,logout
from .models import *
from .forms import *
# Create your views here.
def home(request): 
    stories = Story.objects.all()
    categories = Category.objects.all()
    category = request.GET.get('category')
    category_ = Category.objects.filter(text = category).first()
    if category_: 
        stories = Story.objects.filter(category = category_)
    events = Event.objects.all()
    context = { 
        'stories':stories,
        'categories':categories,
        'category_text':category,
        'events':events
    }
    return render(request,'core/index.html',context)


def storyDetail(request,slug): 
    response_form = CommentForm()
    reply_form = ReplyForm()
    if request.method == 'POST':
        try:
            if request.user.is_authenticated:
                response_form = CommentForm(request.POST)
                text = request.POST.get('text')

                if response_form.is_valid() and text.strip():  # Check if 'text' is not empty after stripping whitespace
                    response = response_form.save(commit=False)
                    response.user = request.user
                    story = Story.objects.get(slug=slug)
                    response.story = story
                    response.save()
                    return redirect('/story/' + str(slug) + '#' + str(response.id))
            else:
                return redirect('/login/')
        except Exception as e:
            print(e)
            raise
   
        
    story = Story.objects.get(slug=slug)
    related_stories = Story.objects.filter(category=story.category).exclude(id=story.id)[:5]

    
    comments = Comment.objects.filter(parent_comment = None,story = story)

    return render(request,'core/storyDetail.html',{ 
        'story':story,
        'comment_form': response_form,
        'reply_form': reply_form,
        'comments':comments,
        'related_stories':related_stories
    })
 

def signin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            redirect_url = request.GET.get('story')

            # Validate required fields
            if not username or not password:
                messages.error(request, 'Both username and password are required.')
                return redirect('login')

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                if redirect_url is not None: 
                    return redirect(f"/story/{redirect_url}") 
                
                else:
                    return redirect('home') # Update with your home URL

            # Invalid credentials
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

        return render(request, 'core/login.html')
    else:
        return redirect('/')

import re

def is_strong_password(password):
    # Password should contain at least one uppercase letter, one lowercase letter, one digit, and be at least 8 characters long
    return re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password) is not None

def is_valid_email(email):
    # Simple email validation using a basic regex pattern
    return re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', email) is not None

def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            redirect_url = request.GET.get('story')

            if not username or not email or not password or not confirm_password:
                messages.error(request, 'All fields are required.')
                return redirect('register')

            if not is_valid_email(email):
                messages.error(request, 'Invalid email format.')
                return redirect('register')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
                return redirect('register')

            if not is_strong_password(password):
                messages.error(request, 'Password should contain at least one uppercase letter, one lowercase letter, one digit, and be at least 8 characters long.')
                return redirect('register')

            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('register')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered.')
                return redirect('register')
            User.objects.create(username=username, email=email, password=make_password(password))

            messages.success(request, f'Account created for {username}! You can now log in.')
            if redirect_url is not None:
                return redirect(f'/story/{redirect_url}')

            return redirect('login')  # Update with your login URL

        return render(request, 'core/register.html')
    else:
        return redirect('/')



def replyPage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                form = ReplyForm(request.POST)
                reply = request.POST.get('text')
                if form.is_valid() and reply.strip():
                    story_slug = request.POST.get('story')
                    parent_id = request.POST.get('parent')
                    
                    reply = form.save(commit=False)
                    reply.user = request.user
                    reply.story = Story.objects.get(slug = story_slug)
                    reply.parent_comment = Comment(id=parent_id)
                    reply.save()
                    return redirect('/story/'+str(story_slug)+'#'+str(reply.parent_comment.id))
                

            except Exception as e:
                print(e)
                raise

        return redirect('home')
    else:
        return redirect('/login')


def user_logout(request):
    logout(request)
    return redirect('home') 


def aboutUs(request):
    return render(request,'core/aboutus.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event, EventRegistration

def eventRegister(request, event_pk):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        institution = request.POST.get('institution')

        # Additional validation
        if not name or not email  or not address:
            messages.error(request, 'All fields are required except for institution.')
            return redirect(f'/eventRegister/{event_pk}')

        # You can add more specific validation based on your requirements

        event_ = Event.objects.filter(pk=event_pk).first()

        event_register = EventRegistration(
            name=name,
            email=email,
            contact=contact,
            address=address,
            institution=institution,
            event=event_
        )
        event_register.save()

        messages.success(request, 'Registration Successful')
        return redirect(f'/eventRegister/{event_pk}')

    return render(request, 'core/eventRegister.html')







def event_details(request,pk):
    event = Event.objects.filter(pk =pk).first()
    return render(request,'core/eventDetail.html',{'event':event})