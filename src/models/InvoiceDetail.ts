import { InvoiceDetail, Prisma } from '@prisma/client';

// Export the Prisma generated types
export type IInvoiceDetail = InvoiceDetail;
export type CreateInvoiceDetailInput = Prisma.InvoiceDetailCreateInput;
export type UpdateInvoiceDetailInput = Prisma.InvoiceDetailUpdateInput;
export type InvoiceDetailWithRelations = Prisma.InvoiceDetailGetPayload<{
  include: {
    invoice: true;
    product: true;
  };
}>;

// Export the model types for backwards compatibility
export { InvoiceDetail };
export default InvoiceDetail;
