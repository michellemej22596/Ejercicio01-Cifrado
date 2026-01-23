BASE64_TABLE = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789+/"
)

ASCII_TABLE = {
    'A': 65, 'B': 66, 'C': 67, 'D': 68,
    'E': 69, 'F': 70, 'G': 71, 'H': 72,
    'I': 73, 'J': 74, 'K': 75, 'L': 76,
    'M': 77, 'N': 78, 'O': 79, 'P': 80,
    'Q': 81, 'R': 82, 'S': 83, 'T': 84,
    'U': 85, 'V': 86, 'W': 87, 'X': 88,
    'Y': 89, 'Z': 90,
    'a': 97, 'b': 98, 'c': 99, 'd': 100,
    'e': 101, 'f': 102, 'g': 103, 'h': 104,
    'i': 105, 'j': 106, 'k': 107, 'l': 108,
    'm': 109, 'n': 110, 'o': 111, 'p': 112,
    'q': 113, 'r': 114, 's': 115, 't': 116,
    'u': 117, 'v': 118, 'w': 119, 'x': 120,
    'y': 121, 'z': 122,
    ' ': 32
}

# invertimos: decimal -> carácter
ASCII_INV = {}
for c in ASCII_TABLE:
    ASCII_INV[ASCII_TABLE[c]] = c


def decimal_a_binario_6_bits(n):
    bits = ""

    while n > 0:
        bits = str(n % 2) + bits
        n = n // 2

    # Relleno a 6 bits
    while len(bits) < 6:
        bits = "0" + bits

    return bits

def base64_a_binario_manual(texto_base64):
    resultado = []

    for caracter in texto_base64:
        # ignoramos padding
        if caracter == "=":
            continue

        # buscar índice en la tabla Base64
        indice = 0
        encontrado = False

        for simbolo in BASE64_TABLE:
            if simbolo == caracter:
                encontrado = True
                break
            indice += 1

        if not encontrado:
            raise ValueError(f"Carácter Base64 inválido: {caracter}")

        # convertir índice a binario (6 bits)
        binario = decimal_a_binario_6_bits(indice)
        resultado.append(binario)

    return resultado

binarios = base64_a_binario_manual("TQ==")

for b in binarios:
    print(b)

def binario_a_decimal_6_bits(binario):
    decimal = 0
    potencia = 0

    for bit in reversed(binario):
        if bit == '1':
            decimal += 2 ** potencia
        potencia += 1

    return decimal

def dividir_en_bloques_de_6(binario):
    bloques = []
    i = 0

    while i < len(binario):
        bloque = binario[i:i+6]

        if len(bloque) < 6:
            bloque = bloque + "0" * (6 - len(bloque))

        bloques.append(bloque)
        i += 6

    return bloques

def binario_a_base64_manual(binario):
    bloques = dividir_en_bloques_de_6(binario)
    resultado = ""

    for bloque in bloques:
        indice = binario_a_decimal_6_bits(bloque)
        resultado += BASE64_TABLE[indice]

    # cálculo simple de padding (=)
    resto = len(binario) % 24
    if resto == 8:
        resultado += "=="
    elif resto == 16:
        resultado += "="

    return resultado

base64 = binario_a_base64_manual("01001101")
print(base64)

def decimal_a_binario_6(n):
    bits = ""
    while n > 0:
        bits = str(n % 2) + bits
        n = n // 2

    while len(bits) < 6:
        bits = "0" + bits

    return bits

def base64_a_binario(texto_base64):
    binario = ""

    for caracter in texto_base64:
        if caracter == "=":
            continue

        indice = 0
        encontrado = False

        for simbolo in BASE64_TABLE:
            if simbolo == caracter:
                encontrado = True
                break
            indice += 1

        if not encontrado:
            raise ValueError(f"Carácter Base64 inválido: {caracter}")

        binario += decimal_a_binario_6(indice)

    return binario

def dividir_en_bytes(binario):
    bytes_ = []
    i = 0

    while i + 8 <= len(binario):
        bytes_.append(binario[i:i+8])
        i += 8

    return bytes_

def binario_a_decimal(binario):
    decimal = 0
    potencia = 0

    for bit in reversed(binario):
        if bit == '1':
            decimal += 2 ** potencia
        potencia += 1

    return decimal

def bytes_ascii_a_texto(lista_bytes):
    texto = ""

    for byte in lista_bytes:
        decimal = binario_a_decimal(byte)

        if decimal not in ASCII_INV:
            raise ValueError(f"ASCII no soportado: {decimal}")

        texto += ASCII_INV[decimal]

    return texto

def base64_a_ascii_manual(texto_base64):
    binario = base64_a_binario(texto_base64)
    bytes_ = dividir_en_bytes(binario)
    texto = bytes_ascii_a_texto(bytes_)
    return texto

resultado = base64_a_ascii_manual("SG9sYQ==")
print(resultado)

