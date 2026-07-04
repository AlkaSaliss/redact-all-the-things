import { UserManager, WebStorageStateStore, type User } from "oidc-client-ts";
import type { AppConfig } from "./config";

export function createUserManager(config: AppConfig): UserManager {
  return new UserManager({
    authority: `https://cognito-idp.${config.awsRegion}.amazonaws.com/${config.cognitoUserPoolId}`,
    client_id: config.cognitoClientId,
    redirect_uri: `${window.location.origin}/auth/callback`,
    post_logout_redirect_uri: window.location.origin,
    response_type: "code",
    scope: "openid email profile",
    metadata: {
      issuer: `https://cognito-idp.${config.awsRegion}.amazonaws.com/${config.cognitoUserPoolId}`,
      authorization_endpoint: `${config.hostedUiUrl}/oauth2/authorize`,
      token_endpoint: `${config.hostedUiUrl}/oauth2/token`,
      end_session_endpoint: `${config.hostedUiUrl}/logout`,
    },
    userStore: new WebStorageStateStore({ store: window.sessionStorage }),
  });
}

export function displayUser(user: User): string {
  return (
    user.profile.email?.toString() ||
    user.profile.name?.toString() ||
    user.profile.sub ||
    "Signed in"
  );
}
