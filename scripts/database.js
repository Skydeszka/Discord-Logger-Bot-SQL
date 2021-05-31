const sqlite3 = require('sqlite3');
const helper = require('./helper');
const config = require('./config');

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


function _ValidateSortyType(sorttype){
  if(sorttype == "desc")
    return "DESC";
  else
    return "ASC";
}


function _HasWHERE(selector){
  return selector.includes(" WHERE ");
}


function _ReadMessages(author, useID, since, before, contains, page, sortby, sorttype){
    return new Promise((reslove, reject) => {
      const _since = _ValidateDate(since);
      const _before = _ValidateDate(before);
      const _sorttype = _ValidateSortyType(sorttype);


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
      else if(!_since && _before){
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

      if(sortby != null){
        if(sortby == "date")
          selector += `ORDER BY DateOfMessage ${_sorttype} `;
        else if(sortby == "content")
          selector += `ORDER BY Content ${_sorttype} `;
        else if(sortby == "author"){
          if(useID)
            selector += `ORDER BY AuthorID ${_sorttype} `;
          else
            selector += `ORDER BY Author ${_sorttype} `;
        }
      }

      selector += `LIMIT ${helper.PageOffset(page, config.config.listPerPage)}, ${config.config.listPerPage}`;

      conn = _OpenDB();

      conn.all(selector, [], (err, rows) =>{
        if(err) reject(err);

        reslove(rows);
      });
  });
};


function _ReadEdits(author, useID, originsince, originbefore, editsince, editbefore, origincontains, editcontains, page, sortby, sorttype){
  return new Promise((reslove, reject) => {
    const _originsince = _ValidateDate(originsince);
    const _originbefore = _ValidateDate(originbefore);
    const _editsince = _ValidateDate(editsince);
    const _editbefore = _ValidateDate(editbefore);
    const _sorttype = _ValidateSortyType(sorttype);

    let selector = "SELECT * FROM edits ";

    if(author != null){
      if(useID == true)
        selector += `WHERE AuthorID = "${author}" `;
      else
      selector += `WHERE Author = "${author}" `;
    }

    if(_editsince && !_editbefore){
      if(_HasWHERE(selector))
        selector += `AND DateOfEdit > "${_editsince}" `;
      else
        selector += `WHERE DateOfEdit > "${_editsince}" `;
    }
    else if(!_editsince && _editbefore){
      if(_HasWHERE(selector))
        selector += `AND DateOfEdit < "${_editbefore}" `;
      else
        selector += `WHERE DateOfEdit < "${_editbefore}" `;
    }
    else if(_editsince && _editbefore){
      if(_HasWHERE(selector))
        selector += `AND DateOfEdit BETWEEN "${_editsince}" AND "${_editbefore}" `;
      else
        selector += `WHERE DateOfEdit BETWEEN "${_editsince}" AND "${_editbefore}" `;
    }

    if(_originsince && !_originbefore){
      if(_HasWHERE(selector))
        selector += `AND DateOfOriginal > "${_originsince}" `;
      else
        selector += `WHERE DateOfOriginal > "${_originsince}" `;
    }
    else if(!_originsince && _originbefore){
      if(_HasWHERE(selector))
        selector += `AND DateOfOriginal < "${_originbefore}" `;
      else
        selector += `WHERE DateOfOriginal < "${_originbefore}" `;
    }
    else if(_originsince && _originbefore){
      if(_HasWHERE(selector))
        selector += `AND DateOfOriginal BETWEEN "${_originsince}" AND "${_originbefore}" `;
      else
        selector += `WHERE DateOfOriginal BETWEEN "${_originsince}" AND "${_originbefore}" `;
    }

    if(editcontains != null){
      if(_HasWHERE(selector))
        selector += `AND EditedContent LIKE "%${editcontains}%"`;
      else
        selector += `WHERE EditedContent LIKE "%${editcontains}%"`;
    }

    if(origincontains != null){
      if(_HasWHERE(selector))
        selector += `AND OriginalContent LIKE "%${origincontains}%"`;
      else
        selector += `WHERE OriginalContent LIKE "%${origincontains}%"`;
    }

    if(sortby != null){
      if(sortby == "origindate")
        selector += `ORDER BY DateOfOriginal ${_sorttype} `;
      if(sortby == "editdate")
        selector += `ORDER BY DateOfEdit ${_sorttype} `;
      else if(sortby == "origincontent")
        selector += `ORDER BY OriginalContent ${_sorttype} `;
      else if(sortby == "editcontent")
        selector += `ORDER BY EditedContent ${_sorttype} `;
      else if(sortby == "author"){
        if(useID)
          selector += `ORDER BY AuthorID ${_sorttype} `;
        else
          selector += `ORDER BY Author ${_sorttype} `;
      }
    }

    selector += `LIMIT ${helper.PageOffset(page, config.config.listPerPage)}, ${config.config.listPerPage}`;

    conn = _OpenDB();

    conn.all(selector, [], (err, rows) =>{
      if(err) reject(err);

      reslove(rows);
    });
});
};


function GetMessages(author, useID, since, before, contains, page = 1, sortby, sorttype){
  return _ReadMessages(author, useID, since, before, contains, page, sortby, sorttype);
}

function GetEdits(author, useID, originsince, originbefore, editsince, editbefore, origincontains, editcontains, page = 1, sortby, sorttype){
  return _ReadEdits(author, useID, originsince, originbefore, editsince, editbefore, origincontains, editcontains, page, sortby, sorttype);
}

module.exports = { GetMessages, GetEdits }