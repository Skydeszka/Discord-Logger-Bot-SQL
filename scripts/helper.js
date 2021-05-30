function ParseBool(value){
    if(isNaN(value)){
        if(value.toLowerCase() == "true")
            return true;
        else
            return false;
    }
    else{
        if(value == 1)
            return true
        else
            return false;
    }
}

module.exports = { ParseBool }