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

    window.location.href = window.location.origin + "/edits" + "?" + params;
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

    window.location.href = window.location.origin + "/edits"
}