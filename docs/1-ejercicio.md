1. Crear una carpeta y dentro un entorno virtual
    
    `uv init --no-package`

2. Activar entorno virtual
    
    `.venv/Script/activate`
    
    `source/bin/activate`

3. Instalar django y djlint
    
    `uv add django`

    `uv add djlint --dev`
	
4. Crear proyecto django
    
    `django-admin startproject config .`

5. Iniciar servidor django
       
    `python manage.py runserver`

6. Crear aplicación django "core" y registrarla
       
    `python manage.py startapp core`

7. Crear un template index.html en core, una función que responda con ese html, una url que sirva para que django responda con la función.

8. Integrar código en la función y mostrar en el html:
    
    - title
    - mensaje
    - fecha

**Tip**: Primero crear `template -> views -> url`