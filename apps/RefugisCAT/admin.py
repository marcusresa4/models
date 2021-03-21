from django.contrib import admin
from apps.RefugisCAT.models import Refugi, Ressenya, Servei, PreuServeiAlRefugi


class RefugiAdmin(admin.ModelAdmin):
    pass


class ServeiAdmin(admin.ModelAdmin):
    pass


class RessenyaAdmin(admin.ModelAdmin):
    pass


class PreuServeiAlRefugiAdmin(admin.ModelAdmin):
    pass


# Defined empty classes PostAdmin and CategoryAdmin. For the purposes of this tutorial,
# you do not need to add any attributes or methods to these classes. They are used
# to customize what is shown on the admin pages.

admin.site.register(Refugi, RefugiAdmin)
admin.site.register(Servei, ServeiAdmin)
admin.site.register(Ressenya, RessenyaAdmin)
admin.site.register(PreuServeiAlRefugi, PreuServeiAlRefugiAdmin)

# These last two lines are the most important. These register the models with the
# admin classes.