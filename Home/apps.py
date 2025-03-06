from django.apps import AppConfig

class HomeConfig(AppConfig):  # Keep only one class for the "Home" app
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Home'  # Make sure this matches your app folder name exactly (lowercase)

    def ready(self):
        import Home.signals  # Import signals correctly from the Home app
        
        
# from django.contrib.auth.models import User
# from your_app.models import UserProfile  # Replace 'your_app' with your actual app name

# for user in User.objects.all():
#     UserProfile.objects.get_or_create(user=user)
