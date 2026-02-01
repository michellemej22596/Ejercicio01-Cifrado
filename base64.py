from binario import (
    decimal_a_binario,
    rellenar_a_n_bits,
    es_binario,
    dividir_en_bytes,
    ascii_binario_a_texto,
    texto_a_ascii_binario
)

BASE64_TABLE = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789+/"
)


def _base64_indice(caracter):
    """Busca manualmente el índice de un caracter en BASE64_TABLE."""
    indice = 0
    for simbolo in BASE64_TABLE:
        if simbolo == caracter:
            return indice
        indice += 1
    return -1


def _indice_a_6_bits(indice):
    """Convierte un número (0..63) a binario de 6 bits, manual."""
    b = decimal_a_binario(indice)
    return rellenar_a_n_bits(b, 6)


def _limpiar_base64(s):
    """Quita espacios/saltos por si vienen en el input."""
    limpio = ""
    for c in s:
        if c in [' ', '\n', '\t', '\r']:
            continue
        limpio += c
    return limpio


def base64_a_binario(texto_base64):
    """
    BASE64 -> BINARIO (de bytes, múltiplo de 8).
    Maneja padding '=' correctamente.

    Devuelve un string binario concatenado.
    """
    s = _limpiar_base64(texto_base64)

    if len(s) == 0:
        return ""

    if len(s) % 4 != 0:
        raise ValueError("Base64 inválido: la longitud debe ser múltiplo de 4")

    # Validación básica de '=': solo permitido al final (máximo 2)
    padding_total = 0
    if s.endswith("=="):
        padding_total = 2
    elif s.endswith("="):
        padding_total = 1

    # Si hay '=', debe estar solo en el último bloque
    if "=" in s[:-4]:
        raise ValueError("Base64 inválido: '=' solo puede aparecer en el último bloque")

    salida = ""

    i = 0
    while i < len(s):
        bloque = s[i:i+4]
        i += 4

        # contar padding en este bloque (solo puede ser 0,1,2)
        pad = 0
        for c in bloque:
            if c == "=":
                pad += 1

        if pad not in (0, 1, 2):
            raise ValueError("Base64 inválido: padding incorrecto")

        # convertir 4 chars -> 24 bits (6 bits c/u). '=' se trata como 0 en bits.
        bits24 = ""
        for c in bloque:
            if c == "=":
                bits24 += "000000"
            else:
                idx = _base64_indice(c)
                if idx == -1:
                    raise ValueError(f"Carácter Base64 inválido: {c}")
                bits24 += _indice_a_6_bits(idx)

        # cortar bits inválidos según padding:
        # pad=0 -> 24 bits (3 bytes)
        # pad=1 -> 16 bits (2 bytes)
        # pad=2 -> 8 bits  (1 byte)
        if pad == 0:
            salida += bits24
        elif pad == 1:
            salida += bits24[:16]
        else:  # pad == 2
            salida += bits24[:8]

    # Aseguramos múltiplo de 8 para bytes
    if len(salida) % 8 != 0:
        raise ValueError("Error interno: binario resultante no es múltiplo de 8")

    return salida


def binario_a_base64(binario):
    """
    BINARIO (múltiplo de 8) -> BASE64.
    Maneja padding '=' correctamente.
    Acepta binario con espacios/saltos; los ignora.
    """
    # limpiar binario (permitir separadores)
    compacto = ""
    for c in binario:
        if c in ['0', '1']:
            compacto += c
        elif c in [' ', '\n', '\t', '\r']:
            continue
        else:
            raise ValueError(f"Carácter inválido en binario: {repr(c)}")

    if len(compacto) == 0:
        return ""

    if not es_binario(compacto):
        raise ValueError("La entrada debe ser binaria (solo 0 y 1)")

    if len(compacto) % 8 != 0:
        raise ValueError("La longitud del binario debe ser múltiplo de 8 para convertir a Base64")

    bytes_ = dividir_en_bytes(compacto)

    resultado = ""
    j = 0
    while j < len(bytes_):
        # tomar hasta 3 bytes (24 bits)
        bloque_bytes = bytes_[j:j+3]
        j += 3

        n_bytes = len(bloque_bytes)
        bits24 = "".join(bloque_bytes)

        # si faltan bytes, rellenar con ceros hasta 24 bits
        if n_bytes < 3:
            bits24 += "0" * (8 * (3 - n_bytes))

        # 24 bits -> 4 grupos de 6 bits -> índices Base64
        grupos6 = [bits24[k:k+6] for k in range(0, 24, 6)]
        indices = []
        for g in grupos6:
            # convertir 6-bit binario a decimal manualmente
            dec = 0
            pot = 0
            for bit in reversed(g):
                if bit == '1':
                    dec += 2 ** pot
                pot += 1
            indices.append(dec)

        # armar 4 caracteres base64
        chars = ""
        for idx in indices:
            chars += BASE64_TABLE[idx]

        # aplicar padding según bytes reales:
        # 3 bytes -> 0 '='
        # 2 bytes -> 1 '='
        # 1 byte  -> 2 '='
        if n_bytes == 3:
            resultado += chars
        elif n_bytes == 2:
            resultado += chars[:3] + "="
        else:  # n_bytes == 1
            resultado += chars[:2] + "=="

    return resultado


def base64_a_ascii(texto_base64):
    """
    BASE64 -> ASCII pasando por BINARIO (bytes).
    """
    b = base64_a_binario(texto_base64)
    return ascii_binario_a_texto(b, acepta_espacios=False)


def ascii_a_base64(texto):
    """
    ASCII -> BINARIO -> BASE64 (útil para pruebas / completitud).
    """
    b = texto_a_ascii_binario(texto)  # binario concatenado
    return binario_a_base64(b)


if __name__ == "__main__":
    print("Base64->bin:", base64_a_binario("TQ=="))          # 'M' = 01001101
    print("Bin->Base64:", binario_a_base64("01001101"))      # TQ==
    print("Base64->ASCII:", base64_a_ascii("SG9sYQ=="))      # Hola
    print("ASCII->Base64:", ascii_a_base64("Hola"))          # SG9sYQ==

# Referencias
# OpenAI. (2026). ChatGPT (versión del 28 de enero) [Modelo de lenguaje de gran tamaño]. https://chat.openai.com/
# Utilizado como referencia para funciones de cifrado y tabla Base64.