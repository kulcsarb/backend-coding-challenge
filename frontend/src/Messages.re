type translate_event = {text: string};

[@bs.deriving abstract]
type status_ = {uid: int, text: string, translation: string, status: string};

type status = {uid: int, text: string, translation: string, status: string};

[@bs.scope "JSON"] [@bs.val]
external parse_status_ : string => status_ = "parse";


[@bs.scope "JSON"] [@bs.val]
external encode_event : translate_event => string = "stringify";

let parse_status = (data: string) : status => {            
    let data = parse_status_(data);
    { uid: uidGet(data), text: textGet(data), translation: translationGet(data), status: statusGet(data) }
}

