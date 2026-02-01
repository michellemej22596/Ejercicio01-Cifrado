from binario import es_binario

def _limpiar_binario(s):
    """Deja solo 0 y 1; permite espacios y saltos como separadores."""
    compacto = ""
    for c in s:
        if c == '0' or c == '1':
            compacto += c
        elif c in [' ', '\n', '\t', '\r']:
            continue
        else:
            raise ValueError(f"Carácter inválido en binario: {repr(c)}")
    return compacto


def xor_bits(bit_a, bit_b):
    """XOR manual de dos bits ('0' o '1')."""
    if bit_a == bit_b:
        return '0'
    return '1'


def xor_binario(binario_a, binario_b, modo_clave="estricto"):
    """
    Aplica XOR bit a bit entre dos binarios.

    modo_clave:
    - "estricto": exige misma longitud (como tu script original)
    - "repetir": si la clave es más corta, se repite cíclicamente

    Devuelve un string binario (sin espacios).
    """
    a = _limpiar_binario(binario_a)
    b = _limpiar_binario(binario_b)

    if len(a) == 0 or len(b) == 0:
        raise ValueError("Las entradas no pueden estar vacías")

    if not es_binario(a) or not es_binario(b):
        raise ValueError("Las entradas deben ser binarios válidos (solo 0 y 1)")

    if modo_clave not in ["estricto", "repetir"]:
        raise ValueError("modo_clave inválido. Usa 'estricto' o 'repetir'")

    if modo_clave == "estricto":
        if len(a) != len(b):
            raise ValueError("Los binarios deben tener la misma longitud (modo estricto)")
        clave = b
    else:
        # Repetimos la clave hasta igualar longitud de a
        clave = ""
        i = 0
        while len(clave) < len(a):
            clave += b[i]
            i += 1
            if i == len(b):
                i = 0

    # XOR manual
    resultado = ""
    for i in range(len(a)):
        resultado += xor_bits(a[i], clave[i])

    return resultado


if __name__ == "__main__":
    mensaje = "01001000"   # 'H'
    clave   = "10101010"

    cifrado = xor_binario(mensaje, clave, modo_clave="estricto")
    print("Cifrado:", cifrado)

    descifrado = xor_binario(cifrado, clave, modo_clave="estricto")
    print("Descifrado:", descifrado)

    # Ejemplo con clave corta (modo repetir)
    mensaje2 = "0100100001101111"  # 'Ho' en binario concatenado
    clave_corta = "1010"
    cif2 = xor_binario(mensaje2, clave_corta, modo_clave="repetir")
    print("Cifrado (repetir):", cif2)
    dec2 = xor_binario(cif2, clave_corta, modo_clave="repetir")
    print("Descifrado (repetir):", dec2)

# Referencias
# OpenAI. (2026). ChatGPT (versión del 28 de enero) [Modelo de lenguaje de gran tamaño]. https://chat.openai.com/
# Utilizado como referencia para limpiar binarios.
