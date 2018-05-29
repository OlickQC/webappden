from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Inventaire, Notes
from .forms import NoteForm
from datetime import datetime



@login_required
def dashboard(request):
    requete = User.objects.all()
    notes = Notes.objects.all().order_by('-date')[:5]
    nbrusers = requete.count()
    nbradmin = requete.filter(is_superuser=1).count()
    nbractifs = requete.filter(is_active=1).count()
    nbrinventaire = Inventaire.objects.all().count()

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
                      "titre": "Accueil intranet",
                      "nbrusers": nbrusers,
                      "nbradmin": nbradmin,
                      "nbractifs": nbractifs,
                      "nbrinventaire": nbrinventaire,
                      "notes": notes,
                      'form': form
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
                      "titre": "Utilisateurs",
                      "inventaire": inventaire,
                  })