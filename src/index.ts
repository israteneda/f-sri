import express from 'express';
import dotenv from 'dotenv';
import cors from 'cors';
import { getCorsConfig } from './config/cors.config';
import prisma from './config/database';
import swaggerSpec from './swagger';
import authRoutes from './routes/auth';
import corsTestRoutes from './routes/cors-test';
import identificationTypeRoutes from './routes/identificationType';
import issuingCompanyRoutes from './routes/issuingCompany';
import clientRoutes from './routes/client';
import productRoutes from './routes/product';
import invoiceRoutes from './routes/invoice';
import invoiceDetailRoutes from './routes/invoiceDetail';
import invoicePDFRoutes from './routes/invoicePDF';
import verifyToken from './middleware/verifyToken';
import corsErrorHandler from './middleware/corsErrorHandler';

dotenv.config();

const app = express();

// Configurar CORS
const corsConfig = getCorsConfig();
app.use(cors(corsConfig));

// Middleware adicional para headers de CORS
app.use((req, res, next) => {
  // Logs para debugging
  console.log(`📡 ${req.method} ${req.path} - Origin: ${req.get('Origin') || 'No origin'}`);

  // Headers adicionales de seguridad
  res.header('Access-Control-Allow-Credentials', 'true');

  // Para peticiones OPTIONS (preflight)
  if (req.method === 'OPTIONS') {
    console.log('✅ Preflight request handled');
    res.status(200).end();
    return;
  }

  next();
});

// Middleware para parsear JSON
app.use(express.json());

// Rutas públicas (sin autenticación)
app.use(authRoutes);
app.use(corsTestRoutes);

const swaggerHtml = `<!DOCTYPE html>
<html>
<head>
  <title>API Docs</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@4.18.3/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@4.18.3/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function() {
      SwaggerUIBundle({ url: '/swagger.json', dom_id: '#swagger-ui' });
    };
  </script>
</body>
</html>`;

// Public routes for documentation
app.get('/swagger.json', (_req, res) => {
  res.json(swaggerSpec);
});

app.get('/docs', (_req, res) => {
  res.type('html').send(swaggerHtml);
});

// Health check endpoint
app.get('/health', async (_req, res: express.Response) => {
  try {
    // Test database connection
    await prisma.$queryRaw`SELECT 1`;
    res.json({
      status: 'OK',
      timestamp: new Date().toISOString(),
      cors: 'enabled',
      environment: process.env.NODE_ENV || 'development',
      database: 'connected',
    });
  } catch (error) {
    res.status(503).json({
      status: 'ERROR',
      timestamp: new Date().toISOString(),
      database: 'disconnected',
      error: process.env.NODE_ENV === 'development' ? error : 'Database connection failed',
    });
  }
});

// Authentication middleware for protected routes
app.use(verifyToken);
app.use('/api/v1/identification-type', identificationTypeRoutes);
app.use('/api/v1/issuing-company', issuingCompanyRoutes);
app.use('/api/v1/client', clientRoutes);
app.use('/api/v1/product', productRoutes);
app.use('/api/v1/invoice', invoiceRoutes);
app.use('/api/v1/invoice-detail', invoiceDetailRoutes);
app.use('/api/v1/invoice-pdf', invoicePDFRoutes);

// Error handling middleware (debe ir al final)
app.use(corsErrorHandler);

// Middleware de manejo general de errores
app.use((err: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('❌ Unhandled error:', err);
  res.status(500).json({
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong',
  });
});

const PORT = process.env.PORT || 3000;

// Start server with database connection test
async function startServer() {
  try {
    // Test database connection
    await prisma.$connect();
    console.log('🗄️ Database connected successfully');
    
    app.listen(PORT, () => {
      console.log(`🚀 Server running on port ${PORT}`);
      console.log(`🌐 Environment: ${process.env.NODE_ENV || 'development'}`);
      console.log(`📄 API Docs: http://localhost:${PORT}/docs`);
      console.log('💾 Database: PostgreSQL with Prisma');
    });
  } catch (error) {
    console.error('❌ Database connection error:', error);
    console.error('💡 Make sure PostgreSQL is running and DATABASE_URL is configured');
    process.exit(1);
  }
}

startServer();

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n🛑 Shutting down gracefully...');
  await prisma.$disconnect();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  console.log('\n🛑 Shutting down gracefully...');
  await prisma.$disconnect();
  process.exit(0);
});
