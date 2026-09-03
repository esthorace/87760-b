# Ejercicio 2

A partir de la vista: 

```py
def ejercicio2(request):
    usuarios = [
        {"nombre": "juan", "email": "juan@django"},
        {"nombre": "santi", "email": "juan@django"},
        {"nombre": "agustín", "email": "juan@django"},
    ]
    return render(request, "core/ejercicio2.html", {"usuarios": usuarios})
```

Crea el template `ejercicio2.html` e iterar sobre la lista y mostrar cada usuario.