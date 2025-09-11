-- Reset and seed database for demo purposes
TRUNCATE TABLE clases_programadas,
               asignaciones_materia,
               disponibilidad_docente,
               docentes,
               materias,
               planes_estudio,
               facultades,
               aulas
RESTART IDENTITY CASCADE;

-- Admins
INSERT INTO admins (username, hashed_password) VALUES
('admin', '$2b$12$EsZwlXKvHEvnxkzuiPKvQ.3uc2h2zcoUq39YDj/86BMhIRQwNHQvm');

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
('Redes', 'NET104', 4, 'Optativa', 1, true),
-- Ingeniería Industrial
('Logística', 'LOG201', 4, 'Obligatoria', 2, false),
('Producción', 'PRO202', 5, 'Obligatoria', 2, false),
('Calidad', 'CAL203', 4, 'Obligatoria', 2, false),
('Automatización', 'AUT204', 4, 'Optativa', 2, true),
-- Psicología
('Psicología General', 'PSI301', 4, 'Obligatoria', 3, false),
('Psicopatología', 'PSI302', 4, 'Obligatoria', 3, false),
('Neuropsicología', 'PSI303', 5, 'Obligatoria', 3, false),
('Psicología Social', 'PSI304', 4, 'Optativa', 3, true),
-- Derecho
('Derecho Penal', 'DER401', 4, 'Obligatoria', 4, false),
('Derecho Civil', 'DER402', 5, 'Obligatoria', 4, false),
('Derecho Constitucional', 'DER403', 5, 'Obligatoria', 4, false),
('Ética Jurídica', 'DER404', 3, 'Optativa', 4, true),
-- Medicina
('Anatomía', 'MED501', 5, 'Obligatoria', 5, false),
('Fisiología', 'MED502', 5, 'Obligatoria', 5, false),
('Farmacología', 'MED503', 4, 'Obligatoria', 5, false),
('Patología', 'MED504', 4, 'Optativa', 5, true),
-- Enfermería
('Fundamentos de Enfermería', 'ENF601', 5, 'Obligatoria', 6, false),
('Enfermería Geriátrica', 'ENF602', 4, 'Obligatoria', 6, false),
('Nutrición Clínica', 'ENF603', 4, 'Optativa', 6, false),
('Cuidados Críticos', 'ENF604', 4, 'Optativa', 6, true);

-- Docentes
INSERT INTO docentes (nombre, correo, numero_empleado, facultad_id) VALUES
('Juan Pérez', 'juan@example.com', 'EMP001', 1),
('Ana Gómez', 'ana@example.com', 'EMP002', 1),
('Luis Morales', 'luis@example.com', 'EMP003', 2),
('Carmen Díaz', 'carmen@example.com', 'EMP004', 3),
('Carlos Ruiz', 'carlos@example.com', 'EMP005', 2),
('Marta López', 'marta@example.com', 'EMP006', 3),
('Pedro Sánchez', 'pedro@example.com', 'EMP007', 1),
('Lucía Ortiz', 'lucia@example.com', 'EMP008', 2),
('Jorge Herrera', 'jorge@example.com', 'EMP009', 3),
('Elena Torres', 'elena@example.com', 'EMP010', 1);

-- Aulas
INSERT INTO aulas (nombre, capacidad) VALUES
('Aula 101', 30),
('Aula 102', 40),
('Laboratorio 1', 20),
('Laboratorio 2', 25),
('Aula Magna', 100),
('Sala de Conferencias', 50);

-- Asignaciones docente ↔ materia
INSERT INTO asignaciones_materia (docente_id, materia_id) VALUES
(1, 1),
(2, 5),
(3, 10),
(4, 15),
(5, 20),
(1, 23),
(6, 2),
(7, 6),
(8, 11),
(9, 16),
(10, 21);

-- Disponibilidad de docentes
INSERT INTO disponibilidad_docente (docente_id, dia, hora_inicio, hora_fin) VALUES
(1, 'lunes', '08:00', '10:00'),
(1, 'miercoles', '10:00', '12:00'),
(2, 'martes', '09:00', '11:00'),
(3, 'jueves', '08:00', '10:00'),
(4, 'viernes', '11:00', '13:00'),
(5, 'lunes', '14:00', '16:00'),
(6, 'martes', '10:00', '12:00'),
(7, 'miercoles', '09:00', '11:00'),
(8, 'jueves', '13:00', '15:00'),
(9, 'viernes', '08:00', '10:00'),
(10, 'lunes', '10:00', '12:00');

-- Clases programadas
INSERT INTO clases_programadas (docente_id, materia_id, aula_id, dia, hora_inicio, hora_fin) VALUES
(1, 1, 1, 'lunes', '08:00', '10:00'),
(2, 5, 2, 'martes', '09:00', '11:00'),
(3, 10, 3, 'miercoles', '08:00', '10:00'),
(4, 15, 4, 'jueves', '10:00', '12:00'),
(5, 20, 5, 'viernes', '11:00', '13:00'),
(6, 2, 1, 'lunes', '10:00', '12:00'),
(7, 6, 2, 'martes', '11:00', '13:00'),
(8, 11, 3, 'miercoles', '12:00', '14:00'),
(9, 16, 4, 'jueves', '08:00', '10:00'),
(10, 21, 5, 'viernes', '09:00', '11:00');

