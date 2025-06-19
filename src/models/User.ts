import { User, Prisma } from '@prisma/client';

// Export the Prisma generated types
export type IUser = User;
export type CreateUserInput = Prisma.UserCreateInput;
export type UpdateUserInput = Prisma.UserUpdateInput;
export type UserWithRelations = Prisma.UserGetPayload<{
  include: {
    issuingCompanies: true;
  };
}>;

// Export the model types for backwards compatibility
export { User };
export default User;
