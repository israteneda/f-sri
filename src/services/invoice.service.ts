import { CreateInvoiceDTO, InvoiceRequest, ProductDetail, AccessKeyDTO } from '../interfaces/invoice.interface';
import { convertirFecha, generarClaveAcceso } from '../utils/invoice.utils';
import { generarXMLFactura } from '../utils/xml.utils';
import { firmarXML } from '../utils/firma.utils';
import { enviarComprobanteSRI, RespuestaSRI } from '../utils/sri.utils';
import { generateInvoicePDF, savePDFToFile } from '../utils/pdf.utils';
import prisma from '../config/database';
import { IIdentificationType } from '../models/IdentificationType';
import { IIssuingCompany } from '../models/IssuingCompany';
import { IClient } from '../models/Client';
import { IProduct } from '../models/Product';
import { IInvoice } from '../models/Invoice';
import { IInvoiceDetail } from '../models/InvoiceDetail';
import fs from 'fs';
import { decrypt } from '../utils/encryption.utils';
import path from 'path';
import os from 'os';
import forge from 'node-forge';
import { exec } from 'child_process';
import { promisify } from 'util';

const execPromise = promisify(exec);

/**
 * Servicio para manejar todas las operaciones relacionadas con facturas
 */
export class InvoiceService {
  /**
   * Valida que los datos básicos de una factura estén presentes
   */
  static validarDatosFactura(invoiceData: InvoiceRequest): boolean {
    return !!(invoiceData.infoTributaria && invoiceData.infoFactura && invoiceData.detalles);
  }

  /**
   * Genera el siguiente secuencial para una empresa
   */
  static async generarSecuencial(rucCompany: string): Promise<string> {
    const empresa = await prisma.issuingCompany.findUnique({
      where: { ruc: rucCompany },
    });
    
    if (!empresa) {
      throw new Error(`Empresa with RUC ${rucCompany} not found`);
    }

    const ultimaFactura = await prisma.invoice.findFirst({
      where: { issuingCompanyId: empresa.id },
      orderBy: { secuencial: 'desc' },
    });

    let secuencial = '000000001';
    if (ultimaFactura) {
      const siguiente = parseInt(ultimaFactura.secuencial) + 1;
      secuencial = siguiente.toString().padStart(9, '0');
    }
    return secuencial;
  }

  /**
   * Busca un tipo de identificación por su código
   */
  static async buscarTipoIdentificacion(codigo: string): Promise<IIdentificationType | null> {
    const tipoIdent = await prisma.identificationType.findUnique({
      where: { codigo },
    });
    return tipoIdent;
  }

  /**
   * Busca una empresa emisora por su RUC
   */
  static async buscarIssuingCompany(
    ruc: string,
  ): Promise<(IIssuingCompany & { certificatePath?: string; certificatePassword?: string }) | null> {
    const empresa = await prisma.issuingCompany.findUnique({
      where: { ruc },
    });
    
    if (!empresa) return null;

    let certificatePath: string | undefined;
    let certificatePassword: string | undefined;

    if (empresa.certificate && empresa.certificatePassword) {
      try {
        if (!empresa.certificate.trim()) {
          throw new Error('El certificado está vacío');
        }

        try {
          const certBuffer = Buffer.from(empresa.certificate, 'base64');
          const tempDir = os.tmpdir();
          const p12Path = path.join(tempDir, `cert-${Date.now()}.p12`);

          if (!fs.existsSync(tempDir)) {
            fs.mkdirSync(tempDir, { recursive: true });
          }

          fs.writeFileSync(p12Path, certBuffer);

          try {
            if (empresa.certificatePassword && empresa.certificatePassword.includes(':')) {
              try {
                certificatePassword = decrypt(empresa.certificatePassword);
              } catch (decryptError: any) {
                certificatePassword = empresa.certificatePassword;
              }
            } else {
              certificatePassword = empresa.certificatePassword;
            }

            if (!certificatePassword || certificatePassword.trim() === '') {
              certificatePassword = '';
            }
          } catch (passError) {
            certificatePassword = empresa.certificatePassword || '';
          }

          certificatePath = p12Path;

          if (!certificatePath || !fs.existsSync(certificatePath) || fs.statSync(certificatePath).size === 0) {
            throw new Error('El archivo del certificado no existe o está vacío');
          }
        } catch (error) {
          throw new Error(
            'Error al procesar el certificado PKCS#12: ' +
              (error instanceof Error ? error.message : 'Error desconocido'),
          );
        }

        if (!certificatePath) {
          throw new Error('No se pudo generar el archivo del certificado');
        }
      } catch (error) {
        throw new Error('Error al procesar el certificado: ' + (error as Error).message);
      }
    }

    return {
      ...empresa,
      certificatePath,
      certificatePassword,
    } as any;
  }

