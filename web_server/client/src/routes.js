import Base from './Base/Base';
import App from './App/App';
import SignUpPage from './SignUp/SignUpPage';
import LoginPage from './Login/LoginPage';
import Auth from './Auth/Auth';

const routes = {
  component: Base,
  childRoutes: [
    {
      path: '/',
      getComponent: (location, callback) => {
        if (Auth.isUserAuthenticated()) {
          callback(null, App);
        } else {
          callback(null, LoginPage);
        }
      },
    },

    {
      path: '/login',
      component: LoginPage,
    },

    {
      path: '/signup',
      component: SignUpPage,
    },

    {
      path: '/logout',
      onEnter: (nextState, replace) => {
        Auth.deauthenticateUser();
        console.log('here')
        replace('/');
      },
    },
  ],
};

export default routes;
