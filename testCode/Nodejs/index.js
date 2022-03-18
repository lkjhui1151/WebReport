const crypto = require("crypto");

var hash = crypto.createHash('sha512');


function func(string) {
    data = hash.update(string).digest('hex');
    // gen_hash = data;
    console.log(data);
}

func("ABCD")