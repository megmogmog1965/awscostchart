/*
 * 型定義です.
 */

module Types {

  // AWS Credentials.
  export interface AwsCredential {
    name: string;
    aws_access_key_id: string;
    aws_secret_access_key: string;
  }

  export interface TValueLink {
    value: any;
    requestChange: (any) => void;
  }

  export interface TSession {
    userId: string;
  }

}

export = Types;
