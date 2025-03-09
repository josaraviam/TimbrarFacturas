from datetime import datetime
from decimal import Decimal
from fiscalapi.models.common_models import FiscalApiSettings
from fiscalapi.services.fiscalapi_client import FiscalApiClient
from fiscalapi.models.fiscalapi_models import Invoice, InvoiceIssuer, InvoiceItem, InvoiceRecipient, ItemTax, TaxCredential

# Configuración de credenciales
settings = FiscalApiSettings(
    api_url="https://test.fiscalapi.com",
    api_key="sk_test_c831609a_751c_49cf_8d8f_2b735fb8b3c8",
    tenant="05607109-b33c-45fb-9eff-5bbd9d752aa5"
)

# Crear cliente de FiscalAPI
client = FiscalApiClient(settings=settings)

# Base64 de los archivos CER y KEY (debes copiar los valores completos)
CER_BASE64 = """MIIF0TCCA7mgAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDMyODIwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWxpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMjMwNTA5MTgwNTQ5WhcNMjcwNTA4MTgwNTQ5WjCBxjEdMBsGA1UEAxMUWE9DSElMVCBDQVNBUyBDSEFWRVoxHTAbBgNVBCkTFFhPQ0hJTFQgQ0FTQVMgQ0hBVkVaMR0wGwYDVQQKExRYT0NISUxUIENBU0FTIENIQVZFWjELMAkGA1UEBhMCTVgxJTAjBgkqhkiG9w0BCQEWFnBydWViYXNAcHJ1ZWJhcy5nb2IubXgxFjAUBgNVBC0TDUNBQ1g3NjA1MTAxUDgxGzAZBgNVBAUTEkNBQ1g3NjA1MTBNR1RTSEMwNDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAJN+xYybIIpmty9Amhi7BbGUM6mKUL+fNBYQ6wVgbqoZdgFdiIdJ0+UoLosqvRB8Dxp2n8x75xsjQfj3MWUoWa5JODNNgBEcq54ddYom+K2R9PNb8l3pvTMYtmQmF4f8LePXwAgKCXVfG4pI7sy7lqarvwfb2F1wo1YyVXnl1kY1r6LVjOrnBaBcRq0zLmGnsLoMb+t3aWIzCsHxnEDY6POW9ooxEmmzpaMNlE5Y7QzbPH74gcINMF+VSI8nJEGk21XgITCR1uliMTbC0QIPouukRsLgP1EAV7Y9hv2yDpbMkHjOUuFcnEtATll8YgJU1yo28k1ghJQ5t2fGGtyg4lcCAwEAAaNPME0wDAYDVR0TAQH/BAIwADALBgNVHQ8EBAMCA9gwEQYJYIZIAYb4QgEBBAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMEBggrBgEFBQcDAjANBgkqhkiG9w0BAQsFAAOCAgEALcom2kjhjW+e+t8doZ2P/bFVXAF8uVN+4txpEUF89JiUObPC/GjvfKB5dNsJyN2z1JWLHn0+PRfTCRgA7F4KdKQT8x4k1237MeXlV3PHEPooWdh5GEfWzA3UJ0fRw97NUes9TQm23yZ9VUjLTdVvv3Bu7moEl+7LFeaFvd6bg2WPSgMIRNVjXRuOEOwXXXm4olAP1Oh4sbBdH5nsJhx2+J+ALfCFQNKcu0zmAzTO6YmTy4SS4tOXkkwtyQpc4Erg44f0Ep0h9eI6BG3paok8BqA4vStA41fVfKe+WUiDUHqaezzTj1ynSMl6qA4WSb6ZN8rHH0OjdsPZxOCv775H7DCnXxnp/RZPRSkvh1n9v//b+7q3ZA1XUXF1fy7QqpEUdU4pnEfnMnzQoQNSA5NtMme88/agbM23sXzdkjBk0WC0jbtmkigoYj/HzFMJBIgAuTta2q3jasR6WJK8Q5k6TK3n4f/paAkJxFyB7TvR53kcMkCokxgXKqlCkfRNFy7Z4tr8jilp7CqSBztV8iTypN/DCehFzcI0ncQhZNQAoRyCmgc6e41GX3J/VbeE2qNikE6RlP4jhu28wt9wI43jlxiljrnq4RbowStIWxKo3lemPsUieb9imLT+B8uS5GYXnrprdZmHkf2bzEXKO6zvw/JH6AR9K/lz5X5/0eAw9E0="""
KEY_BASE64 = """MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAgEAAoIBAQACAggAMBQGCCqGSIb3DQMHBAgwggS+AgEAMASCBMh4EHl7aNSCaMDA1VlRoXCZ5UUmqErAbuck7ujDnmKxSZDgtsIno8HqdidGQ3dOb38JDBucKxauR6VT75eH/iwAyQj+0oZpbZ4ZMVjyBWEADH5VrjXrq2K8ReolaYeqxCs/fwIo7P3cdChOnNY4j5Vq2EYWY/haqDvghg/iQx58KkbFfQvll631fUIPqGrl0Bb3+NKQ8CTuVOwupWnzgNsFqoW39gKn4ca+liIMp9Vhu1kPMfWymBIf7ZuQoMN2/TloDQ+fMcOAYmaI0npLdymGv1KcOasOv9Hgj3gyBE/+IBdOK72psET1AKIhIDfYHg00HiCOCCNYOIgxyIGoPhNFGQieWmhtzF3N2cku2IwwWsUhS0sIJwMOMc8AgDCNgp1cLBNRkGhnjHx/0Mh1reyyVJuH9wIMc0WMZ9IB+nN4hQeVceDFghtCbmwenGebyf+6/KUXbsYBa6/Ux5sPqBQOK5M0W2n0GE5qbHmd/2IHDG6m2ebbNWa95qyE8po+d5EGbOXmUAzbxfZxIZnQfppHNLSxrioe+/24v7nkgjVhNvTywCz9ArSowIyXG6zP3hLajvebsxDlfkTzu8oSrR5andrGxxhrttS6zzk3sInLO/bWCFPIpSdhcN5rYv4BvH+6kmAST0Yji7q+7/NWxwkBL4GZiaTA5bM6WUGJ4rwnIAM/6qKCLEoWdOB5fRlM5//btlZj1FlwyTxhbKpsgFbuV65fLY6dqRd6t50Xbh6rjJIFZTB02aJQ95ViWLk9p8U1V7xzs6dGCbkTygk6s1yWAIgwckoImXwxsyrf2hcbgy5Ri4c+txv5CYJgB3rKzPis3z/7YBVdiwrbKFMSW6cnSQ7kpohqse+Zj72g5amBCF2rvF9vF1HxQiQWGkf/oYu9gTyAAG/gjg3EhHgucrDGv6Irg3q90fpMTXhl8K0rwvZOExEyhb4f8lsAmjT0+/ZX/tpCdHSQAUPrIb30AR1rKLk+2IlYupv8W8L7oZ/IKQZTEqsvHwwxFOaeFe0czU6uOTxeVJYuMEpeiEI41TqTe54So3qQGct5V740BzAKUOnnQndglFddIn5bcqo6VjLaKPaUVqCI5Qo1zjNDbwf60cgNML68vXyFh+Ei0mg4xsyrjDIWgdH9sZ3nFPWvfdPqJK6dsw83SEpR+I9nllean7OZaNUQHvTnTPEVW7LNNrAH4MqtaseBkkuQJGGDK2IdbsglQfv0rq0rv0VWIHAx7n7uxQ0Zssd3/LoO3ilS9EFnsY0ZO9wFhl3/ypaSopqJLh8Ib0DFVzcYEmQfxRwBnip2U2yHaQgbN/CY47oI37YDyR56AUcI8DXLYiIuLRpuhiRx6V+80Js1UCQY9NrYuaxdTWtyKUvpBvk019Bb1JmkkVTdJ9nJ2Tn7V12OXXdKkT6Brw8pEOgwFCO/Rbd9xPlFLgIdnexlCjwE9a6uVojEO2IgMlkHBe3Y/zAS79MKvwk+xyjEcMqMpq19EPZFwi+wJZikymK7H021oVZPnePOtWEllsaxkluKv8C1sqtP6J0r3MliBdvH3usVBty0cfIjwvzenJzKUc1icBOnRnmlIP5t5WscfS6O1183yQpbayIGEroKFuRfvkF+8Und1ZYogxX6PEw="""

# Crear objeto Invoice
invoice = Invoice(
    version_code="4.0",
    series="A",
    folio="12345",
    date=datetime.strptime("2024-03-05T12:00:00", "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S"),
    payment_form_code="01",
    payment_conditions="Contado",
    currency_code="MXN",
    type_code="I",  # Factura de ingreso
    expedition_zip_code="64000",
    payment_method_code="PUE",
    exchange_rate=1,
    export_code="01",

    # Datos del Emisor
    issuer=InvoiceIssuer(
        tin="AAA010101AAA",
        legal_name="EMPRESA EMISORA S.A. DE C.V.",
        tax_regime_code="601",
        tax_credentials=[
            TaxCredential(
                base64_file=CER_BASE64,
                file_type=0,
                password="12345678a"
            ),
            TaxCredential(
                base64_file=KEY_BASE64,
                file_type=1,
                password="12345678a"
            )
        ]
    ),

    # Datos del Receptor (RFC corregido)
    recipient=InvoiceRecipient(
        tin="BBB020202XX9",  # Formato válido de RFC
        legal_name="CLIENTE EJEMPLO",
        zip_code="64000",
        tax_regime_code="601",
        cfdi_use_code="G03"
    ),

    # Conceptos (con ItemSku corregido)
    items=[
        InvoiceItem(
            item_code="01010101",
            quantity=Decimal("1"),
            unit_of_measurement_code="H87",
            description="Producto de prueba",
            unit_price=Decimal("1000.00"),
            tax_object_code="02",
            discount=Decimal("0.00"),
            item_sku="7501000101010",  # SKU obligatorio
            item_taxes=[
                ItemTax(
                    tax_code="002",
                    tax_type_code="Tasa",
                    tax_rate=Decimal("0.160000"),
                    tax_flag_code="T"
                )
            ]
        )
    ]
)

# Enviar solicitud de timbrado
api_response = client.invoices.create(invoice)

# Procesar respuesta
if api_response.succeeded:
    print("✅ Factura timbrada con éxito!")
    print("UUID:", api_response.data.uuid)

    # Guardar XML timbrado
    with open("factura_timbrada.xml", "w", encoding="utf-8") as file:
        file.write(api_response.data.xml)

    print("📄 Factura guardada en 'factura_timbrada.xml'.")
else:
    print("❌ ERROR en timbrado:", api_response.message)
