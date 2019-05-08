const boxsdk = require('boxsdk')
const mysql = require("./mysql")
// 应用级别
let myBoxApp = new boxsdk.BoxApp('http://test.box.imeete.com', 1043, 'cf243f9328b755c9916e17ca08dc474f');
let ticket;
function Box() {
    var _this = this;
    this.token = function (temp_ticket, req, cb) {
        myBoxApp.auth_verify(temp_ticket).then(data => {
            console.log(data, 'login')
            if (data.code == 0) {
                req.session.app_token = data.data.app_token;
                cb(true, data.app_token);
            }
            else {
                cb(false)
            }
        })
    }
    this.logout = function (token, cb) {
        myBoxApp.logout(token).then(data => {
            console.log(data, 'logout');
            if (data.code == 0) {
                cb(true);
            } else {
                cb(false);
            }
        })
    }
    this.getuserinfo = function (token, cb) {

        myBoxApp.user_info(token, 'menus').then(data => {
            console.log(data.data, 'user')
                cb(data.data)
        })
    }
    this.getusercurrent_scop_info = function (token, cb) {
        myBoxApp.user_info(token, 'current_scope_info').then(data => {
            console.log(data.data.current_scope_info.svalue, 'current_scope_info');
            mysql.init(data.data.current_scope_info.svalue, function (result, list) {
                if (result) {
                    list.push(data.data.current_scope_info.svalue);
                    cb(true,list);
                } else {
                    cb(false)
                }

            })
        })


    }
}
module.exports = new Box();