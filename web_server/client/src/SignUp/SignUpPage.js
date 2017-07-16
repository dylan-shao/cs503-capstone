import React from 'react';
import PropTypes from 'prop-types';
import SignUpForm from './SignUpForm';

class SignUpPage extends React.Component {
  constructor(props, context) {
    super(props, context);

    this.state = {
      errors: {},
      user: {
        email: '',
        password: '',
        confirm_password: ''
      }
    };
  }

  processForm = (event) => {
    event.preventDefault();

    const email = this.state.user.email;
    const password = this.state.user.password;
    const confirm_password = this.state.user.confirm_password;

    console.log('email:' + email);
    console.log('password:' + password);
    console.log('confirm_password:' + password);

    if (password !== confirm_password) {
      return;
    }

    const serverUrl = location.protocol + '//' + location.host
    fetch(serverUrl + '/auth/signup', {
      method: 'POST',
      cache: false,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
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

        this.context.router.replace('/login');
      } else {
        response.json().then(function(json) {
          console.log(json);
          const errors = json.errors ? json.errors : {};
          errors.summary = json.message;
          console.log(this.state.errors);
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
      user
    });

    if (this.state.user.password !== this.state.user.confirm_password) {
        const errors = this.state.errors;
        errors.password = `Password and Confirm Password don't match.`;
        this.setState({
          errors,
        });
    } else {
      const errors = this.state.errors;
      errors.password = '';
      this.setState({
        errors,
      });
    }
  }

  render() {
    return (
      <SignUpForm
        onSubmit={this.processForm}
        onChange={this.emailOrPasswordChanged}
        errors={this.state.errors}
      />
    );
  }
}

SignUpPage.contextTypes = {
  router: PropTypes.object.isRequired,
};

export default SignUpPage;
