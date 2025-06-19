#!/bin/bash

echo "🚀 Setting up PostgreSQL migration for F-SRI..."

# Install dependencies
echo "📦 Installing new dependencies..."
npm install

# Install Prisma CLI globally if not present
if ! command -v prisma &> /dev/null; then
    echo "🔧 Installing Prisma CLI..."
    npm install -g prisma
fi

# Generate Prisma client
echo "⚙️  Generating Prisma client..."
npx prisma generate

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  DATABASE_URL environment variable is not set!"
    echo "📝 Please set your DATABASE_URL in your .env file:"
    echo "   DATABASE_URL=\"postgresql://username:password@localhost:5432/f-sri\""
    echo ""
    echo "💡 Example for local development:"
    echo "   DATABASE_URL=\"postgresql://postgres:password@localhost:5432/f_sri_dev\""
else
    echo "✅ DATABASE_URL is configured"
    
    # Run migrations
    echo "🗄️  Running database migrations..."
    npx prisma migrate dev --name init
    
    echo "🌱 Seeding database with initial data..."
    npx prisma db seed
fi

echo ""
echo "✅ PostgreSQL setup complete!"
echo "🔧 Next steps:"
echo "   1. Ensure your PostgreSQL server is running"
echo "   2. Update your .env file with the correct DATABASE_URL"
echo "   3. Run 'npm run dev' to start the server"
echo ""
echo "📚 For more information, see the ACR document: ACR-001-Migracion-MongoDB-PostgreSQL.md"