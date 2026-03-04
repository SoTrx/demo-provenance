from os import getenv
from typing import List

import litellm
import urllib3
from litellm import Message, completion
from requests import post

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
litellm.ssl_verify = False

API_BASE = getenv("SCAYLE_API_BASE", "https://172.16.59.5:32443")
API_USER = getenv("SCAYLE_API_USER", "admin")
API_PASSWORD = getenv("SCAYLE_API_PASSWORD", "password")


class ScayleClient:
    def __init__(self, api_base: str, user: str, password: str):
        self.api_base = api_base
        self.api_key = self._fetch_token(api_base, user, password)

    def _fetch_token(self, auth_base_url: str, user: str, password: str) -> str:
        """Retrieve an API token via LDAP authentication."""
        url = f"{auth_base_url}/api/v1/auths/ldap"
        response = post(
            url,
            json={"user": user, "password": password},
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            verify=False,
        )
        response.raise_for_status()
        return response.json()["token"]

    def completion(self, model: str, messages: List[Message]) -> str:
        response = completion(
            api_base=f"{self.api_base}/api",
            api_key=self.api_key,
            model=model,
            messages=messages
        )
        return response.choices[0].message.content

    def explain(self, model: str, query: str, provenance: str) -> str:
        messages = [
            Message(role="system", content=EXPLANATION_PROMPT),
            Message(role="user",
                    content=f"Query: {query}\nProvenance: {provenance}")
        ]
        return self.completion(model, messages)

    def explain_stream(self, model: str, query: str, provenance: str):
        """Yield text chunks from the LLM as they arrive."""
        messages = [
            Message(role="system", content=EXPLANATION_PROMPT),
            Message(role="user",
                    content=f"Query: {query}\nProvenance: {provenance}")
        ]
        response = completion(
            api_base=f"{self.api_base}/api",
            api_key=self.api_key,
            model=model,
            messages=messages,
            stream=True,
        )
        for chunk in response:
            token = chunk.choices[0].delta.content
            if token:
                yield token


client = ScayleClient(API_BASE, API_USER, API_PASSWORD)

