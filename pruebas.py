from binario import (
    texto_a_ascii_binario_lista,
    texto_a_ascii_binario,
    ascii_binario_a_texto
)

from base64 import (
    base64_a_binario,
    binario_a_base64,
    base64_a_ascii,
    ascii_a_base64
)

from xor import xor_binario


def imprimir_titulo(titulo):
    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)


def prueba_ascii_binario():
    imprimir_titulo("1) ASCII -> BINARIO y BINARIO -> ASCII")

    texto = "Hola 123!"
    b_lista = texto_a_ascii_binario_lista(texto)
    b_concat = texto_a_ascii_binario(texto)
    b_con_espacios = " ".join(b_lista)

    print("Texto:", texto)
    print("BIN (lista bytes):", b_lista)
    print("BIN (concat):", b_concat)
    print("BIN (con espacios):", b_con_espacios)

    rec1 = ascii_binario_a_texto(b_concat, acepta_espacios=False)
    rec2 = ascii_binario_a_texto(b_con_espacios, acepta_espacios=True)

    print("Recuperado (concat):", rec1)
    print("Recuperado (espacios):", rec2)


def prueba_base64_binario():
    imprimir_titulo("2) BASE64 -> BINARIO y BINARIO -> BASE64 (con padding)")

    casos = [
        ("TQ==", "M"),       # 1 byte -> '=='
        ("TWE=", "Ma"),      # 2 bytes -> '='
        ("TWFu", "Man"),     # 3 bytes -> sin '='
        ("SG9sYQ==", "Hola") # ejemplo clásico
    ]

    for b64, esperado_ascii in casos:
        print("\nBase64:", b64)
        b = base64_a_binario(b64)
        print("BIN (bytes):", " ".join([b[i:i+8] for i in range(0, len(b), 8)]))
        b64_roundtrip = binario_a_base64(b)
        print("Base64 (roundtrip):", b64_roundtrip)

        ascii = base64_a_ascii(b64)
        print("ASCII:", ascii, "| esperado:", esperado_ascii)


def prueba_ascii_base64_via_binario():
    imprimir_titulo("3) ASCII -> BASE64 (pasando por BINARIO) y vuelta")

    texto = "Hola"
    b64 = ascii_a_base64(texto)
    vuelta = base64_a_ascii(b64)

    print("ASCII:", texto)
    print("BASE64:", b64)
    print("Vuelta ASCII:", vuelta)


def prueba_xor():
    imprimir_titulo("4) XOR sobre BINARIO (cifrar y descifrar)")

    # Caso 1: 1 byte (modo estricto)
    mensaje = "01001000"   # 'H'
    clave   = "10101010"

    cifrado = xor_binario(mensaje, clave, modo_clave="estricto")
    descifrado = xor_binario(cifrado, clave, modo_clave="estricto")

    print("Mensaje:", mensaje)
    print("Clave:", clave)
    print("Cifrado:", cifrado)
    print("Descifrado:", descifrado)

    # Caso 2: varios bytes (modo repetir)
    mensaje2 = texto_a_ascii_binario("Hola")  # binario concatenado
    clave_corta = "1010"

    cif2 = xor_binario(mensaje2, clave_corta, modo_clave="repetir")
    dec2 = xor_binario(cif2, clave_corta, modo_clave="repetir")

    print("\nMensaje2 (Hola en BIN):", mensaje2)
    print("Clave corta:", clave_corta, "(modo repetir)")
    print("Cifrado2:", cif2)
    print("Descifrado2:", dec2)
    print("Descifrado2 -> ASCII:", ascii_binario_a_texto(dec2, acepta_espacios=False))


def main():
    prueba_ascii_binario()
    prueba_base64_binario()
    prueba_ascii_base64_via_binario()
    prueba_xor()

    imprimir_titulo("✅ Fin de pruebas")


if __name__ == "__main__":
    main()

# Referencias
# OpenAI. (2026). ChatGPT (versión del 28 de enero) [Modelo de lenguaje de gran tamaño]. https://chat.openai.com/
# Utilizado como referencia para ejecución de pruebas y validación de funciones.