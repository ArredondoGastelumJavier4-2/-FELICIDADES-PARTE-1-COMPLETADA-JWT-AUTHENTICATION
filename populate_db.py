"""
Script para poblar la base de datos con datos de prueba
Ejecutar con: python populate_db.py
"""

import os
import django
from datetime import date, timedelta
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca_project.settings')
django.setup()

from django.contrib.auth.models import User
from libros.models import Autor, Categoria, Libro, Prestamo


def crear_usuarios():
    print("Creando usuarios...")

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@biblioteca.com',
            password='admin123',
            first_name='Administrador',
            last_name='Sistema'
        )
        print("✓ Superusuario creado")

    usuarios = [
        {'username': 'juan_perez', 'email': 'juan@email.com', 'first_name': 'Juan', 'last_name': 'Pérez'},
        {'username': 'maria_lopez', 'email': 'maria@email.com', 'first_name': 'María', 'last_name': 'López'},
    ]

    for data in usuarios:
        if not User.objects.filter(username=data['username']).exists():
            User.objects.create_user(password='user123', **data)
            print(f"✓ Usuario {data['username']} creado")


def crear_categorias():
    print("\nCreando categorías...")

    categorias = [
        "Ficción",
        "Poesía",
        "Ensayo",
        "Historia",
        "Ciencia Ficción"
    ]

    for nombre in categorias:
        Categoria.objects.get_or_create(nombre=nombre)


def crear_autores():
    print("\nCreando autores...")

    autores = [
        ("Gabriel", "García Márquez", date(1927, 3, 6), "Colombia"),
        ("Isabel", "Allende", date(1942, 8, 2), "Chile"),
        ("Jorge Luis", "Borges", date(1899, 8, 24), "Argentina"),
    ]

    for nombre, apellido, fecha, pais in autores:
        Autor.objects.get_or_create(
            nombre=nombre,
            apellido=apellido,
            defaults={
                "fecha_nacimiento": fecha,
                "pais_origen": pais,
                "biografia": "Autor reconocido internacionalmente."
            }
        )


def crear_libros():
    print("\nCreando libros...")

    admin = User.objects.get(username='admin')

    ficcion = Categoria.objects.get(nombre="Ficción")
    ensayo = Categoria.objects.get(nombre="Ensayo")

    garcia = Autor.objects.get(apellido="García Márquez")
    borges = Autor.objects.get(apellido="Borges")

    libros = [
        {
            "titulo": "Cien años de soledad",
            "isbn": "9780307474728",
            "autor": garcia,
            "categoria": ficcion,
            "editorial": "Editorial Sudamericana",
            "fecha_publicacion": date(1967, 5, 30),
            "paginas": 471,
            "descripcion": "Obra maestra del realismo mágico.",
            "stock": 5,
            "precio": Decimal("450.00"),
            "valoracion": Decimal("4.80"),
        },
        {
            "titulo": "Ficciones",
            "isbn": "9780802130303",
            "autor": borges,
            "categoria": ficcion,
            "editorial": "Editorial Sur",
            "fecha_publicacion": date(1944, 1, 1),
            "paginas": 174,
            "descripcion": "Colección de cuentos filosóficos.",
            "stock": 3,
            "precio": Decimal("320.00"),
            "valoracion": Decimal("4.50"),
        },
        {
            "titulo": "El laberinto de la soledad",
            "isbn": "9786071613578",
            "autor": garcia,
            "categoria": ensayo,
            "editorial": "Fondo de Cultura Económica",
            "fecha_publicacion": date(1950, 1, 1),
            "paginas": 191,
            "descripcion": "Ensayo sobre identidad latinoamericana.",
            "stock": 2,
            "precio": Decimal("380.00"),
            "valoracion": Decimal("4.20"),
        }
    ]

    for data in libros:
        Libro.objects.get_or_create(
            isbn=data["isbn"],
            defaults={
                **data,
                "creado_por": admin
            }
        )


def crear_prestamos():
    print("\nCreando préstamos...")

    juan = User.objects.get(username='juan_perez')
    libro = Libro.objects.first()

    if libro and libro.stock > 0:
        prestamo, created = Prestamo.objects.get_or_create(
            libro=libro,
            usuario=juan,
            estado=Prestamo.ACTIVO,
            defaults={
                "fecha_devolucion_esperada": date.today() + timedelta(days=14)
            }
        )

        if created:
            libro.actualizar_stock(-1)
            print("✓ Préstamo creado")


def main():
    print("="*50)
    print("POBLANDO BASE DE DATOS - MySQL")
    print("="*50)

    crear_usuarios()
    crear_categorias()
    crear_autores()
    crear_libros()
    crear_prestamos()

    print("\nBase de datos poblada correctamente")


if __name__ == "__main__":
    main()


#xd