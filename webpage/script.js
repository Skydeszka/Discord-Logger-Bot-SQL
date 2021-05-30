function log(){
    const author = document.getElementById("authorName").value;
    const useID = document.getElementById("useID").value;
    const date1 = document.getElementById("date1").value;
    const date2 = document.getElementById("date2").value;
    const contains = document.getElementById("contains").value;

    let params = new URLSearchParams(
        new URL(window.location.href).search.slice(1)
    );

    params = "";

    if(author.length != 0) params += `&author=${author}`;
    if(useID.length != 0) params += `&author=${useID}`;
    if(date1.length != 0) params += `&author=${date1}`;
    if(date2.length != 0) params += `&author=${date2}`;
    if(contains.length != 0) params += `&author=${contains}`;

    window.location.href = window.location.origin + "?" + params;
}