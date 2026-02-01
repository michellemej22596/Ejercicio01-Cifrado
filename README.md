# Conversión ASCII, BINARIO, BASE64 y XOR (Implementación Manual)
### Michelle Mejía Villela 22596

##  Descripción

Este proyecto implementa conversiones manuales entre:

* ASCII ↔ BINARIO (8 bits)
* BASE64 ↔ BINARIO
* BASE64 ↔ ASCII (pasando por binario)
* Aplicación de XOR sobre binario

Todas las conversiones se realizan manualmente, sin usar librerías como `base64` o funciones automáticas de conversión.

---

## Estructura del Proyecto

```
binario.py     → Conversión ASCII ↔ BINARIO
base64.py      → Conversión BASE64 ↔ BINARIO y BASE64 ↔ ASCII
xor.py         → Aplicación de XOR sobre binario
pruebas.py     → Script de pruebas generales
README.md      → Documentación del proyecto
```

---

# ASCII ↔ BINARIO

Archivo: `binario.py`

### ASCII → BINARIO

Convierte texto ASCII a binario (8 bits por carácter).

```python
from binario import texto_a_ascii_binario

texto = "Hola"
binario = texto_a_ascii_binario(texto)
print(binario)
```

Salida:

```
01001000011011110110110001100001
```

---

### BINARIO → ASCII

```python
from binario import ascii_binario_a_texto

binario = "01001000011011110110110001100001"
texto = ascii_binario_a_texto(binario)
print(texto)
```

Salida:

```
Hola
```

---

# BASE64 ↔ BINARIO

Archivo: `base64.py`

### BASE64 → BINARIO

```python
from base64 import base64_a_binario

b = base64_a_binario("SG9sYQ==")
print(b)
```

Salida (bytes en binario):

```
01001000011011110110110001100001
```

---

### BINARIO → BASE64

```python
from base64 import binario_a_base64

binario = "01001000011011110110110001100001"
b64 = binario_a_base64(binario)
print(b64)
```

Salida:

```
SG9sYQ==
```

---

# BASE64 ↔ ASCII (pasando por BINARIO)

### BASE64 → ASCII

```python
from base64 import base64_a_ascii

print(base64_a_ascii("SG9sYQ=="))
```

Salida:

```
Hola
```

---

### ASCII → BASE64

```python
from base64 import ascii_a_base64

print(ascii_a_base64("Hola"))
```

Salida:

```
SG9sYQ==
```

---

# XOR sobre BINARIO

Archivo: `xor.py`

### Modo Estricto (misma longitud)

```python
from xor import xor_binario

mensaje = "01001000"
clave   = "10101010"

cifrado = xor_binario(mensaje, clave, modo_clave="estricto")
print(cifrado)

descifrado = xor_binario(cifrado, clave, modo_clave="estricto")
print(descifrado)
```

---

### Modo Repetir Clave

```python
mensaje = "0100100001101111"
clave = "1010"

cifrado = xor_binario(mensaje, clave, modo_clave="repetir")
descifrado = xor_binario(cifrado, clave, modo_clave="repetir")
```

---

# Ejecutar Pruebas

Para ejecutar todas las pruebas:

```bash
python pruebas.py
```

El script valida:

* ASCII ↔ BINARIO
* BASE64 ↔ BINARIO
* BASE64 ↔ ASCII
* ASCII ↔ BASE64
* XOR (cifrado y descifrado)