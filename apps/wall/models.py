from django.db import models
from ..users.models import User

# Create your models here.
class WallManager(models.Manager):
    def add_message(self, wall_id, author_id, postdata):
        response = {}
        if 'message' in postdata:
            if not postdata['message']:
                response['message'] = "Message cannot be blank."
                response['status'] = False
                return response
            the_wall = User.objects.filter(id=wall_id)
            if the_wall:
                the_wall = the_wall[0]
            else:
                response['user'] = "User wall does not exist"
                response['status'] = False
                return response
            the_author = User.objects.filter(id=author_id)
            if the_author:
                the_author = the_author[0]
            else:
                response['user'] = "User author does not exist"
                response['status'] = False
                return response

            self.create(message=postdata['message'], wall=the_wall, author=the_author)
            response['status'] = True
            return response
        response['status'] = False
        return response

    def add_comment(self, message_id, author_id, postdata):
        response = {}
        if 'comment' in postdata:
            if not postdata['comment']:
                response['comment'] = "Comment cannot be blank."
                response['status'] = False
                return response
            the_message = Message.objects.filter(id=message_id)
            if the_message:
                the_message = the_message[0]
            else:
                response['message'] = "No message with this ID"
                response['status'] = False
                return response
            the_author = User.objects.filter(id=author_id)
            if the_author:
                the_author = the_author[0]
            else:
                response['user'] = "User author does not exist"
                response['status'] = False
                return response

            self.create(
                comment=postdata['comment'],
                message=the_message,
                author=the_author
            )
            response['status'] = True
            return response
        response['status'] = False
        return response

    def get_messages(self, wall_id):
        the_wall = User.objects.filter(id=wall_id)
        if the_wall:
            return self.filter(wall=the_wall[0]).order_by('-created_at')
        return []

    def get_comments(self, message_id):
        the_message = self.filter(id=message_id)
        if the_message:
            return the_message[0].comments.all().order_by('-created_at')
        return []

class Message(models.Model):
    message = models.TextField()
    wall = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wall_messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_messages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = WallManager()

    def get_comments(self):
        return self.comments.all().order_by('created_at')

class Comment(models.Model):
    comment = models.TextField()
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = WallManager()
