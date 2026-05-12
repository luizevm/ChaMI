from .models import Perfil

def perfil_usuario(request):
    if request.user.is_authenticated:
        try:
            perfil = Perfil.objects.get(user=request.user)
            return {'perfil': perfil}
        except Perfil.DoesNotExist:
            return {'perfil': None}
    return {'perfil': None}