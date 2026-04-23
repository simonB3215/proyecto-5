-- Ejecuta esto en el SQL Editor de Supabase

-- Crear tabla de usuarios (Opcional, podrías usar auth.users de Supabase)
CREATE TABLE public.usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Crear tabla de productos
CREATE TABLE public.productos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID REFERENCES public.usuarios(id) ON DELETE CASCADE,
    nombre_comercial TEXT NOT NULL,
    fecha_compra DATE NOT NULL,
    meses_garantia INTEGER NOT NULL,
    link_manual_pdf TEXT,
    fecha_vencimiento DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Crear tabla de documentos
CREATE TABLE public.documentos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    producto_id UUID REFERENCES public.productos(id) ON DELETE CASCADE,
    ruta_archivo TEXT NOT NULL,
    tipo_mime TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Habilitar RLS (opcional para el MVP, pero recomendado)
ALTER TABLE public.usuarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.productos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.documentos ENABLE ROW LEVEL SECURITY;

-- Crear políticas básicas para permitir todo el acceso (MVP Local)
CREATE POLICY "Allow all actions" ON public.usuarios FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all actions" ON public.productos FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all actions" ON public.documentos FOR ALL USING (true) WITH CHECK (true);

-- No olvides ir al Storage y crear un bucket público llamado 'documentos_garantia'
-- y configurarle una política "Allow all actions" temporalmente.
