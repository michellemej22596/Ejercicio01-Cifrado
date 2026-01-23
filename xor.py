def xor_bits(bit_a, bit_b):
    # XOR manual
    if bit_a == bit_b:
        return '0'
    else:
        return '1'

def es_binario(cadena):
    for bit in cadena:
        if bit != '0' and bit != '1':
            return False
    return True

def validar_longitud(a, b):
    if len(a) != len(b):
        raise ValueError("Los binarios deben tener la misma longitud")

def xor_binario_manual(binario_a, binario_b):
    # Validaciones
    if not es_binario(binario_a) or not es_binario(binario_b):
        raise ValueError("Las entradas deben ser binarios válidos")

    validar_longitud(binario_a, binario_b)

    resultado = ""

    for i in range(len(binario_a)):
        bit_a = binario_a[i]
        bit_b = binario_b[i]

        bit_xor = xor_bits(bit_a, bit_b)
        resultado += bit_xor

    return resultado

mensaje = "01001000"
clave   = "10101010"

cifrado = xor_binario_manual(mensaje, clave)
print(cifrado)
descifrado = xor_binario_manual(cifrado, clave)
print(descifrado)

descifrado = xor_binario_manual(cifrado, clave)
print(descifrado)
