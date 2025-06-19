import { InvoicePDF, Prisma } from '@prisma/client';

// Export the Prisma generated types
export type IInvoicePDF = InvoicePDF;
export type CreateInvoicePDFInput = Prisma.InvoicePDFCreateInput;
export type UpdateInvoicePDFInput = Prisma.InvoicePDFUpdateInput;
export type InvoicePDFWithRelations = Prisma.InvoicePDFGetPayload<{
  include: {
    invoice: true;
  };
}>;

// Export the model types for backwards compatibility
export { InvoicePDF };
export default InvoicePDF;
