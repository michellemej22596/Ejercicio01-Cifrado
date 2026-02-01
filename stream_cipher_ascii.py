# stream_cipher_b64.py
# Requerimientos:
# 1) Generar llaves dinámicas (ASCII)
# 2) Generar cipher en ASCII usando llave k fija (salida representada en Base64)
# 3) Generar cipher en ASCII usando llave k dinámica (salida representada en Base64)
#
# Nota: El XOR se aplica SIEMPRE sobre binario (bytes).
# La salida se devuelve como Base64 para que sea imprimible/transportable.

from binario import texto_a_ascii_binario, ascii_binario_a_texto
from xor import xor_binario
from base64 import binario_a_base64, base64_a_binario
from binario import ASCII_TABLE 

ALFABETO_LLAVE = []
for ch in ASCII_TABLE:
    if ch not in ['\n', '\t']:
        ALFABETO_LLAVE.append(ch)



def _hash_ascii_simple(texto):
    """
    Mezcla simple para obtener semilla (NO criptográfico).
    Suficiente para ejercicio didáctico de keystream.
    """
    h = 0
    for c in texto:
        h = (h * 131 + ord(c)) % (2**32)
    return h


def _lcg_next(x):
    """
    PRNG LCG: x_{n+1} = (a*x_n + c) mod 2^32
    (didáctico, no seguro para uso real)
    """
    a = 1664525
    c = 1013904223
    return (a * x + c) % (2**32)


# ============================================================
# 1) Generación de llaves dinámicas (ASCII)
# ============================================================
def generar_llave_dinamica_ascii(longitud, semilla="seed", nonce="0"):
    """
    Genera una llave/keystream ASCII imprimible de longitud dada.

    - semilla: "clave maestra" (puede ser una palabra)
    - nonce: valor que DEBE cambiar por mensaje para no repetir keystream
    """
    if longitud <= 0:
        raise ValueError("La longitud debe ser > 0")

    state = _hash_ascii_simple(str(semilla) + "|" + str(nonce))

    llave = ""
    for _ in range(longitud):
        state = _lcg_next(state)
        idx = state % len(ALFABETO_LLAVE)
        llave += ALFABETO_LLAVE[idx]

    return llave


def _repetir_llave(llave, longitud_objetivo):
    """Repite cíclicamente la llave hasta cubrir longitud_objetivo."""
    if len(llave) == 0:
        raise ValueError("La llave no puede ser vacía")

    out = ""
    i = 0
    while len(out) < longitud_objetivo:
        out += llave[i]
        i += 1
        if i == len(llave):
            i = 0
    return out


# ============================================================
# 2) Cipher con llave k fija (salida Base64)
# ============================================================
def cifrar_ascii_llave_fija_a_base64(mensaje_ascii, llave_fija_ascii):
    """
    Cifra un mensaje ASCII usando una llave ASCII fija.
    Si la llave es más corta, se repite.

    Flujo:
    ASCII -> BIN -> XOR -> BIN(cipher) -> BASE64 (imprimible)
    """
    if len(mensaje_ascii) == 0:
        return ""

    llave_expandida = _repetir_llave(llave_fija_ascii, len(mensaje_ascii))

    m_bin = texto_a_ascii_binario(mensaje_ascii)
    k_bin = texto_a_ascii_binario(llave_expandida)

    c_bin = xor_binario(m_bin, k_bin, modo_clave="estricto")
    cipher_b64 = binario_a_base64(c_bin)
    return cipher_b64


def descifrar_base64_con_llave_fija(cipher_base64, llave_fija_ascii):
    """
    Descifra un cipher Base64 usando la misma llave fija ASCII.
    (descifrar = XOR con misma llave)

    Flujo:
    BASE64 -> BIN(cipher) -> XOR -> BIN(plain) -> ASCII
    """
    if len(cipher_base64) == 0:
        return ""

    c_bin = base64_a_binario(cipher_base64)

    # reconstruimos cuántos caracteres tenía el mensaje (1 char = 1 byte = 8 bits)
    n_chars = len(c_bin) // 8
    llave_expandida = _repetir_llave(llave_fija_ascii, n_chars)

    k_bin = texto_a_ascii_binario(llave_expandida)
    m_bin = xor_binario(c_bin, k_bin, modo_clave="estricto")

    # aquí sí esperamos texto "normal" => usamos la conversión estándar
    mensaje = ascii_binario_a_texto(m_bin, acepta_espacios=False)
    return mensaje


# ============================================================
# 3) Cipher con llave k dinámica (salida Base64)
# ============================================================
def cifrar_ascii_llave_dinamica_a_base64(mensaje_ascii, clave_maestra, nonce):
    """
    Cifra usando una llave/keystream dinámica del tamaño exacto del mensaje.
    La llave se genera con (clave_maestra + nonce).

    IMPORTANTE: no reutilizar nonce con la misma clave_maestra.
    """
    if len(mensaje_ascii) == 0:
        return ""

    llave_dinamica = generar_llave_dinamica_ascii(
        longitud=len(mensaje_ascii),
        semilla=clave_maestra,
        nonce=nonce
    )

    m_bin = texto_a_ascii_binario(mensaje_ascii)
    k_bin = texto_a_ascii_binario(llave_dinamica)

    c_bin = xor_binario(m_bin, k_bin, modo_clave="estricto")
    cipher_b64 = binario_a_base64(c_bin)
    return cipher_b64


def descifrar_base64_con_llave_dinamica(cipher_base64, clave_maestra, nonce):
    """
    Descifra un cipher Base64 usando (clave_maestra + nonce) para regenerar
    exactamente la misma llave dinámica.
    """
    if len(cipher_base64) == 0:
        return ""

    c_bin = base64_a_binario(cipher_base64)
    n_chars = len(c_bin) // 8

    llave_dinamica = generar_llave_dinamica_ascii(
        longitud=n_chars,
        semilla=clave_maestra,
        nonce=nonce
    )

    k_bin = texto_a_ascii_binario(llave_dinamica)
    m_bin = xor_binario(c_bin, k_bin, modo_clave="estricto")

    mensaje = ascii_binario_a_texto(m_bin, acepta_espacios=False)
    return mensaje


if __name__ == "__main__":
    # Pruebas rápidas
    mensaje = "Hola 123!"
    print("Mensaje:", mensaje)

    print("\n(1) Llave dinámica (ejemplo)")
    print(generar_llave_dinamica_ascii(12, semilla="MASTERKEY", nonce="0001"))

    print("\n(2) Cifrado con llave fija -> Base64")
    llave_fija = "CLAVE"
    c1 = cifrar_ascii_llave_fija_a_base64(mensaje, llave_fija)
    p1 = descifrar_base64_con_llave_fija(c1, llave_fija)
    print("Cipher Base64:", c1)
    print("Plain:", p1)

    print("\n(3) Cifrado con llave dinámica -> Base64")
    clave_maestra = "MASTERKEY"
    nonce = "0001"
    c2 = cifrar_ascii_llave_dinamica_a_base64(mensaje, clave_maestra, nonce)
    p2 = descifrar_base64_con_llave_dinamica(c2, clave_maestra, nonce)
    print("Cipher Base64:", c2)
    print("Plain:", p2)
