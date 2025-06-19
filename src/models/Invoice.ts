import { Invoice, Prisma } from '@prisma/client';

// Export the Prisma generated types
export type IInvoice = Invoice;
export type CreateInvoiceInput = Prisma.InvoiceCreateInput;
export type UpdateInvoiceInput = Prisma.InvoiceUpdateInput;
export type InvoiceWithRelations = Prisma.InvoiceGetPayload<{
  include: {
    issuingCompany: true;
    client: true;
    details: {
      include: {
        product: true;
      };
    };
    pdfs: true;
  };
}>;

// Export the model types for backwards compatibility
export { Invoice };
export default Invoice;
