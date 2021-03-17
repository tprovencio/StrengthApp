from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def register_validator(self,post_data):
        errors= {}


        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] ='Invalid email'

        if len(post_data['password']) < 8:
            errors["password"] ='password must be at least 8 characters'

        if post_data['password'] !=post_data['confirm_password']:
            errors['confirm_password'] ='password does not match'

        return errors
        
    def login_validator(self,post_data):
        errors ={}
        user_with_matching_email = User.objects.filter(
            email=post_data['login_email']).first()
        if user_with_matching_email == None:
            errors['login_email'] = "not found. please register"
        else:
            if bcrypt.checkpw(post_data['login_password'].encode(), user_with_matching_email.password.encode()) == False:
                errors['login_password'] = "Password does not Match"
        return errors


class User(models.Model):
    email = models.CharField(max_length=48)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Workout(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    set1 = models.CharField(max_length=255)
    weight1 = models.IntegerField()
    set2 = models.CharField(max_length=255)
    weight2 = models.IntegerField()
    set3 = models.CharField(max_length=255)
    weight3 = models.IntegerField()
    set4 = models.CharField(max_length=255)
    weight4 = models.IntegerField()
    set5 = models.CharField(max_length=255)
    weight5 = models.IntegerField()
    workout_creator = models.ForeignKey(User, related_name="workouts", on_delete = models.CASCADE)
    #need to add a foreignKey to make a one to many relationship
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= UserManager()