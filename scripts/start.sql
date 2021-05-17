CREATE TABLE messages(
    MessageID INTEGER PRIMARY KEY,
    Author TEXT,
    DateOfMessage DATE,
    Content TEXT
);

CREATE TABLE edits(
    MessageID INTEGER PRIMARY KEY,
    Author TEXT,
    DateOfOriginal DATE,
    DateOfEdit DATE,
    OriginalContent TEXT,
    EditedContent TEXT
);

CREATE TABLE logfetches(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    FetchDate DATE,
    Author TEXT,
    FetchType VARCHAR(10)
)