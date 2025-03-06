from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home_page'),
    path('category/<int:cat_id>/', views.books_by_category, name='books_by_category'), 
    path('books/<int:bookid>/', views.bookdetails, name='detail'),
    
    #User Authentication
    path('register/', views.RegisterView, name='register_page'),
    path('login/', views.LoginView, name='login_page'),
    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.ResetPassword, name='reset-password'),
    path('logout/', views.LogoutView, name='logout_page'),
    path('<int:profile_id>/', views.ProfileView, name='profile_page'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='Home/change_password.html', success_url='change_password'), name='change_password'),
    path('suggested-books/', views.SuggestedBooksView, name='suggested_books_page'),
    
    # Comment and Like URLs
    path('books/<int:bookid>/comment/', views.add_comment, name='add_comment'),
    path('books/<int:bookid>/like/', views.like_book, name='like_book'),
]
