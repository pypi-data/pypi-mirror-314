# botrun_flow_lang

## 安裝
- 用 poetry 管理 python 環境

## 輸出可用的 requirements.txt
```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes --without-urls
```

### 建立 dev 的 index
```bash
gcloud firestore indexes composite create \
  --collection-group=botrun-hatch-dev-hatch \
  --field-config=field-path=user_id,order=ascending \
  --field-config=field-path=name,order=ascending \
  --field-config=field-path=__name__,order=ascending \
  --project=scoop-386004
```

### 打包 dev
```bash
gcloud builds submit --config cloudbuild_fastapi_dev.yaml --project=scoop-386004
```
### deploy cloud run, dev 的版本
```bash
gcloud run deploy botrun-flow-lang-fastapi-dev \
  --image asia-east1-docker.pkg.dev/scoop-386004/botrun-flow-lang/botrun-flow-lang-fastapi-dev \
  --port 8080 \
  --platform managed \
  --allow-unauthenticated \
  --project=scoop-386004 \
  --region=asia-east1 \
  --cpu 2 \
  --memory 8Gi \
  --min-instances 0 \
  --max-instances 5 \
  --timeout 3600s \
  --concurrency 300 \
  --cpu-boost \
```

### 建立 staging 的 index
```bash
gcloud firestore indexes composite create \
  --collection-group=botrun-hatch-hatch \
  --field-config=field-path=user_id,order=ascending \
  --field-config=field-path=name,order=ascending \
  --field-config=field-path=__name__,order=ascending \
  --project=scoop-386004
```

### 打包 Cloud Run, staging 的版本
```bash
gcloud builds submit --config cloudbuild_fastapi.yaml --project=scoop-386004
```

### 佈署 cloud run, staging 的版本
```bash
gcloud run deploy botrun-flow-lang-fastapi \
  --image asia-east1-docker.pkg.dev/scoop-386004/botrun-flow-lang/botrun-flow-lang-fastapi \
  --port 8080 \
  --platform managed \
  --allow-unauthenticated \
  --project=scoop-386004 \
  --region=asia-east1 \
  --cpu 2 \
  --memory 8Gi \
  --min-instances 0 \
  --max-instances 5 \
  --timeout 3600s \
  --concurrency 300 \
  --cpu-boost \
```

## 為了要減少冷啟動的時間，每十分鐘呼叫一次 heartbeat
```bash
gcloud scheduler jobs create http botrun-flow-lang-heartbeat-job-$ENV \
  --schedule "*/10 * * * *" \
  --time-zone "Asia/Taipei" \
  --uri "https://botrun-flow-lang-fastapi-$ENV-36186877499.asia-east1.run.app/heartbeat" \
  --http-method GET \
  --location "asia-east1" \
  --project "scoop-386004"
```
測試 scheduler
```bash
gcloud scheduler jobs run botrun-flow-lang-heartbeat-job-$ENV --location "asia-east1" --project "scoop-386004"
```
