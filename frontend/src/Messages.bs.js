// Generated by BUCKLESCRIPT VERSION 5.0.0, PLEASE EDIT WITH CARE
'use strict';


function parse_status(data) {
  var data$1 = JSON.parse(data);
  return /* record */[
          /* uid */data$1.uid,
          /* text */data$1.text,
          /* translation */data$1.translation,
          /* status */data$1.status
        ];
}

exports.parse_status = parse_status;
/* No side effect */