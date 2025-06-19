import { Client, Prisma } from '@prisma/client';

// Export the Prisma generated types
export type IClient = Client;
export type CreateClientInput = Prisma.ClientCreateInput;
export type UpdateClientInput = Prisma.ClientUpdateInput;
export type ClientWithRelations = Prisma.ClientGetPayload<{
  include: {
    identificationType: true;
    invoices: true;
  };
}>;

// Export the model types for backwards compatibility
export { Client };
export default Client;
