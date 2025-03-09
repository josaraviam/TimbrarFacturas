from datetime import datetime
from decimal import Decimal
from fiscalapi.models.common_models import FiscalApiSettings
from fiscalapi.services.fiscalapi_client import FiscalApiClient
from fiscalapi.models.fiscalapi_models import Invoice, InvoiceIssuer, InvoiceItem, InvoiceRecipient, ItemTax, TaxCredential

# Configuración de credenciales para el uso de FiscalAPI
settings = FiscalApiSettings(
    api_url="https://test.fiscalapi.com",
    api_key="sk_test_c831609a_751c_49cf_8d8f_2b735fb8b3c8",
    tenant="05607109-b33c-45fb-9eff-5bbd9d752aa5"
)

# Crear cliente de FiscalAPI
client = FiscalApiClient(settings=settings)

# Base64 de los archivos CER y KEY (para autenticación y firma)
CER_BASE64 = """MIIF0TCCA7mgAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDMyODIwDQYJKoZIhvcNAQELBQAwggEr..."""
KEY_BASE64 = """MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAgEAAoIBAQACAggAMBQGCCqGSIb..."""

# Crear objeto Invoice con los datos de la factura a timbrar
invoice = Invoice(
    version_code="4.0",  # Versión del CFDI
    series="A",  # Serie del comprobante
    folio="12345",  # Número de folio
    date=datetime.strptime("2024-03-05T12:00:00", "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S"),
    payment_form_code="01",  # Forma de pago
    payment_conditions="Contado",  # Condiciones de pago
    currency_code="MXN",  # Moneda
    type_code="I",  # Tipo de comprobante (Ingreso)
    expedition_zip_code="64000",  # Código postal de expedición
    payment_method_code="PUE",  # Método de pago
    exchange_rate=1,  # Tipo de cambio
    export_code="01",  # Código de exportación

    # Datos del Emisor (empresa que emite la factura)
    issuer=InvoiceIssuer(
        tin="AAA010101AX5",  # RFC del emisor
        legal_name="EMPRESA EMISORA S.A. DE C.V.",  # Razón social del emisor
        tax_regime_code="601",  # Régimen fiscal del emisor
        tax_credentials=[  # Archivos de firma digital
            TaxCredential(
                base64_file=CER_BASE64,
                file_type=0,  # Certificado
                password="12345678a"
            ),
            TaxCredential(
                base64_file=KEY_BASE64,
                file_type=1,  # Llave privada
                password="12345678a"
            )
        ]
    ),

    # Datos del Receptor (cliente que recibe la factura)
    recipient=InvoiceRecipient(
        tin="BBB020202BX6",  # RFC del receptor
        legal_name="CLIENTE EJEMPLO",  # Nombre del receptor
        zip_code="64000",  # Código postal del receptor
        tax_regime_code="601",  # Régimen fiscal del receptor
        cfdi_use_code="G03"  # Uso del CFDI
    ),

    # Detalles de los productos/servicios facturados
    items=[
        InvoiceItem(
            item_code="01010101",  # Clave de producto/servicio
            quantity=Decimal("1"),  # Cantidad de unidades
            unit_of_measurement_code="H87",  # Clave de unidad de medida
            description="Producto de prueba",  # Descripción del producto
            unit_price=Decimal("1000.00"),  # Precio unitario
            tax_object_code="02",  # Código de objeto de impuesto
            discount=Decimal("0.00"),  # Descuento aplicado
            item_sku="7501000101010",  # SKU del producto
            item_taxes=[  # Impuestos aplicables
                ItemTax(
                    tax_code="002",  # Código de impuesto (IVA)
                    tax_type_code="Tasa",  # Tipo de impuesto
                    tax_rate=Decimal("0.160000"),  # Tasa de impuesto (16%)
                    tax_flag_code="T"  # Tipo de factor
                )
            ]
        )
    ]
)

# Enviar solicitud de timbrado al servicio de FiscalAPI
api_response = client.invoices.create(invoice)

# Verificar si la factura fue timbrada exitosamente
if api_response.succeeded:
    print("✅ Factura timbrada con éxito!")
    print("UUID:", api_response.data.uuid)

    # Guardar el XML timbrado en un archivo local
    with open("factura_timbrada.xml", "w", encoding="utf-8") as file:
        file.write(api_response.data.xml)
    print("📄 Factura guardada en 'factura_timbrada.xml'.")
else:
    print("❌ ERROR en timbrado:", api_response.message)
