const express = require('express');
const path = require('path');
const cors = require('cors');
const passport = require('passport');
const bodyParser = require('body-parser');

const winston = require('winston');
// Config the logging file path, so it can be forwarded by Filebeat
winston.configure({
  transports: [
    new (winston.transports.File)({ filename: '/var/log/coconut_news/web_server.log' })
  ],
  exitOnError: false,
});

const indexRouter = require('./routes/index');
const authRouter = require('./routes/auth');
const newsRouter = require('./routes/news');

const app = express();

const config = require('./config');
require('./models/main.js').connect(config.MONGODB_URI);

// view engine setup
app.set('view engine', 'jade');
app.set('views', path.join(__dirname, '../client/build'));

app.use('/static', express.static(path.join(__dirname, '../client/build/static')));
app.use(bodyParser.json());

// TODO: Remove this after development is done.
app.use(cors());
  
app.use(passport.initialize());
const signupPassportStrategy = require('./passport/signupPassportStrategy');
const loginPassportStrategy = require('./passport/loginPassportStrategy');
passport.use('signup', signupPassportStrategy);
passport.use('login', loginPassportStrategy);

app.use('/', indexRouter);
app.use('/auth', authRouter);

const authChecker = require('./middlewares/authChecker');
app.use('/news', authChecker);
app.use('/news', newsRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  res.send('404 Not Found!');
});

module.exports = app;
