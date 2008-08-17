from django.db import models

###########################################################
# Models for Tags
###########################################################

###########################################################
# Tag Model
###########################################################
class Tag(models.Model):
    """ A tag. """
    name = models.CharField(max_length=64, unique=True)
    def __unicode__(self):
        return self.name
