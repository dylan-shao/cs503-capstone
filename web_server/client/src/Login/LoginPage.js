import React from 'react';
import PropTypes from 'prop-types';
import LoginForm from './LoginForm';
import Auth from '../Auth/Auth';

class LoginPage extends React.Component {
  constructor(props, context) {
    super(props, context);

    this.state = {
      errors: {},
      user: {
        email: '',
        password: '',
      },
    };
  }

  processForm = (event) => {
    event.preventDefault();

    const email = this.state.user.email;
    const password = this.state.user.password;

    // TODO: Delete after test
    console.log(`email: ${email}`);
    console.log(`password: ${password}`);

    const serverUrl = location.protocol + '//' + location.host
    fetch(serverUrl + '/auth/login', {
      method: 'POST',
      cache: false,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: this.state.user.email,
        password: this.state.user.password
      })
    }).then(response => {
      if (response.status === 200) {
        this.setState({
          errors: {},
        });

        response.json().then(function(json) {
          console.log(json);
          Auth.authenticateUser(json.token, email);
          this.context.router.replace('/');
        }.bind(this));
      } else {
        console.log('Login failed');
        response.json().then(function(json) {
          const errors = json.errors ? json.errors : {};
          errors.summary = json.message;
          this.setState({
            errors,
          });
        }.bind(this));
      }
    });
  }

  emailOrPasswordChanged = (event) => {
    const field = event.target.name;
    const user = this.state.user;
    user[field] = event.target.value;

    this.setState({
      user,
    });
  }

  render() {
    return (
      <LoginForm
        onSubmit={this.processForm}
        onChange={this.emailOrPasswordChanged}
        errors={this.state.errors}
      />
    );
  }
}

LoginPage.contextTypes = {
  router: PropTypes.object.isRequired
};

export default LoginPage;
