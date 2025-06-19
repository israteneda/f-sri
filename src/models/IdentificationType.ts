import { IdentificationType, Prisma } from '@prisma/client';

// Export the Prisma generated types
export type IIdentificationType = IdentificationType;
export type CreateIdentificationTypeInput = Prisma.IdentificationTypeCreateInput;
export type UpdateIdentificationTypeInput = Prisma.IdentificationTypeUpdateInput;
export type IdentificationTypeWithRelations = Prisma.IdentificationTypeGetPayload<{
  include: {
    clients: true;
  };
}>;

// Export the model types for backwards compatibility
export { IdentificationType };
export default IdentificationType;
