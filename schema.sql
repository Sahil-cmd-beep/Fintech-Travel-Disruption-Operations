-- schema.sql
-- Relational database layout mapping Fintech users to Travel Operations logs

CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    subscription_tier VARCHAR(20) CHECK (subscription_tier IN ('Standard', 'Plus', 'Premium', 'Metal', 'Ultra')),
    country VARCHAR(50),
    preferred_currency VARCHAR(3)
);

CREATE TABLE transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    amount DECIMAL(18, 2),
    currency VARCHAR(3),
    status VARCHAR(20) CHECK (status IN ('completed', 'failed', 'refunded', 'pending')),
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE flight_bookings (
    booking_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    pnr VARCHAR(6) UNIQUE,
    airline VARCHAR(50),
    base_currency VARCHAR(3),
    ticket_cost DECIMAL(18, 2),
    flight_status VARCHAR(20) CHECK (flight_status IN ('ontime', 'delayed', 'cancelled')),
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE support_tickets (
    ticket_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    channel VARCHAR(20),
    initial_tag VARCHAR(50),
    handle_time_minutes INT,
    status VARCHAR(20) CHECK (status IN ('open', 'resolved', 'escalated')),
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
