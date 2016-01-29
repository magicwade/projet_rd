--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE users (
    id integer NOT NULL,
    login text NOT NULL,
    email text NOT NULL,
    password character(150),
    admin boolean DEFAULT false
);


ALTER TABLE users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY users (id, login, email, password, admin) FROM stdin;
20	Luigi	luigi@nintendo.fr	b7476ec230768534194e53c9b70d95af8c6ccb15453fb548ce269b1c75d09eeb2383fb7303cc27a38a93b7437f12f1fb9c53669815bfd2726cf9907ec8c26af1                      	f
21	Waluigi	waluigi@nintendo.fr	818226879e01a3402189d16e1b4010f51895b8677d5fb95d614f5d61cab9a0089eba1b65068d7f356105bafb546b106ca14572fa0b6ae66e08abd91373814688                      	f
22	Wario	wario@nintendo.fr	e179ff2e26c22b2bffe574c854f213167f2e775bee13706062e37e0ed2b1caa5c806c5ca76c7c36d6bb1b662713f51648abe3b157bd1b9767f61e3fe709f5813                      	f
23	Wade	wade@mediawade.com	ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff                      	f
24	Bowser	bowser@nintendo.fr	72d770fadaca115f4f431f95fa809871ac69bca1f9db1d12604b158b142c4c996a41a3b05abddb79490528ea2bfde5a3e9f594f01fdaa096db9f533d997f0c25                      	f
25	admin	admin@mediawade.com	ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff                      	f
17	Link	link@nintendo.fr	ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff                      	f
18	Toad	toad@nintendo.fr	ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff                      	f
26	Master Hand	masterhand@nintendo.fr	ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff                      	t
19	Mario	mario@nintendo.fr	76bb849338db38e0ede3b8ae726373c42992152747c39e484f096b623946c8a265adde3a72c8177a70a8876694b9403f06d44decfcfe44be25f1078be0282239                      	f
27	Roy	roy@nintendo.fr	\N	t
29	Donkey Kong	donkeykong@nintendo.fr	ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff                      	f
28	Kirby	kirby@nintento.fr	c69ce856d9761ca3dc36d7527f723aec721a37965457e4e819a28a194430ea447ab605a060b539264cdca37f74eb3a6ee40fbf8e7694fae297ad646fe517f65b                      	f
30	Samus	samus@nintendo.fr	ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff                      	f
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('users_id_seq', 30, true);


--
-- Name: email_unique; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT email_unique UNIQUE (email);


--
-- Name: login_unique; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT login_unique UNIQUE (login);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

