from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    is_manager = models.BooleanField(default=False)  # Ajout du champ pour gérer le chef de service

    def __str__(self):
        role = " (Chef de Service)" if self.is_manager else ""
        return f"{self.user.username}{role}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['service'],
                condition=models.Q(is_manager=True),  # Vérifie que le chef est unique par service
                name='unique_manager_per_service'
            )
        ]

    


class Permission(models.Model):
    STATUT_CHOICES = [
        ('en cour de traitement', 'en cour de traitement'),
        ('approuvé', 'approuvé'),
        ('refusé', 'refusé'),
    ]

    ETAT_CHOICES = [
        ('en cour ', 'en cour '),
        ('terminé', 'terminé'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, default='none')
    #service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True, default='sercice commercial')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    is_approved = models.CharField(max_length=25, choices=STATUT_CHOICES, default='en cour de traitement')
    date_send = models.DateField(auto_now_add=True)
    etat = models.CharField(max_length=100, choices=STATUT_CHOICES,default='')
    bool = models.BooleanField(default=False)
    
    def clean(self):
        overlapping_permissions = Permission.objects.filter(
            #service=self.service,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date,
            is_approved='approuvé'
        ).count()


    def __str__(self):
        return f"{self.employee.user.username} - {self.start_date} to {self.end_date}"

    class Meta:
        unique_together = ('employee', 'start_date', 'end_date')



