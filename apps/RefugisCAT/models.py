from django.db import models


class Refugi(models.Model):
    nom_Refugi = models.CharField(max_length=70)
    coordenades = models.CharField(max_length=100)
    descripcio_Refugi = models.TextField()
    valoracio_Refugi = models.FloatField()
    members = models.ManyToManyField('Servei', related_name='serveis', blank=True, through='PreuServeiAlRefugi')
    imatge = models.CharField(max_length=100)
    # reference_link = models.URLField(max_length=250)

    def __str__(self):
        return self.nom_Refugi


class Servei(models.Model):
    nom_Servei = models.CharField(max_length=70)

    def __str__(self):
        return self.nom_Servei


class Ressenya(models.Model):
    nom_Autor = models.CharField(max_length=70)
    titol_Ressenya = models.CharField(max_length=20)
    text_Ressenya = models.TextField()
    valoracio = models.IntegerField()
    data_Creacio = models.DateTimeField(auto_now_add=True)
    refugi = models.ForeignKey('Refugi', on_delete=models.CASCADE)

    def __str__(self):
        return self.titol_Ressenya



class PreuServeiAlRefugi(models.Model):
    servei = models.ForeignKey('Servei', on_delete=models.CASCADE)
    refugi = models.ForeignKey('Refugi', on_delete=models.CASCADE)
    descripcio_Servei = models.TextField()
    preu_Servei = models.FloatField()

    def __str__(self):
        to_return = "Preu al refugi "+self.refugi.__str__()+" del servei " + self.servei.__str__()
        return to_return

# CharField is used for short strings and specifies a maximum length.
# TextField is similar to CharField but can be used for longer form text as it
# doesn’t have a maximum length limit.
# FilePathField also holds a string but must point to a file path name.
# URLField is a CharField for an URL, validated by URLValidator.

# __str__ function returns the representation, as string, for every Project instance.
