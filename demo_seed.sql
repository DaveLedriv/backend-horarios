-- Reset and seed database for demo purposes
TRUNCATE TABLE clases_programadas RESTART IDENTITY CASCADE;
TRUNCATE TABLE disponibilidad_docente RESTART IDENTITY CASCADE;
TRUNCATE TABLE asignaciones_materia RESTART IDENTITY CASCADE;
TRUNCATE TABLE grupos RESTART IDENTITY CASCADE;
TRUNCATE TABLE docentes RESTART IDENTITY CASCADE;
TRUNCATE TABLE materias RESTART IDENTITY CASCADE;
TRUNCATE TABLE planes_estudio RESTART IDENTITY CASCADE;
TRUNCATE TABLE facultades RESTART IDENTITY CASCADE;
TRUNCATE TABLE aulas RESTART IDENTITY CASCADE;
TRUNCATE TABLE admins RESTART IDENTITY CASCADE;

-- Admins
INSERT INTO admins (username, hashed_password) VALUES
('admin', '$2b$12$EsZwlXKvHEvnxkzuiPKvQ.3uc2h2zcoUq39YDj/86BMhIRQwNHQvm'),
('admin_sis', '$2b$12$EsZwlXKvHEvnxkzuiPKvQ.3uc2h2zcoUq39YDj/86BMhIRQwNHQvm'),
('admin_psico', '$2b$12$EsZwlXKvHEvnxkzuiPKvQ.3uc2h2zcoUq39YDj/86BMhIRQwNHQvm'),
('admin_medicina', '$2b$12$EsZwlXKvHEvnxkzuiPKvQ.3uc2h2zcoUq39YDj/86BMhIRQwNHQvm'),
('admin_fisica', '$2b$12$EsZwlXKvHEvnxkzuiPKvQ.3uc2h2zcoUq39YDj/86BMhIRQwNHQvm'),
('admin_filosofia', '$2b$12$EsZwlXKvHEvnxkzuiPKvQ.3uc2h2zcoUq39YDj/86BMhIRQwNHQvm'),
('admin_economia', '$2b$12$EsZwlXKvHEvnxkzuiPKvQ.3uc2h2zcoUq39YDj/86BMhIRQwNHQvm'),
('admin_arquitectura', '$2b$12$EsZwlXKvHEvnxkzuiPKvQ.3uc2h2zcoUq39YDj/86BMhIRQwNHQvm'),
('admin_educacion', '$2b$12$EsZwlXKvHEvnxkzuiPKvQ.3uc2h2zcoUq39YDj/86BMhIRQwNHQvm'),
('admin_comunicacion', '$2b$12$EsZwlXKvHEvnxkzuiPKvQ.3uc2h2zcoUq39YDj/86BMhIRQwNHQvm');

-- Facultades
INSERT INTO facultades (nombre) VALUES
('Facultad de Ingeniería'),
('Facultad de Ciencias Sociales'),
('Facultad de Medicina'),
('Facultad de Ciencias Exactas'),
('Facultad de Artes y Humanidades'),
('Facultad de Economía'),
('Facultad de Arquitectura'),
('Facultad de Educación'),
('Facultad de Comunicación'),
('Facultad de Ciencias Ambientales');

-- Planes de estudio
INSERT INTO planes_estudio (nombre, facultad_id) VALUES
('Ingeniería en Sistemas', 1),
('Psicología', 2),
('Medicina General', 3),
('Física Aplicada', 4),
('Filosofía', 5),
('Economía Empresarial', 6),
('Arquitectura Sustentable', 7),
('Educación Primaria', 8),
('Comunicación Digital', 9),
('Gestión Ambiental', 10);

