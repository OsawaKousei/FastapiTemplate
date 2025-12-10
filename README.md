# Serverless Mock API Generator

FastAPI と DynamoDB を使用した、サーバーレス対応のモック API ジェネレーターです。
AWS Lambda Web Adapter を使用することで、AWS Lambda 上で通常の Web サーバーのように動作するように設計されています。

## 特徴

- **動的なモック作成**: API 経由でエンドポイント（パス、メソッド、レスポンス、ヘッダー）を動的に登録・削除可能。
- **遅延シミュレーション**: レスポンスに任意の遅延（latency_ms）を設定し、タイムアウト処理のテストなどが可能。
- **サーバーレス最適化**: AWS Lambda Web Adapter を採用し、FastAPI アプリケーションをそのまま Lambda にデプロイ可能。
- **高速な開発環境**: パッケージマネージャー `uv` と Docker Compose を使用した高速なローカル開発環境。
- **厳格な設計指針**: 保守性を高めるための厳格な型定義と制限された OOP ガイドラインに準拠。

## 技術スタック

- **言語**: Python 3.12
- **フレームワーク**: FastAPI
- **データベース**: Amazon DynamoDB (ローカル開発時は DynamoDB Local)
- **パッケージ管理**: uv
- **デプロイ**: Docker, AWS Lambda Web Adapter

## ローカル開発環境のセットアップ

### 前提条件

- Docker Desktop (または Docker Engine + Docker Compose)

### 起動方法

1. **コンテナのビルドと起動**

   ```bash
   docker compose up --build
   ```

   API サーバーは `http://localhost:8080` で起動します。
   DynamoDB Local は `http://localhost:8000` で起動します。

2. **動作確認 (テストスクリプト)**
   付属のスクリプトを実行することで、DB の初期化からモックの作成・テスト・削除までを一括で確認できます。
   ```bash
   chmod +x test.sh
   ./test.sh
   ```

### 手動での DB 初期化

もし手動でテーブルを作成したい場合は、以下のコマンドを実行してください。

```bash
docker compose exec app uv run python scripts/init_dynamodb.py
```

## API 利用例

### 1. ヘルスチェック

```bash
curl http://localhost:8080/
```

### 2. モックエンドポイントの作成

```bash
curl -X POST http://localhost:8080/api/mocks \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/test-endpoint",
    "method": "GET",
    "status_code": 200,
    "response_body": {"message": "This is a mock response"},
    "headers": {"X-Custom-Header": "mock-value"},
    "latency_ms": 500
  }'
```

### 3. モックエンドポイントの呼び出し

```bash
curl -v http://localhost:8080/test-endpoint
```

### 4. モックエンドポイントの削除

作成時に返却された ID を指定して削除します。

```bash
curl -X DELETE http://localhost:8080/api/mocks/{mock_id}
```

## 本番デプロイ (AWS Lambda)

本プロジェクトは AWS Lambda Web Adapter を使用しています。

1. **本番用イメージのビルド**

   ```bash
   docker build -f Dockerfile.prod -t my-mock-api .
   ```

2. **デプロイ手順の概要**
   - ビルドしたイメージを Amazon ECR にプッシュします。
   - AWS Lambda 関数を作成し、コンテナイメージとしてプッシュしたイメージを指定します。
   - 環境変数を設定します（`DYNAMODB_ENDPOINT_URL` は本番では不要、AWS 認証情報は IAM ロールで管理）。
   - 必要に応じて DynamoDB テーブル (`MockEndpoints`) を作成します。

## ディレクトリ構成

```
.
├── app/                    # アプリケーションソースコード
│   ├── src/                # 主要ロジック
│   ├── scripts/            # ユーティリティスクリプト
│   └── pyproject.toml      # 依存関係定義
├── Dockerfile.dev          # 開発用 Dockerfile
├── Dockerfile.prod         # 本番用 Dockerfile (Lambda Web Adapter)
├── docker-compose.yaml     # ローカル開発用構成
└── test.sh                 # 動作確認用スクリプト
```
