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

ASCII_INV = {}
for caracter in ASCII_TABLE:
    ASCII_INV[ASCII_TABLE[caracter]] = caracter

def decimal_a_binario(n):
    if n == 0:
        return "0"

    bits = ""
    while n > 0:
        resto = n % 2
        bits = str(resto) + bits
        n = n // 2

    return bits

def rellenar_a_8_bits(binario):
    while len(binario) < 8:
        binario = "0" + binario
    return binario

def texto_a_ascii_binario_manual(texto):
    resultado = []

    for caracter in texto:
        if caracter not in ASCII_TABLE:
            raise ValueError(f"Carácter no soportado: {caracter}")

        ascii_decimal = ASCII_TABLE[caracter]
        ascii_binario = decimal_a_binario(ascii_decimal)
        ascii_binario = rellenar_a_8_bits(ascii_binario)

        resultado.append(ascii_binario)

    return resultado

def binario_a_decimal(binario):
    decimal = 0
    potencia = 0

    # recorremos de derecha a izquierda
    for bit in reversed(binario):
        if bit == '1':
            decimal += 2 ** potencia
        potencia += 1

    return decimal

def ascii_binario_a_texto_manual(lista_binarios):
    texto = ""

    for binario in lista_binarios:
        if len(binario) != 8:
            raise ValueError(f"Bloque inválido: {binario}")

        ascii_decimal = binario_a_decimal(binario)

        if ascii_decimal not in ASCII_INV:
            raise ValueError(f"Código ASCII no soportado: {ascii_decimal}")

        texto += ASCII_INV[ascii_decimal]

    return texto

binarios = [
    "01001000",
    "01101111",
    "01101100",
    "01100001"
]

# Texto a binario
texto = "Hola"
binario = texto_a_ascii_binario_manual(texto)

for c, b in zip(texto, binario):
    print(f"{c} -> {b}")

# Binario a texto
texto = ascii_binario_a_texto_manual(binarios)
print(texto)


