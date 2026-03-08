-- HexaDynamics WordPress Database Initialization
-- This file runs at MySQL container startup.

-- Grant full privileges to wp_user on the wordpress database
GRANT ALL PRIVILEGES ON wordpress.* TO 'wp_user'@'%';
FLUSH PRIVILEGES;

-- Create a hidden table with a flag (discoverable via DB enumeration)
CREATE TABLE IF NOT EXISTS hexa_internal_notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    note_title VARCHAR(255) NOT NULL,
    note_content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO hexa_internal_notes (note_title, note_content) VALUES
('Migration Status', 'WordPress migration from on-prem to Docker completed. Old admin creds rotated.'),
('DB Flag', 'FLAG{DATABASE_DIRECT_ACCESS_hexa_internal}'),
('Backup Schedule', 'Daily backups at 02:00 UTC to /backups/ directory. Encryption pending.');
