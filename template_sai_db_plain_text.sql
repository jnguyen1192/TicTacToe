--
-- PostgreSQL database dump
--

-- Dumped from database version 11.5 (Debian 11.5-1.pgdg90+1)
-- Dumped by pg_dump version 12.0

-- Started on 2019-10-05 04:10:31

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

SET default_tablespace = '';

--
-- TOC entry 196 (class 1259 OID 16384)
-- Name: Action; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Action" (
    id_action integer NOT NULL,
    name text
);


ALTER TABLE public."Action" OWNER TO postgres;

--
-- TOC entry 197 (class 1259 OID 16390)
-- Name: Action_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Action_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Action_id_seq" OWNER TO postgres;

--
-- TOC entry 2895 (class 0 OID 0)
-- Dependencies: 197
-- Name: Action_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Action_id_seq" OWNED BY public."Action".id_action;


--
-- TOC entry 198 (class 1259 OID 16392)
-- Name: Has_action; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Has_action" (
    id_strategy bigint NOT NULL,
    id_action integer NOT NULL,
    xml text
);


ALTER TABLE public."Has_action" OWNER TO postgres;

--
-- TOC entry 199 (class 1259 OID 16398)
-- Name: Strategie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Strategie" (
    id_strategie bigint NOT NULL,
    id_action integer,
    "order" text
);


ALTER TABLE public."Strategie" OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 16404)
-- Name: Strategie_id_strategie_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Strategie_id_strategie_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Strategie_id_strategie_seq" OWNER TO postgres;

--
-- TOC entry 2896 (class 0 OID 0)
-- Dependencies: 200
-- Name: Strategie_id_strategie_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Strategie_id_strategie_seq" OWNED BY public."Strategie".id_strategie;


--
-- TOC entry 2753 (class 2604 OID 16406)
-- Name: Action id_action; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Action" ALTER COLUMN id_action SET DEFAULT nextval('public."Action_id_seq"'::regclass);


--
-- TOC entry 2754 (class 2604 OID 16407)
-- Name: Strategie id_strategie; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Strategie" ALTER COLUMN id_strategie SET DEFAULT nextval('public."Strategie_id_strategie_seq"'::regclass);


--
-- TOC entry 2885 (class 0 OID 16384)
-- Dependencies: 196
-- Data for Name: Action; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Action" (id_action, name) FROM stdin;
1	m_click
2	m_double_click
3	m_find
4	m_move
\.


--
-- TOC entry 2887 (class 0 OID 16392)
-- Dependencies: 198
-- Data for Name: Has_action; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Has_action" (id_strategy, id_action, xml) FROM stdin;
\.


--
-- TOC entry 2888 (class 0 OID 16398)
-- Dependencies: 199
-- Data for Name: Strategie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Strategie" (id_strategie, id_action, "order") FROM stdin;
\.


--
-- TOC entry 2897 (class 0 OID 0)
-- Dependencies: 197
-- Name: Action_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Action_id_seq"', 4, true);


--
-- TOC entry 2898 (class 0 OID 0)
-- Dependencies: 200
-- Name: Strategie_id_strategie_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Strategie_id_strategie_seq"', 1, false);


--
-- TOC entry 2756 (class 2606 OID 16409)
-- Name: Action Action_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Action"
    ADD CONSTRAINT "Action_pkey" PRIMARY KEY (id_action);


--
-- TOC entry 2758 (class 2606 OID 16411)
-- Name: Has_action Has_action_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Has_action"
    ADD CONSTRAINT "Has_action_pkey" PRIMARY KEY (id_strategy, id_action);


--
-- TOC entry 2760 (class 2606 OID 16413)
-- Name: Strategie Strategie_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Strategie"
    ADD CONSTRAINT "Strategie_pkey" PRIMARY KEY (id_strategie);


--
-- TOC entry 2763 (class 2606 OID 16414)
-- Name: Strategie fk_id_action->action; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Strategie"
    ADD CONSTRAINT "fk_id_action->action" FOREIGN KEY (id_action) REFERENCES public."Action"(id_action);


--
-- TOC entry 2761 (class 2606 OID 16419)
-- Name: Has_action fk_id_action->action; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Has_action"
    ADD CONSTRAINT "fk_id_action->action" FOREIGN KEY (id_action) REFERENCES public."Action"(id_action);


--
-- TOC entry 2762 (class 2606 OID 16424)
-- Name: Has_action fk_id_strategie->strategie; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Has_action"
    ADD CONSTRAINT "fk_id_strategie->strategie" FOREIGN KEY (id_strategy) REFERENCES public."Strategie"(id_strategie);


-- Completed on 2019-10-05 04:10:31

--
-- PostgreSQL database dump complete
--

