import execjs


def get_token(pwd, salt):
    Passwd = execjs.compile(open(r"aes.js").read()).call('encryptPassword', pwd, salt)
    return Passwd
