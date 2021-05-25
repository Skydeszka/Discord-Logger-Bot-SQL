function log(){
    const author = document.getElementById("authorName").value;
    const useID = document.getElementById("useID").value;
    const date1 = document.getElementById("date1").value;
    const date2 = document.getElementById("date2").value;
    const contains = document.getElementById("contains").value;

    let params = new URLSearchParams(
        new URL(window.location.href).search.slice(1)
    );

    if(author.length != 0) params = ("selectBy=" + `name,${author}`)
    else params = "";

    window.location.href = window.location.origin + "?" + params;
}