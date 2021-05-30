// Module import
const bodyParser = require("body-parser");
const express = require("express");
const path = require("path")
const db = require("./database");

// Setting up
const app = express();
app.set('view engine', 'pug');
const stat_path = path.join(__dirname + "../../");
app.use(express.static(stat_path));
app.use(bodyParser.json());


const port = process.env.PORT || 3000;


app.get('/logs', (req, res) =>{
    const author = req.query.author;
    const useID = req.query.useid;
    const since = req.query.since;
    const before = req.query.before;
    const contains = req.query.contains;


    db.GetMessages(author, useID, since, before, contains).then(rows => {
        res.render('logpage', {
            author: author,
            useID: useID,
            since: since,
            before: before,
            contains: contains,
            messages: rows
        })
    })
});

app.listen(port, () =>{
    console.log(`Listening on port ${port}...`);
});