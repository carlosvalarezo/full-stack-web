/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'https://127.0.0.1:10443', // the running FLASK api server url
  auth0: {
    url: 'dev-2ntz9src', // the auth0 domain prefix
    audience: 'drinks-api', // the audience set for the auth0 app
    clientId: 'K9HellnWmJ4FMnVBfziWUVGUjzpdFmpz', // the client id generated for the auth0 app
    callbackURL: 'https://127.0.0.1:4200', // the base url of the running ionic application.,
  }
};
