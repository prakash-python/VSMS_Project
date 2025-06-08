from django.http import HttpResponse
from django.shortcuts import redirect

def checksuperuser(fun):
    
    def innerfun(request):
        if request.user.is_superuser and request.user.is_authenticated:
            return fun(request)
        else:
            return redirect('staffloginurl')
    return innerfun