const jayson = require('jayson');
const moment = require('moment');
const winston = require('winston');
const config = require('../config');
const metricsClient = require('../metrics_client/metrics_client');

const client = jayson.client.http({
  hostname: config.BACKEND_SERVICE_HOST,
  port: config.BACKEND_SERVICE_PORT,
});

const add = (a, b, callback) => {
  client.request('add', [a, b], (err, error, response) => {
    if (err) {
        throw err;
    }

    callback(response);
  });
};

// Get news summaries for a user
const getNewsSummariesForUser = (user_id, page_num, callback) => {
  const startTime = moment();

  client.request('getNewsSummariesForUser', [user_id, page_num], (err, error, response) => {
    if (err) {
      winston.error(`web_server getNewsSummariesForUser RPC call error: ${err.message}`);
      throw err;
    }

    // Send the time took to response metric.
    const endTime = moment();
    const timeInMilliSeconds = endTime.diff(startTime);
    metricsClient.timing('coconut_news.web_server.getNewsSummariesForUser', Math.ceil(timeInMilliSeconds));

    callback(response);
  });
};

// Log a news click event for a user
const logNewsClickForUser = (user_id, news_id) => {
    const startTime = moment();

    client.request('logNewsClickForUser', [user_id, news_id], (err, error, response) => {
        if (err) {
          winston.error(`web_server logNewsClickForUser RPC call error: ${err.message}`);
          throw err;
        }

        // Send the time took to response metric.
        const endTime = moment();
        const timeInMilliSeconds = endTime.diff(startTime);
        metricsClient.timing('coconut_news.web_server.logNewsClickForUser', Math.ceil(timeInMilliSeconds));
    });
};

module.exports = {
  add,
  getNewsSummariesForUser,
  logNewsClickForUser,
};
