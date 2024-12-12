# chat/views.py
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

def index(request):

    form = IndexForm(request.POST or None, initial={'room': 'pycun'})

    if request.POST:
        if form.is_valid():
            username = form.cleaned_data['username']
            room = form.cleaned_data['room']
            return HttpResponseRedirect(F"{reverse('room', args=[room])}?username={username}")

    return render(request, 'chat/index.html', {
        'form': form,
    })


class IndexForm(forms.Form):

    username = forms.CharField(label='Usuario', max_length=50)
    room = forms.CharField(label='Sala', max_length=50)


def room(request, room_name):

    url_websocket = F"ws://{request.headers.get('Host')}/ws/chat/{room_name}/"

    username = request.GET['username']

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username': username,
        'url_websocket': url_websocket,
    })
