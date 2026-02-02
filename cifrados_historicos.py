from binario import ASCII_TABLE


# ============================================================
# Helpers
# ============================================================

def _es_letra_ascii(c):
    """
    Retorna True si c es una letra ASCII A-Z o a-z.
    (Usa ASCII_TABLE para evitar conversiones externas.)
    """
    if c not in ASCII_TABLE:
        return False
    code = ASCII_TABLE[c]
    # 'A'..'Z' => 65..90  |  'a'..'z' => 97..122
    return (65 <= code <= 90) or (97 <= code <= 122)


def _es_mayuscula(c):
    """True si c está en 'A'..'Z'."""
    if c not in ASCII_TABLE:
        return False
    code = ASCII_TABLE[c]
    return 65 <= code <= 90


def _letra_a_indice(c):
    """
    Convierte letra a índice 0..25.
    A/a -> 0, B/b -> 1, ..., Z/z -> 25
    """
    if not _es_letra_ascii(c):
        raise ValueError(f"No es letra ASCII: {repr(c)}")

    code = ASCII_TABLE[c]
    if 65 <= code <= 90:      # mayúscula
        return code - 65
    else:                     # minúscula 97..122
        return code - 97


def _indice_a_letra(i, mayuscula=True):
    """
    Convierte índice 0..25 a letra.
    mayuscula=True -> 'A'..'Z'
    mayuscula=False -> 'a'..'z'
    """
    if i < 0 or i > 25:
        raise ValueError("Índice fuera de rango (0..25)")

    code = (65 + i) if mayuscula else (97 + i)

    # Conveierte código ASCII a carácter usando una tabla inversa construida desde ASCII_TABLE
    for ch in ASCII_TABLE:
        if ASCII_TABLE[ch] == code:
            return ch

    raise ValueError("ASCII_TABLE no contiene el carácter esperado para ese código")


def _mod_26(n):
    """
    Módulo 26 manual que funciona con negativos.
    """
    while n < 0:
        n += 26
    while n >= 26:
        n -= 26
    return n


def _normalizar_desplazamiento(desplazamiento):
    """Convierte cualquier entero a rango 0..25."""
    # Si desplazamiento es negativo o grande, lo normalizamos con mod 26 manual.
    return _mod_26(desplazamiento)


# ============================================================
# 1) Cifrado César
# ============================================================

def cesar_cifrar(mensaje, desplazamiento):
    """
    Cifra con César:
    - Solo cifra letras A-Z y a-z.
    - Mantiene mayúsculas/minúsculas.
    - Deja igual espacios, números y signos.

    Parámetros:
    - mensaje: string
    - desplazamiento: int (puede ser negativo o grande)

    Retorna: string cifrado
    """
    k = _normalizar_desplazamiento(desplazamiento)

    resultado = ""
    for c in mensaje:
        if not _es_letra_ascii(c):
            # No se cifra: se copia tal cual
            resultado += c
            continue

        idx = _letra_a_indice(c)
        nuevo = _mod_26(idx + k)
        resultado += _indice_a_letra(nuevo, mayuscula=_es_mayuscula(c))

    return resultado


def cesar_descifrar(mensaje, desplazamiento):
    """
    Descifra César:
    - Misma lógica que cifrar, pero restando el desplazamiento.
    """
    k = _normalizar_desplazamiento(desplazamiento)
    # descifrar = cifrar con -k
    return cesar_cifrar(mensaje, -k)

# ============================================================
# 2) Cifrado ROT13 (caso especial de César)
# ============================================================

def rot13(mensaje):
    """
    Aplica ROT13 a un mensaje.
    ROT13 es un caso especial del cifrado César con desplazamiento = 13.

    Nota:
    - ROT13 es autoinverso: rot13(rot13(m)) = m
    """
    return cesar_cifrar(mensaje, 13)

# ============================================================
# 3) Cifrado Vigenère
# ============================================================

def _limpiar_clave_vigenere(clave):
    """
    Devuelve una lista de índices (0..25) correspondientes
    a las letras de la clave.
    Ignora cualquier carácter que no sea letra.
    """
    indices = []

    for c in clave:
        if _es_letra_ascii(c):
            indices.append(_letra_a_indice(c))

    if len(indices) == 0:
        raise ValueError("La clave Vigenère debe contener al menos una letra")

    return indices


