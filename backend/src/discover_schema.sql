-- Meal Maker database schema

DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS recipe_user_likes;
DROP TABLE IF EXISTS recipe_reviews_votes;
DROP TABLE IF EXISTS recipe_reviews;
DROP TABLE IF EXISTS recipe_ingredients;
DROP TABLE IF EXISTS recipes;
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
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE recipe_ingredients (
    ingredient_id   SERIAL,
    recipe_id       INTEGER NOT NULL,
    ingredient_name VARCHAR(30) NOT NULL,
    quantity        INTEGER NOT NULL,
    unit            VARCHAR(10) NOT NULL,
    PRIMARY KEY (ingredient_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE
);

CREATE TABLE recipe_reviews (
    review_id       SERIAL,
    recipe_id       INTEGER NOT NULL,
    user_id         INTEGER NOT NULL,
    rating          INTEGER NOT NULL,
    comment         TEXT,
    reply           TEXT,
    created_on      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (review_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT one_review_per_recipe UNIQUE(recipe_id, user_id)
);

CREATE TABLE recipe_reviews_votes (
    vote_id         SERIAL,
    review_id       INTEGER NOT NULL,
    user_id         INTEGER NOT NULL,
    is_upvote       BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (vote_id),
    FOREIGN KEY (review_id) REFERENCES recipe_reviews(review_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT one_vote_per_review UNIQUE(review_id, user_id)
);

CREATE TABLE recipe_user_likes (
    like_id         SERIAL,
    user_id         INTEGER NOT NULL,
    recipe_id       INTEGER NOT NULL,
    PRIMARY KEY (like_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    CONSTRAINT one_like_per_recipe UNIQUE(user_id, recipe_id)
);

CREATE TABLE subscriptions (
    subscription_id SERIAL,
    following_id    INTEGER NOT NULL,
    follower_id     INTEGER NOT NULL,
    FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE
);

INSERT INTO
    users(id, display_name, email, password)
VALUES
    (1, 'PersonA', 'persona@gmail.com', 12345),
    (2, 'PersonB', 'personb@gmail.com', 12345),
    (3, 'PersonC', 'personc@gmail.com', 12345),
    (4, 'PersonD', 'persond@gmail.com', 12345),
    (5, 'PersonE', 'persone@gmail.com', 12345),
    (6, 'PersonF', 'personf@gmail.com', 12345),
    (7, 'PersonG', 'persong@gmail.com', 12345),
    (8, 'PersonH', 'personh@gmail.com', 12345),
    (9, 'PersonI', 'personi@gmail.com', 12345),
    (10, 'PersonJ', 'personj@gmail.com', 12345),
    (11, 'PersonK', 'personk@gmail.com', 12345);
    -- (12, 'PersonL', 'personl@gmail.com', 12345);

INSERT INTO
    recipes(recipe_id, recipe_name, recipe_description, owner_id, servings, recipe_status)
VALUES
    (1, 'RecipeA', 'A', 2, 4, 'published'),
    (2, 'RecipeB', 'B', 8, 4, 'published'),
    (3, 'RecipeC', 'C', 3, 4, 'published'),
    (4, 'RecipeD', 'D', 4, 4, 'published'),
    (5, 'RecipeE', 'E', 2, 4, 'published'),
    (6, 'RecipeF', 'F', 2, 4, 'published');

INSERT INTO
    recipe_reviews(review_id, recipe_id, user_id, rating)
VALUES
    (1, 1, 1, 1),
    (2, 1, 3, 3),
    (3, 1, 5, 5),
    (4, 1, 8, 5),
    (5, 1, 10, 4),
    (6, 2, 3, 5),
    (7, 2, 4, 4),
    (8, 2, 6, 4),
    (9, 2, 9, 2),
    (10, 2, 10, 1),
    (11, 2, 11, 3),
    (12, 3, 1, 2),
    (13, 3, 2, 4),
    (14, 3, 4, 1),
    (15, 3, 6, 3),
    (16, 3, 8, 4),
    (17, 3, 9, 3),
    (18, 3, 10, 5),
    (19, 4, 2, 2),
    (20, 4, 3, 4),
    (21, 4, 7, 4),
    (22, 4, 10, 2),
    (23, 5, 3, 4),
    (24, 5, 4, 3),
    (25, 5, 5, 2),
    (26, 5, 10, 2),
    (27, 5, 11, 5),
    (28, 6, 1, 1),
    (29, 6, 3, 3),
    (30, 6, 7, 2),
    (31, 6, 10, 4);
    -- (32, 3, 12, 2)
    -- (33, 4, 12, 5)
    -- (34, 5, 12, 4)
    -- (35, 6, 12, 3)

SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
SELECT setval('recipes_recipe_id_seq', (SELECT MAX(recipe_id) FROM recipes));
SELECT setval('recipe_reviews_review_id_seq', (SELECT MAX(review_id) FROM recipe_reviews));

