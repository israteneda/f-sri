# ACR-001: Migración de MongoDB a PostgreSQL

## Información General
- **ID del ACR**: ACR-001
- **Título**: Migración de Base de Datos de MongoDB a PostgreSQL
- **Fecha**: 2024-12-27
- **Autor**: Tech Lead
- **Estado**: Propuesto
- **Prioridad**: Alta

## Resumen Ejecutivo
Este documento propone la migración del sistema de facturación electrónica F-SRI de MongoDB (con Mongoose ODM) a PostgreSQL (con Prisma ORM), con el objetivo de mejorar la integridad de datos, performance y mantenibilidad del sistema.

## Contexto y Motivación

### Situación Actual
El sistema F-SRI actualmente utiliza MongoDB como base de datos principal con las siguientes características:
- **ODM**: Mongoose para el mapeo de objetos
- **Esquema**: Dinámico con validaciones básicas
- **Relaciones**: Referencias mediante ObjectId
- **Transacciones**: Limitadas y complejas de implementar

### Problemática Identificada
1. **Integridad de Datos**: MongoDB no garantiza integridad referencial automática
2. **Transacciones Complejas**: Las operaciones ACID son limitadas y complejas
3. **Consultas Relacionales**: Dificultad para realizar consultas complejas entre entidades relacionadas
4. **Escalabilidad**: Limitaciones para reportes y análisis de datos financieros
5. **Cumplimiento**: Los datos financieros requieren mayor rigor en la consistencia

## Análisis de la Solución Propuesta

### ¿Por qué PostgreSQL?
PostgreSQL es la opción ideal para el sistema de facturación electrónica por las siguientes razones:

#### 1. **Integridad de Datos Financieros**
- **Constraints**: Claves foráneas, checks, unique constraints
- **ACID Completo**: Atomicidad, Consistencia, Aislamiento y Durabilidad
- **Validaciones a Nivel de Base**: Garantías de integridad antes de que lleguen a la aplicación

#### 2. **Estructura Relacional Óptima para Facturas**
Los datos de facturación son inherentemente relacionales:
```
Usuario → Empresa Emisora → Facturas → Detalles de Factura ← Productos
                     ↓
                  Clientes ← Tipos de Identificación
```

#### 3. **Performance para Consultas Complejas**
- **Índices Optimizados**: B-tree, GiST, GIN para diferentes tipos de consultas
- **Query Planner**: Optimizador de consultas avanzado
- **Joins Eficientes**: Mejor performance para consultas relacionales

#### 4. **Soporte JSON Híbrido**
- **Campos JSON**: Para datos flexibles como `sri_mensajes`
- **Indexing JSON**: Búsquedas eficientes en campos JSON
- **Lo Mejor de Ambos Mundos**: Estructura relacional + flexibilidad NoSQL

#### 5. **Ecosistema y Herramientas**
- **Prisma ORM**: Type-safe, migrations automáticas, query builder intuitivo
- **Backup/Recovery**: Herramientas robustas para datos críticos
- **Monitoring**: Mejor observabilidad y métricas

## Arquitectura Propuesta

### Stack Tecnológico
- **Base de Datos**: PostgreSQL 15+
- **ORM**: Prisma 5.x
- **Migraciones**: Prisma Migrate
- **Type Safety**: Tipos automáticos generados por Prisma

