// Module import
const bodyParser = require("body-parser");
const express = require("express");
const path = require("path")
const fetch = require("node-fetch")

// Setting up
const app = express();
app.set('view engine', 'pug');
const stat_path = path.join(__dirname + "../../");
app.use(express.static(stat_path));
app.use(bodyParser.json());
const sqlite3 = require('sqlite3').verbose();


const port = process.env.PORT || 3000;


function open_db(){
    return new sqlite3.Database('./database/logs.db3', sqlite3.OPEN_READONLY, (err) => {
        if (err) {
          console.error(err.message);
        }
        console.log('Connected to database.');
      });
}


app.get('/', (req, res) =>{

    fetch(`http://localhost:${port}/api/logs`).then(res => {
        return res.json();
    })
    .then(json => {
        console.log(json)
        res.render('index', {
            messages: json
        })
    });
});

app.get('/api/logs', (req, res) =>{
    const db = open_db();

    const orderBy = req.query.orderBy;
    let selectBy = req.query.selectBy;

    db.all("SELECT * FROM messages", [], (err, rows) => {
        if(err) throw err;

        let rawdata = {};

        if(selectBy){
            selectBy = selectBy.split(',');
            if(selectBy[0].toLowerCase() == "name")
                rawdata = rows.filter(x => x.Author.slice(0, -5) === selectBy[1]);
            else if(selectBy[0].toLowerCase() == "id")
                rawdata = rows.filter(x => x.AuthorID === selectBy[1]);
            else if(selectBy[0].toLowerCase() == "since")
                rawdata = rows.filter(x => new Date(x.DateOfMessage) >= new Date(selectBy[1]));
            else if(selectBy[0].toLowerCase() == "between")
                rawdata = rows.filter(x => {return new Date(x.DateOfMessage) >= new Date(selectBy[1]) && new Date(x.DateOfMessage) <= new Date(selectBy[2])});
            else if(selectBy[0].toLowerCase() == "before")
                rawdata = rows.filter(x => new Date(x.DateOfMessage) <= new Date(selectBy[1]));
            else if(selectBy[0].toLowerCase() == "contains")
                rawdata = rows.filter(x => x.Content.includes(selectBy[1]));
        }
        else
            rawdata = rows;


        if(rawdata.length == 0)
            res.status(404).send("No match found");
        else
            res.json(rawdata);
    });

    db.close();
});

app.listen(port, () =>{
    console.log(`Listening on port ${port}...`);
});