-- Populate the user dimension table
INSERT INTO dim_users (user_id, email, name, is_customer)
SELECT id, email, name, is_customer FROM users;

-- Populate the conversation_parts dimension table
INSERT INTO dim_conversation_parts (part_id, conversation_id, part_type, created_at)
SELECT id, conversation_id, part_type, created_at FROM conversation_parts;

-- Populate the consolidated_messages fact table
-- First insert the conversation starts (message_type = 'open')
INSERT INTO consolidated_messages (user_id, email, conversation_id, message, message_type, created_at)
SELECT 
    u.id AS user_id,
    cs.conv_dataset_email AS email,
    cs.id AS conversation_id,
    cs.message AS message,
    'open' AS message_type,
    cs.created_at AS created_at
FROM 
    conversation_start cs
JOIN 
    users u ON cs.conv_dataset_email = u.email
WHERE 
    u.is_customer = 1

UNION ALL

-- Then insert all conversation parts
SELECT 
    u.id AS user_id,
    cp.conv_dataset_email AS email,
    cp.conversation_id AS conversation_id,
    cp.message AS message,
    cp.part_type AS message_type,
    cp.created_at AS created_at
FROM 
    conversation_parts cp
JOIN 
    conversation_start cs ON cp.conversation_id = cs.id
JOIN 
    users u ON cs.conv_dataset_email = u.email
WHERE 
    u.is_customer = 1;

-- Handle cases where conversation starter is not a customer
INSERT INTO consolidated_messages (user_id, email, conversation_id, message, message_type, created_at)
SELECT 
    u.id AS user_id,
    cs.conv_dataset_email AS email,
    cs.id AS conversation_id,
    cs.message AS message,
    'open' AS message_type,
    cs.created_at AS created_at
FROM 
    conversation_start cs
JOIN 
    conversation_parts cp ON cs.id = cp.conversation_id
JOIN 
    users u ON cp.conv_dataset_email = u.email
WHERE 
    u.is_customer = 1
AND 
    cs.id NOT IN (SELECT conversation_id FROM consolidated_messages);

-- Sort the consolidated_messages
CREATE TABLE temp_consolidated_messages AS
SELECT * FROM consolidated_messages
ORDER BY conversation_id, created_at;

DROP TABLE consolidated_messages;
ALTER TABLE temp_consolidated_messages RENAME TO consolidated_messages;

