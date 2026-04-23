CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    login           VARCHAR(100)    NOT NULL UNIQUE,
    first_name      VARCHAR(100)    NOT NULL,
    last_name       VARCHAR(100)    NOT NULL,
    email           VARCHAR(255)    NOT NULL UNIQUE,
    password_hash   VARCHAR(255)    NOT NULL,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_users_login_not_empty CHECK (length(trim(login)) > 0),
    CONSTRAINT chk_users_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE INDEX idx_users_login ON users (login);
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_first_name_trgm ON users USING gin (first_name gin_trgm_ops);
CREATE INDEX idx_users_last_name_trgm ON users USING gin (last_name gin_trgm_ops);



CREATE TABLE parcels (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_id            UUID            NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tracking_number     VARCHAR(50)     NOT NULL UNIQUE,
    description         TEXT            NOT NULL DEFAULT '',
    weight_kg           NUMERIC(10, 2)  NOT NULL DEFAULT 0.00,
    dimensions          VARCHAR(50)     NOT NULL DEFAULT '',
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_parcels_weight_positive CHECK (weight_kg >= 0),
    CONSTRAINT chk_parcels_tracking_not_empty CHECK (length(trim(tracking_number)) > 0)
);

CREATE INDEX idx_parcels_owner_id ON parcels (owner_id);
CREATE INDEX idx_parcels_tracking_number ON parcels (tracking_number);



CREATE TABLE deliveries (
    id                          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sender_id                   UUID            NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    recipient_id                UUID            NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    parcel_id                   UUID            NOT NULL REFERENCES parcels(id) ON DELETE RESTRICT,
    status                      VARCHAR(20)     NOT NULL DEFAULT 'pending',
    sender_address              TEXT            NOT NULL DEFAULT '',
    recipient_address           TEXT            NOT NULL DEFAULT '',
    estimated_delivery_date     TIMESTAMPTZ,
    actual_delivery_date        TIMESTAMPTZ,
    created_at                  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at                  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_deliveries_status CHECK (
        status IN ('pending', 'in_transit', 'delivered', 'cancelled')
    ),
    CONSTRAINT chk_deliveries_different_users CHECK (sender_id != recipient_id)
);

CREATE INDEX idx_deliveries_sender_id ON deliveries (sender_id);
CREATE INDEX idx_deliveries_recipient_id ON deliveries (recipient_id);
CREATE INDEX idx_deliveries_parcel_id ON deliveries (parcel_id);
CREATE INDEX idx_deliveries_status_created ON deliveries (status, created_at DESC);



CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_parcels_updated_at
    BEFORE UPDATE ON parcels
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_deliveries_updated_at
    BEFORE UPDATE ON deliveries
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
