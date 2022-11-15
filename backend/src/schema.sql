-- Meal Maker database schema
-- Please make database schema changes directly to this file then run
-- http://localhost:5000/reset

DROP TABLE IF EXISTS cookbook_followers;
DROP TABLE IF EXISTS cookbook_recipes;
DROP TABLE IF EXISTS cookbooks;
DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS recipe_user_likes;
DROP TABLE IF EXISTS recipe_reviews_votes;
DROP TABLE IF EXISTS recipe_reviews;
DROP TABLE IF EXISTS recipe_ingredients;
DROP TABLE IF EXISTS message_room_members;
DROP TABLE IF EXISTS message_room_owners;
DROP TABLE IF EXISTS message_emojis;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS payment_methods;
DROP TABLE IF EXISTS cart_items;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS shopping_carts;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS message_rooms;
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
    PRIMARY KEY (subscription_id),
    FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE shopping_carts (
    cart_id         SERIAL,
    owner_id        INTEGER NOT NULL,
    cart_status     VARCHAR(9) NOT NULL DEFAULT ('active'),
    last_updated    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (cart_id),
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT valid_cart_status CHECK (cart_status in ('saved', 'active'))
    -- Look into enforcing one active cart per owner
    -- CONSTRAINT one_active_cart UNIQUE(owner_id, )
);

CREATE TABLE cart_items (
    item_id         SERIAL,
    ingredient_name VARCHAR(30) NOT NULL,
    ingredient_quantity INTEGER NOT NULL,
    ingredient_cost MONEY NOT NULL,
    cart_id         INTEGER NOT NULL,
    PRIMARY KEY (item_id),
    FOREIGN KEY (cart_id) REFERENCES shopping_carts(cart_id) ON DELETE CASCADE
);

CREATE TABLE order_items (
    item_id         SERIAL,
    ingredient_name VARCHAR(30) NOT NULL,
    ingredient_quantity INTEGER NOT NULL,
    ingredient_cost MONEY NOT NULL,
    order_id        INTEGER NOT NULL,
    PRIMARY KEY (item_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
)

CREATE TABLE payment_methods (
    method_id       SERIAL,
    owner_id        INTEGER NOT NULL,
    cardholder_name VARCHAR(30) NOT NULL,
    card_number     VARCHAR(20) NOT NULL,
    expiration_date DATE NOT NULL,
    cvv             VARCHAR(4) NOT NULL,
    PRIMARY KEY (method_id),
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE orders (
    order_id        SERIAL,
    order_number    CHAR(10) NOT NULL UNIQUE,
    cart_id         INTEGER NOT NULL,
    placed_on       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_on    TIMESTAMP,
    order_status    VARCHAR(10) NOT NULL DEFAULT ('pending'),
    payment_method_id INTEGER NOT NULL,
    delivery_time   TIMESTAMP NOT NULL,
    delivery_address TEXT NOT NULL,
    payment_amount  MONEY NOT NULL,
    PRIMARY KEY (order_id),
    FOREIGN KEY (cart_id) REFERENCES shopping_carts(cart_id) ON DELETE CASCADE,
    FOREIGN KEY (payment_method_id) REFERENCES payment_methods(method_id) ON DELETE CASCADE,
    CONSTRAINT valid_order_status CHECK (order_status in ('pending', 'processing', 'approved', 'completed'))
);


CREATE TABLE message_rooms (
    room_id SERIAL,
    room_name TEXT,
    PRIMARY KEY (room_id)
);

CREATE TABLE message_room_owners (
    message_room_owner_id SERIAL,
    room_id INTEGER NOT NULL,
    owner_id INTEGER NOT NULL,
    FOREIGN KEY (room_id) REFERENCES message_rooms(room_id) ON DELETE CASCADE,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (message_room_owner_id)
);


CREATE TABLE messages (
    message_id SERIAL,
    message_content TEXT, 
    is_edited BOOLEAN DEFAULT FALSE,
    is_deleted BOOLEAN DEFAULT FALSE,
    time_sent TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sender_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES message_rooms(room_id) ON DELETE CASCADE,
    PRIMARY KEY (message_id)
);

CREATE TABLE message_emojis (
    emoji_id SERIAL,
    emoji_utf8 CHAR(9) NOT NULL,
    message_id INTEGER NOT NULL,
    reactor_id INTEGER NOT NULL,
    FOREIGN KEY (message_id) REFERENCES messages(message_id) ON DELETE CASCADE,
    FOREIGN KEY (reactor_id) REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (emoji_id)
);


CREATE TABLE message_room_members (
    message_room_member_id SERIAL,
    room_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    FOREIGN KEY (room_id) REFERENCES message_rooms(room_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (message_room_member_id)
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
