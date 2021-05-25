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
        console.log('Connected to database');
      });
}


app.get('/', (req, res) =>{

    let dest_url = `http://localhost:${port}/api/logs`;

    fetch(dest_url).then(res => {
        return res.json();
    })
    .then(json => {
        res.render('foundlog', {
            messages: json
        })
    })
    .catch(err => {
        res.render('nolog', {
            error: true,
            err: err
        });
    })
});

app.get('/api/logs', (req, res) =>{
    const db = open_db();

    const author = req.query.author;
    const authorid = req.query.authorid;
    const useid = (req.query.useid === "true")

    const since = Date.parse(req.query.since);
    const before = Date.parse(req.query.before);

    const contains = req.query.contains;

    db.all("SELECT * FROM messages", [], (err, rows) => {
        if(err) throw err;

        if((useid != null && authorid != null) || author != null){
            console.log("Author passed");
            if(useid)
                rows = rows.filter(row => row.AuthorID === authorid);
            else
                rows = rows.filter(row => row.Author.slice(0, -5) === author);
        }
        if((since != null && !isNaN(since) && (before == null || isNaN(before)))){
            console.log("Since passed")
            rows = rows.filter(row => new Date(row.DateOfMessage) > since);
        } else if((since == null || isNaN(since) && (before != null && !isNaN(before)))){
            console.log("Before passed")
            rows = rows.filter(row => new Date(row.DateOfMessage) < before);
        }else if((since != null && !isNaN(since) && (before != null && !isNaN(before)))){
            console.log("Between passed")
            rows = rows.filter(row =>(
                new Date(row.DateOfMessage) > since
                &&
                new Date(row.DateOfMessage) < before)
                );
        }
        if(contains != null)
            rows = rows.filter(row => row.Content.includes(contains));

        if(rows.length != 0){
            res.json(rows);
        }
        else{
            res.status(404).send("Error 404");
        }
    });

    db.close();
});

app.listen(port, () =>{
    console.log(`Listening on port ${port}...`);
});