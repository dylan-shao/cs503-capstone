const mongoose = require('mongoose');
const winston = require('winston');

const connect = (uri) => {
  mongoose.connect(uri);

  mongoose.connection.on('error', (err) => {
    console.error('Mongoose connection error: %{err}');
    winston.error(`web_server MongoDB connect error : ${err.message}`);
    process.exit(1);
  });

  require('./user');
};

module.exports = {
  connect,
};