MATHE_SCHEMA = """
--
-- PostgreSQL database dump
--

-- Dumped from database version 14.18 (Homebrew)
-- Dumped by pg_dump version 14.18 (Homebrew)

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
-- Name: mathe; Type: SCHEMA; Schema: -; Owner: provdemo
--

CREATE SCHEMA mathe;


ALTER SCHEMA mathe OWNER TO provdemo;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: assessment; Type: TABLE; Schema: mathe; Owner: provdemo
--

CREATE TABLE mathe.assessment (
    id bigint NOT NULL,
    student_id bigint NOT NULL,
    question_id bigint NOT NULL,
    topic bigint NOT NULL,
    subtopic bigint,
    question_level bigint NOT NULL,
    answer bigint NOT NULL,
    date timestamp with time zone NOT NULL,
    duration bigint,
    option_selected bigint
);


ALTER TABLE mathe.assessment OWNER TO provdemo;

--
-- Name: assessment_id_seq; Type: SEQUENCE; Schema: mathe; Owner: provdemo
--

CREATE SEQUENCE mathe.assessment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mathe.assessment_id_seq OWNER TO provdemo;

--
-- Name: assessment_id_seq; Type: SEQUENCE OWNED BY; Schema: mathe; Owner: provdemo
--

ALTER SEQUENCE mathe.assessment_id_seq OWNED BY mathe.assessment.id;


--
-- Name: last_assessment_levels; Type: TABLE; Schema: mathe; Owner: provdemo
--

CREATE TABLE mathe.last_assessment_levels (
    student_id bigint NOT NULL,
    topic bigint NOT NULL,
    subtopic bigint,
    last_level bigint NOT NULL,
    last_date timestamp with time zone NOT NULL
);


ALTER TABLE mathe.last_assessment_levels OWNER TO provdemo;

--
-- Name: material_top_sub; Type: TABLE; Schema: mathe; Owner: provdemo
--

CREATE TABLE mathe.material_top_sub (
    id bigint NOT NULL,
    platformmaterialid bigint NOT NULL,
    platformtopicid bigint NOT NULL,
    platformsubtopicid bigint
);


ALTER TABLE mathe.material_top_sub OWNER TO provdemo;

--
-- Name: material_top_sub_id_seq; Type: SEQUENCE; Schema: mathe; Owner: provdemo
--

CREATE SEQUENCE mathe.material_top_sub_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mathe.material_top_sub_id_seq OWNER TO provdemo;

--
-- Name: material_top_sub_id_seq; Type: SEQUENCE OWNED BY; Schema: mathe; Owner: provdemo
--

ALTER SEQUENCE mathe.material_top_sub_id_seq OWNED BY mathe.material_top_sub.id;


--
-- Name: material_type; Type: TABLE; Schema: mathe; Owner: provdemo
--

CREATE TABLE mathe.material_type (
    id bigint NOT NULL,
    description character varying(25) NOT NULL
);


ALTER TABLE mathe.material_type OWNER TO provdemo;

--
-- Name: material_type_id_seq; Type: SEQUENCE; Schema: mathe; Owner: provdemo
--

CREATE SEQUENCE mathe.material_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mathe.material_type_id_seq OWNER TO provdemo;

--
-- Name: material_type_id_seq; Type: SEQUENCE OWNED BY; Schema: mathe; Owner: provdemo
--

ALTER SEQUENCE mathe.material_type_id_seq OWNED BY mathe.material_type.id;


--
-- Name: platform__keywords; Type: TABLE; Schema: mathe; Owner: provdemo
--

CREATE TABLE mathe.platform__keywords (
    id bigint NOT NULL,
    id_top bigint DEFAULT '0'::bigint NOT NULL,
    id_sub bigint,
    name character varying(255) NOT NULL,
    hidden integer DEFAULT 0 NOT NULL
);


ALTER TABLE mathe.platform__keywords OWNER TO provdemo;

--
-- Name: platform__keywords_id_seq; Type: SEQUENCE; Schema: mathe; Owner: provdemo
--

CREATE SEQUENCE mathe.platform__keywords_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mathe.platform__keywords_id_seq OWNER TO provdemo;

--
-- Name: platform__keywords_id_seq; Type: SEQUENCE OWNED BY; Schema: mathe; Owner: provdemo
--

ALTER SEQUENCE mathe.platform__keywords_id_seq OWNED BY mathe.platform__keywords.id;


--
-- Name: platform__sna__questions; Type: TABLE; Schema: mathe; Owner: provdemo
--

CREATE TABLE mathe.platform__sna__questions (
    id bigint NOT NULL,
    id_lect bigint NOT NULL,
    description text,
    topic integer NOT NULL,
    subtopic integer,
    question text,
    level character varying(50) NOT NULL,
    answer1 text,
    answer2 text,
    answer3 text,
    answer4 text,
    file_name character varying(250) DEFAULT NULL::character varying,
    file_ext character varying(5) DEFAULT NULL::character varying,
    date timestamp with time zone,
    validate integer NOT NULL,
    validate_date timestamp with time zone,
    validate_by bigint,
    newlevel bigint,
    algorithmlevel bigint,
    checked bigint
);


ALTER TABLE mathe.platform__sna__questions OWNER TO provdemo;

--
-- Name: platform__sna__questions_id_seq; Type: SEQUENCE; Schema: mathe; Owner: provdemo
--

CREATE SEQUENCE mathe.platform__sna__questions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mathe.platform__sna__questions_id_seq OWNER TO provdemo;

--
-- Name: platform__sna__questions_id_seq; Type: SEQUENCE OWNED BY; Schema: mathe; Owner: provdemo
--

ALTER SEQUENCE mathe.platform__sna__questions_id_seq OWNED BY mathe.platform__sna__questions.id;


--
-- Name: platform__subtopic; Type: TABLE; Schema: mathe; Owner: provdemo
--

CREATE TABLE mathe.platform__subtopic (
    id bigint NOT NULL,
    id_top bigint NOT NULL,
    name character varying(250) NOT NULL,
    hidden integer NOT NULL
);


ALTER TABLE mathe.platform__subtopic OWNER TO provdemo;

--
-- Name: platform__subtopic_id_seq; Type: SEQUENCE; Schema: mathe; Owner: provdemo
--

CREATE SEQUENCE mathe.platform__subtopic_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mathe.platform__subtopic_id_seq OWNER TO provdemo;

--
-- Name: platform__subtopic_id_seq; Type: SEQUENCE OWNED BY; Schema: mathe; Owner: provdemo
--

ALTER SEQUENCE mathe.platform__subtopic_id_seq OWNED BY mathe.platform__subtopic.id;


--
-- Name: platform__topic; Type: TABLE; Schema: mathe; Owner: provdemo
--

CREATE TABLE mathe.platform__topic (
    id bigint NOT NULL,
    name character varying(250) NOT NULL,
    hidden integer NOT NULL
);


ALTER TABLE mathe.platform__topic OWNER TO provdemo;

--
-- Name: platform__topic_id_seq; Type: SEQUENCE; Schema: mathe; Owner: provdemo
--

CREATE SEQUENCE mathe.platform__topic_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mathe.platform__topic_id_seq OWNER TO provdemo;

--
-- Name: platform__topic_id_seq; Type: SEQUENCE OWNED BY; Schema: mathe; Owner: provdemo
--

ALTER SEQUENCE mathe.platform__topic_id_seq OWNED BY mathe.platform__topic.id;


--
-- Name: platform_keyword_snaquestion; Type: TABLE; Schema: mathe; Owner: provdemo
--

CREATE TABLE mathe.platform_keyword_snaquestion (
    platformkeywordid bigint NOT NULL,
    platformsnaquestionid bigint NOT NULL
);


ALTER TABLE mathe.platform_keyword_snaquestion OWNER TO provdemo;

--
-- Name: platform_material_keyword; Type: TABLE; Schema: mathe; Owner: provdemo
--

CREATE TABLE mathe.platform_material_keyword (
    platformmaterialid bigint NOT NULL,
    platformkeywordid bigint NOT NULL
);


ALTER TABLE mathe.platform_material_keyword OWNER TO provdemo;

--
-- Name: platform_materials; Type: TABLE; Schema: mathe; Owner: provdemo
--

CREATE TABLE mathe.platform_materials (
    id bigint NOT NULL,
    id_lect bigint NOT NULL,
    title character varying(255) NOT NULL,
    author character varying(255) NOT NULL,
    type bigint NOT NULL,
    description text NOT NULL,
    link character varying(255) NOT NULL,
    languages character varying(255) DEFAULT NULL::character varying,
    file_name character varying(255) DEFAULT NULL::character varying,
    file_ext character varying(5) DEFAULT NULL::character varying,
    date timestamp with time zone,
    validate integer NOT NULL,
    validate_date timestamp with time zone,
    validate_by bigint,
    clicks bigint DEFAULT '0'::bigint NOT NULL
);


ALTER TABLE mathe.platform_materials OWNER TO provdemo;

--
-- Name: platform_materials_id_seq; Type: SEQUENCE; Schema: mathe; Owner: provdemo
--

CREATE SEQUENCE mathe.platform_materials_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mathe.platform_materials_id_seq OWNER TO provdemo;

--
-- Name: platform_materials_id_seq; Type: SEQUENCE OWNED BY; Schema: mathe; Owner: provdemo
--

ALTER SEQUENCE mathe.platform_materials_id_seq OWNED BY mathe.platform_materials.id;


--
-- Name: assessment id; Type: DEFAULT; Schema: mathe; Owner: provdemo
--

ALTER TABLE ONLY mathe.assessment ALTER COLUMN id SET DEFAULT nextval('mathe.assessment_id_seq'::regclass);


--
-- Name: material_top_sub id; Type: DEFAULT; Schema: mathe; Owner: provdemo
--

ALTER TABLE ONLY mathe.material_top_sub ALTER COLUMN id SET DEFAULT nextval('mathe.material_top_sub_id_seq'::regclass);


--
-- Name: material_type id; Type: DEFAULT; Schema: mathe; Owner: provdemo
--

ALTER TABLE ONLY mathe.material_type ALTER COLUMN id SET DEFAULT nextval('mathe.material_type_id_seq'::regclass);


--
-- Name: platform__keywords id; Type: DEFAULT; Schema: mathe; Owner: provdemo
--

ALTER TABLE ONLY mathe.platform__keywords ALTER COLUMN id SET DEFAULT nextval('mathe.platform__keywords_id_seq'::regclass);


--
-- Name: platform__sna__questions id; Type: DEFAULT; Schema: mathe; Owner: provdemo
--

ALTER TABLE ONLY mathe.platform__sna__questions ALTER COLUMN id SET DEFAULT nextval('mathe.platform__sna__questions_id_seq'::regclass);


--
-- Name: platform__subtopic id; Type: DEFAULT; Schema: mathe; Owner: provdemo
--

ALTER TABLE ONLY mathe.platform__subtopic ALTER COLUMN id SET DEFAULT nextval('mathe.platform__subtopic_id_seq'::regclass);


--
-- Name: platform__topic id; Type: DEFAULT; Schema: mathe; Owner: provdemo
--

ALTER TABLE ONLY mathe.platform__topic ALTER COLUMN id SET DEFAULT nextval('mathe.platform__topic_id_seq'::regclass);


--
-- Name: platform_materials id; Type: DEFAULT; Schema: mathe; Owner: provdemo
--

ALTER TABLE ONLY mathe.platform_materials ALTER COLUMN id SET DEFAULT nextval('mathe.platform_materials_id_seq'::regclass);


"""
EXPLANATION_PROMPT = """

# System Prompt

You are an expert in **SQL query interpretation and database provenance**.

Your task is to explain **why a SQL query returned a specific result**, using **provenance information**.

You must generate explanations using **domain-specific language derived from the database schema**.

The explanations must be understandable by someone who understands the **application domain**, even if they do not understand SQL or provenance theory.

---

## Database Schema

The following schema describes the meaning of the database tables and fields.

[SCHEMA]

Use the schema to interpret:

- table names
- column names
- relationships between tables

Always explain results using the **domain meaning of the schema**, not technical SQL terminology.

---

## Provenance Concepts

The provenance formula explains **which tuples contributed to producing the query result**.

Rules:

- Elements like `table@pXrY` refer to **specific tuples from a table**.
- The operator **⊗** indicates that tuples were **combined through joins** in the query.
- A formula represents **one derivation explaining why the result exists**.
- Multiple formulas mean that **multiple independent derivations produced the same result**.

The tuple data associated with each reference describes the **actual database records** involved.

Your task is to translate this provenance information into a **clear explanation using the schema vocabulary**.

---

## Output Structure

Your explanation must follow this structure:

### Query intent

Explain **what the query is trying to find**, using the meaning of the tables and attributes defined in the schema.

Structure:

The query asks for **[natural language explanation of the query using schema terms]**.

---

### Result explanation

Explain what the returned result represents in the domain.

Structure:

The result "`[RESULT]`" means that **[interpret the result using schema concepts]**.

---

### Provenance explanation

Explain **why this result appears**, based on the provenance formula.

Structure:

The provenance tells us that we obtained this result because:

For each derivation:

- Identify the tuples involved
- Explain what each tuple represents in the domain
- Explain how the tuples are connected through the relationships defined in the schema
- Explain how together they justify the result

If multiple derivations exist, explain that **multiple records independently support the same result**.

---

## Important Rules

- Always use **domain language derived from the schema**.
- Do **not repeat raw SQL syntax in the explanation**.
- Focus on **how the records contributed to producing the result**.
- Clearly explain **how the joined tuples lead to the returned value**.
- Prefer **clear natural explanations rather than technical database terminology**.
""".replace("[SCHEMA]", MATHE_SCHEMA)