  /**
   * Busca un cliente por su identificación
   */
  static async buscarClient(identificacion: string): Promise<IClient | null> {
    const cliente = await prisma.client.findUnique({
      where: { identificacion },
    });
    return cliente;
  }

  /**
   * Busca un producto por su código
   */
  static async buscarProduct(codigo: string): Promise<IProduct | null> {
    const producto = await prisma.product.findUnique({
      where: { codigo },
    });
    return producto;
  }

  /**
   * Busca todos los productos listados en los detalles de una factura
   */
  static async buscarProducts(detalles: ProductDetail[]): Promise<IProduct[]> {
    const productos = [];
    for (const det of detalles) {
      const codigo = det.detalle?.codigoPrincipal;
      const producto = await this.buscarProduct(codigo);
      if (!producto) {
        throw new Error(`Product not found: ${codigo}`);
      }
      productos.push(producto);
    }
    return productos;
  }

  /**
   * Crea una nueva factura en la base de datos
   */
  static async crearFactura(datos: CreateInvoiceDTO) {
    const factura = await prisma.invoice.create({
      data: {
        issuingCompanyId: datos.empresaId,
        clientId: datos.clienteId,
        fechaEmision: datos.fechaEmision,
        claveAcceso: datos.claveAcceso,
        secuencial: datos.secuencial,
        estado: 'CREADA',
        totalSinImpuestos: datos.totalSinImpuestos,
        totalIva: datos.totalIva,
        totalConImpuestos: datos.totalConImpuestos,
      },
    });

    return factura;
  }

  /**
   * Crea los detalles de una factura en la base de datos
   */
  static async crearDetallesInvoice(facturaId: number, detalles: ProductDetail[], products: IProduct[]) {
    const detallesGuardados = [];

    for (let i = 0; i < detalles.length; i++) {
      const det = detalles[i].detalle;
      const prod = products[i];

      const detDoc = await prisma.invoiceDetail.create({
        data: {
          invoiceId: facturaId,
          productId: prod.id,
          cantidad: parseFloat(det.cantidad),
          precioUnitario: parseFloat(det.precioUnitario),
          subtotal: parseFloat(det.precioTotalSinImpuesto),
          valorIva: parseFloat(det.impuestos[0].impuesto.valor),
        },
      });

      detallesGuardados.push(detDoc);
    }

    return detallesGuardados;
  }

  /**
   * Procesa la creación completa de una factura y sus detalles
   */
  static async procesarFacturaCompleta(datosFactura: InvoiceRequest) {
    if (!this.validarDatosFactura(datosFactura)) {
      throw new Error('Datos de factura inválidos o incompletos');
    }

    const tipoIdent = await this.buscarTipoIdentificacion(datosFactura.infoFactura.tipoIdentificacionComprador);
    if (!tipoIdent) {
      throw new Error('Identification type not found');
    }

    const empresa = await this.buscarIssuingCompany(datosFactura.infoTributaria.ruc);
    if (!empresa) {
      throw new Error('Empresa emisora no encontrada');
    }

    const cliente = await this.buscarClient(datosFactura.infoFactura.identificacionComprador);
    if (!cliente) {
      throw new Error('Client not found');
    }

    const productos = await this.buscarProducts(datosFactura.detalles);
    const secuencial = await this.generarSecuencial(empresa.ruc);
    const fechaEmision = convertirFecha(datosFactura.infoFactura.fechaEmision);

    if (isNaN(fechaEmision.getTime())) {
      throw new Error('Invalid date format');
    }

    return {
      empresa,
      cliente,
      productos,
      secuencial,
      fechaEmision,
    };
  }

