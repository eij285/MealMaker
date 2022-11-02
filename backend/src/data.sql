-- Meal Maker database data
-- Please ensure database schema exists before importing the following data
-- Insert any database records you need into this file, then:
-- first run: http://localhost:5000/reset
-- then run: http://localhost:5000/populatedb
--
-- the reason schema insn't created and data inserted as a single action is
-- that you may wish to start with an empty database
--
-- a database dump containing more extensive data including WYSIWYG content
-- and images will be created at a later stage

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
    recipes(recipe_id, recipe_name, recipe_description, owner_id, servings, recipe_status, created_on)
VALUES
    (1, 'RecipeA', 'A', 2, 4, 'published', '2022-10-28 22:13:35.270770'),
    (2, 'RecipeB', 'B', 8, 4, 'published', '2022-10-28 22:54:35.270770'),
    (3, 'RecipeC', 'C', 3, 4, 'published', '2022-11-01 17:15:35.270770'),
    (4, 'RecipeD', 'D', 4, 4, 'published', '2022-11-01 22:23:35.270770'),
    (5, 'RecipeE', 'E', 2, 4, 'published', '2022-11-02 14:34:35.270770'),
    (6, 'RecipeF', 'F', 2, 4, 'published', '2022-11-02 18:46:35.270770');

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

