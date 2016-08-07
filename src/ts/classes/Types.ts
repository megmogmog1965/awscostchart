/*
 * 型定義です.
 */

module Types {

  // AWS Credentials.
  export interface TAwsCredential {
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

  export interface TChargeSample {
    timestamp: number;
    value: number;
    aws_access_key_id: string;
  }

  export interface TEstimatedCharge {
    AWSDataTransfer: TChargeSample[];
    AWSQueueService: TChargeSample[];
    AmazonEC2: TChargeSample[];
    AmazonES: TChargeSample[];
    AmazonElastiCache: TChargeSample[];
    AmazonRDS: TChargeSample[];
    AmazonRoute53: TChargeSample[];
    AmazonS3: TChargeSample[];
    AmazonSNS: TChargeSample[];
    awskms: TChargeSample[];
  }

}

export = Types;
