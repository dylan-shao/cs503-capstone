const fs = require('fs');
const yaml = require('js-yaml');
const _ = require('lodash');

let config = {
  MONGODB_URI: undefined,
  JWT_SECRET: undefined,
  BACKEND_SERVICE_HOST: undefined,
  BACKEND_SERVICE_PORT: undefined,
  STATSD_HOST: undefined,
  STATSD_PORT: undefined,
};

try {
  const configFilePath = `${__dirname}/../../config.yaml`;
  const doc = yaml.safeLoad(fs.readFileSync(configFilePath));

  config.MONGODB_URI = _.get(doc, 'web_service.mongodb_uri');
  config.JWT_SECRET = _.get(doc, 'web_service.jwt_secret');

  config.BACKEND_SERVICE_HOST = _.get(doc, 'backend_service.host');
  config.BACKEND_SERVICE_PORT = _.get(doc, 'backend_service.port');

  config.STATSD_HOST = _.get(doc, 'statsd.host');
  config.STATSD_PORT = _.get(doc, 'statsd.port');
} catch (e) {
  console.log(e);
}

module.exports = config;
