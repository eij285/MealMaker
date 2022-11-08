-- Meal Maker database schema
-- Please make database schema changes directly to this file then run
-- http://localhost:5000/reset

DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS recipe_user_likes;
DROP TABLE IF EXISTS recipe_reviews_votes;
DROP TABLE IF EXISTS recipe_reviews;
DROP TABLE IF EXISTS recipe_ingredients;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS cookbook_followers;
DROP TABLE IF EXISTS cookbook_recipes;
DROP TABLE IF EXISTS cookbooks;

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
    PRIMARY KEY (subscription_id),
    FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE cookbooks (
    cookbook_id     SERIAL,
    cookbook_name   VARCHAR(255) NOT NULL,
    cookbook_description TEXT,
    owner_id        INTEGER NOT NULL,
    cookbook_photo  TEXT,
    cookbook_status VARCHAR(9) NOT NULL DEFAULT ('draft'),
    PRIMARY KEY (cookbook_id),
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT valid_cookbook_status CHECK (cookbook_status in ('draft', 'published'))
);

CREATE TABLE cookbook_recipes (
    cookbook_recipe_id  SERIAL,
    cookbook_id         INTEGER NOT NULL,
    recipe_id           INTEGER NOT NULL,
    PRIMARY KEY (cookbook_recipe_id),
    FOREIGN KEY (cookbook_id) REFERENCES cookbooks(cookbook_id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    CONSTRAINT unique_cookbook_recipes UNIQUE(cookbook_id, recipe_id)
);

CREATE TABLE cookbook_followers (
    cookbook_follower_id  SERIAL,
    cookbook_id           INTEGER NOT NULL,
    follower_id           INTEGER NOT NULL,
    PRIMARY KEY (cookbook_follower_id),
    FOREIGN KEY (cookbook_id) REFERENCES cookbooks(cookbook_id) ON DELETE CASCADE,
    FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT unique_cookbook_followers UNIQUE(cookbook_id, follower_id)
);
