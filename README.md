# Informe: Proceso de Generación, Firma y Timbrado de CFDI 4.0

## Resumen Ejecutivo

Este informe presenta el proceso completo de generación, firma y timbrado de un Comprobante Fiscal Digital por Internet (CFDI) versión 4.0, utilizando Python como lenguaje de programación. Se han implementado todas las etapas requeridas para crear un CFDI válido, desde la construcción del documento XML hasta su timbrado mediante un Proveedor Autorizado de Certificación (PAC).

## Paso a Paso del Proceso
1. **Generación del XML CFDI**: Creación del documento estructurado según el Anexo 20 del SAT.
2. **Cálculo de la Cadena Original**: Transformación XSLT para obtener la representación canónica.
3. **Firma Digital**: Aplicación del sello digital utilizando la llave privada del CSD.
4. **Verificación**: Validación del sello digital para asegurar su integridad.
5. **Timbrado**: Envío a un PAC para obtener el Timbre Fiscal Digital (TFD).

## 1. Introducción

El Comprobante Fiscal Digital por Internet (CFDI) es el estándar de facturación electrónica implementado por el Servicio de Administración Tributaria (SAT) en México. Este informe detalla el proceso técnico para generar, firmar y timbrar un CFDI 4.0 utilizando Python, desde la creación del documento XML hasta la obtención del comprobante validado por el SAT.

## 2. Conceptos Fundamentales

### 2.1 ¿Qué es un CFDI?

El CFDI es un documento fiscal digital que cumple con los requisitos legales y normativos establecidos por el SAT. Reemplaza a las facturas tradicionales en papel y garantiza la autenticidad e integridad mediante firmas digitales.

### 2.2 Componentes del CFDI 4.0

- **XML Base**: Documento estructurado según el estándar definido en el Anexo 20 del SAT.
- **Cadena Original**: Representación textual de los datos fiscales relevantes del CFDI.
- **Sello Digital del Emisor**: Firma electrónica avanzada que garantiza la autoría e integridad.
- **Timbre Fiscal Digital (TFD)**: Sello digital añadido por el SAT a través de un PAC.
- **Certificados Digitales**: Archivos .cer y .key que validan la identidad del emisor.

### 2.3 Certificado de Sello Digital (CSD)

El CSD es emitido por el SAT y consta de dos archivos:
- **Certificado (.cer)**: Archivo público que contiene información del contribuyente.
- **Llave privada (.key)**: Archivo cifrado que permite generar el sello digital.

### 2.4 Proveedores Autorizados de Certificación (PAC)

Los PAC son empresas autorizadas por el SAT para validar, asignar folios y timbrar los CFDI. Actúan como intermediarios entre el contribuyente y el SAT.

## 3. Proceso Técnico Implementado

### 3.1 Generación del XML CFDI

El proceso inicia con la creación de un documento XML que cumple con la estructura definida en el Anexo 20 del SAT:

```python
from lxml import etree

# Crear el elemento raíz con los namespaces requeridos
comprobante = etree.Element("{http://www.sat.gob.mx/cfd/4}Comprobante", 
    Version="4.0",
    Serie="A", 
    Folio="12345",
    Fecha="2024-03-05T12:00:00",
    FormaPago="01",
    SubTotal="1000.00",
    Moneda="MXN",
    Total="1160.00",
    TipoDeComprobante="I",
    Exportacion="01",
    MetodoPago="PUE",
    LugarExpedicion="64000"
)

# Agregar nodos adicionales como Emisor, Receptor, Conceptos, etc.
```

### 3.2 Generación de la Cadena Original

La cadena original se genera aplicando una transformación XSLT al XML:

```python
def generar_cadena_original(xml_path, xslt_path):
    """Genera la cadena original aplicando la transformación XSLT."""
    try:
        xml_doc = etree.parse(xml_path)
        xslt_doc = etree.parse(xslt_path)
        transform = etree.XSLT(xslt_doc)
        cadena = transform(xml_doc)
        return str(cadena)
    except Exception as e:
        print(f"❌ Error al generar la cadena original: {e}")
        return None
```

Esta cadena es una representación textual de los datos fiscales más relevantes del comprobante, presentados en un formato específico definido por el SAT.

### 3.3 Firma Digital con el CSD

Utilizando la biblioteca `cryptography`, firmamos la cadena original con la llave privada (.key) del CSD:

```python
def firmar_cadena(cadena_original, llave_privada):
    """Firma la cadena original con la llave privada usando SHA256."""
    try:
        firma = llave_privada.sign(
            cadena_original.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        sello = base64.b64encode(firma).decode('utf-8')
        return sello
    except Exception as e:
        print(f"❌ Error al firmar la cadena original: {e}")
        return None
```

