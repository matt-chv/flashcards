/* DB schemas v0.2
*/
PRAGMA encoding="UTF-8";
CREATE TABLE IF NOT EXISTS USERS( ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT);
CREATE TABLE IF NOT EXISTS QUESTIONS( ID INTEGER PRIMARY KEY, Q_TEXT TEXT);
CREATE TABLE IF NOT EXISTS HISTORY (
    TIME TIMESTAMP,
    ANSWER TEXT,
    EXPECTED_ANSWER TEXT,
    TIME_TO_ANSWER INTEGER,
    TARGET_TIME_TO_ANSWER INTEGER,
    NUMBER_ATTEMPTS INTEGER,
    Q_ID INTEGER,
    U_ID INTEGER,
    FOREIGN KEY (Q_ID) REFERENCES questions(id),
    FOREIGN KEY (U_ID) REFERENCES users(id)
    );
INSERT INTO users (id, name) VALUES (0, 'Demo');