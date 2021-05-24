// Module import
const express = require("express");
const app = express();

const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./database/logs.db3', sqlite3.OPEN_READONLY, (err) => {
    if (err) {
      console.error(err.message);
    }
    console.log('Connected to database.');
  });


const port = process.env.PORT || 3000;


app.get('/', (req, res) =>{
    res.send("How are you world?");
});

app.get('/api/logs', (req, res) =>{
    const selector = "SELECT * FROM messages";

    db.all(selector, [], (err, rows) =>{
        if(err) throw err;
        res.send(JSON.stringify(rows));
    });
});

app.get('/api/logs/:msgid', (req, res) =>{
    const selector = "SELECT * FROM messages WHERE MessageID = ?";

    db.all(selector, [req.params.msgid], (err, rows) =>{
        if(err) throw err;

        if(rows.length == 0)
            res.status(404).send("No logs were found with this message ID.");
        else
            res.send(JSON.stringify(rows));
    });
});

app.listen(port, () =>{
    console.log(`Listening on port ${port}...`);
});