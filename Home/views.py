from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import ProfileEditForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
import uuid
from .models import User
from .models import Books, Comments, Likes


# Create your views here.
def home(request):
    Categories = BooksCategories.objects.all()
    return render(request, 'Home/home.html', {'Categories': Categories})


def books_by_category(request,cat_id):
    
    category = get_object_or_404(BooksCategories, pk=cat_id)
    books = Books.objects.filter(category=category)#write the fk name here 
    return render(request, 'Home/books.html', {'books': books,'category': category})


@login_required(login_url = 'login_page')
def ProfileView(request, profile_id):
    profile = get_object_or_404(UserProfile, pk=profile_id)
    return render(request, 'Home/profile.html', {'profile': profile})




@login_required(login_url='login_page')
def edit_profile(request):
    #Fetch The UserProfile
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
#                                            uploaded files, 
        form = ProfileEditForm(request.POST, request.FILES, instance=user_profile, user=request.user)
        if form.is_valid():
            # Update first name and last name in the User model
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()
            
            form.save()
            return redirect('profile_page', profile_id=user_profile.id)  # Redirect to profile page

    else:
        form = ProfileEditForm(instance=user_profile, user=request.user)

    return render(request, 'Home/edit_profile.html', {'form': form})


def bookdetails(request, bookid):
    book = get_object_or_404(Books, pk=bookid)
    
    # Check if the logged-in user has liked the book
    user_has_liked = False
    if request.user.is_authenticated:  # Ensure user is logged in
        user_has_liked = Likes.objects.filter(book=book, user=request.user).exists()

    return render(request, 'Home/bookdetails.html', {'book': book, 'user_has_liked': user_has_liked})


@login_required(login_url = 'login_page')
def add_comment(request, bookid): #take book id
    book = get_object_or_404(Books, pk=bookid)

    if request.method == "POST":
        text = request.POST.get('text') #store the comment from user in text
        if text: #if user has wrote something 
            #Comments model me login user selected book pe kuch text(jo upar likha hai ) it will be added
            Comments.objects.create(book=book, user=request.user, text=text)
    
    # after saving the commnet back to the book details page. Isse refresh bhi ho jayenga and it'll show updated comment
    return redirect('detail', bookid=book.id)  

@login_required(login_url = 'login_page')
def like_book(request, bookid):
    """Allows a logged-in user to like or unlike a book (page refresh required)."""
    book = get_object_or_404(Books, pk=bookid)
    like, created = Likes.objects.get_or_create(book=book, user=request.user)

    if not created:
        like.delete()  # Unlike if already liked
    
    return redirect('detail', bookid=book.id)  # Refreshes the page



@login_required(login_url='login_page')
def SuggestedBooksView(request):
    user = request.user

    # Like Boss Fetch here
    liked_books = Books.objects.filter(likes__user=user).distinct()

    # Comment Bokks fetch here
    commented_books = Books.objects.filter(comments__user=user).distinct()

    # remove duplicate and give a list
    suggested_books = set(liked_books) | set(commented_books)

    return render(request, 'Home/suggested_books.html', {'suggested_books': suggested_books})


def RegisterView(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user_error = False

        if User.objects.filter(username=username).exists():
            user_error = True
            messages.error(request, 'Username already exist')

        if User.objects.filter(email=email).exists():
            user_error = True
            messages.error(request, 'Email Already Exist')
        
        if len(password)<6:
            user_error = True
            messages.error(request, 'Password must be at least 6 character')
        
        if user_error:
            return redirect(request, 'register_page')
        
        else:
            new_user = User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password
            )
            messages.success(request, "Account created. Login Now")
            return redirect('login_page')
    return render(request, 'Home/register.html')

def LoginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "No Account found with this username")
            return  redirect('login_page')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, "Invailid Password")
            return redirect('login_page')
    
    return render(request, 'Home/login.html')

def LogoutView(request):
    logout(request)

    # redirect to login page after logout
    return redirect('login_page')



def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()
            
            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})

            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            email_body = f'Reset your password using the link below: \n\n\n{full_password_reset_url}'

            email_message = EmailMessage(
                'Reset Your Book Bank Password',
                email_body,
                settings.EMAIL_HOST_USER,
                [email]
            )
            
            email_message.fail_silently = True
            # email_message.fail_silently = False
            print(f'Sending email to {email}...')  # Debugging
            email_message.send()
            print('Email sent successfully!')  # Debugging
            
            print('This is calling')
            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')
    

    return render(request, 'Home/forgot_password.html')

def PasswordResetSent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'Home/password_reset_sent.html')
    else:
        messages.error(request, 'Invailid reset id')
        return redirect('forgot-password')
    
    
def ResetPassword(request, reset_id):
    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            password_error = False

            if password != confirm_password:
                password_error = True
                messages.error(request, 'Password do not mathch')
            
            if len(password) < 5:
                password_error = True
                messages.error(request, 'Password must be at least 6 character')
            
            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                password_error = True
                messages.error(request, 'Reset Link Has Expired')

                password_reset_id.delete()
                
            if not password_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()
                
                password_reset_id.delete()
                
                messages.success(request, 'Password Reset. Proceed to login')
                return redirect('login_page')
            else:
                return redirect('reset-password', reset_id=reset_id)
        
    except PasswordReset.DoesNotExist:
        messages.error(request, 'Something Went Wrong')
        return redirect('forgot-password')
    
    return render(request, 'Home/reset_password.html')