from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Inventaire, Notes
from .forms import NoteForm
from datetime import datetime
from webappden import settings
from django.contrib.auth.views import login
from decimal import Decimal
@login_required
def dashboard(request):
    requete = User.objects.all()
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            notebody = form.save(commit=False)
            notebody.added_by = request.user
            notebody.date = datetime.now()
            notebody.save()
    else:
        form = NoteForm()

    return render(request, "dashboard.html",
                  {
                      "titre": "Accueil",
                      "nbrusers": requete.count(),
                      "nbradmin": requete.filter(is_superuser=1).count(),
                      "nbractifs": requete.filter(is_active=1).count(),
                      "nbrinventaire": Inventaire.objects.all().count(),
                      "notes": Notes.objects.all().order_by('-date')[:5],
                      'form': form,
                      'adname': settings.LDAP_AUTH_URL,
                      'date': datetime.now(),
                      'adhook': settings.LDAP_AUTH_CONNECTION_USERNAME,
                      'addb': settings.LDAP_AUTH_SEARCH_BASE,
                  })

@login_required
def utilisateurs(request):
    userlist = User.objects.all()
    return render(request, "userlist.html",
                  {
                      "titre": "Utilisateurs",
                      "userlist": userlist,
                  })

@login_required
def inventaire(request):
    inventaire = Inventaire.objects.all()
    return render(request, "inventaire.html",
                  {
                      "titre": "Inventaire",
                      "inventaire": inventaire,
                  })


def custom_login(request):
    if request.user.is_authenticated():
        return redirect('dashboard')
    else:
        return login(request)