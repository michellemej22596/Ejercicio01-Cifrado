BASE64_TABLE = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789+/"
)

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
