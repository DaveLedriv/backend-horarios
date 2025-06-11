-- Facultades
INSERT INTO facultades (nombre) VALUES
('Facultad de Ingeniería'),
('Facultad de Ciencias Sociales'),
('Facultad de Medicina');

-- Planes de estudio (2 por facultad)
INSERT INTO planes_estudio (nombre, facultad_id) VALUES
('Ingeniería en Sistemas', 1),
('Ingeniería Industrial', 1),
('Psicología', 2),
('Derecho', 2),
('Medicina General', 3),
('Enfermería', 3);

-- Materias (4 por plan)
INSERT INTO materias (nombre, codigo, creditos, tipo, plan_estudio_id, permite_superposicion) VALUES
-- Ingeniería en Sistemas
('Programación I', 'PRG101', 5, 'Obligatoria', 1, false),
('Algoritmos', 'ALG102', 5, 'Obligatoria', 1, false),
('Sistemas Operativos', 'SO103', 4, 'Obligatoria', 1, false),
('Redes', 'NET104', 4, 'Optativa', 1, false),
-- Ingeniería Industrial
('Logística', 'LOG201', 4, 'Obligatoria', 2, false),
('Producción', 'PRO202', 5, 'Obligatoria', 2, false),
('Calidad', 'CAL203', 4, 'Obligatoria', 2, false),
('Automatización', 'AUT204', 4, 'Optativa', 2, false),
-- Psicología
('Psicología General', 'PSI301', 4, 'Obligatoria', 3, false),
('Psicopatología', 'PSI302', 4, 'Obligatoria', 3, false),
('Neuropsicología', 'PSI303', 5, 'Obligatoria', 3, false),
('Psicología Social', 'PSI304', 4, 'Optativa', 3, false),
-- Derecho
('Derecho Penal', 'DER401', 4, 'Obligatoria', 4, false),
('Derecho Civil', 'DER402', 5, 'Obligatoria', 4, false),
('Derecho Constitucional', 'DER403', 5, 'Obligatoria', 4, false),
('Ética Jurídica', 'DER404', 3, 'Optativa', 4, false),
-- Medicina
('Anatomía', 'MED501', 5, 'Obligatoria', 5, false),
('Fisiología', 'MED502', 5, 'Obligatoria', 5, false),
('Farmacología', 'MED503', 4, 'Obligatoria', 5, false),
('Patología', 'MED504', 4, 'Optativa', 5, false),
-- Enfermería
('Fundamentos de Enfermería', 'ENF601', 5, 'Obligatoria', 6, false),
('Enfermería Geriátrica', 'ENF602', 4, 'Obligatoria', 6, false),
('Nutrición Clínica', 'ENF603', 4, 'Optativa', 6, false),
('Cuidados Críticos', 'ENF604', 4, 'Optativa', 6, false);

-- Docentes (total: 5)
INSERT INTO docentes (nombre, correo, numero_empleado, facultad_id) VALUES
('Juan Pérez', 'juan@example.com', 'EMP001', 1),
('Ana Gómez', 'ana@example.com', 'EMP002', 1),
('Luis Morales', 'luis@example.com', 'EMP003', 2),
('Carmen Díaz', 'carmen@example.com', 'EMP004', 3),
('Carlos Ruiz', 'carlos@example.com', 'EMP005', 2);

-- Asignaciones aleatorias docente ↔ materia
INSERT INTO asignaciones_materia (docente_id, materia_id) VALUES
(1, 1),
(2, 5),
(3, 10),
(4, 15),
(5, 20),
(1, 23);
