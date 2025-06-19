import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Seeding database...');

  // Seed identification types (common in Ecuador)
  const identificationTypes = [
    { codigo: '04', descripcion: 'RUC' },
    { codigo: '05', descripcion: 'Cédula' },
    { codigo: '06', descripcion: 'Pasaporte' },
    { codigo: '07', descripcion: 'Venta a consumidor final' },
    { codigo: '08', descripcion: 'Identificación del exterior' },
  ];

  for (const idType of identificationTypes) {
    await prisma.identificationType.upsert({
      where: { codigo: idType.codigo },
      update: {},
      create: idType,
    });
  }

  console.log('✅ Identification types seeded');

  // You can add more seed data here as needed
  // Example: Default products, sample companies, etc.

  console.log('🎉 Seeding completed successfully!');
}

main()
  .catch((e) => {
    console.error('❌ Error during seeding:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });