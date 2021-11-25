from .models import Animal
from .models import Equipement
from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm

# Create your views here.
def post_list(request):
    animaux = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'blog/post_list.html', {'animaux': animaux,'equipements':equipements})

def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    ancien_lieu1= animal.lieu
    message=""
    if request.method == "POST":
        form = MoveForm(request.POST, instance=animal)
    else:
        form = MoveForm()
    if form.is_valid():
        nouvel_animal = form.save(commit=False)
        if nouvel_animal.lieu.disponibilite=="libre":
            ancien_lieu = get_object_or_404(Equipement, id_equip=ancien_lieu1.id_equip)
            ancien_lieu.disponibilite = "libre"
            ancien_lieu.save()
            nouveau_lieu = get_object_or_404(Equipement, id_equip=nouvel_animal.lieu.id_equip)
            if nouveau_lieu.id_equip == "Mangeoire":
                nouvel_animal.etat = "repus"
            if nouveau_lieu.id_equip =="Roue":
                nouvel_animal.etat ="fatigué"
            if nouveau_lieu.id_equip=="Nid":
                nouvel_animal.etat ="endormi"
            if nouveau_lieu.id_equip=="Litière":
                nouvel_animal.etat = "affamé"
            if nouveau_lieu.id_equip !="Litière":
                nouveau_lieu.disponibilite = "occupé"
                nouveau_lieu.save()
            nouvel_animal.save()
            if nouveau_lieu.id_equip =="Nid":
                message= f"Félicitations, {id_animal} s'est correctement déplacé dans le nid et est maintenant endormi"
            else:
                message= f"Félicitations, {id_animal} s'est correctement déplacé dans la {nouveau_lieu.id_equip}"
            return render(request,'blog/animal_detail.html',{'animal': animal, 'lieu': animal.lieu, 'form': form, 'message': message})
        else:
            message ="Impossible ce lieu est déjà occupé par un autre animal !"
    return render(request,'blog/animal_detail.html',{'animal': animal, 'lieu': animal.lieu, 'form': form, 'message': message})
