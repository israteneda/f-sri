import { Product, Prisma } from '@prisma/client';

// Export the Prisma generated types
export type IProduct = Product;
export type CreateProductInput = Prisma.ProductCreateInput;
export type UpdateProductInput = Prisma.ProductUpdateInput;
export type ProductWithRelations = Prisma.ProductGetPayload<{
  include: {
    invoiceDetails: true;
  };
}>;

// Export the model types for backwards compatibility
export { Product };
export default Product;