def vigenere_cifrar(mensaje, clave):
    """
    Cifra un mensaje usando el cifrado Vigenère.

    - Solo cifra letras A-Z / a-z
    - Mantiene mayúsculas/minúsculas
    - La clave se repite cíclicamente
    - Caracteres no letra no se cifran ni consumen clave
    """
    clave_indices = _limpiar_clave_vigenere(clave)
    resultado = ""

    pos_clave = 0  # posición dentro de la clave

    for c in mensaje:
        if not _es_letra_ascii(c):
            resultado += c
            continue

        shift = clave_indices[pos_clave % len(clave_indices)]
        idx = _letra_a_indice(c)
        nuevo = _mod_26(idx + shift)

        resultado += _indice_a_letra(nuevo, mayuscula=_es_mayuscula(c))
        pos_clave += 1

    return resultado


def vigenere_descifrar(mensaje, clave):
    """
    Descifra un mensaje cifrado con Vigenère.
    La lógica es la misma que cifrar, pero restando el desplazamiento.
    """
    clave_indices = _limpiar_clave_vigenere(clave)
    resultado = ""

    pos_clave = 0

    for c in mensaje:
        if not _es_letra_ascii(c):
            resultado += c
            continue

        shift = clave_indices[pos_clave % len(clave_indices)]
        idx = _letra_a_indice(c)
        nuevo = _mod_26(idx - shift)

        resultado += _indice_a_letra(nuevo, mayuscula=_es_mayuscula(c))
        pos_clave += 1

    return resultado

# ============================================================
# 4) Análisis de Frecuencias
# ============================================================

def analisis_frecuencia(mensaje):
    """
    Analiza la frecuencia de letras en un mensaje.

    - Solo considera letras A-Z / a-z
    - Ignora mayúsculas/minúsculas (A == a)
    - Devuelve una tabla de frecuencia

    Retorna:
    - lista de tuplas: (letra, conteo, porcentaje)
      ordenada de mayor a menor frecuencia
    """
    # Inicializar conteo para A..Z
    conteo = {}
    for i in range(26):
        letra = _indice_a_letra(i, mayuscula=True)
        conteo[letra] = 0

    total_letras = 0

    # Contar ocurrencias
    for c in mensaje:
        if _es_letra_ascii(c):
            idx = _letra_a_indice(c)
            letra = _indice_a_letra(idx, mayuscula=True)
            conteo[letra] += 1
            total_letras += 1

    # Construir tabla de frecuencias
    tabla = []

    for letra in conteo:
        count = conteo[letra]
        if total_letras > 0:
            porcentaje = (count / total_letras) * 100
        else:
            porcentaje = 0.0

        tabla.append((letra, count, porcentaje))

    # Ordenar por frecuencia descendente
    tabla.sort(key=lambda x: x[1], reverse=True)

    return tabla

# ============================================================
# Pruebas rápidas
# ============================================================
if __name__ == "__main__":
    msg = "Hola Mundo!"
    k = 3

    c = cesar_cifrar(msg, k)
    p = cesar_descifrar(c, k)

    print("Mensaje:", msg)
    print("Cifrado César:", c)
    print("Descifrado:", p)

    # Normalización: desplazamientos grandes/negativos
    print("Cifrado (k=29):", cesar_cifrar("Abc XyZ", 29))   # equivale a k=3
    print("Cifrado (k=-3):", cesar_cifrar("Def AbC", -3))

    msg = "Hola Mundo!"
    r = rot13(msg)
    vuelta = rot13(r)

    print("\nMensaje:", msg)
    print("ROT13:", r)
    print("ROT13(ROT13):", vuelta)

    msg = "Hola Mundo!"
    clave = "CLAVE"

    c = vigenere_cifrar(msg, clave)
    p = vigenere_descifrar(c, clave)

    print("\nMensaje:", msg)
    print("Clave:", clave)
    print("Cifrado Vigenere:", c)
    print("Descifrado:", p)

    texto = "\nEste es un ejemplo sencillo para analizar frecuencias."
    tabla = analisis_frecuencia(texto)

    print(texto)
    print("Letra | Conteo | Porcentaje")
    print("---------------------------")
    for letra, count, pct in tabla:
        if count > 0:
            print(f"  {letra}   |   {count:3d}   | {pct:6.2f}%")

# Referencias
# OpenAI. (2026). ChatGPT (versión del 2 de febrero) [Modelo de lenguaje de gran tamaño]. https://chat.openai.com/
# Utilizado como apoyo para consultar sobre el funcionamiento de los algoritmos de cifrado históricos.
