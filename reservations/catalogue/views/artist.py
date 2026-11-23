
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from catalogue.models import Artist
from catalogue.forms import ArtistForm
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required


def index(request):
    artists = Artist.objects.all()
    title = 'Liste des artistes'

    return render(request, 'artist/index.html', {
        'artists': artists,
        'title': title
    })


def show(request, artist_id):
    try:
        artist = Artist.objects.get(id=artist_id)
    except Artist.DoesNotExist:
        raise Http404('Artist inexistant')

    title = "Fiche d'un artiste"

    return render(request, 'artist/show.html', {
        'artist': artist,
        'title': title
    })

@login_required
@permission_required('catalogue.change_artist', raise_exception=True)
def edit(request, artist_id):
    artist = Artist.objects.get(id=artist_id)
    form = ArtistForm(request.POST or None, instance=artist)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'PUT':
            if form.is_valid():
                form.save()
                messages.success(request, "Artiste modifié avec succès.")

                return render(request, 'artist/show.html', {
                    'artist': artist,
                })

            messages.error(request, "Échec de la modification de l'artiste !")

    return render(request, 'artist/edit.html', {
        'form': form,
        'artist': artist,
    })

@login_required
@permission_required('catalogue.add_artist', raise_exception=True)
def create(request):
    form = ArtistForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Artiste ajouté avec succès.")
            return redirect('catalogue:artist-index')
        messages.error(request, "Échec de l'ajout de l'artiste !")

    return render(request, 'artist/create.html', {
        'form': form,
    })

@login_required
@permission_required('catalogue.delete_artist', raise_exception=True)
def delete(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'DELETE':
            artist.delete()
            messages.success(request, "Artiste supprimé avec succès.")
            return redirect('catalogue:artist-index')

    messages.error(request, "Échec de la suppression de l'artiste !")

    return render(request, 'artist/show.html', {
        'artist': artist,
    })