-- Materias (4 por plan de estudio)
INSERT INTO materias (nombre, codigo, creditos, tipo, plan_estudio_id, permite_superposicion) VALUES
-- Ingeniería en Sistemas
('Introducción a la Programación', 'SIS101', 5, 'Obligatoria', 1, false),
('Estructuras de Datos', 'SIS102', 5, 'Obligatoria', 1, false),
('Bases de Datos', 'SIS201', 4, 'Obligatoria', 1, false),
('Desarrollo Web', 'SIS202', 4, 'Optativa', 1, true),
-- Psicología
('Psicología General', 'PSI101', 4, 'Obligatoria', 2, false),
('Psicopatología', 'PSI201', 4, 'Obligatoria', 2, false),
('Neurociencias', 'PSI202', 5, 'Obligatoria', 2, false),
('Psicología Social', 'PSI203', 3, 'Optativa', 2, true),
-- Medicina General
('Anatomía Humana', 'MED101', 5, 'Obligatoria', 3, false),
('Fisiología', 'MED102', 5, 'Obligatoria', 3, false),
('Farmacología', 'MED201', 4, 'Obligatoria', 3, false),
('Semiología', 'MED202', 4, 'Optativa', 3, false),
-- Física Aplicada
('Cálculo Vectorial', 'FIS101', 4, 'Obligatoria', 4, false),
('Mecánica Clásica', 'FIS102', 5, 'Obligatoria', 4, false),
('Física Moderna', 'FIS201', 4, 'Obligatoria', 4, false),
('Métodos Numéricos', 'FIS202', 3, 'Optativa', 4, true),
-- Filosofía
('Historia de la Filosofía', 'FIL101', 4, 'Obligatoria', 5, false),
('Ética Contemporánea', 'FIL102', 3, 'Obligatoria', 5, false),
('Lógica', 'FIL201', 4, 'Obligatoria', 5, false),
('Filosofía Política', 'FIL202', 3, 'Optativa', 5, true),
-- Economía Empresarial
('Microeconomía', 'ECO101', 4, 'Obligatoria', 6, false),
('Macroeconomía', 'ECO102', 4, 'Obligatoria', 6, false),
('Econometría', 'ECO201', 5, 'Obligatoria', 6, false),
('Finanzas Públicas', 'ECO202', 3, 'Optativa', 6, true),
-- Arquitectura Sustentable
('Diseño Arquitectónico I', 'ARQ101', 4, 'Obligatoria', 7, false),
('Materiales de Construcción', 'ARQ102', 4, 'Obligatoria', 7, false),
('Urbanismo', 'ARQ201', 4, 'Obligatoria', 7, false),
('Eficiencia Energética', 'ARQ202', 3, 'Optativa', 7, true),
-- Educación Primaria
('Pedagogía General', 'EDU101', 4, 'Obligatoria', 8, false),
('Didáctica de la Matemática', 'EDU102', 4, 'Obligatoria', 8, false),
('Gestión Educativa', 'EDU201', 3, 'Obligatoria', 8, false),
('Evaluación del Aprendizaje', 'EDU202', 3, 'Optativa', 8, true),
-- Comunicación Digital
('Comunicación Corporativa', 'COM101', 4, 'Obligatoria', 9, false),
('Producción Audiovisual', 'COM102', 4, 'Obligatoria', 9, false),
('Periodismo Digital', 'COM201', 3, 'Obligatoria', 9, false),
('Marketing de Contenidos', 'COM202', 3, 'Optativa', 9, true),
-- Gestión Ambiental
('Ecología', 'AMB101', 4, 'Obligatoria', 10, false),
('Gestión de Recursos Naturales', 'AMB102', 4, 'Obligatoria', 10, false),
('Legislación Ambiental', 'AMB201', 3, 'Obligatoria', 10, false),
('Energías Renovables', 'AMB202', 3, 'Optativa', 10, true);

-- Aulas
INSERT INTO aulas (nombre, capacidad) VALUES
('Aula 101', 30),
('Aula 102', 35),
('Aula 201', 40),
('Aula 202', 45),
('Laboratorio Informática', 25),
('Laboratorio Psicología', 20),
('Sala de Simulación', 18),
('Taller de Arquitectura', 30),
('Aula Magna', 120),
('Sala Multimedia', 50);

