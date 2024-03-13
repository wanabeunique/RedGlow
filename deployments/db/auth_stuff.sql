CREATE OR REPLACE FUNCTION create_user(
    username VARCHAR(255),
    password VARCHAR(255),
    email VARCHAR(255)
) RETURNS BIGINT AS
$$
DECLARE
    inserted_id BIGINT;
BEGIN
    INSERT INTO users("username", "password", "email") VALUES (username,crypt(password, gen_salt('bf')),email) RETURNING id INTO inserted_id;
    
    RETURN inserted_id;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE commit_user(
    user_email VARCHAR(255)
) LANGUAGE plpgsql AS
$$
BEGIN
    UPDATE users SET is_active=true WHERE email=user_email;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Incorrect old password';
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION check_user_by_credits(
    user_email VARCHAR(255),
    user_password VARCHAR(255)
) RETURNS TABLE (
    username VARCHAR(255),
    email VARCHAR(255),
    photo_path VARCHAR(255),
    background_path VARCHAR(255),
    phone_number VARCHAR(255)
) AS
$$
BEGIN
    RETURN QUERY
    SELECT 
        users.username,users.email, users.photo_path,users.background_path,users.phone_number
    FROM users
    WHERE is_active=true AND users.email=user_email AND users.password=crypt(user_password, users.password);
    IF NOT FOUND THEN
        RAISE EXCEPTION 'User not found';
    END IF;
END;
$$
LANGUAGE PLPGSQL;

CREATE OR REPLACE PROCEDURE change_password(
    user_id BIGINT,
    old_password VARCHAR(255),
    new_password VARCHAR(255)
) LANGUAGE PLPGSQL AS
$$
BEGIN
    UPDATE users
    SET password = crypt(new_password, gen_salt('bf'))
    WHERE id = user_id AND password = crypt(old_password, password);

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Incorrect old password';
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE change_forgotten_password(
    user_id BIGINT,
    new_password VARCHAR(255)
) LANGUAGE PLPGSQL AS
$$
BEGIN
    UPDATE users
    SET password = crypt(new_password, gen_salt('bf'))
    WHERE id = user_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Incorrect old password';
    END IF;
END;
$$;