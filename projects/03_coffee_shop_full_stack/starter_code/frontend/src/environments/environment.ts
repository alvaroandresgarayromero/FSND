/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-amj9exua.us', // the auth0 domain prefix
    audience: 'dev', // the audience set for the auth0 app
    clientId: 'TTutbKettxTUMH6y4smXwpsKaB5eJF0p', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8100', // the base url of the running ionic application.
  }
};
