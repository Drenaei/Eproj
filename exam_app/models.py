from django.db import models
import re


class UserManager(models.Manager):
    def user_validator(self, postdata):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if len(postdata['f_n']) < 2:
            errors['f_n'] = "First name and last name should be at least 2 characters."
        if len(postdata['l_n']) < 2:
            errors['l_n'] = "Last name and last name should be at least 2 characters."
        if not email_regex.match(postdata['email']):
            errors['email'] = "Email must be a valid format."
        if len(postdata['pw']) < 8:
            errors['pw'] = "Password should be at least 8 characters."
        if postdata['conf_pw'] != postdata['pw']:
            errors['conf_pw'] = "Password and confirm password field should match."
        return errors
    def edit_validator(self, postdata):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if len(postdata['first']) < 2:
            errors['first'] = "First name and last name should be at least 2 characters."
        if len(postdata['last']) < 2:
            errors['last'] = "Last name and last name should be at least 2 characters."
        if not email_regex.match(postdata['email']):
            errors['email'] = "Email must be a valid format."
        return errors

class QuoteManager(models.Manager):
    def quote_validator(self, postdata):
        errors={}
        if len(postdata['author']) < 3:
            errors['author'] = "Author field requires at least 3 characters."
        if len(postdata['quote']) < 10:
            errors['quote'] = "Quote field requires at least 10 characters."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length=100)
    quote = models.CharField(max_length=255)
    created_by = models.ForeignKey(User , related_name="quotes_created", on_delete=models.CASCADE)
    users_who_liked = models.ManyToManyField(User , related_name="liked_quotes")
    objects = QuoteManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)