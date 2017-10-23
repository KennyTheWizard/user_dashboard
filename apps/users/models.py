from django.db import models
import bcrypt
import re

# Create your models here.
class UserManager(models.Manager):
    ''' User model controller '''
    def edit_user(self, user_id, postdata):
        ''' send edit user to correct method return response '''
        if 'password' in postdata:
            response = self.edit_user_password(user_id, postdata)
        elif 'email' in postdata:
            response = self.edit_user_info(user_id, postdata)
        elif 'description' in postdata:
            response = self.edit_user_description(user_id, postdata)
        return response

    def edit_user_description(self, user_id, postdata):
        the_user = self.filter(id=user_id)
        response = {}
        if the_user:
            the_user.update(description=postdata['description'])
            response['status'] = True
            response['user_id'] = the_user[0].id
            return response
        response['status'] = False
        response['user'] = "User Not Found"
        return response

    def edit_user_info(self, user_id, postdata):
        ''' checks form for valid data then updates user returns
        status true with user id if successful return status false
        and error messages if failed'''
        the_user = self.filter(id=user_id)
        if the_user:
            email_match = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
            name_match = re.compile(r"[a-zA-z]{2,}$")
            response = {}
            input_valid = True
            if not re.match(name_match, postdata['first_name']):
                response['first_name'] = "First name must be a least 2 letters. Letters only."
                input_valid = False
            if not re.match(name_match, postdata['last_name']):
                response['last_name'] = "Last name must be a least 2 letters. Letters only."
                input_valid = False
            if not re.match(email_match, postdata['email']):
                response['email'] = "Email must be valid email."
                input_valid = False
            if input_valid:
                the_user.update(first_name=postdata['first_name'],
                                last_name=postdata['last_name'],
                                email=postdata['email'],
                                user_level=postdata['user_level'] if 'user_level' in postdata else 1)
                response['id'] = the_user[0].id
            response['status'] = input_valid
            return response
        response['status'] = False
        response['user'] = "User Not Found"
        return response

    def edit_user_password(self, user_id, postdata):
        ''' returns status true and user id if success
        return status false and error message if fail'''
        response = {}
        the_user = self.filter(id=user_id)
        if the_user:
            input_valid = True
            if len(postdata['password']) < 8:
                response['password'] = "Password is too short minimum length 8."
                input_valid = False
            elif postdata['password'] != postdata['passwordconf']:
                response['password'] = "Password doesn't match confirmation."
                input_valid = False
        if input_valid:
            hash_pw = bcrypt.hashpw(postdata['password'].encode(), bcrypt.gensalt())
            the_user.update(password=hash_pw)
            response['id'] = the_user[0].id
        response['status'] = input_valid
        return response

    def get_user(self, user_id):
        '''returns the user object if it exists or false if not'''
        the_user = self.filter(id=user_id)
        if the_user:
            return the_user[0]
        return False

    def check_admin(self, user_id):
        ''' returns true if user is admin '''
        the_user = self.filter(id=user_id)
        if the_user:
            if the_user[0].user_level == 9:
                return True
        return False

    def delete_user(self, user_id):
        '''returns true if user deleted false if user not found'''
        if self.filter(id-user_id):
            self.get(id=user_id).delete()
            return True
        return False

    def validate_registration(self, postdata, user_level=1):
        '''checks reg form returns a dict with status true 
        and id if user created, status false and error messages if not'''
        response = {}
        input_valid = True
        email_match = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        name_match = re.compile(r"[a-zA-z]{2,}$")

        if not re.match(name_match, postdata['first_name']):
            response['first_name'] = "First name must be a least 2 letters. Letters only."
            input_valid = False
        if not re.match(name_match, postdata['last_name']):
            response['last_name'] = "Last name must be a least 2 letters. Letters only."
            input_valid = False
        if not re.match(email_match, postdata['email']):
            response['email'] = "Email must be valid email."
            input_valid = False
        if len(postdata['password']) < 8:
            response['password'] = "Password is too short minimum length 8."
            input_valid = False
        elif postdata['password'] != postdata['passwordconf']:
            response['password'] = "Password doesn't match confirmation."
            input_valid = False

        if input_valid:
            check_email = self.filter(email=postdata['email'])
            if check_email:
                response['email'] = "Email already in use."
                input_valid = False
            else:
                hash_pw = bcrypt.hashpw(postdata['password'].encode(), bcrypt.gensalt())
                new_user = self.create(first_name=postdata['first_name'],
                                       last_name=postdata['last_name'],
                                       email=postdata['email'],
                                       password=hash_pw,
                                       user_level=user_level)
                response['id'] = new_user.id
        response['status'] = input_valid
        return response

    def validate_login(self, postdata):
        '''checks login form return status true and id if found,
        status false and error messages if not found'''
        response = {}
        input_valid = True
        email_match = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        if not re.match(email_match, postdata['email']):
            response['email'] = "Email must be valid email."
            input_valid = False
        else:
            user_info = self.filter(email=postdata['email'])
            if user_info:
                user_info = user_info[0]
                if not bcrypt.checkpw(postdata['password'].encode(), user_info.password.encode()):
                    input_valid = False
            else:
                input_valid = False
            if input_valid:
                response['id'] = user_info.id
            else:
                response['email'] = "Check email and Password"
        response['status'] = input_valid
        return response


class User(models.Model):
    '''basic user model'''
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=60)
    user_level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, default="")
    objects = UserManager()