  /**
   * Procesa y guarda una factura completa con todos sus detalles
   * @param datosFactura Los datos de la factura recibidos del cliente
   * @returns La factura creada y sus detalles
   */
  static async crearFacturaCompleta(datosFactura: InvoiceRequest) {
    const { empresa, cliente, productos, secuencial, fechaEmision } = await this.procesarFacturaCompleta(datosFactura);

    const serie = `${empresa.codigoEstablecimiento}${empresa.puntoEmision}`;
    const claveAcceso = generarClaveAcceso({
      fecha: fechaEmision,
      tipoComprobante: '01',
      ruc: empresa.ruc,
      ambiente: empresa.tipoAmbiente.toString(),
      serie,
      secuencial,
      codigoNumerico: Math.floor(10000000 + Math.random() * 89999999).toString(),
      tipoEmision: empresa.tipoEmision.toString(),
    });

    const totalSinImpuestos = parseFloat(datosFactura.infoFactura.totalSinImpuestos);
    const totalIva = datosFactura.detalles.reduce(
      (s: number, d: any) => s + parseFloat(d.detalle.impuestos[0].impuesto.valor),
      0,
    );
    const totalConImpuestos = parseFloat(datosFactura.infoFactura.importeTotal);

    const xml = generarXMLFactura(datosFactura, empresa, cliente, productos, claveAcceso, secuencial);

    const facturaCreada = await this.crearFactura({
      empresaId: empresa.id,
      clienteId: cliente.id,
      fechaEmision,
      claveAcceso,
      secuencial,
      totalSinImpuestos,
      totalIva,
      totalConImpuestos,
    });

    // Update with XML and SRI status
    const facturaActualizada = await prisma.invoice.update({
      where: { id: facturaCreada.id },
      data: {
        xml: xml,
        sriEstado: 'PENDIENTE',
        datosOriginales: JSON.stringify(datosFactura),
      },
    });

    // Process SRI sending asynchronously
    this.procesarEnvioSRI(facturaActualizada, empresa, cliente, productos, datosFactura).catch((error) => {
      console.error('Error in asynchronous SRI sending process:', error);
    });

    const detallesGuardados = await this.crearDetallesInvoice(facturaCreada.id, datosFactura.detalles, productos);

    return {
      factura: facturaActualizada,
      detalles: detallesGuardados,
      xml: facturaActualizada.xml,
      xml_firmado: facturaActualizada.xmlFirmado || null,
      respuesta_sri: null,
    };
  }

  /**
   * Procesa el envío asíncrono de la factura al SRI
   * @param factura La factura a enviar
   * @param empresa La empresa emisora
   * @param cliente El cliente
   * @param productos Los productos
   * @param datosFactura Los datos originales de la factura
   */
  static async procesarEnvioSRI(
    factura: IInvoice,
    empresa: any,
    cliente: IClient,
    productos: IProduct[],
    datosFactura: InvoiceRequest,
  ): Promise<void> {
    let respuestaSRI: RespuestaSRI | null = null;

    try {
      const p12Path = empresa.certificatePath;
      const p12Password = empresa.certificatePassword || '';

      if (p12Path && fs.existsSync(p12Path)) {
        try {
          const diagnosis = await InvoiceService.diagnoseP12Certificate(p12Path, p12Password);

          if (!diagnosis.fileExists) {
            throw new Error('El archivo del certificado P12 no existe');
          }

          if (diagnosis.fileSize === 0) {
            throw new Error('El archivo del certificado P12 está vacío');
          }

          if (!diagnosis.isValidP12) {
            throw new Error(`El archivo P12 no es válido: ${diagnosis.error}`);
          }

          const passwordVerification = await InvoiceService.verifyP12Password(p12Path, p12Password);

          let workingPassword = p12Password;

          if (!passwordVerification.valid) {
            const passwordSearch = await InvoiceService.findWorkingP12Password(p12Path, p12Password);

            if (passwordSearch.password !== null) {
              workingPassword = passwordSearch.password;
            } else {
              throw new Error(
                `Error de contraseña del certificado P12: ${passwordVerification.error}. Se probaron múltiples contraseñas sin éxito. Verifique que la contraseña del certificado sea correcta.`,
              );
            }
          }

          const pemPath = await InvoiceService.convertP12ToPem(p12Path, workingPassword);
          const xmlFirmado = await firmarXML(factura.xml!, pemPath, workingPassword);

          // Update with signed XML
          const facturaConFirma = await prisma.invoice.update({
            where: { id: factura.id },
            data: { xmlFirmado: xmlFirmado },
          });

          if (facturaConFirma.xmlFirmado) {
            // Update send date
            await prisma.invoice.update({
              where: { id: factura.id },
              data: { sriFechaEnvio: new Date() },
            });

            respuestaSRI = await enviarComprobanteSRI(facturaConFirma.xmlFirmado);

            // Update with SRI response
            await prisma.invoice.update({
              where: { id: factura.id },
              data: {
                sriFechaRespuesta: new Date(),
                sriEstado: respuestaSRI.estado,
                sriMensajes: respuestaSRI.mensajes || {},
              },
            });

            if (respuestaSRI.estado === 'RECIBIDA') {
              console.log(
                `✅ FACTURA RECIBIDA POR SRI - ID: ${factura.id}, Clave: ${factura.claveAcceso}, Secuencial: ${factura.secuencial}`,
              );
              await this.generarPDFFactura(facturaConFirma, empresa, cliente, productos, datosFactura);
            } else {
              console.log(`⚠️ SRI Estado: ${respuestaSRI.estado} - Factura ID: ${factura.id}`);
            }
          }
        } catch (error: any) {
          console.error('Error during certificate conversion or signing:', error.message);
          await prisma.invoice.update({
            where: { id: factura.id },
            data: {
              sriEstado: 'ERROR_FIRMA',
              sriMensajes: { error: error.message },
            },
          });
        }
      } else {
        await prisma.invoice.update({
          where: { id: factura.id },
          data: {
            sriEstado: 'ERROR_FIRMA',
            sriMensajes: { mensaje: 'Certificate not found for signing' },
          },
        });
      }
    } catch (error: any) {
      console.error('Error during signing or sending to SRI:', error.message);
      await prisma.invoice.update({
        where: { id: factura.id },
        data: {
          sriEstado: 'ERROR_PROCESO',
          sriMensajes: { error: error.message },
        },
      });
    }
  }

