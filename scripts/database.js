const sqlite3 = require('sqlite3');

function _OpenDB(){
    return new sqlite3.Database('./database/logs.db3', sqlite3.OPEN_READONLY, (err) => {
        if (err) {
          console.error(err.message);
        }
        console.log('Connected to database');
      });
};


function _ValidateDate(date){
  let _date = Date.parse(date);

  if(!isNaN(_date)){
    _date = new Date(_date);
    return new Date(_date.getTime() - _date.getTimezoneOffset() * 60000).toISOString().slice(0,19).replace('T', ' ')
  }
  else
    return false;
}


function _HasWHERE(selector){
  return selector.includes(" WHERE ");
}


function _ReadMessages(author, useID, since, before, contains){
    return new Promise((reslove, reject) => {
      const _since = _ValidateDate(since);
      const _before = _ValidateDate(before);

      let selector = "SELECT * FROM messages ";

      if(author != null){
        if(useID == true)
          selector += `WHERE AuthorID = "${author}" `;
        else
        selector += `WHERE Author = "${author}" `;
      }

      if(_since && !_before){
        if(_HasWHERE(selector))
          selector += `AND DateOfMessage > "${_since}" `;
        else
          selector += `WHERE DateOfMessage > "${_since}" `;
      }
      else if(!_since && before){
        if(_HasWHERE(selector))
          selector += `AND DateOfMessage < "${_before}" `;
        else
          selector += `WHERE DateOfMessage < "${_before}" `;
      }
      else if(_since && _before){
        if(_HasWHERE(selector))
          selector += `AND DateOfMessage BETWEEN "${_since}" AND "${_before}" `;
        else
          selector += `WHERE DateOfMessage BETWEEN "${_since}" AND "${_before}" `;
      }

      if(contains != null){
        if(_HasWHERE(selector))
          selector += `AND Content LIKE "%${contains}%"`;
        else
          selector += `WHERE Content LIKE "%${contains}%"`;
      }

      conn = _OpenDB();

      conn.all(selector, [], (err, rows) =>{
        if(err) reject(err);

        reslove(rows);
      });
  });
};


function _ReadEdits(author, useID, since, before, contains){
  return new Promise((reslove, reject) => {
    const _since = _ValidateDate(since);
    const _before = _ValidateDate(before);

    let selector = "SELECT * FROM edits ";

    if(author != null){
      if(useID == true)
        selector += `WHERE AuthorID = "${author}" `;
      else
      selector += `WHERE Author = "${author}" `;
    }

    if(_since && !_before){
      if(_HasWHERE(selector))
        selector += `AND DateOfEdit > "${_since}" `;
      else
        selector += `WHERE DateOfEdit > "${_since}" `;
    }
    else if(!_since && before){
      if(_HasWHERE(selector))
        selector += `AND DateOfEdit < "${_before}" `;
      else
        selector += `WHERE DateOfEdit < "${_before}" `;
    }
    else if(_since && _before){
      if(_HasWHERE(selector))
        selector += `AND DateOfEdit BETWEEN "${_since}" AND "${_before}" `;
      else
        selector += `WHERE DateOfEdit BETWEEN "${_since}" AND "${_before}" `;
    }

    if(contains != null){
      if(_HasWHERE(selector))
        selector += `AND EditedContent LIKE "%${contains}%"`;
      else
        selector += `WHERE EditedContent LIKE "%${contains}%"`;
    }

    conn = _OpenDB();

    conn.all(selector, [], (err, rows) =>{
      if(err) reject(err);

      reslove(rows);
    });
});
};


function GetMessages(author, useID, since, before, contains){
  return _ReadMessages(author, useID, since, before, contains);
}

function GetEdits(author, useID, since, before, contains){
  return _ReadEdits(author, useID, since, before, contains);
}

module.exports = { GetMessages, GetEdits }