# st.title(client.explain(
#     model="openai/kimi-k2.5",
#     query="SELECT distinct t.name FROM assessment a JOIN platform__sna__questions q ON(a.question_id=q.id) JOIN platform__topic t ON(t.id=q.topic) WHERE id_lect=78 AND answer=-1 AND question_level=4",
#     provenance="""
# [
#       {
#         "name": "Complex Numbers",
#         "formula": [
#           {
#             "reference": "assessment@p108r52",
#             "data": {
#               "id": 8764,
#               "student_id": 1582,
#               "question_id": 349,
#               "topic": 10,
#               "subtopic": null,
#               "question_level": 4,
#               "answer": -1,
#               "date": "2020-07-06T08:48:49+00:00",
#               "duration": null,
#               "option_selected": null,
#               "provsql": "c05d6084-b184-42ac-acc3-ed7e2de33524"
#             }
#           },
#           {
#             "reference": "platform__sna__questions@p17r7",
#             "data": {
#               "id": 349,
#               "id_lect": 78,
#               "description": "",
#               "topic": 10,
#               "subtopic": null,
#               "question": "The set of points in the complex plane that satisfy the relation $|z+2i|\\leq 1$ is the",
#               "level": "Advanced",
#               "answer1": "disc of radius $1$ and center $-2i$.",
#               "answer2": "disc of radius $1$ and center $2i$.",
#               "answer3": "circle of radius $1$ and center $-2i$.",
#               "answer4": "circle of radius $1$ and center $2i$.",
#               "file_name": null,
#               "file_ext": null,
#               "date": "2019-04-26T13:44:49+00:00",
#               "validate": 1,
#               "validate_date": "2019-04-27T09:43:48+00:00",
#               "validate_by": 37,
#               "newlevel": 5,
#               "algorithmlevel": 6,
#               "checked": 1,
#               "provsql": "501843c3-c42a-4a18-875e-4e40e2b7b65d"
#             }
#           },
#           {
#             "reference": "platform__topic@p0r5",
#             "data": {
#               "id": 10,
#               "name": "Complex Numbers",
#               "hidden": 0,
#               "provsql": "626b5784-7d54-4b4e-bbe9-463d942dae23"
#             }
#           }
#         ],
#         "provsql": "d0163fa6-26c2-507f-8d20-8ef001e2c597"
#       },
#       {
#         "name": "Complex Numbers",
#         "formula": [
#           {
#             "reference": "assessment@p145r39",
#             "data": {
#               "id": 11538,
#               "student_id": 1891,
#               "question_id": 349,
#               "topic": 10,
#               "subtopic": null,
#               "question_level": 4,
#               "answer": -1,
#               "date": "2021-01-18T07:54:28+00:00",
#               "duration": null,
#               "option_selected": null,
#               "provsql": "f4334cc5-dd3f-41f3-bf52-c534bbf8d5e9"
#             }
#           },
#           {
#             "reference": "platform__sna__questions@p17r7",
#             "data": {
#               "id": 349,
#               "id_lect": 78,
#               "description": "",
#               "topic": 10,
#               "subtopic": null,
#               "question": "The set of points in the complex plane that satisfy the relation $|z+2i|\\leq 1$ is the",
#               "level": "Advanced",
#               "answer1": "disc of radius $1$ and center $-2i$.",
#               "answer2": "disc of radius $1$ and center $2i$.",
#               "answer3": "circle of radius $1$ and center $-2i$.",
#               "answer4": "circle of radius $1$ and center $2i$.",
#               "file_name": null,
#               "file_ext": null,
#               "date": "2019-04-26T13:44:49+00:00",
#               "validate": 1,
#               "validate_date": "2019-04-27T09:43:48+00:00",
#               "validate_by": 37,
#               "newlevel": 5,
#               "algorithmlevel": 6,
#               "checked": 1,
#               "provsql": "501843c3-c42a-4a18-875e-4e40e2b7b65d"
#             }
#           },
#           {
#             "reference": "platform__topic@p0r5",
#             "data": {
#               "id": 10,
#               "name": "Complex Numbers",
#               "hidden": 0,
#               "provsql": "626b5784-7d54-4b4e-bbe9-463d942dae23"
#             }
#           }
#         ],
#         "provsql": "57c85dd4-d176-51f4-ae2b-8433afcd312f"
#       },
#       {
#         "name": "Complex Numbers",
#         "formula": [
#           {
#             "reference": "assessment@p5r68",
#             "data": {
#               "id": 785,
#               "student_id": 380,
#               "question_id": 349,
#               "topic": 10,
#               "subtopic": null,
#               "question_level": 4,
#               "answer": -1,
#               "date": "2019-10-09T12:17:19+00:00",
#               "duration": null,
#               "option_selected": null,
#               "provsql": "dd48708d-92a5-4694-aaef-33748fc803ba"
#             }
#           },
#           {
#             "reference": "platform__sna__questions@p17r7",
#             "data": {
#               "id": 349,
#               "id_lect": 78,
#               "description": "",
#               "topic": 10,
#               "subtopic": null,
#               "question": "The set of points in the complex plane that satisfy the relation $|z+2i|\\leq 1$ is the",
#               "level": "Advanced",
#               "answer1": "disc of radius $1$ and center $-2i$.",
#               "answer2": "disc of radius $1$ and center $2i$.",
#               "answer3": "circle of radius $1$ and center $-2i$.",
#               "answer4": "circle of radius $1$ and center $2i$.",
#               "file_name": null,
#               "file_ext": null,
#               "date": "2019-04-26T13:44:49+00:00",
#               "validate": 1,
#               "validate_date": "2019-04-27T09:43:48+00:00",
#               "validate_by": 37,
#               "newlevel": 5,
#               "algorithmlevel": 6,
#               "checked": 1,
#               "provsql": "501843c3-c42a-4a18-875e-4e40e2b7b65d"
#             }
#           },
#           {
#             "reference": "platform__topic@p0r5",
#             "data": {
#               "id": 10,
#               "name": "Complex Numbers",
#               "hidden": 0,
#               "provsql": "626b5784-7d54-4b4e-bbe9-463d942dae23"
#             }
#           }
#         ],
#         "provsql": "6d72a9f1-ce4e-58d3-84e7-de4e887e67f6"
#       }
#     ],
#     [
#       {
#         "name": "Complex Numbers",
#         "whyprov_now": "{\"{assessment@p108r52,platform__sna__questions@p17r7,platform__topic@p0r5}\"}",
#         "provsql": "d0163fa6-26c2-507f-8d20-8ef001e2c597",
#         "why": []
#       },
#       {
#         "name": "Complex Numbers",
#         "whyprov_now": "{\"{assessment@p145r39,platform__sna__questions@p17r7,platform__topic@p0r5}\"}",
#         "provsql": "57c85dd4-d176-51f4-ae2b-8433afcd312f",
#         "why": []
#       },
#       {
#         "name": "Complex Numbers",
#         "whyprov_now": "{\"{assessment@p5r68,platform__sna__questions@p17r7,platform__topic@p0r5}\"}",
#         "provsql": "6d72a9f1-ce4e-58d3-84e7-de4e887e67f6",
#         "why": []
#       }
#     ]
#   ]
#     """
# ))
