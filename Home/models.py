from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
class BooksCategories(models.Model):
    book_category_name = models.CharField(max_length=50)
    book_category_coverpage = models.ImageField(upload_to='Categories_Cover_Pages/',)
    book_category_description = models.TextField(default='No Discription Available')
    
    def __str__(self):
        return self.book_category_name

class Books(models.Model):
    category = models.ForeignKey(BooksCategories, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=50)
    book_author = models.CharField(max_length=50)
    book_coverpage = models.ImageField(upload_to='BooksCoverPage/')
    book_summary = models.TextField()
    book_pdf = models.FileField(upload_to='BooksPdfFiles/', blank=True, null=True)
    
    def __str__(self):
        return self.book_name


#Mode for Comments
class Comments(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="comments")  # Connect comment to a book
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Connect comment to a user
    text = models.TextField()  # comment box
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timenow

    def __str__(self):
        return f"{self.user.username} on {self.book.book_name}"

# Models for  Likes
class Likes(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="likes")  # Connect like to a book
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Connect like to a user

    class Meta:
        unique_together = ('book', 'user')  # Ensure a user can like a book only once

    def __str__(self):
        return f"{self.user.username} likes {self.book.book_name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to='ProfilePictures/', default='default_profile.jpg')
    bio = models.TextField(blank=True, null=True)  # Optional bio field
    def __str__(self):
        return self.user.username
    
class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"