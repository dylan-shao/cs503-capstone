const lynx = require('lynx');
const config = require('../config');

const metricsClient = new lynx(config.STATSD_HOST, config.STATSD_PORT);

module.exports = metricsClient;
