-- Migration script to add calendar support to cleaning_assignments table
-- This adds support for specific date assignments alongside weekly assignments

-- Add new columns to support calendar-based assignments
ALTER TABLE cleaning_assignments ADD COLUMN fecha_especifica DATE;
ALTER TABLE cleaning_assignments ADD COLUMN tipo_asignacion TEXT DEFAULT 'semanal';
ALTER TABLE cleaning_assignments ADD COLUMN semana_referencia DATE;

-- Update existing records to maintain compatibility
UPDATE cleaning_assignments SET 
    tipo_asignacion = 'semanal',
    semana_referencia = week_start,
    fecha_especifica = NULL
WHERE tipo_asignacion IS NULL;

-- Create index for better performance on calendar queries
CREATE INDEX IF NOT EXISTS idx_cleaning_assignments_fecha ON cleaning_assignments(fecha_especifica);
CREATE INDEX IF NOT EXISTS idx_cleaning_assignments_tipo ON cleaning_assignments(tipo_asignacion);

-- Add constraint to ensure either weekly or calendar assignment
-- Note: This may need to be adjusted based on your database system
-- ALTER TABLE cleaning_assignments ADD CONSTRAINT check_assignment_type 
-- CHECK (
--     (tipo_asignacion = 'semanal' AND dia_semana IS NOT NULL AND week_start IS NOT NULL) OR
--     (tipo_asignacion = 'calendario' AND fecha_especifica IS NOT NULL)
-- );
