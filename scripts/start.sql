CREATE TABLE messages(
    MessageID INTEGER PRIMARY KEY,
    Author TEXT,
    AuthorID INTEGER,
    DateOfMessage DATE,
    Content TEXT
);

CREATE TABLE edits(
    MessageID INTEGER PRIMARY KEY,
    Author TEXT,
    AuthorID INTEGER,
    DateOfOriginal DATE,
    DateOfEdit DATE,
    OriginalContent TEXT,
    EditedContent TEXT
);