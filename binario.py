ASCII_TABLE = {
    # Mayúsculas
    'A': 65, 'B': 66, 'C': 67, 'D': 68,
    'E': 69, 'F': 70, 'G': 71, 'H': 72,
    'I': 73, 'J': 74, 'K': 75, 'L': 76,
    'M': 77, 'N': 78, 'O': 79, 'P': 80,
    'Q': 81, 'R': 82, 'S': 83, 'T': 84,
    'U': 85, 'V': 86, 'W': 87, 'X': 88,
    'Y': 89, 'Z': 90,

    # Minúsculas
    'a': 97, 'b': 98, 'c': 99, 'd': 100,
    'e': 101, 'f': 102, 'g': 103, 'h': 104,
    'i': 105, 'j': 106, 'k': 107, 'l': 108,
    'm': 109, 'n': 110, 'o': 111, 'p': 112,
    'q': 113, 'r': 114, 's': 115, 't': 116,
    'u': 117, 'v': 118, 'w': 119, 'x': 120,
    'y': 121, 'z': 122,

    # Números
    '0': 48, '1': 49, '2': 50, '3': 51, '4': 52,
    '5': 53, '6': 54, '7': 55, '8': 56, '9': 57,

    # Espacios y control básico
    ' ': 32,
    '\n': 10,
    '\t': 9,

    # Signos comunes
    '.': 46, ',': 44, ';': 59, ':': 58,
    '!': 33, '?': 63,
    '(': 40, ')': 41,
    '"': 34, "'": 39,
    '-': 45, '_': 95,
    '/': 47
}

# Invertimos: decimal -> carácter
ASCII_INV = {}
for ch in ASCII_TABLE:
    ASCII_INV[ASCII_TABLE[ch]] = ch


def decimal_a_binario(n):
    """Convierte un número decimal a binario (sin relleno). Manual."""
    if n == 0:
        return "0"

    bits = ""
    while n > 0:
        bits = str(n % 2) + bits
        n = n // 2

    return bits


def rellenar_a_n_bits(binario, n_bits):
    """Rellena con ceros a la izquierda hasta n_bits."""
    while len(binario) < n_bits:
        binario = "0" + binario
    return binario


def es_binario(cadena):
    """Valida si una cadena contiene solo 0 y 1."""
    for c in cadena:
        if c != '0' and c != '1':
            return False
    return True


def texto_a_ascii_binario_lista(texto):
    """
    ASCII -> lista de bytes binarios (strings de 8 bits), manual.
    Ej: "Hola" -> ["01001000","01101111","01101100","01100001"]
    """
    resultado = []

    for caracter in texto:
        if caracter not in ASCII_TABLE:
            raise ValueError(f"Carácter no soportado: {repr(caracter)}")

        ascii_decimal = ASCII_TABLE[caracter]
        ascii_binario = decimal_a_binario(ascii_decimal)
        ascii_binario = rellenar_a_n_bits(ascii_binario, 8)

        resultado.append(ascii_binario)

    return resultado


def texto_a_ascii_binario(texto, separador=""):
    """
    ASCII -> binario (string). Por defecto concatena.
    separador=" " devuelve bytes separados por espacio.
    """
    lista = texto_a_ascii_binario_lista(texto)
    if separador == "":
        return "".join(lista)
    return separador.join(lista)


def binario_a_decimal(binario):
    """Convierte un binario (string) a decimal, manual."""
    if not es_binario(binario) or len(binario) == 0:
        raise ValueError("Binario inválido")

    decimal = 0
    potencia = 0

    for bit in reversed(binario):
        if bit == '1':
            decimal += 2 ** potencia
        potencia += 1

    return decimal


def dividir_en_bytes(binario):
    """
    Divide un binario (string) en bytes de 8 bits.
    Requiere longitud múltiplo de 8.
    """
    if not es_binario(binario):
        raise ValueError("La entrada debe ser binaria (solo 0 y 1)")

    if len(binario) % 8 != 0:
        raise ValueError("La longitud del binario debe ser múltiplo de 8 para dividir en bytes")

    bytes_ = []
    i = 0
    while i < len(binario):
        bytes_.append(binario[i:i+8])
        i += 8

    return bytes_


def ascii_binario_lista_a_texto(lista_binarios):
    """
    Lista de bytes binarios (8 bits) -> ASCII, manual.
    """
    texto = ""

    for byte in lista_binarios:
        if len(byte) != 8 or not es_binario(byte):
            raise ValueError(f"Bloque inválido (debe ser 8 bits): {byte}")

        ascii_decimal = binario_a_decimal(byte)

        if ascii_decimal not in ASCII_INV:
            raise ValueError(f"Código ASCII no soportado: {ascii_decimal}")

        texto += ASCII_INV[ascii_decimal]

    return texto


def ascii_binario_a_texto(binario, acepta_espacios=True):
    """
    Binario (string) -> ASCII.
    - Si acepta_espacios=True, permite entradas tipo: '01001000 01101001'
    - Si no, espera todo concatenado.
    """
    if acepta_espacios:
        # eliminar espacios y saltos
        compacto = ""
        for c in binario:
            if c in ['0', '1']:
                compacto += c
            elif c in [' ', '\n', '\t', '\r']:
                continue
            else:
                raise ValueError(f"Carácter inválido en binario: {repr(c)}")
        binario = compacto

    lista_bytes = dividir_en_bytes(binario)
    return ascii_binario_lista_a_texto(lista_bytes)


if __name__ == "__main__":
    texto = "Hola 123!"
    b_lista = texto_a_ascii_binario_lista(texto)
    print("Lista bytes:", b_lista)

    #b_concat = texto_a_ascii_binario(texto)
    #print("Binario concat:", b_concat)

    recuperado = ascii_binario_lista_a_texto(b_lista)
    print("Recuperado:", recuperado)

    #recuperado2 = ascii_binario_a_texto(" ".join(b_lista))
    #print("Recuperado (con espacios):", recuperado2)

# Referencias
# OpenAI. (2026). ChatGPT (versión del 28 de enero) [Modelo de lenguaje de gran tamaño]. https://chat.openai.com/
# Utilizado como referencia para funciones de cifrado y tablas ASCII.