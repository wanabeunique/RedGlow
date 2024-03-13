CREATE OR REPLACE FUNCTION create_user_related()
RETURNS TRIGGER AS $$
DECLARE
    row record;
BEGIN
    INSERT INTO user_behaviors(user_id) VALUES (NEW.id);
    FOR row IN SELECT * FROM games LOOP
        INSERT INTO user_elo(user_id,game_id) VALUES (NEW.id, row.id);
    END LOOP;
END;
$$ LANGUAGE PLPGSQL;

CREATE TRIGGER create_user_related_trigger
AFTER INSERT
ON users
FOR EACH ROW
EXECUTE FUNCTION create_user_related();