from lxml import etree
import base64
import re
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def validar_sello(xml_path, cer_path):
    """
    Valida el sello digital en un CFDI 4.0 verificando su autenticidad con la llave pública del CSD.
    """
    try:
        # Cargar el XML y extraer la raíz
        xml_doc = etree.parse(xml_path)
        root = xml_doc.getroot()

        # Definir espacio de nombres CFDI 4.0
        ns = {"cfdi": "http://www.sat.gob.mx/cfd/4"}

        # Extraer el nodo Comprobante y su atributo 'Sello'
        comprobante = root.xpath("//cfdi:Comprobante", namespaces=ns)
        if not comprobante:
            print("❌ ERROR: No se encontró el nodo 'Comprobante' en el XML.")
            return

        sello = comprobante[0].get("Sello")
        if not sello:
            print("❌ ERROR: El XML no tiene un sello digital.")
            return

        print("✅ Sello encontrado en el XML:", sello[:50] + "...")

        # Validar formato Base64 del sello
        if not validar_base64(sello):
            print("❌ ERROR: El sello no es un Base64 válido.")
            return
        print("✅ El sello tiene un formato Base64 válido.")

        # Generar la cadena original del XML
        cadena_original = generar_cadena_original(xml_path, "cadenaoriginal_4_0.xslt")
        if not cadena_original:
            print("❌ ERROR: No se pudo generar la cadena original.")
            return
        print("✅ Cadena Original generada correctamente.")

        # Extraer la llave pública del CSD
        llave_publica = cargar_llave_publica(cer_path)
        if not llave_publica:
            print("❌ ERROR: No se pudo cargar la llave pública del CSD.")
            return
        print("✅ Llave pública del CSD cargada.")

        # Verificar la validez del sello digital
        if verificar_sello(cadena_original, sello, llave_publica):
            print("✅ El sello es válido y fue generado correctamente con el CSD.")
        else:
            print("❌ ERROR: El sello no es válido o no coincide con la llave pública.")

    except Exception as e:
        print(f"❌ ERROR al validar el XML: {e}")

def validar_base64(cadena):
    """Verifica si una cadena tiene un formato Base64 válido."""
    patron = r'^[A-Za-z0-9+/]+={0,2}$'  # Base64 puede terminar en '=' o '=='
    return bool(re.match(patron, cadena))

def generar_cadena_original(xml_path, xslt_path):
    """Genera la cadena original a partir del XML CFDI usando XSLT."""
    try:
        xml_doc = etree.parse(xml_path)
        xslt_doc = etree.parse(xslt_path)
        transform = etree.XSLT(xslt_doc)
        resultado = transform(xml_doc)
        cadena = str(resultado).strip()
        print(f"Resultado de transformación: {cadena[:50]}...")
        return cadena
    except Exception as e:
        print(f"❌ Error al generar la cadena original: {e}")
        return None

def cargar_llave_publica(cer_path):
    """Carga la llave pública desde el certificado CSD (.cer)."""
    try:
        with open(cer_path, "rb") as cer_file:
            cer_data = cer_file.read()

        try:
            cert = x509.load_der_x509_certificate(cer_data, default_backend())
            print("Certificado cargado en formato DER")
        except Exception:
            cert = x509.load_pem_x509_certificate(cer_data, default_backend())
            print("Certificado cargado en formato PEM")

        return cert.public_key()
    except Exception as e:
        print(f"❌ Error al cargar la llave pública: {e}")
        return None

def verificar_sello(cadena_original, sello, llave_publica):
    """Verifica si el sello digital es válido utilizando la llave pública del CSD."""
    try:
        firma = base64.b64decode(sello)
        llave_publica.verify(
            firma,
            cadena_original.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True  # La firma es válida si no se lanza una excepción
    except Exception as e:
        print(f"❌ ERROR al verificar el sello: {e}")
        return False

# Rutas de los archivos de prueba
xml_firmado_path = "cfdi_firmado.xml"
certificado_csd_path = "mi_certificado.cer"

# Ejecutar la validación del sello
validar_sello(xml_firmado_path, certificado_csd_path)