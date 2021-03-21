



from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Refugi, Ressenya, Servei,  PreuServeiAlRefugi
from django.http import HttpResponse
import json
from django.db.models import Q

def welcome(request):
    #Si estàs identificat, vas a la pantalla d'inici
    queryset=request.GET.get('buscar')
    print(queryset)
    if queryset:  
        refugis = Refugi.objects.filter(
            Q(descripcio_Refugi__icontains = queryset)
        ).distinct()
        print(refugis)
        template=loader.get_template("buscar.html")
        context={
            'refugis':refugis,
        }
        return HttpResponse(template.render(context,request))
    else:
        return render(request, "welcome.html")
        


from django.contrib.auth.forms import UserCreationForm

def register(request):
    form = UserCreationForm()

    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None

    if request.method == "POST":
        # S'afegeixen les dades que introdueix l'usuari
        form = UserCreationForm(data=request.POST)
        
        # Si les dades son valides
        if form.is_valid():

            # Es crea un nou usuari
            user = form.save()

            #Si es crea correctament, es logueja i redirecciona automàticament a la pàgina d'inici
            if user is not None:
                do_login(request, user)
                return redirect('/main')

    return render(request, "register.html", {'form': form})

def login(request):
    # Es crea el formulari d'autentificació
    form = AuthenticationForm()
    if request.method == "POST":
        # S'afegeixen les dades que introdueix l'usuari
        form = AuthenticationForm(data=request.POST)
        # Si les dades son valides
        if form.is_valid():
            # S'obtenen les dades d'usuari i contrasenya
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Es comprova que són correctes, és a dir, que hi ha un usuari previ creat amb aquelles dades
            user = authenticate(username=username, password=password)

            # Si existeix un usuari, es logueja i redirecciona automàticament a la pàgina d'inici
            if user is not None:
                do_login(request, user)
                return redirect('/main')
    else:	
        if request.GET.get("Entra sense registrar-se")=="Entra sense registrar-se":
            return redirect('/main')
        else:
            return render(request, "login.html", {'form': form})

    return render(request, "login.html", {'form': form})

from django.contrib.auth import logout as do_logout

def logout(request):
    # Es finalitza sessió i es redirecciona a la portada
    do_logout(request)
    return redirect('/')

    

from django.template import loader

def refugis(request, refugi_id):
    refugis=Refugi.objects.filter(id=refugi_id)
    ressenyes=Ressenya.objects.filter(refugi=refugi_id)
    valoracio_total=0
    num_ressenyes=0
    for ressenya in ressenyes:
        valoracio_total+=ressenya.valoracio
        num_ressenyes+=1
    if num_ressenyes>0:
        valoracio_final=valoracio_total/num_ressenyes
        valoracio=round(valoracio_final,2)
    else:
        valoracio=""
    
    template=loader.get_template("refugis.html")
    context={
        'refugis':refugis,
        'ressenyes':ressenyes,
        'valoracio':valoracio
    }
    return HttpResponse(template.render(context,request))

def serveis_refugi(request, refugi_id):
    refugis = Refugi.objects.filter(id=refugi_id)
    serveis = Servei.objects.all()
    preus_serveis =  PreuServeiAlRefugi.objects.filter(refugi=refugi_id)
    template = loader.get_template("serveis.html")
    context = {
        'refugis': refugis,
        'serveis': serveis,
        'preus_serveis': preus_serveis,
    }
    return HttpResponse(template.render(context, request))
    
@login_required
def ressenya(request,refugi_id):
    refugis=Refugi.objects.filter(id=refugi_id)
    ressenyes=Ressenya.objects.filter(refugi=refugi_id)
    template=loader.get_template("ressenya.html")
    context={
        'refugis':refugis,
    }
    if request.method == "POST":
        autor=request.POST.get('autor')
        titol=request.POST.get('titol')
        descripcio=request.POST.get('descripcio')
        valoracions=request.POST.get('valoracio')
        nova_ressenya=Ressenya()
        nova_ressenya.nom_Autor=autor
        nova_ressenya.titol_Ressenya=titol
        nova_ressenya.text_Ressenya=descripcio
        nova_ressenya.valoracio=valoracions
        nova_ressenya.refugi=Refugi.objects.get(id=refugi_id)
        nova_ressenya.save()



    return HttpResponse(template.render(context,request))

def veure_ressenyes(request,refugi_id):
    refugis=Refugi.objects.filter(id=refugi_id)
    ressenyes=Ressenya.objects.filter(refugi=refugi_id)
    template=loader.get_template("veure_ressenyes.html")
    context={
        'refugis':refugis,
        'ressenyes':ressenyes,
    }
    
    return HttpResponse(template.render(context,request))