### Esquema de Base de Datos
```sql
-- Usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tipos de Identificación
CREATE TABLE identification_types (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    descripcion VARCHAR(100) NOT NULL
);

-- Empresas Emisoras
CREATE TABLE issuing_companies (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    ruc VARCHAR(13) UNIQUE NOT NULL,
    razon_social VARCHAR(255) NOT NULL,
    nombre_comercial VARCHAR(255) NOT NULL,
    -- ... otros campos
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Clientes
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    identification_type_id INTEGER REFERENCES identification_types(id),
    identificacion VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(255) NOT NULL,
    -- ... otros campos
);

-- Productos
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    tiene_iva BOOLEAN NOT NULL DEFAULT true
);

-- Facturas
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    issuing_company_id INTEGER REFERENCES issuing_companies(id),
    client_id INTEGER REFERENCES clients(id),
    fecha_emision TIMESTAMP NOT NULL,
    clave_acceso VARCHAR(49) UNIQUE NOT NULL,
    secuencial VARCHAR(9) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    total_sin_impuestos DECIMAL(10,2) NOT NULL,
    total_iva DECIMAL(10,2) NOT NULL,
    total_con_impuestos DECIMAL(10,2) NOT NULL,
    xml TEXT,
    xml_firmado TEXT,
    ride_pdf BYTEA,
    sri_estado VARCHAR(20),
    sri_mensajes JSONB, -- JSON para flexibilidad
    sri_fecha_envio TIMESTAMP,
    sri_fecha_respuesta TIMESTAMP,
    datos_originales JSONB, -- JSON para datos flexibles
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Detalles de Facturas
CREATE TABLE invoice_details (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    cantidad DECIMAL(10,3) NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    valor_iva DECIMAL(10,2) NOT NULL
);
```

## Plan de Migración

### Fase 1: Preparación (1-2 días)
1. **Setup PostgreSQL**: Configurar base de datos local y desarrollo
2. **Instalar Dependencias**: Prisma, PostgreSQL client
3. **Esquema Inicial**: Crear esquema Prisma basado en modelos actuales

### Fase 2: Migración de Modelos (2-3 días)
1. **Crear Schema Prisma**: Definir todas las entidades y relaciones
2. **Generar Migraciones**: Crear scripts de migración automáticos
3. **Actualizar Interfaces**: Adaptar interfaces TypeScript

### Fase 3: Migración de Servicios (3-4 días)
1. **Actualizar Servicios**: Reemplazar queries Mongoose por Prisma
2. **Mantener API**: Asegurar que las APIs externas no cambien
3. **Testing**: Pruebas unitarias e integración

### Fase 4: Migración de Datos (1 día)
1. **Script de Migración**: Herramienta para migrar datos existentes
2. **Validación**: Verificar integridad de datos migrados
3. **Rollback Plan**: Plan de contingencia

### Fase 5: Deployment (1 día)
1. **Configuración Producción**: Variables de entorno PostgreSQL
2. **Monitoreo**: Métricas y alertas
3. **Documentación**: Actualizar documentación técnica

## Beneficios Esperados

### Técnicos
- **Integridad de Datos**: 100% de consistencia garantizada por FOREIGN KEY constraints
- **Performance**: Mejora del 30-50% en consultas complejas
- **Type Safety**: Eliminación de errores de runtime por tipos incorrectos
- **Facilidad de Mantenimiento**: Migraciones automáticas y rollbacks

### Operacionales
- **Backups Confiables**: pg_dump/pg_restore para backups consistentes
- **Monitoreo Avanzado**: Métricas detalladas de performance
- **Escalabilidad**: Mejor soporte para crecimiento de datos

### Cumplimiento
- **Auditoría**: Mejor trazabilidad de cambios de datos
- **Consistency**: Datos financieros siempre consistentes
- **Recovery**: Mejor recovery point objective (RPO)

## Riesgos y Mitigaciones

### Riesgos Identificados
1. **Tiempo de Migración**: Posible downtime durante migración
   - **Mitigación**: Migración en horarios de menor uso + base de datos de respaldo
2. **Bugs en Queries**: Diferencias entre Mongoose y Prisma
   - **Mitigación**: Testing exhaustivo + rollback automático
3. **Performance Inicial**: Posible degradación temporal
   - **Mitigación**: Optimización de índices + monitoreo continuo

## Conclusión

La migración de MongoDB a PostgreSQL representa una mejora arquitectural significativa para el sistema F-SRI. PostgreSQL ofrece las garantías de integridad, performance y escalabilidad necesarias para un sistema de facturación electrónica robusto y confiable.

**Recomendación**: Proceder con la migración siguiendo el plan propuesto, con especial énfasis en el testing y validación de datos durante cada fase.

---

**Próximos Pasos:**
1. Aprobación del ACR por parte del equipo técnico
2. Configuración del entorno de desarrollo con PostgreSQL
3. Inicio de la Fase 1 del plan de migración

**Revisado por:** Tech Lead  
**Fecha de Revisión:** 2024-12-27