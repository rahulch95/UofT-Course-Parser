var express = require('express'),
    app = express(),
    http = require('http'),
    request_lib = require('request'),
    server = http.createServer(app),
    ejs = require('ejs'),
    mongoose = require('mongoose'),
    fs = require('fs'),
    cronjob = require('cron').CronJob,
    cheerio = require('cheerio'),
    URL = 'http://www.artsandscience.utoronto.ca/ofr/calendar/';

// set the port and view engine

app.set('port', (process.env.PORT || 5000));
app.set('view engine', 'ejs');
app.use(express.static(__dirname + '/public'));

// connect to mongoose database
fs.readFile('api-key.txt', 'utf8', function(err, data) {
  if (err) throw err;
  var db_url = data.split('\n');
  // connects to database - use your own database here!
  try {
  	mongoose.connect(db_url);
  }
  catch(e) {

  	console.log("Unable to connect to database at " + db_url + "\n");
  	console.log(e);
  }
});


request_lib(URL, function(err, res, body) {

	var $ = cheerio.load(body);
	var stream = fs.createWriteStream("links.txt");

	stream.once('open', function(fd) {

		$('div.items').find('ul.simple').find('a').each(function(index, val) {

			 link = $(this).attr('href');
			 if(link.indexOf('crs') == 0) {
			 	stream.write(URL + link + '\n');
			 }

		});

		stream.end();
	});

});
