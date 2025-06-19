# Migration Guide: MongoDB to PostgreSQL

This guide provides step-by-step instructions for migrating the F-SRI system from MongoDB to PostgreSQL.

## 🚀 Quick Start

1. **Install PostgreSQL** (if not already installed)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   
   # macOS
   brew install postgresql
   
   # Windows: Download from postgresql.org
   ```

2. **Create database**
   ```bash
   sudo -u postgres createdb f_sri_dev
   ```

3. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your PostgreSQL connection details
   ```

4. **Run migration setup**
   ```bash
   npm run setup:postgresql
   ```

5. **Start the server**
   ```bash
   npm run dev
   ```

## 📋 Detailed Migration Steps

### Phase 1: Environment Setup

1. **Update environment variables**
   ```env
   DATABASE_URL="postgresql://username:password@localhost:5432/f_sri_dev"
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Generate Prisma client**
   ```bash
   npm run db:generate
   ```

### Phase 2: Database Migration

1. **Run database migrations**
   ```bash
   npm run db:migrate
   ```

2. **Seed initial data**
   ```bash
   npm run db:seed
   ```

3. **Verify database structure**
   ```bash
   npm run db:studio
   ```

### Phase 3: Data Migration (if needed)

If you have existing MongoDB data that needs to be migrated:

1. **Export MongoDB data**
   ```bash
   # Create export script for your existing data
   mongoexport --db f-sri --collection invoices --out invoices.json
   ```

2. **Create migration script**
   ```typescript
   // Create a custom migration script in scripts/migrate-data.ts
   // to transform and import your existing data
   ```

## 🔄 Key Changes

### Database Models

| MongoDB Model | PostgreSQL Table | Key Changes |
|---------------|------------------|-------------|
| `Invoice` | `invoices` | `_id` → `id`, ObjectId refs → integer FKs |
| `Client` | `clients` | Snake_case field mapping |
| `IssuingCompany` | `issuing_companies` | Added `user_id` FK, timestamps |
| `Product` | `products` | Decimal types for prices |
| `InvoiceDetail` | `invoice_details` | Proper FK relationships |

### Field Mappings

```typescript
// MongoDB → PostgreSQL
empresa_emisora_id → issuingCompanyId
cliente_id → clientId
fecha_emision → fechaEmision
total_sin_impuestos → totalSinImpuestos
sri_estado → sriEstado
sri_mensajes → sriMensajes (JSON)
```

### Query Changes

```typescript
// Before (Mongoose)
const invoice = await Invoice.findOne({ clave_acceso: key });

// After (Prisma)
const invoice = await prisma.invoice.findUnique({
  where: { claveAcceso: key }
});
```

## 🛡️ Rollback Plan

If you need to rollback to MongoDB:

1. **Keep MongoDB connection**
   ```bash
   # Don't remove MONGO_URI from .env until migration is confirmed
   ```

2. **Switch back to old models**
   ```bash
   git checkout HEAD~1 -- src/models/
   ```

3. **Restore index.ts**
   ```bash
   git checkout HEAD~1 -- src/index.ts
   ```

## ✅ Verification Checklist

- [ ] PostgreSQL server is running
- [ ] Database connection is successful
- [ ] All tables are created with correct schema
- [ ] Initial data is seeded (identification types)
- [ ] Health check endpoint returns database: 'connected'
- [ ] Basic CRUD operations work for all entities
- [ ] Invoice creation flow works end-to-end
- [ ] PDF generation still functions
- [ ] SRI integration remains functional

## 🐛 Troubleshooting

### Common Issues

1. **Connection refused**
   ```bash
   # Check if PostgreSQL is running
   sudo systemctl status postgresql
   
   # Start if needed
   sudo systemctl start postgresql
   ```

2. **Authentication failed**
   ```bash
   # Reset PostgreSQL password
   sudo -u postgres psql
   \password postgres
   ```

3. **Migration fails**
   ```bash
   # Reset database
   npm run db:reset
   
   # Then run setup again
   npm run setup:postgresql
   ```

4. **TypeScript errors**
   ```bash
   # Regenerate Prisma client
   npm run db:generate
   
   # Restart TypeScript server in your IDE
   ```

## 📊 Performance Benefits

After migration, you should see:

- **30-50% faster** complex queries with joins
- **100% data consistency** with foreign key constraints
- **Better concurrent performance** for high-load scenarios
- **Improved backup/restore** reliability
- **Enhanced monitoring** capabilities

## 🔗 Useful Commands

```bash
# Database operations
npm run db:studio          # Open Prisma Studio
npm run db:migrate         # Run migrations
npm run db:reset           # Reset database
npm run db:seed            # Seed initial data

# Development
npm run dev                # Start development server
npm run typecheck          # Check TypeScript
npm run test               # Run tests

# Production
npm run build              # Build for production
npm run db:migrate:prod    # Run production migrations
```

## 📚 Additional Resources

- [Prisma Documentation](https://www.prisma.io/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [ACR Document](./ACR-001-Migracion-MongoDB-PostgreSQL.md)
- [Migration Script](./scripts/setup-postgresql.sh)

---

**Need help?** Check the ACR document for architectural details or create an issue if you encounter problems during migration.