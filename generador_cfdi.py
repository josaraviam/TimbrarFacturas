from lxml import etree


def generar_xml_cfdi():
    """Genera un archivo XML CFDI 4.0 con datos de emisor, receptor, conceptos e impuestos."""

    # Definir espacio de nombres para el XML
    NSMAP = {
        "cfdi": "http://www.sat.gob.mx/cfd/4",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance"
    }

    # Crear la raíz del XML con los atributos obligatorios
    cfdi = etree.Element("{http://www.sat.gob.mx/cfd/4}Comprobante",
                         Version="4.0",
                         Serie="A",
                         Folio="12345",
                         Fecha="2024-03-09T12:00:00",
                         FormaPago="01",
                         CondicionesDePago="Contado",
                         SubTotal="1000.00",
                         Moneda="MXN",
                         Total="1160.00",
                         TipoDeComprobante="I",
                         MetodoPago="PUE",
                         LugarExpedicion="64000",
                         NoCertificado="30001000000400002434",
                         nsmap=NSMAP
                         )

    # Agregar el nodo Emisor con su información fiscal
    emisor = etree.SubElement(cfdi, "{http://www.sat.gob.mx/cfd/4}Emisor",
                              Rfc="AAA010101AX5",
                              Nombre="EMPRESA EMISORA S.A. DE C.V.",
                              RegimenFiscal="601"
                              )

    # Agregar el nodo Receptor con su información fiscal
    receptor = etree.SubElement(cfdi, "{http://www.sat.gob.mx/cfd/4}Receptor",
                                Rfc="BBB020202BX6",
                                Nombre="CLIENTE EJEMPLO",
                                UsoCFDI="G03",
                                DomicilioFiscalReceptor="64000",
                                RegimenFiscalReceptor="601"
                                )

    # Crear el nodo Conceptos y agregar un concepto de ejemplo
    conceptos = etree.SubElement(cfdi, "{http://www.sat.gob.mx/cfd/4}Conceptos")
    concepto = etree.SubElement(conceptos, "{http://www.sat.gob.mx/cfd/4}Concepto",
                                ClaveProdServ="01010101",
                                Cantidad="1",
                                ClaveUnidad="H87",
                                Descripcion="Producto de prueba",
                                ValorUnitario="1000.00",
                                Importe="1000.00",
                                ObjetoImp="02"
                                )

    # Crear el nodo de Impuestos y agregar impuestos trasladados
    impuestos = etree.SubElement(cfdi, "{http://www.sat.gob.mx/cfd/4}Impuestos", TotalImpuestosTrasladados="160.00")
    traslados = etree.SubElement(impuestos, "{http://www.sat.gob.mx/cfd/4}Traslados")
    traslado = etree.SubElement(traslados, "{http://www.sat.gob.mx/cfd/4}Traslado",
                                Base="1000.00",
                                Impuesto="002",
                                TipoFactor="Tasa",
                                TasaOCuota="0.160000",
                                Importe="160.00"
                                )

    # Convertir el XML en una cadena y guardarlo en un archivo
    xml_string = etree.tostring(cfdi, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    with open("cfdi_generado.xml", "wb") as f:
        f.write(xml_string)

    print("✅ XML CFDI 4.0 generado correctamente: cfdi_generado.xml")


# Ejecutar la función para generar el XML CFDI
generar_xml_cfdi()
