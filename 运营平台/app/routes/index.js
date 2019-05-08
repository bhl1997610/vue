
var express = require('express');
var router = express.Router();
const mysql = require("./mysql");
const Box = require('./box');
const child_process = require('child_process');
const fs = require('fs');
const path = require('path');
/* GET home page. */

router.get('/getqrcode', function (req, res, next) {
    fs.readdir('public/images', function(err, files) {
      if (err) {
          throw err;
      }
      
       res.send(files)
  });
 
});
  
router.get('/home', function (req, res, next) {
 
  res.render("index")
});
router.get('/', function (req, res, next) {
  
  res.redirect('http://test.box.imeete.com/v2/auth/index?redirect=http%3A%2F%2F192.168.146.159:3000%2Fticket%3Fredirect%3Dhttp%253A%252F%252F192.168.146.159:3000%2Fhome%2F&app_id=1043')
  
});
router.get('/App', function (req, res, next) {
  res.render("index")
});
router.get('/qrcode', function (req, res, next) {
  res.render("index")
});

router.get('/ticket', function (req, res, next) {
  var data = req.query;
  console.log(data)
  Box.token(data.ticket, req, function (result, a) {
    if (result) {
      console.log("換票成功");
      res.cookie("token", req.session.app_token);
      res.redirect(data.redirect);
    }
    else {
      console.log("換票失敗");
      res.send("错误");
    }
  });
});
router.get('/userinfo', function (req, res, next) {
  var data = req.query;
  console.log(data.token)
  Box.getuserinfo(data.token, function (menu) {
        res.send(menu);
  })


});

router.get('/find', function (req, res, next) {
  var data = req.query;
  var date = data.date;
  var qudao = data.qudao;
  var projiectName = data.projiectName;
  mysql.find(projiectName, date, qudao, function (result, data) {
    if (result) {
    
      res.send(data);
    }
    else {
      res.send("false");
    }
  });

});
router.get('/init', function (req, res, next) {
  var data = req.query
  Box.getusercurrent_scop_info(data.token, function (result, list) {
    if (result) {

      res.send(list)
    } else {
      res.send("false")
    }

  });


});
router.get('/add', function (req, res, next) {
  var data = req.query;
  var projiectName = data.projiectName;
  mysql.added(projiectName, function (result, data) {
    if (result) {
      res.send(data);
    }
    else {
      res.send("false");
    }
  });

});
function createSpider() {


  fs.readFile(path.join(__dirname, '../configure.json'), 'utf8', function (err, data) {
    if (err) throw err;
    data2 = JSON.parse(data);
    //console.log(data2);
    for (key in data2) {
      
      if (parseInt(key)  < 2000) {
        child_process.exec('python wxmp.py ' + key, function (error, stdout, stderr) {
          if (error) {
            console.log(error.stack);
            console.log('Error code: ' + error.code);
            console.log('Signal received: ' + error.signal);
          }
          console.log('stdout: ' + stdout);
          console.log('stderr: ' + stderr);

        });
      }
      else {
        child_process.exec('python magicsquare.py ' + key, function (error, stdout, stderr) {
          if (error) {
            console.log(error.stack);
            console.log('Error code: ' + error.code);
            console.log('Signal received: ' + error.signal);
          }
          console.log('stdout: ' + stdout);
          console.log('stderr: ' + stderr);

        });
      }

     }

  });

}
createSpider()
module.exports = router;
