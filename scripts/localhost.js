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
    res.render('foundlog', {
        //messages: 
    })
});

app.listen(port, () =>{
    console.log(`Listening on port ${port}...`);
});