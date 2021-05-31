function search(){
    const author = document.getElementById("authorName").value;
    const useID = document.getElementById("useID").checked;
    const date1 = document.getElementById("date1").value;
    const date2 = document.getElementById("date2").value;
    const contains = document.getElementById("contains").value;

    let params = new URLSearchParams();

    if(author.length != 0) params.append("author", author);
    if(useID.length != 0) params.append("useid", useID);
    if(date1.length != 0) params.append("since", date1);
    if(date2.length != 0) params.append("before", date2);
    if(contains.length != 0) params.append("contains", contains);

    window.location.href = window.location.origin + "/logs/" + "?" + params;
}


function reset(){
    const author = document.getElementById("authorName").value = null;
    const useID = document.getElementById("useID").checked = false;
    const date1 = document.getElementById("date1").value = null;
    const date2 = document.getElementById("date2").value = null;
    const contains = document.getElementById("contains").value = null;

    window.location.href = window.location.origin + "/logs/"
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

    window.location.href = window.location.origin + "/logs/" + "?" + paramString;
}