### 3.4 Inserción del Sello en el XML

El sello digital generado debe insertarse en el XML como atributo `Sello`:

```python
def insertar_sello_en_xml(xml_path, sello, output_path):
    """Inserta el sello digital en el XML CFDI."""
    try:
        xml_doc = etree.parse(xml_path)
        root = xml_doc.getroot()
        root.set("Sello", sello)
        xml_doc.write(output_path, xml_declaration=True, encoding='UTF-8')
        print(f"✅ XML firmado correctamente: {output_path}")
    except Exception as e:
        print(f"❌ Error al insertar el sello en el XML: {e}")
```

### 3.5 Verificación del Sello Digital

Es importante verificar que el sello se haya generado correctamente antes de enviar el CFDI al PAC:

```python
def verificar_sello(cadena_original, sello, llave_publica):
    """Verifica si el sello digital es válido usando la llave pública del CSD."""
    try:
        firma = base64.b64decode(sello)
        llave_publica.verify(
            firma,
            cadena_original.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"❌ ERROR al verificar el sello: {e}")
        return False
```

### 3.6 Timbrado con PAC

Finalmente, se envía el XML firmado a un Proveedor Autorizado de Certificación (PAC) para su timbrado:

#### Opción 1: Utilizando la API REST de SW (Smart Web)

```python
def timbrar_xml(token, xml_path):
    """Envía el archivo XML firmado a la API de timbrado."""
    url_timbrado = "http://services.test.sw.com.mx/cfdi40/issue/v4"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    with open(xml_path, "rb") as xml_file:
        files = {
            "xml": (xml_path.split("/")[-1], xml_file, "application/xml")
        }
        response = requests.post(url_timbrado, headers=headers, files=files)
        return response
```

#### Opción 2: Utilizando la biblioteca FiscalAPI

```python
from fiscalapi.models.common_models import FiscalApiSettings
from fiscalapi.services.fiscalapi_client import FiscalApiClient
from fiscalapi.models.fiscalapi_models import Invoice

# Configurar cliente
settings = FiscalApiSettings(
    api_url="https://test.fiscalapi.com",
    api_key="api_key",
    tenant="tenant_id"
)
client = FiscalApiClient(settings=settings)

# Enviar solicitud de timbrado
api_response = client.invoices.create(invoice)
```

El PAC valida el CFDI y, si es correcto, añade el Timbre Fiscal Digital (TFD) que contiene el sello del SAT y un UUID único.

## 4. Herramientas y Bibliotecas Utilizadas

### 4.1 Bibliotecas principales

- **lxml**: Para el manejo y procesamiento de documentos XML.
- **cryptography**: Para operaciones criptográficas (firma y verificación).
- **requests**: Para comunicación HTTP con las APIs de los PAC.
- **base64**: Para la codificación y decodificación de datos binarios.
- **fiscalapi**: SDK para interactuar con la API de FiscalAPI (segunda opción).

### 4.2 Recursos adicionales

- **cadenaoriginal_4_0.xslt**: Archivo de transformación proporcionado por el SAT.
- **Certificados de prueba**: CSD de prueba para entornos de desarrollo.

## 5. Desafíos y Soluciones

### 5.1 Problema con la generación de la cadena original

**Desafío**: Error "ElementTree not initialized, missing root" al intentar generar la cadena original.

**Solución**: Se modificó el método de carga del XSLT para usar `etree.parse()` directamente en lugar de leer los archivos manualmente y usar `fromstring()`.

```python
# Código problemático
xml_doc = etree.fromstring(contenido_xml.encode("utf-8"))
xslt_doc = etree.fromstring(contenido_xslt.encode("utf-8"))

# Solución
xml_doc = etree.parse(xml_path)
xslt_doc = etree.parse(xslt_path)
```

### 5.2 Dificultades con la carga del certificado

**Desafío**: Error al intentar cargar la llave pública desde el certificado CSD.

**Solución**: Implementación de un método más robusto que intenta cargar el certificado en diferentes formatos (DER y PEM):

```python
def cargar_llave_publica(cer_path):
    try:
        with open(cer_path, "rb") as cer_file:
            cer_data = cer_file.read()
        
        try:
            # Intentar como DER (formato binario)
            cert = x509.load_der_x509_certificate(cer_data, default_backend())
        except Exception:
            # Si falla, intentar como PEM (formato base64)
            cert = x509.load_pem_x509_certificate(cer_data, default_backend())
        
        public_key = cert.public_key()
        return public_key
    except Exception as e:
        print(f"❌ Error al cargar la llave pública: {e}")
        return None
```

