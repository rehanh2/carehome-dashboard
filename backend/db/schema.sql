DROP TABLE IF EXISTS note_chunks_v2, notes, residents, employees CASCADE;

CREATE TABLE employees (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    role        TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE residents (
    id          SERIAL PRIMARY KEY,
    first_name  TEXT NOT NULL,
    last_name   TEXT NOT NULL,
    room        TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE notes (
    id                SERIAL PRIMARY KEY,
    resident_id       INT NOT NULL REFERENCES residents(id),
    employee_id       INT NOT NULL REFERENCES employees(id),
    category          TEXT NOT NULL CHECK (category IN ('incident','medication','wellbeing','nutrition','general')),
    shift             TEXT NOT NULL CHECK (shift IN ('day','night')),
    content           TEXT NOT NULL,
    source            TEXT NOT NULL DEFAULT 'typed',
    embedding_status  TEXT NOT NULL DEFAULT 'pending' CHECK (embedding_status IN ('pending','done','failed')),
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Synthetic sample data
INSERT INTO employees (name, role) VALUES ('Sarah Jones', 'Senior Carer'), ('Tom Evans', 'Carer');
INSERT INTO residents (first_name, last_name, room) VALUES ('John', 'Smith', '4'), ('Margaret', 'Brown', '7');