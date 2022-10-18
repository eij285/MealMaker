-- Meal Maker database schema

DROP TABLE IF EXISTS recipe;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id              SERIAL,
    pronoun         VARCHAR(20),
    given_names     VARCHAR(20),
    last_name       VARCHAR(20),
    display_name    VARCHAR(30) NOT NULL,
    email           VARCHAR(60) NOT NULL UNIQUE,
    password        CHAR(60) NOT NULL,
    password_reset  CHAR(32),
    base64_image    TEXT,
    country         VARCHAR(20),
    about           TEXT,
    visibility      VARCHAR(7) NOT NULL DEFAULT ('private'),
    breakfast       BOOLEAN NOT NULL DEFAULT TRUE,
    lunch           BOOLEAN NOT NULL DEFAULT TRUE,
    dinner          BOOLEAN NOT NULL DEFAULT TRUE,
    snack           BOOLEAN NOT NULL DEFAULT TRUE,
    vegetarian      BOOLEAN NOT NULL DEFAULT FALSE,
    vegan           BOOLEAN NOT NULL DEFAULT FALSE,
    kosher          BOOLEAN NOT NULL DEFAULT FALSE,
    halal           BOOLEAN NOT NULL DEFAULT FALSE,
    dairy_free      BOOLEAN NOT NULL DEFAULT FALSE,
    gluten_free     BOOLEAN NOT NULL DEFAULT FALSE,
    nut_free        BOOLEAN NOT NULL DEFAULT FALSE,
    egg_free        BOOLEAN NOT NULL DEFAULT FALSE,
    shellfish_free  BOOLEAN NOT NULL DEFAULT FALSE,
    soy_free        BOOLEAN NOT NULL DEFAULT FALSE,
    units           VARCHAR(8) NOT NULL DEFAULT ('Metric'),
    efficiency      VARCHAR(12) NOT NULL DEFAULT ('Intermediate'),
    last_request    TIMESTAMP,
    token           TEXT,
    PRIMARY KEY (id),
    CONSTRAINT valid_visibility CHECK (visibility in ('private', 'public')),
    CONSTRAINT valid_units CHECK (units in ('Metric', 'Imperial')),
    CONSTRAINT valid_efficiency CHECK (efficiency in ('Beginner', 'Intermediate', 'Expert'))
);

CREATE TABLE recipes (
    recipe_id       SERIAL,
    owner_id        INTEGER NOT NULL,
    recipe_name     VARCHAR(255) NOT NULL,
    recipe_description TEXT NOT NULL,
    recipe_photo    TEXT,
    recipe_status   VARCHAR(9) NOT NULL DEFAULT ('draft'),
    recipe_method   TEXT,
    created_on      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edited_on       TIMESTAMP,
    preparation_hours INTEGER,
    preparation_minutes INTEGER,
    servings        INTEGER NOT NULL,
    energy          INTEGER,
    protein         INTEGER,
    carbohydrates   INTEGER,
    fats            INTEGER,
    cuisine         VARCHAR(30),
    breakfast       BOOLEAN NOT NULL DEFAULT FALSE,
    lunch           BOOLEAN NOT NULL DEFAULT FALSE,
    dinner          BOOLEAN NOT NULL DEFAULT FALSE,
    snack           BOOLEAN NOT NULL DEFAULT FALSE,
    vegetarian      BOOLEAN NOT NULL DEFAULT FALSE,
    vegan           BOOLEAN NOT NULL DEFAULT FALSE,
    kosher          BOOLEAN NOT NULL DEFAULT FALSE,
    halal           BOOLEAN NOT NULL DEFAULT FALSE,
    dairy_free      BOOLEAN NOT NULL DEFAULT FALSE,
    gluten_free     BOOLEAN NOT NULL DEFAULT FALSE,
    nut_free        BOOLEAN NOT NULL DEFAULT FALSE,
    egg_free        BOOLEAN NOT NULL DEFAULT FALSE,
    shellfish_free  BOOLEAN NOT NULL DEFAULT FALSE,
    soy_free        BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT valid_status CHECK (recipe_status in ('draft', 'published')),
    PRIMARY KEY (recipe_id),
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

INSERT INTO
    users(id, display_name, email, password)
VALUES
    (123, 'PersonA', 'persona@gmail.com', 12345);
