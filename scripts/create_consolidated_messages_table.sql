-- Create consolidated_messages fact table
CREATE TABLE IF NOT EXISTS consolidated_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    email TEXT NOT NULL,
    conversation_id INTEGER NOT NULL,
    message TEXT,
    message_type TEXT NOT NULL,
    created_at INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (conversation_id) REFERENCES conversation_start(id)
);

-- Create user dimension table
CREATE TABLE IF NOT EXISTS dim_users (
    user_id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    name TEXT,
    is_customer BOOLEAN NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create conversation_parts dimension table
CREATE TABLE IF NOT EXISTS dim_conversation_parts (
    part_id INTEGER PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    part_type TEXT NOT NULL,
    created_at INTEGER NOT NULL,
    FOREIGN KEY (part_id) REFERENCES conversation_parts(id),
    FOREIGN KEY (conversation_id) REFERENCES conversation_start(id)
);