  /**
   * Verifica si la contraseña del certificado P12 es correcta
   * @param p12Path Ruta al archivo P12
   * @param password Contraseña a verificar
   * @returns Promise<boolean> true si la contraseña es correcta
   */
  static async verifyP12Password(p12Path: string, password: string): Promise<{ valid: boolean; error?: string }> {
    try {
      const p12Buffer = fs.readFileSync(p12Path);
      const p12Base64 = p12Buffer.toString('base64');
      const p12Der = forge.util.decode64(p12Base64);
      const p12Asn1 = forge.asn1.fromDer(p12Der);

      try {
        const p12 = forge.pkcs12.pkcs12FromAsn1(p12Asn1, false, password);
        return { valid: true };
      } catch (error: any) {
        return { valid: false, error: error.message };
      }
    } catch (error: any) {
      return { valid: false, error: error.message };
    }
  }

  /**
   * Convierte un archivo P12 a formato PEM usando node-forge
   * @param p12Path Ruta al archivo P12
   * @param password Contraseña del certificado
   * @returns Promesa con la ruta al archivo PEM generado
   */
  static async convertP12ToPem(p12Path: string, password: string): Promise<string> {
    try {
      const p12Buffer = fs.readFileSync(p12Path);
      const p12Base64 = p12Buffer.toString('base64');
      const p12Der = forge.util.decode64(p12Base64);
      const p12Asn1 = forge.asn1.fromDer(p12Der);

      let p12;
      try {
        p12 = forge.pkcs12.pkcs12FromAsn1(p12Asn1, false, password);
      } catch (pkcs12Error: any) {
        if (password && password.length > 0) {
          try {
            p12 = forge.pkcs12.pkcs12FromAsn1(p12Asn1, false, '');
          } catch (emptyPassError: any) {
            try {
              p12 = forge.pkcs12.pkcs12FromAsn1(p12Asn1, false, null as any);
            } catch (nullPassError: any) {
              throw new Error(
                `Error de contraseña del certificado P12. Verifique que la contraseña sea correcta. Error original: ${pkcs12Error.message}`,
              );
            }
          }
        } else {
          throw new Error(
            `Error de contraseña del certificado P12. La contraseña proporcionada no es válida. Error: ${pkcs12Error.message}`,
          );
        }
      }

      const bags = p12.getBags({ bagType: forge.pki.oids.certBag });
      const certBags = bags[forge.pki.oids.certBag] || [];

      const keyBags = p12.getBags({ bagType: forge.pki.oids.pkcs8ShroudedKeyBag });
      const keyBag =
        keyBags[forge.pki.oids.pkcs8ShroudedKeyBag]?.[0] ||
        p12.getBags({ bagType: forge.pki.oids.keyBag })[forge.pki.oids.keyBag]?.[0];

      if (!certBags.length || !keyBag) {
        throw new Error(
          'Certificado o clave privada no encontrados en el archivo P12. El archivo puede estar corrupto o tener un formato incorrecto.',
        );
      }

      const certBag = certBags[0];
      const privateKey = keyBag.key;
      const certificate = certBag.cert;

      if (!privateKey || !certificate) {
        throw new Error('No se pudo extraer el certificado o la clave privada del archivo P12');
      }

      const pemCertificate = forge.pki.certificateToPem(certificate);
      const pemPrivateKey = forge.pki.privateKeyToPem(privateKey);

      const pemContent = `${pemPrivateKey}\n${pemCertificate}`;
      const tempDir = os.tmpdir();
      const pemPath = path.join(tempDir, `cert-${Date.now()}.pem`);

      fs.writeFileSync(pemPath, pemContent);
      return pemPath;
    } catch (error: any) {
      throw new Error('Error converting P12 to PEM: ' + error.message);
    }
  }