## 6. Demostración Paso a Paso

Para facilitar la comprensión del proceso completo, a continuación se presenta una guía paso a paso de cómo ejecutar los scripts desarrollados para generar y timbrar un CFDI:

### 6.1 Requisitos Previos

1. **Instalación de dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Archivos necesarios**:
   - Certificados de prueba (.cer y .key)
   - Archivo XSLT para la transformación (cadenaoriginal_4_0.xslt)

### 6.2 Paso 1: Generar el XML CFDI

Ejecutar el script `generador_cfdi.py` para crear un XML CFDI básico:

```bash
python generador_cfdi.py
```

Este script genera un archivo `cfdi_generado.xml` con la estructura básica del CFDI 4.0, incluyendo datos del emisor, receptor, conceptos e impuestos.

### 6.3 Paso 2: Firmar el XML

Ejecutar el script `firma_cfdi.py` para calcular la cadena original y aplicar el sello digital:

```bash
python firma_cfdi.py
```

Este script realizará las siguientes acciones:
- Leer el XML generado
- Calcular la cadena original aplicando la transformación XSLT
- Cargar la llave privada
- Firmar la cadena original
- Insertar el sello en el XML
- Guardar el XML firmado como `cfdi_firmado.xml`

### 6.4 Paso 3: Verificar el XML Firmado

Ejecutar el script `verificador.py` para validar que la firma sea correcta:

```bash
python verificador.py
```

Este script:
- Extrae el sello del XML
- Recalcula la cadena original
- Carga la llave pública del certificado
- Verifica que el sello corresponda a la cadena original usando la llave pública

### 6.5 Paso 4: Timbrar el CFDI

Se proporcionan dos opciones para el timbrado:

**Opción 1**: Usando SmartWeb (API directa):
```bash
python timbrado2.py
```

**Opción 2**: Usando FiscalAPI (más abstraída):
```bash
python timbrado.py
```

Ambos scripts envían el XML firmado al PAC correspondiente y reciben el XML timbrado con el Timbre Fiscal Digital (TFD).

## 7. Conclusiones

### 7.1 Conclusiones

El proceso de generación, firma y timbrado de CFDI 4.0 en Python involucra múltiples etapas técnicas que requieren un manejo cuidadoso de:
- Formato XML según especificaciones del Anexo 20
- Transformaciones XSLT para generar la cadena original
- Operaciones criptográficas para firma y verificación
- Comunicación con APIs de PAC para el timbrado

La implementación desarrollada demuestra la viabilidad de automatizar completamente este proceso utilizando herramientas de código abierto, sin embargo, encontramos limitaciones para realizar el timbrado a no ser una empresa; intentamos solicitar en varias ocasiones el Token sin éxito, la siguiente opción era pagar membresías poco accesibles.

## 8. Evaluación de Alternativas

### 8.1 Comparación de Bibliotecas

| Biblioteca      | Ventajas                                     | Desventajas                               |
|-----------------|----------------------------------------------|--------------------------------------------|
| **lxml**        | Rápida, eficiente, soporte completo de XML   | Curva de aprendizaje más pronunciada       |
| **ElementTree** | Incluida en la biblioteca estándar           | Menos funcionalidades que lxml             |
| **pycfdi**      | Específica para CFDI                         | Menos flexible para casos particulares     |

### 8.2 Comparación de PACs

| PAC            | Ventajas                                     | Desventajas                                |
|----------------|----------------------------------------------|---------------------------------------------|
| **SW SmartWeb**| API bien documentada, sandbox gratuito       | Requiere gestión manual de tokens           |
| **FiscalAPI**  | API más abstraída, manejo integrado de CSD   | Mayor dependencia de biblioteca externa     |
| **Edicom**     | Estable y confiable                          | Documentación menos accesible              |

## 9. Referencias

1. SAT - Anexo 20 Versión 4.0: [Portal SAT](https://www.sat.gob.mx)
2. Documentación de lxml: [lxml.de](https://lxml.de/index.html)
3. Documentación de cryptography: [cryptography.io](https://cryptography.io)
4. API de SW SmartWeb: [Developer Portal SW](https://developers.sw.com.mx)
5. Documentación de FiscalAPI: [FiscalAPI Docs](https://fiscalapi.com/docs)
6. Estándar Técnico del Complemento de Timbre Fiscal Digital: [Documentación TFD](https://www.sat.gob.mx)
