CREATE TABLE IF NOT EXISTS Users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(25) UNIQUE,
    photo_path VARCHAR(255),
    background_path VARCHAR(255),
    is_active BOOLEAN,
    is_admin BOOLEAN DEFAULT false NOT NULL,
    steam_id VARCHAR(255) UNIQUE
);

CREATE TYPE friendship_status AS ENUM('Invited','Friends');

CREATE TABLE IF NOT EXISTS Friendships(
    accepter_id BIGINT REFERENCES Users(id) NOT NULL,
    inviter_id BIGINT REFERENCES Users(id) NOT NULL,
    status friendship_status NOT NULL,
    date_created TIMESTAMP NOT NULL,
    CONSTRAINT friendships_pk PRIMARY KEY(accepter_id,inviter_id)
);

CREATE TABLE IF NOT EXISTS user_behaviors(
    id BIGSERIAL PRIMARY KEY,
    decency INTEGER NOT NULL DEFAULT 10000,
    reports_got INTEGER NOT NULL DEFAULT 0,
    reports_owned INTEGER NOT NULL DEFAULT 8,
    user_id BIGINT REFERENCES Users(id) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS user_meta_data(
    id BIGSERIAL PRIMARY KEY,
    ip_adress VARCHAR(40) NOT NULL,
    country VARCHAR(255) NOT NULL,
    user_id BIGINT REFERENCES Users(id) NOT NULL
);

CREATE TYPE check_type AS ENUM('Subscribe','Balance deposit');

CREATE TABLE IF NOT EXISTS checks(
    id BIGSERIAL PRIMARY KEY,
    payment_method VARCHAR(255) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    date_paid TIMESTAMP NOT NULL,
    type check_type NOT NULL
);

CREATE TABLE IF NOT EXISTS user_subscribes(
    id BIGSERIAL PRIMARY KEY,
    date_ends TIMESTAMP NOT NULL,
    user_id BIGINT REFERENCES Users(id) NOT NULL,
    check_id BIGINT REFERENCES checks(id) NOT NULL UNIQUE
);

-- Active: 1701255656119@@127.0.0.1@5432@redglow@public
CREATE TABLE IF NOT EXISTS games(
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    max_players INTEGER NOT NULL,
    min_players INTEGER NOT NULL,
    strict_players BOOLEAN
);

CREATE TABLE IF NOT EXISTS game_entities(
    id BIGSERIAL PRIMARY KEY,
    game_id BIGINT REFERENCES games(id) NOT NULL,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_game_queues(
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) NOT NULL UNIQUE,
    game_id BIGINT REFERENCES games(id) NOT NULL,
    is_active BOOLEAN DEFAULT true NOT NULL,
    match_found BOOLEAN DEFAULT false NOT NULL,
    queued_from TIMESTAMP NOT NULL,
    target_players INTEGER,
    elo_filter BOOLEAN NOT NULL
);

CREATE TYPE ban_type AS ENUM('Sabotaging','Advantage');

CREATE TABLE IF NOT EXISTS user_bans(
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) NOT NULL,
    game_id BIGINT REFERENCES games(id) NOT NULL,
    type ban_type,
    ban_started_since TIMESTAMP NOT NULL,
    ban_ends_at TIMESTAMP NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    streak_ends_at TIMESTAMP NOT NULL
);

CREATE TYPE match_status AS ENUM('Created','Preparing','Picking','Playing','Ended','Canceled');

CREATE TABLE IF NOT EXISTS matches(
    id BIGSERIAL PRIMARY KEY,
    game_id BIGINT REFERENCES games(id) NOT NULL,
    hash VARCHAR(255),
    status match_status,
    date_created TIMESTAMP NOT NULL,
    date_started TIMESTAMP,
    date_ended TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_matches(
    user_id BIGINT REFERENCES users(id) NOT NULL,
    match_id BIGINT REFERENCES matches(id) NOT NULL,
    elo_change INTEGER,
    place INTEGER,
    game_entity_id BIGINT REFERENCES game_entities(id),
    is_accepted BOOLEAN
);