-- Docentes
INSERT INTO docentes (nombre, correo, numero_empleado, facultad_id) VALUES
('Juan Pérez', 'juan.perez@uni.edu', 'EMP001', 1),
('Ana Gómez', 'ana.gomez@uni.edu', 'EMP002', 1),
('Luis Morales', 'luis.morales@uni.edu', 'EMP003', 2),
('Carmen Díaz', 'carmen.diaz@uni.edu', 'EMP004', 3),
('Carlos Ruiz', 'carlos.ruiz@uni.edu', 'EMP005', 4),
('Marta López', 'marta.lopez@uni.edu', 'EMP006', 5),
('Pedro Sánchez', 'pedro.sanchez@uni.edu', 'EMP007', 6),
('Lucía Ortiz', 'lucia.ortiz@uni.edu', 'EMP008', 7),
('Jorge Herrera', 'jorge.herrera@uni.edu', 'EMP009', 8),
('Elena Torres', 'elena.torres@uni.edu', 'EMP010', 9),
('Diego Navarro', 'diego.navarro@uni.edu', 'EMP011', 10),
('Sofía Ramos', 'sofia.ramos@uni.edu', 'EMP012', 3);

-- Disponibilidad de docentes
INSERT INTO disponibilidad_docente (docente_id, dia, hora_inicio, hora_fin) VALUES
(1, 'lunes', '08:00', '10:00'),
(1, 'miercoles', '10:00', '12:00'),
(2, 'martes', '09:00', '11:00'),
(2, 'jueves', '08:00', '10:00'),
(3, 'viernes', '09:00', '11:00'),
(4, 'lunes', '13:00', '15:00'),
(4, 'sabado', '08:00', '10:00'),
(5, 'jueves', '11:00', '13:00'),
(6, 'miercoles', '08:00', '10:00'),
(7, 'martes', '15:00', '17:00'),
(8, 'viernes', '10:00', '12:00'),
(9, 'sabado', '09:00', '11:00'),
(10, 'domingo', '10:00', '12:00'),
(11, 'domingo', '08:00', '10:00'),
(12, 'lunes', '07:00', '09:00');

-- Asignaciones docente ↔ materia
INSERT INTO asignaciones_materia (docente_id, materia_id) VALUES
(1, 1),
(1, 3),
(2, 2),
(2, 4),
(3, 5),
(3, 6),
(4, 9),
(4, 11),
(5, 13),
(5, 15),
(6, 17),
(6, 19),
(7, 21),
(7, 23),
(8, 25),
(8, 28),
(9, 29),
(9, 31),
(10, 33),
(10, 35),
(11, 37),
(11, 40),
(12, 10),
(12, 12);

-- Grupos
INSERT INTO grupos (nombre, plan_estudio_id, num_estudiantes) VALUES
('SIS-1A', 1, 32),
('SIS-1B', 1, 28),
('PSI-1A', 2, 30),
('MED-1A', 3, 35),
('MED-1B', 3, 33),
('FIS-1A', 4, 26),
('FIL-1A', 5, 22),
('ECO-1A', 6, 40),
('ARQ-1A', 7, 27),
('EDU-1A', 8, 34),
('COM-1A', 9, 31),
('AMB-1A', 10, 29);

-- Clases programadas
INSERT INTO clases_programadas (docente_id, materia_id, aula_id, grupo_id, dia, hora_inicio, hora_fin) VALUES
(1, 1, 1, 1, 'lunes', '08:00', '10:00'),
(2, 2, 2, 2, 'martes', '09:00', '11:00'),
(1, 3, 3, 2, 'miercoles', '10:00', '12:00'),
(5, 13, 4, 6, 'jueves', '11:00', '13:00'),
(3, 5, 6, 3, 'viernes', '09:00', '11:00'),
(4, 11, 7, 4, 'sabado', '08:00', '10:00'),
(10, 33, 10, 11, 'domingo', '10:00', '12:00'),
(4, 9, 9, 5, 'lunes', '13:00', '15:00'),
(6, 17, 5, 7, 'miercoles', '08:00', '10:00'),
(7, 21, 4, 8, 'martes', '15:00', '17:00'),
(8, 25, 8, 9, 'viernes', '10:00', '12:00'),
(9, 29, 2, 10, 'sabado', '09:00', '11:00'),
(11, 37, 6, 12, 'domingo', '08:00', '10:00'),
(12, 10, 5, 4, 'lunes', '07:00', '09:00');
