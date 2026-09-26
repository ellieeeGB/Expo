import random

def contar_puntos_en_circulo(n_puntos):
    """Cuenta cuántos puntos aleatorios caen dentro del círculo unitario."""
    dentro = 0
    for _ in range(n_puntos):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x*x + y*y <= 1:
            dentro += 1
    return dentro
