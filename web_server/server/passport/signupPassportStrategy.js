const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;
const winston = require('winston');

const signupPassportStrategy = new PassportLocalStrategy({
  usernameField: 'email',
  passwordField: 'password',
  passReqToCallback: true
}, (req, email, password, done) => {
  const userData = {
    email: email.trim(),
    password: password.trim(),
  };

  const newUser = new User(userData);
  newUser.save((err) => {
    console.log('Save new user!');
    if (err) {
      winston.error(`web_server error: ${err.message}`)
      return done(err);
    }

    return done(null);
  });
});

module.exports = signupPassportStrategy;
