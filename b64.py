import base64


def convertir_a_base64(ruta_archivo):
    """
    Convierte un archivo en Base64.

    Parámetros:
        ruta_archivo (str): Ruta del archivo a convertir.

    Retorna:
        str: Contenido del archivo en formato Base64.
    """
    try:
        with open(ruta_archivo, "rb") as file:
            return base64.b64encode(file.read()).decode()
    except FileNotFoundError:
        print(f"❌ ERROR: No se encontró el archivo: {ruta_archivo}")
        return None
    except Exception as e:
        print(f"❌ ERROR al convertir el archivo a Base64: {e}")
        return None


# Convertir archivos CER y KEY a Base64
cer_base64 = convertir_a_base64("mi_certificado.cer")
key_base64 = convertir_a_base64("mi_llave.key")

# Imprimir resultados si la conversión fue exitosa
if cer_base64:
    print("CER Base64:\n", cer_base64)
if key_base64:
    print("KEY Base64:\n", key_base64)
