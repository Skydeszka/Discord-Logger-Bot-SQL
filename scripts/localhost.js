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

app.listen(port, () =>{
    console.log(`Listening on port ${port}...`);
});