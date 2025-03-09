import base64

def convertir_a_base64(ruta_archivo):
    with open(ruta_archivo, "rb") as file:
        return base64.b64encode(file.read()).decode()

cer_base64 = convertir_a_base64("mi_certificado.cer")
key_base64 = convertir_a_base64("mi_llave.key")

print("CER Base64:\n", cer_base64)
print("KEY Base64:\n", key_base64)
