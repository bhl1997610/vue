const mysql = require('mysql');
const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'mysql',
    port: 3306
});
function DataBase() {
    this.added = function (str, cb) {
        var sql = 'INSERT INTO test(渠道号) VALUES(?)';
        connection.query(sql, [str], function (err, result) {

            if (err) {
                cb(false);
                console.log(err);
                return;
            }
            else if (result) {
                cb(true);
                console.log("添加成功");
            }
            else {
                cb(false);
                console.log("添加失败");
            }

        })
    }
    this.init = function (tbname, cb) {
        var exsit="SELECT table_name FROM information_schema.TABLES WHERE table_name = " +  "'"+tbname+"'"+""
        var sql = 'select * from ' + tbname;
        //var creat="CREATE TABLE  " + tbname + " (渠道号 varchar(255),渠道名 varchar(255),素材 varchar(255),消耗 varchar(255),曝光 varchar(255),点击 varchar(255),点击率 varchar(255),新增（授权前） varchar(255),新增（授权后） varchar(255),授权转化 varchar(255),开局账号数 varchar(255),开局率 varchar(255),人均盘数 varchar(255),日期 varchar(255))"

        connection.query(exsit, function (err, result) {
            if (err) {
                
                console.log(err);
                return;
            }
            else if (result.length) {
                connection.query(sql, function (err, result) {
                    if (err) {
                        cb(false);
                        console.log(err);
                        return;
                    }
                    else if (result) {
                        cb(true,result)
                        console.log("init");
    
                    }
                    else {
                        cb(false);
                        console.log("initfalse");
                    }
    
                })
               
               
            }
            else{
                console.log("没有此表");
            }
        });
    };
    this.create=function(tbname){
        
    }
        this.find = function (pname, date, qudao, cb) {
            var length = qudao.length;
            var datalist = [];
            var sql;
            if (pname && date && !qudao) {
                sql = 'select * from ' + pname + ' where  日期=?';
                datalist = [date];
            }
            if (pname && date && qudao) {
                if (length == 1) {
                    sql = 'select * from ' + pname + ' where  日期=? and  渠道号=?';
                }
                else {
                    sql = 'select * from ' + pname + ' where   日期=? and  (渠道号=?';
                }

                datalist = [date, qudao[0]];
                for (var i = 1; i < length; i++) {
                    datalist.push(qudao[i]);
                    if (i == length - 1) {
                        sql += "or 渠道号=?)"
                        break;
                    }
                    sql += "or 渠道号=?";
                }

            }
            if (pname && !date && qudao) {
                if (length == 1) {
                    sql = 'select * from ' + pname + ' where   渠道号=?';
                }
                else {
                    sql = 'select * from ' + pname + ' where  (渠道号=?';
                }
                datalist = [qudao[0]];
                for (var i = 1; i < length; i++) {
                    datalist.push(qudao[i]);
                    if (i == length - 1) {
                        sql += "or 渠道号=?)"
                        break;
                    }
                    sql += "or 渠道号=?";
                }

            }
            if (pname && !date && !qudao) {
                sql = 'select * from ' + pname + '';
            }

            connection.query(sql, datalist, function (err, result) {
                if (err) {
                    cb(false);
                    console.log(err);
                    return;
                }
                else if (result) {
                    cb(true, result);

                }
                else {
                    cb(false);
                    console.log("错误");
                }

            })
        }

    connection.connect(function (err) {
        if (err) {
            console.log("数据库连接失败" + err);
        }
        else {
            console.log("数据库连接成功");
        }
    });
   this.create()
}

module.exports = new DataBase();

