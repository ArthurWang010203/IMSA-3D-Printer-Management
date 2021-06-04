//Arthur Wang & Andrew Wang 1/1/2021
var express = require('express');
var app = express();
const port = 3000
const router = express.Router();
var bodyParser = require('body-parser');
var urlencodedParser = bodyParser.urlencoded({ extended: true });
// mainDiction is dictionary of printers
var mainDiction = {};
const fs = require('fs')
// var mainDiction = {'10.0.0.141:MK3 Prusa':{'name':'10.0.0.141:MK3 Prusa', 'status':'Connected','printJobStarted':'1/1/2021','estimatedPrintTime':'','job':''},'10.0.0.115:Creality 3D Ender 3':{'name':'10.0.0.115:Creality 3D Ender 3','status':'Available','printJobStarted':'','estimatedPrintTime':'','job':''}}

app.use(bodyParser.json());

app.set('view engine', 'ejs');

app.get('/', function(req, res) {
        var arr = [];
        for(var key in mainDiction){
		arr.push(mainDiction[key]);
		if(mainDiction[key]['status']=='Available (Last Print Failed)'){
			fs.appendFileSync('printLog.txt', (mainDiction[key]['name']+" "+mainDiction[key]['job']['user']+": "+mainDiction[key]['job']['file']['name']+" started at "+mainDiction[key]['printJobStarted']+" for "+mainDiction[key]['estimatedPrintTime']+": Failed\n\n"));
		}
		else if(mainDiction[key]['status'=='Available (Last Print Finished)']){
			fs.appendFileSync('printLog.txt', (mainDiction[key]['name']+" "+mainDiction[key]['job']['user']+": "+mainDiction[key]['job']['file']['name']+" started at "+mainDiction[key]['printJobStarted']+" for "+mainDiction[key]['estimatedPrintTime']+": Failed\n\n"));
		}
        }
        res.render('/home/pi/statusPage/index.ejs', {
                printerInfo: arr
        });
});

//trying lights
//button trigger
//python script (import paramiko, import scp)
//copy python script to printer pi
//stdin, stdout, stderr = con.exec_command('bash /tmp/test.sh') //run gpio toggle (https://instructobit.com/tutorial/116/Remotely-running-commands-or-scripts-with-python)
//toggle/on for set duration
//end lights

app.post('/', (request, response) => {
        console.log(request.body);

        var jsonRequest = request.body;
        var name = jsonRequest.name;
        mainDiction[name] = jsonRequest;
        var jsonResponse = jsonRequest.name;
        response.send(jsonResponse);
});

app.use('/', router);
console.log('Operating on Port: '+port);
app.listen(process.env.port || port);
