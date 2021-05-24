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
    const sortBy = req.query.sortBy;

    db.all("SELECT * FROM messages", [], (err, rows) => {
        if(err) throw err;

        res.send(JSON.stringify(rows.find()))
    });
});

app.listen(port, () =>{
    console.log(`Listening on port ${port}...`);
});