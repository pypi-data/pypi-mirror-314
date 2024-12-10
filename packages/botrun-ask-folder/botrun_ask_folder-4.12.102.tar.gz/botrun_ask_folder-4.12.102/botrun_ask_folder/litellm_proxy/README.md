# Proxy Server
- config.yaml 裡要有的 model，才能使用
## 安裝
- 需要安裝 litellm[proxy]

## 執行 server
目前改成 docker 方式，所以這一行可能無法執行了，但是還是留著參考
```shell
litellm --config botrun_ask_folder/litellm_proxy/config/config.yaml
```

## 執行 server docker
```shell
docker-compose up -d
```
## test
```shell
curl -X POST 'http://0.0.0.0:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer api-key' \
-d '{
    "model": "botrun/botrun-波創價學會",
    "messages": [{"role": "user", "content": "創價學會的宗指為何？"}],
}'
curl -X POST 'http://0.0.0.0:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer api-key' \
-H "Accept: text/event-stream" \
-d '{
    "model": "botrun/botrun-波創價學會",
    "messages": [{"role": "user", "content": "創價學會的宗指為何？"}],
    "stream":true
}'
curl -X POST 'http://0.0.0.0:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer api-key' \
-d '{
    "model": "botrun/taide-botrun-4.11-70b",
    "messages": [{"role": "user", "content": "講一個小紅帽的故事"}],
}'
curl -X POST 'http://0.0.0.0:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer api-key' \
-H "Accept: text/event-stream" \
-d '{
    "model": "botrun/taide-botrun-t-4.11-405b",
    "messages": [{"role": "user", "content": "講一個小紅帽的故事"}],
    "stream":true
}'
```
這個是沒有 import_rag_plus 的
```shell
curl -X POST 'http://dev.botrun.ai:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer api-key' \
-d '{
    "model": "botrun/botrun-波分段",
    "messages": [{"role": "user", "content": "你好，請介紹一下你自己"}],
}'
curl -X POST 'http://dev.botrun.ai:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer api-key' \
-H "Accept: text/event-stream" \
-d '{
    "model": "botrun/botrun-波分段",
    "messages": [{"role": "user", "content": "你好，請介紹一下你自己"}],
    "stream":true
}'

```

## 生 key
給所有的 model
```shell
curl --location 'http://dev.botrun.ai:4000/key/generate' \
--header 'Authorization: Bearer bo-1cda98a6-4f5f-46c5-ab5f-6ff62b9aec00' \
--header 'Content-Type: application/json' \
--data '{
    "metadata": {"user": "seba"}
}'
```
給特殊的 model
```shell
curl --location 'http://dev.botrun.ai:4000/key/generate' \
--header 'Authorization: Bearer bo-1cda98a6-4f5f-46c5-ab5f-6ff62b9aec00' \
--header 'Content-Type: application/json' \
--data '{
      "models": ["botrun/botrun-波創價學會"],
     "metadata": {"user": "seba波"}
}'
```
