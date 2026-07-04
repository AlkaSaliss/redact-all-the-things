export interface AppConfig {
  apiEndpoint: string;
  awsRegion: string;
  cognitoUserPoolId: string;
  cognitoClientId: string;
  hostedUiUrl: string;
}

export function readConfig(): AppConfig {
  return {
    apiEndpoint: import.meta.env.VITE_API_ENDPOINT ?? "",
    awsRegion: import.meta.env.VITE_AWS_REGION ?? "eu-west-1",
    cognitoUserPoolId: import.meta.env.VITE_COGNITO_USER_POOL_ID ?? "",
    cognitoClientId: import.meta.env.VITE_COGNITO_CLIENT_ID ?? "",
    hostedUiUrl: import.meta.env.VITE_COGNITO_HOSTED_UI_URL ?? "",
  };
}

export function missingConfig(config: AppConfig): string[] {
  return Object.entries(config)
    .filter(([, value]) => !value)
    .map(([key]) => key);
}
