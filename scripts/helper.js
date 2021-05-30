function ParseBool(value){
    if(typeof value == "string"){
        if(value.toLowerCase() == "true")
            return true;
        else
            return false;
    }
    else if(typeof value == "number"){
        if(value == 1)
            return true
        else
            return false;
    }
    else if(typeof value == "boolean"){
        if(value)
            return true;
        else
            return false;
    }
    else
        return false;
}

module.exports = { ParseBool }