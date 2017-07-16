const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const config = require('../config');

module.exports = (req, res, next) => {
  if (!req.headers.authorization) {
    return res.status(401).end();
  }

  // 'bearer token'
  const token = req.headers.authorization.split(' ')[1];

  console.log('authChekcer: token: ' + token);

  // decode the token using a secret key-phrase
  return jwt.verify(token, config.JWT_SECRET, (err, decoded) => {
    // the 401 code is for unauthorized status
    if (err) {
      return res.status(401).end();
    }

    const id = decoded.sub;

    // check if a user exists
    return User.findById(id, (userErr, user) => {
      if (userErr || !user) {
        return res.status(401).end();
      }

      return next();
    });
  });
};
