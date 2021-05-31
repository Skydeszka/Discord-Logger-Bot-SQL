function search(){
    const author = document.getElementById("authorName").value;
    const useID = document.getElementById("useID").checked;
    const origindate1 = document.getElementById("origindate1").value;
    const origindate2 = document.getElementById("origindate2").value;
    const editdate1 = document.getElementById("editdate1").value;
    const editdate2 = document.getElementById("editdate2").value;
    const origincontains = document.getElementById("origincontains").value;
    const editcontains = document.getElementById("editcontains").value;

    let params = new URLSearchParams();

    if(author.length != 0) params.append("author", author);
    if(useID.length != 0) params.append("useid", useID);
    if(origindate1.length != 0) params.append("originsince", origindate1);
    if(origindate2.length != 0) params.append("originbefore", origindate2);
    if(editdate1.length != 0) params.append("editsince", editdate1);
    if(editdate2.length != 0) params.append("editbefore", editdate2);
    if(origincontains.length != 0) params.append("origincontains", origincontains);
    if(editcontains.length != 0) params.append("editcontains", editcontains);

    window.location.href = window.location.origin + "/edits/" + "?" + params;
}


function reset(){
    const author = document.getElementById("authorName").value = null;
    const useID = document.getElementById("useID").checked = false;
    const origindate1 = document.getElementById("origindate1").value = null;
    const origindate2 = document.getElementById("origindate2").value = null;
    const editdate1 = document.getElementById("editdate1").value = null;
    const editdate2 = document.getElementById("editdate2").value = null;
    const origincontains = document.getElementById("origincontains").value = null;
    const editcontains = document.getElementById("editcontains").value = null;

    window.location.href = window.location.origin + "/edits/"
}

function changepage(offset){

    let params = new URLSearchParams(document.location.search);

    let paramString = new URLSearchParams();

    let page = false;

    params.forEach((value, key) => {
        if(key == "page")
            page = parseInt(value);
        else
            paramString.append(key, value);
    });

    if(!page)
        page = 1

    page += offset;

    if(page < 1)
        page = 1

    paramString.append("page", page);

    window.location.href = window.location.origin + "/edits/" + "?" + paramString;
}