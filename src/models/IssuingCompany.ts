import { IssuingCompany, Prisma } from '@prisma/client';

// Export the Prisma generated types
export type IIssuingCompany = IssuingCompany;
export type CreateIssuingCompanyInput = Prisma.IssuingCompanyCreateInput;
export type UpdateIssuingCompanyInput = Prisma.IssuingCompanyUpdateInput;
export type IssuingCompanyWithRelations = Prisma.IssuingCompanyGetPayload<{
  include: {
    user: true;
    invoices: true;
  };
}>;

// Export the model types for backwards compatibility
export { IssuingCompany };
export default IssuingCompany;
