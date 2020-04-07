from django.db import models

from model_utils.models import TimeStampedModel
from django_fsm import transition, FSMIntegerField

from users.models import User


# Create your models here.
class Task(TimeStampedModel):
    NEW = 0
    IN_PROGRESS = 1
    DONE = 2
    STATUS_CHOICES = (
        (NEW, 'New'),
        (IN_PROGRESS, 'In Progress'),
        (DONE, 'Done'),
        
    )
    owner = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    related_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    status = FSMIntegerField(choices=STATUS_CHOICES, default=NEW, protected=True)

    def __str__(self):
        return self.title

    @property
    def can_edit(self):
        """check if user can edit task as it only be editable in NEW status"""
        if self.status == self.NEW:
            return True
        else:
            return False

    @property
    def can_link(self):
        """
        check if user can link task to another task
         as it only be available in IN PROGRESS status
         """
        if self.status == self.IN_PROGRESS:
            return True
        else:
            return False

    def can_mark_done(self):
        """
        check if user can move task from IN PROGRESS to DONE
        as you cant move task to DONE without linking it to another one
        """
        if self.related_to is not None:
            return True
        else:
            return False                

    @transition(field=status, source=NEW, target=IN_PROGRESS)
    def in_progress(self):
        """Move task from NEW to IN PROGRESS"""


    @transition(field=status, source=IN_PROGRESS, target=DONE, conditions=[can_mark_done])
    def done(self):
        """Move task from IN PROGRESS to DONE"""    

    
