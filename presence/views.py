
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from .forms import CustomLoginForm,SignUpForm,PermissionForm,EmployeeForm
from .models import  Permission
from django.http import HttpResponse
from django import forms
from datetime import datetime, timedelta
from django.utils.timezone import now,timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
# views.py

from django.shortcuts import render, redirect
from .models import Service,Employee
from .forms import ServiceForm

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'presence/employee_list.html', {'employees': employees})

@login_required
def service_list(request):
    services = Service.objects.all().prefetch_related('employees')  # Précharge les employés associés à chaque service
    return render(request, 'presence/service_list.html', {'services': services})


'''
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        services = Service.objects.all()
        if form.is_valid():
            form.save()
            return redirect('add_service')  # Redirige vers la liste des services après ajout
    else:
        form = ServiceForm()
    return render(request, 'presence/add_service.html', {'form': form,'services': services})

'''

def add_service(request):
    # Récupérer tous les services
    services = Service.objects.all()

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service ajouté avec succès!')
            return redirect('add_service')
    else:
        form = ServiceForm()

    return render(request, 'presence/add_service.html', {'form': form, 'services': services})



# Modifier un service
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service modifié avec succès!')
            return redirect('add_service')  # Redirige après modification
    else:
        form = ServiceForm(instance=service)
    
    return render(request, 'presence/edit_service.html', {'form': form, 'service': service})

# Supprimer un service

def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    employees = Employee.objects.filter(service=service)
    employees.delete()
    service.delete()
    messages.success(request, 'Service supprimé avec succès!')
    return redirect('add_service') 


# Create your views here.
def login_signup_view(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST, prefix='signup')
        if 'login_submit' in request.POST and login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.info(request, f"You are now logged in as {user.username}.")
            return redirect('dashboard')
        
    else:
        login_form = CustomLoginForm(prefix='login')
        signup_form = SignUpForm(prefix='signup')

    context = {
        'login_form': login_form,
        'signup_form': signup_form
    }
    return render(request, 'presence/login_signup.html', context)


@login_required
def dashboard(request):
    return render(request, 'presence/dashboard.html')


'''
@login_required
def permission_history(request):
    permission_requests = Permission.objects.filter(employee_id=request.user.id)
    return render(request, 'presence/permission_history.html', {'permission_requests': permission_requests, 'title': 'Toutes les Permissions'})
'''


@login_required
def permission_history(request):
    # Récupérer l'employé connecté
    emp = Employee.objects.get(user=request.user)
    # Récupérer les permissions de cet employé
    permissions = Permission.objects.filter(employee=emp).order_by('-start_date')
    
    return render(request, 'presence/permission_history.html', {'permissions': permissions})


@login_required
def edit_permission(request, permission_id):
    # Récupérer la permission ou renvoyer une erreur 404 si elle n'existe pas
    permission = get_object_or_404(Permission, id=permission_id)

    if permission.bool==True:
        messages.error(request, "Vous ne pouvez pas modifier une permission déjà traitée.")
        return redirect('permission_history')  # Rediriger vers la liste des permissions

    # Traitement du formulaire
    if request.method == 'POST':
        form = PermissionForm(request.POST, instance=permission)
        if form.is_valid():
            form.save()
            messages.success(request, "La permission a été modifiée avec succès.")
            return redirect('permission_history')  
    else:
        form = PermissionForm(instance=permission)

    return render(request, 'presence/edit_permission.html', {'form': form, 'permission': permission})


@login_required
def logout(request):
    #logout(request)  # Déconnexion de l'utilisateur
    return redirect('login')
    

def logIn(request):
    if request.method == 'POST':
        login_form = CustomLoginForm(request, data=request.POST, prefix='login')
        if 'login_submit' in request.POST and login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            #messages.info(request, f"You are now logged in as {user.username}.")
            return redirect('dashboard')
        
    else:
        login_form = CustomLoginForm(prefix='login')
        

    context = {
        'login_form': login_form,
        
    }
    return render(request, 'presence/login.html', context)

@login_required
def admin_dashboard(request):
    permissions = Permission.objects.filter(is_approved='en cour de traitement', bool=True)
    return render(request, 'presence/admin_dashboard.html', {'permissions': permissions})    

@login_required
def profile(request):
    return render(request, 'presence/profile.html') 

