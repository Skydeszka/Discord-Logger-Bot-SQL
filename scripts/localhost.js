// Module import
const bodyParser = require("body-parser");
const express = require("express");
const path = require("path")
const db = require("./database");
const helper = require("./helper");

// Setting up
const app = express();
app.set('view engine', 'pug');
const stat_path = path.join(__dirname + "../..//public");
app.use(express.static(stat_path));
app.use(bodyParser.json());


const port = process.env.PORT || 3000;


app.get('/', (req, res) =>{
    const fullUrl = req.protocol + "://" + req.get('host');

    res.render('main', {
        url: fullUrl
    });
});


app.get('/logs', (req, res) =>{
    const author = req.query.author;
    const useID = helper.ParseBool(req.query.useid);
    const since = req.query.since;
    const before = req.query.before;
    const contains = req.query.contains;
    let page = 1;

    if(!isNaN(parseInt(req.query.page)))
        page = req.query.page;
        

    const fullUrl = req.protocol + "://" + req.get('host');

    db.GetMessages(author, useID, since, before, contains, page).then(rows => {
        res.render('logpage', {
            url: fullUrl,
            author: author,
            useID: useID,
            since: since,
            before: before,
            contains: contains,
            messages: rows
        });
    });
});


app.get('/edits', (req, res) => {
    const author = req.query.author;
    const useID = helper.ParseBool(req.query.useid);
    const originsince = req.query.originsince;
    const originbefore = req.query.originbefore;
    const origincontains = req.query.origincontains;
    const editsince = req.query.editsince;
    const editbefore = req.query.editbefore;
    const editcontains = req.query.editcontains;

    const fullUrl = req.protocol + "://" + req.get('host');

    db.GetEdits(author, useID, originsince, originbefore, editsince, editbefore, origincontains, editcontains).then(rows => {
        res.render('editpage', {
            url: fullUrl,
            author: author,
            useID: useID,
            originsince: originsince,
            originbefore: originbefore,
            origincontains: origincontains,
            editsince: editsince,
            editbefore: editbefore,
            editcontains: editcontains,
            edits: rows
        });
    });
});

app.use((req, res) =>{
    res.render('error404');
});

app.listen(port, () =>{
    console.log(`Listening on port ${port}...`);
});