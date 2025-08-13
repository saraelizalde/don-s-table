from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta

STATUS = ((0, "Pending"), (1, "Confirmed"))

# Create your models here.
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    end_time = models.TimeField(editable=False)
    guests = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(14)]
    )
    special_requests = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def save(self, *args, **kwargs):
        if self.time:
            self.end_time = (datetime.combine(self.date, self.time) + timedelta(hours=1)).time()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reservation for {self.user.username} on {self.date} at {self.time}"
    
    class Meta:
        ordering = ['date', 'time']