@login_required
def permissions_last_month(request):
    today = now().date()
    last_month = today - timedelta(days=30)
    permission_requests = Permission.objects.filter(Employee=request.user, start_date__gte=last_month)
    return render(request, 'presence/permission_history.html', {'permission_requests': permission_requests, 'title': 'Permissions du dernier mois'})


@login_required
def submit_permission(request):
    if request.method == 'POST':
        form = PermissionForm(request.POST)
        if form.is_valid():
            user = request.user

            # Vérifie si l'utilisateur a un employé associé
            emp = get_object_or_404(Employee, user=user)

            # Récupération des valeurs du formulaire
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            reason = form.cleaned_data.get('reason')

            # Vérifications avant l'enregistrement
            errors = []
            #permission=Permission.objects.get(start_date=start_date, end_date=end_date)

            if end_date <= start_date:
                errors.append("La date de fin doit être supérieure à la date de début.")
            
            max_duration = timedelta(days=5)
            if end_date - start_date > max_duration:
                errors.append("La durée maximale de la permission est de 5 jours.")

            if errors:
                for error in errors:
                    messages.error(request, error)
                return render(request, 'presence/submit_permission.html', {'form': form})

            # Enregistrement de la permission
            permission = Permission.objects.create(
                employee=emp,
                start_date=start_date,
                end_date=end_date,
                reason=reason,
                is_approved='en cour de traitement'  # Correction orthographique
            )

            messages.success(request, 'Permission enregistrée avec succès')
            return redirect('submit_permission')

        else:
            messages.warning(request, "Veuillez remplir correctement les champs.")

    else:
        form = PermissionForm()

    return render(request, 'presence/submit_permission.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect

@login_required
def approve_permission(request, permission_id):
    permission = get_object_or_404(Permission, pk=permission_id)
    employee = permission.employee
    permission.is_approved='approuvé'  # Récupérer l'employé associé à la demande de permission

    # Vérification des permissions ici
    #permission.is_approved = True  # Ou une valeur 'approuvé' si c'est un champ de choix
    permission.save()

    # Envoyer un e-mail à l'employé pour l'informer de l'état de sa demande
    subject = "Mise à jour de votre demande de permission"
    message = f"Bonjour {employee.user.first_name},\n\n" \
              f"Votre demande de permission pour la période du {permission.start_date} au {permission.end_date} a été approuvée.\n\n" \
              f"Cordialement,\nL'équipe de gestion des permissions"
    recipient_list = [employee.user.email]
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
        messages.success(request, 'La permission a été approuvée avec succès et l\'employé a été notifié par e-mail.')
    except Exception as e:
        # Si l'envoi échoue, affichez une erreur
        messages.error(request, f'Erreur lors de l\'envoi de l\'e-mail : {str(e)}')

    # Rendre la page avec les messages affichés
    return redirect(admin_dashboard)


from django.conf import settings

@login_required
def approve_permission_chef(request, permission_id):
    permission = get_object_or_404(Permission, pk=permission_id)
    employee = permission.employee  # Récupérer l'employé associé à la demande de permission
    # Vérification des permissions ici
    #permission.is_approved = 'en cour de traitement'
    permission.bool = True
    permission.save()

    # Envoyer un e-mail à l'employé pour l'informer de l'état de sa demande
    subject = "Mise à jour de votre demande de permission"
    message = f"Bonjour {employee.user.first_name},\n\n" \
              f"Votre demande de permission pour la période du {permission.start_date} au {permission.end_date} est actuellement en cours de traitement.\n" \
              f"Nous vous informerons dès qu'une décision sera prise.\n\n" \
              f"Cordialement,\nL'équipe de gestion des permissions"
    recipient_list = [employee.user.email]
    send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
    messages.success(request, 'La permission a été approuvée avec succès et l\'employé a été notifié par e-mail.')

    return redirect('permissions_service')


@login_required
def reject_permission(request, permission_id):
    permission = get_object_or_404(Permission, pk=permission_id)
    permission.is_approved = 'refusé'
    permission.save()
    messages.success(request, 'La permission a été refusée.')
    return redirect('admin_dashboard') 

@login_required
def reject_permission_chef(request, permission_id):
    permission = get_object_or_404(Permission, pk=permission_id)
    permission.is_approved = 'refusé'
    permission.save()
    messages.success(request, 'La permission a été refusée.')
    return redirect('permissions_service') # Redirige vers une vue qui liste les permissions


from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee, Service
from django.contrib import messages

@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    services = Service.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        service_id = request.POST.get('service')
        is_manager = request.POST.get('is_manager') == 'on'

        # Vérification si le service a déjà un chef
        service = Service.objects.get(id=service_id)
        if is_manager:
            if service.employee_set.filter(is_manager=True).exists() and service.employee_set.filter(is_manager=True).first().user.username != username:
                 # Utilisation de la relation inverse 'employee_set'
                # Ajouter un message d'erreur
                messages.error(request, "Ce service a déjà un chef.")
                return redirect('edit_employee', employee_id=employee_id)

        # Mise à jour des informations
        employee.user.username = username
        employee.user.email = email
        if password:
            employee.user.set_password(password)
        employee.user.save()

        # Mise à jour du service et de la position de chef
        employee.service = service
        employee.is_manager = is_manager
        employee.save()

        messages.success(request, "L'employé a été mis à jour avec succès.")
        return redirect('employee_list')

    return render(request, 'presence/edit_employee.html', {
        'employee': employee,
        'services': services
    })

@login_required
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    permissions= Permission.objects.get(employee_user=employee)
    permissions.delete()
    employee.delete()
    messages.success(request, 'l\'employee a ete supprimé  avec succès!')
    return redirect('employee_list') 

@login_required
def delete_permission(request, permission_id):
    permission = get_object_or_404(Permission, id=permission_id)
                                                                                                                                                                                                                                                                                                                                                                        
    if permission.bool==True:
        messages.error(request, "Vous ne pouvez pas supprimer une permission déjà traitée.")
        return redirect('permission_history') 
    
    permission.delete()
    #employee.delete()
    messages.success(request, ' cette permission a ete supprimé  avec succès!')
    return redirect('permission_history') 


# presence/views.py
@login_required
def add_employee(request):
    if request.method == 'POST':
        # Récupérer les valeurs envoyées par le formulaire
        username = request.POST['username']
        email = request.POST['email']
        service_id = request.POST['service']
        is_manager = request.POST.get('is_manager', False)  # Toggle pour chef de service

        # Créer un utilisateur avec les informations fournies
        user = User.objects.create_user(username=username, email=email, password=email)

        # Récupérer le service sélectionné
        service = Service.objects.get(id=service_id)

        # Créer l'employé
        employee = Employee.objects.create(user=user, service=service, is_manager=is_manager)

        # Ajouter un message de succès
        messages.success(request, f"L'employé {username} a été ajouté avec succès.")
        
        # Rediriger vers la liste des employés
        return redirect('employee_list')

    else:
        # Récupérer la liste des services pour les afficher dans le formulaire
        services = Service.objects.all()
        return render(request, 'presence/add_employee.html', {'services': services})

@login_required
def permissions_service(request):
    if request.user.employee.is_manager:
        emp = Employee.objects.get(user=request.user)
        service = emp.service.name
        # Filtrer les permissions en fonction de l'état booléen à False (ou 0)
        permissions = Permission.objects.filter(employee__service=emp.service, bool=False)
        
        return render(request, 'presence/permissions_service.html', {'permissions': permissions, 'service': service})
    else:
        return redirect('dashboard')



from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib.auth.forms import PasswordChangeForm


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        
        # Vérification manuelle du mot de passe actuel
        old_password = request.POST.get('old_password')
        if not request.user.check_password(old_password):  # Vérifie si le mot de passe actuel est correct
            messages.error(request, "Le mot de passe actuel est incorrect.")
        elif form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Empêche la déconnexion après modification du mot de passe
            messages.success(request, "Votre mot de passe a été changé avec succès !")
            return redirect('profile')  # Redirige vers la page de profil ou autre
            
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'presence/change_password.html', {'form': form})



@login_required
def service_calendar(request, service_id):
    """Retourne les permissions d'un service particulier sous forme de JSON."""
    permissions = Permission.objects.filter(employee__service_id=service_id)

    events = [
        {
            "title": f"{perm.employee.user.username}",
            "start": perm.start_date.strftime("%Y-%m-%d"),
            "end": perm.end_date.strftime("%Y-%m-%d"),
            "backgroundColor": "#4a90e2" if perm.etat == "Approuvé" else "#e74c3c",
        }
        for perm in permissions
    ]

    return JsonResponse(events, safe=False)
