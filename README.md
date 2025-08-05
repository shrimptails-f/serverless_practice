# プロジェクト概要

本リポジトリは Serverless Framework の学習用リポジトリです。  
本来はサービス単位でリポジトリを分けるべきですが、学習効率を優先してまとめています。

## 使用技術

### 言語

- Python3.9

### ローカル環境

- Docker
- DevContainer
- LocalStack

### AWS サービス

- DynamoDB
- Lambda

## ディレクトリ構成

```project root
├── .devcontainer 環境構築資材
├── .vscode エディタの設定ファイル
├── dynamodb DynamoDB関連のデプロイ資材
└── lambda lambda関連のデプロイ資材
```

## 環境構築手順

### ソースをクローンする

### .env をコピーする

```bash
cp .devcontainer/.env.sample .devcontainer/.env
```

#### VsCode でプロジェクトフォルダーを開く

### Reopen in Container を押下

Ctrl Shift P → Reopen in container と入力して実行

## ローカル環境での動作確認手順

以下の手順は全て VsCode のターミナルで実行してください。

### DynamoDB へテーブル作成を行う。

```
cd dynamodb
task local-dynamodb-deploy
```

### Lambda にデプロイする。

```
cd lambda
task local-deploy
```

### ローカルで動作確認を行う

```
pwd
/data/lambda

task test-users
```

## AWS へのデプロイ手順

以下の手順は全て VsCode のターミナルで実行してください。

/data/.devcontainer/.env で下記項目が設定されていることを確認してください。  
下記のキーは AWS_ACCESS_KEY_ID 取得方法などで調べて、AWS から取得してください。

```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
```

### Lambda にデプロイする。

```
cd dynamodb
task production-deploy-aws
```

### Lambda にデプロイする。

```
cd lambda
task production-deploy
```

## リソースの削除手順

```
cd dynamodb
task production-destroy-aws

cd lambda
task production-destroy
```
