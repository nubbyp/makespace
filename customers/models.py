from django.db import models


class Plan(models.Model):
    user_id = models.CharField(max_length=50, blank=False, null=False)
    storage_plan = models.CharField(max_length=50, blank=False, null=False)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return (self.user_id + " " + self.storage_plan)
