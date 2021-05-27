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


app.get('/', (req, res) =>{
    res.render('foundlog', {
        //messages: 
    })
});

app.listen(port, () =>{
    console.log(`Listening on port ${port}...`);
});