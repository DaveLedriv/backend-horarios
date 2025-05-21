--
-- PostgreSQL database dump
--

-- Dumped from database version 15.12 (Debian 15.12-1.pgdg120+1)
-- Dumped by pg_dump version 15.12 (Debian 15.12-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS '';


--
-- Name: diasemanaenum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.diasemanaenum AS ENUM (
    'lunes',
    'martes',
    'miercoles',
    'jueves',
    'viernes',
    'sabado',
    'domingo'
);


ALTER TYPE public.diasemanaenum OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admins (
    id integer NOT NULL,
    username character varying NOT NULL,
    hashed_password character varying NOT NULL
);


ALTER TABLE public.admins OWNER TO postgres;

--
-- Name: admins_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.admins_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.admins_id_seq OWNER TO postgres;

--
-- Name: admins_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.admins_id_seq OWNED BY public.admins.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: asignaciones_materia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.asignaciones_materia (
    id integer NOT NULL,
    docente_id integer NOT NULL,
    materia_id integer NOT NULL
);


ALTER TABLE public.asignaciones_materia OWNER TO postgres;

--
-- Name: asignaciones_materia_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.asignaciones_materia_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.asignaciones_materia_id_seq OWNER TO postgres;

--
-- Name: asignaciones_materia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.asignaciones_materia_id_seq OWNED BY public.asignaciones_materia.id;


--
-- Name: clases_programadas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clases_programadas (
    id integer NOT NULL,
    docente_id integer,
    materia_id integer,
    aula character varying NOT NULL,
    dia public.diasemanaenum NOT NULL,
    hora_inicio time without time zone NOT NULL,
    hora_fin time without time zone NOT NULL
);


ALTER TABLE public.clases_programadas OWNER TO postgres;

--
-- Name: clases_programadas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clases_programadas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.clases_programadas_id_seq OWNER TO postgres;

--
-- Name: clases_programadas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clases_programadas_id_seq OWNED BY public.clases_programadas.id;


--
-- Name: docentes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.docentes (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    correo character varying(100) NOT NULL,
    numero_empleado character varying(20) NOT NULL,
    facultad_id integer NOT NULL
);


ALTER TABLE public.docentes OWNER TO postgres;

--
-- Name: docentes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.docentes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.docentes_id_seq OWNER TO postgres;

--
-- Name: docentes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.docentes_id_seq OWNED BY public.docentes.id;


--
-- Name: facultades; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.facultades (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL
);


ALTER TABLE public.facultades OWNER TO postgres;

--
-- Name: facultades_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.facultades_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.facultades_id_seq OWNER TO postgres;

--
-- Name: facultades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.facultades_id_seq OWNED BY public.facultades.id;


--
-- Name: materias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.materias (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    codigo character varying(20) NOT NULL,
    creditos integer NOT NULL,
    tipo character varying(50),
    plan_estudio_id integer NOT NULL,
    permite_superposicion boolean
);


ALTER TABLE public.materias OWNER TO postgres;

--
-- Name: materias_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.materias_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.materias_id_seq OWNER TO postgres;

--
-- Name: materias_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.materias_id_seq OWNED BY public.materias.id;


--
-- Name: planes_estudio; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.planes_estudio (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    facultad_id integer NOT NULL
);


ALTER TABLE public.planes_estudio OWNER TO postgres;

--
-- Name: planes_estudio_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.planes_estudio_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.planes_estudio_id_seq OWNER TO postgres;

--
-- Name: planes_estudio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.planes_estudio_id_seq OWNED BY public.planes_estudio.id;


--
-- Name: admins id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins ALTER COLUMN id SET DEFAULT nextval('public.admins_id_seq'::regclass);


--
-- Name: asignaciones_materia id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignaciones_materia ALTER COLUMN id SET DEFAULT nextval('public.asignaciones_materia_id_seq'::regclass);


--
-- Name: clases_programadas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clases_programadas ALTER COLUMN id SET DEFAULT nextval('public.clases_programadas_id_seq'::regclass);


--
-- Name: docentes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.docentes ALTER COLUMN id SET DEFAULT nextval('public.docentes_id_seq'::regclass);


--
-- Name: facultades id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facultades ALTER COLUMN id SET DEFAULT nextval('public.facultades_id_seq'::regclass);


--
-- Name: materias id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materias ALTER COLUMN id SET DEFAULT nextval('public.materias_id_seq'::regclass);


--
-- Name: planes_estudio id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planes_estudio ALTER COLUMN id SET DEFAULT nextval('public.planes_estudio_id_seq'::regclass);


--
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admins (id, username, hashed_password) FROM stdin;
1	admin	$2b$12$SDMmJT13Tr2sFpOkXN8HBuY06nQ.mOxszy6cNNnYi2JWClBJSV9P2
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
fdd019a23ed8
\.


--
-- Data for Name: asignaciones_materia; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.asignaciones_materia (id, docente_id, materia_id) FROM stdin;
\.


--
-- Data for Name: clases_programadas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clases_programadas (id, docente_id, materia_id, aula, dia, hora_inicio, hora_fin) FROM stdin;
1	1	1	Aula 101	lunes	08:00:00	09:30:00
2	1	2	Aula 102	martes	10:00:00	11:30:00
\.


--
-- Data for Name: docentes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.docentes (id, nombre, correo, numero_empleado, facultad_id) FROM stdin;
1	Juan Pérez	juan@example.com	EMP001	1
2	Ana Gómez	ana@example.com	EMP002	1
\.


--
-- Data for Name: facultades; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.facultades (id, nombre) FROM stdin;
1	Facultad de Ingeniería
\.


--
-- Data for Name: materias; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.materias (id, nombre, codigo, creditos, tipo, plan_estudio_id, permite_superposicion) FROM stdin;
1	Programación I	PRG101	5	Obligatoria	1	f
2	Base de Datos	BD202	4	Obligatoria	1	f
\.


--
-- Data for Name: planes_estudio; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.planes_estudio (id, nombre, facultad_id) FROM stdin;
1	Ingeniería en Sistemas	1
\.


--
-- Name: admins_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.admins_id_seq', 1, true);


--
-- Name: asignaciones_materia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.asignaciones_materia_id_seq', 1, false);


--
-- Name: clases_programadas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clases_programadas_id_seq', 1, false);


--
-- Name: docentes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.docentes_id_seq', 1, false);


--
-- Name: facultades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.facultades_id_seq', 1, false);


--
-- Name: materias_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.materias_id_seq', 1, false);


--
-- Name: planes_estudio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.planes_estudio_id_seq', 1, false);


--
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: asignaciones_materia asignaciones_materia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignaciones_materia
    ADD CONSTRAINT asignaciones_materia_pkey PRIMARY KEY (id);


--
-- Name: clases_programadas clases_programadas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clases_programadas
    ADD CONSTRAINT clases_programadas_pkey PRIMARY KEY (id);


--
-- Name: docentes docentes_correo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.docentes
    ADD CONSTRAINT docentes_correo_key UNIQUE (correo);


--
-- Name: docentes docentes_numero_empleado_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.docentes
    ADD CONSTRAINT docentes_numero_empleado_key UNIQUE (numero_empleado);


--
-- Name: docentes docentes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.docentes
    ADD CONSTRAINT docentes_pkey PRIMARY KEY (id);


--
-- Name: facultades facultades_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facultades
    ADD CONSTRAINT facultades_nombre_key UNIQUE (nombre);


--
-- Name: facultades facultades_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facultades
    ADD CONSTRAINT facultades_pkey PRIMARY KEY (id);


--
-- Name: materias materias_codigo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materias
    ADD CONSTRAINT materias_codigo_key UNIQUE (codigo);


--
-- Name: materias materias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materias
    ADD CONSTRAINT materias_pkey PRIMARY KEY (id);


--
-- Name: planes_estudio planes_estudio_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planes_estudio
    ADD CONSTRAINT planes_estudio_pkey PRIMARY KEY (id);


--
-- Name: asignaciones_materia uix_docente_materia; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignaciones_materia
    ADD CONSTRAINT uix_docente_materia UNIQUE (docente_id, materia_id);


--
-- Name: ix_admins_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_admins_id ON public.admins USING btree (id);


--
-- Name: ix_admins_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_admins_username ON public.admins USING btree (username);


--
-- Name: ix_asignaciones_materia_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_asignaciones_materia_id ON public.asignaciones_materia USING btree (id);


--
-- Name: ix_clases_programadas_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_clases_programadas_id ON public.clases_programadas USING btree (id);


--
-- Name: ix_docentes_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_docentes_id ON public.docentes USING btree (id);


--
-- Name: ix_facultades_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_facultades_id ON public.facultades USING btree (id);


--
-- Name: ix_materias_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_materias_id ON public.materias USING btree (id);


--
-- Name: ix_planes_estudio_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_planes_estudio_id ON public.planes_estudio USING btree (id);


--
-- Name: asignaciones_materia asignaciones_materia_docente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignaciones_materia
    ADD CONSTRAINT asignaciones_materia_docente_id_fkey FOREIGN KEY (docente_id) REFERENCES public.docentes(id);


--
-- Name: asignaciones_materia asignaciones_materia_materia_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.asignaciones_materia
    ADD CONSTRAINT asignaciones_materia_materia_id_fkey FOREIGN KEY (materia_id) REFERENCES public.materias(id);


--
-- Name: clases_programadas clases_programadas_docente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clases_programadas
    ADD CONSTRAINT clases_programadas_docente_id_fkey FOREIGN KEY (docente_id) REFERENCES public.docentes(id);


--
-- Name: clases_programadas clases_programadas_materia_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clases_programadas
    ADD CONSTRAINT clases_programadas_materia_id_fkey FOREIGN KEY (materia_id) REFERENCES public.materias(id);


--
-- Name: docentes docentes_facultad_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.docentes
    ADD CONSTRAINT docentes_facultad_id_fkey FOREIGN KEY (facultad_id) REFERENCES public.facultades(id);


--
-- Name: materias materias_plan_estudio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materias
    ADD CONSTRAINT materias_plan_estudio_id_fkey FOREIGN KEY (plan_estudio_id) REFERENCES public.planes_estudio(id);


--
-- Name: planes_estudio planes_estudio_facultad_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planes_estudio
    ADD CONSTRAINT planes_estudio_facultad_id_fkey FOREIGN KEY (facultad_id) REFERENCES public.facultades(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;


--
-- PostgreSQL database dump complete
--