  /**
   * Genera y guarda el PDF de la factura
   */
  static async generarPDFFactura(
    factura: IInvoice,
    empresa: IIssuingCompany,
    cliente: IClient,
    productos: IProduct[],
    datosFactura: InvoiceRequest,
  ): Promise<void> {
    try {
      console.log(`📄 Generando PDF para factura ${factura.id}...`);

      // Create PDF data structure matching the expected format
      const pdfData = {
        factura: datosFactura,
        empresa,
        cliente,
        productos,
        claveAcceso: factura.claveAcceso,
        secuencial: factura.secuencial,
        fechaEmision: factura.fechaEmision,
        numeroAutorizacion: factura.claveAcceso,
        fechaAutorizacion: factura.sriFechaRespuesta || new Date(),
      };

      const pdfBuffer = await generateInvoicePDF(pdfData);

      if (pdfBuffer && pdfBuffer.length > 0) {
        // Save PDF to database
        await prisma.invoicePDF.create({
          data: {
            invoiceId: factura.id,
            filename: `factura-${factura.claveAcceso}.pdf`,
            pdfData: pdfBuffer,
            contentType: 'application/pdf',
          },
        });

        // Update invoice with PDF buffer
        await prisma.invoice.update({
          where: { id: factura.id },
          data: { ridePdf: pdfBuffer },
        });

        console.log(`✅ PDF generado exitosamente para factura ${factura.id}`);
      } else {
        console.error(`❌ Error: PDF vacío para factura ${factura.id}`);
      }
    } catch (error: any) {
      console.error('Error generating PDF:', error.message);
    }
  }

  /**
   * Busca trabajar con diferentes contraseñas para el certificado P12
   */
  static async findWorkingP12Password(
    p12Path: string,
    originalPassword: string,
  ): Promise<{ password: string | null; error?: string }> {
    const passwordsToTry = [
      originalPassword,
      '',
      'password',
      '123456',
      'changeme',
      originalPassword.toLowerCase(),
      originalPassword.toUpperCase(),
    ];

    for (const testPassword of passwordsToTry) {
      const result = await this.verifyP12Password(p12Path, testPassword);
      if (result.valid) {
        return { password: testPassword };
      }
    }

    return { password: null, error: 'No working password found' };
  }

  /**
   * Diagnostica un certificado P12
   */
  static async diagnoseP12Certificate(
    p12Path: string,
    password: string,
  ): Promise<{
    fileExists: boolean;
    fileSize: number;
    isValidP12: boolean;
    passwordWorks: boolean;
    certificateInfo?: any;
    error?: string;
  }> {
    const result: {
      fileExists: boolean;
      fileSize: number;
      isValidP12: boolean;
      passwordWorks: boolean;
      certificateInfo?: any;
      error?: string;
    } = {
      fileExists: false,
      fileSize: 0,
      isValidP12: false,
      passwordWorks: false,
    };

    try {
      result.fileExists = fs.existsSync(p12Path);
      if (!result.fileExists) {
        return { ...result, error: 'File does not exist' };
      }

      const stats = fs.statSync(p12Path);
      result.fileSize = stats.size;

      if (result.fileSize === 0) {
        return { ...result, error: 'File is empty' };
      }

      const p12Buffer = fs.readFileSync(p12Path);
      const p12Base64 = p12Buffer.toString('base64');
      const p12Der = forge.util.decode64(p12Base64);
      const p12Asn1 = forge.asn1.fromDer(p12Der);

      result.isValidP12 = true;

      const passwordVerification = await this.verifyP12Password(p12Path, password);
      result.passwordWorks = passwordVerification.valid;

      if (result.passwordWorks) {
        const p12 = forge.pkcs12.pkcs12FromAsn1(p12Asn1, false, password);
        const bags = p12.getBags({ bagType: forge.pki.oids.certBag });
        const certBags = bags[forge.pki.oids.certBag] || [];

        if (certBags.length > 0) {
          const cert = certBags[0].cert;
          result.certificateInfo = {
            subject: cert?.subject.attributes.map((attr: any) => `${attr.shortName}=${attr.value}`).join(', '),
            issuer: cert?.issuer.attributes.map((attr: any) => `${attr.shortName}=${attr.value}`).join(', '),
            validFrom: cert?.validity.notBefore,
            validTo: cert?.validity.notAfter,
            serialNumber: cert?.serialNumber,
          };
        }
      }

      return result;
    } catch (error: any) {
      return { ...result, error: error.message };
    }
  }
}
