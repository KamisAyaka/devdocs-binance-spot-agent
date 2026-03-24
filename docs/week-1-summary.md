# 第 1 周收口总结（2026-03-23 至 2026-03-29）

## 本周目标达成情况

- FastAPI 服务骨架：已完成
- `GET /health`：已完成
- 配置管理与 `.env` 约定：已完成
- 结构化日志、请求追踪、统一异常处理：已完成
- 模型层抽象（`ModelClient` + OpenAI 兼容适配器）：已完成
- 工具层抽象（`ToolClient` + 搜索/抓取适配器）：已完成

## 可演示能力

- API 能力：
  - `GET /health`
  - `GET /config`
- 基础工程能力：
  - request id 与耗时响应头
  - 统一错误码和错误响应结构
- 抽象层能力：
  - 模型适配器：`openai-compatible`
  - 工具适配器：`web_search`、`web_fetch`

## 关键产物

- 配置与基础设施：
  - `app/core/config.py`
  - `app/core/logging.py`
  - `app/core/middleware.py`
  - `app/core/exceptions.py`
- 模型层：
  - `app/models/base.py`
  - `app/models/types.py`
  - `app/models/openai_compatible.py`
  - `app/models/factory.py`
- 工具层：
  - `app/tools/base.py`
  - `app/tools/types.py`
  - `app/tools/web_search.py`
  - `app/tools/web_fetch.py`
  - `app/tools/factory.py`
- 测试：
  - `tests/test_health.py`
  - `tests/test_config.py`
  - `tests/test_errors_and_middleware.py`
  - `tests/test_model_factory.py`
  - `tests/test_openai_compatible_client.py`
  - `tests/test_tool_factory.py`
  - `tests/test_web_search_tool.py`
  - `tests/test_web_fetch_tool.py`

## 技术债与待办

- 配置严格模式未启用：
  - 关键配置缺失时目前仍可由默认值兜底
  - 进入联调前需改为启动即失败

- Web Search 结果解析仍偏保守：
  - 当前以 DuckDuckGo 返回结构为主
  - 后续可增加 provider 抽象和结果归一化策略

- Web Fetch 文本清洗策略为轻量版：
  - 当前用正则去标签
  - 后续可增加正文抽取策略（正文识别、去导航/页脚）

- 模型调用与工具调用尚未挂到 `/chat` 主链路：
  - 这是第 2 周 RAG 链路与 Workflow 的主要接入点

## 下周进入点（Week 2）

1. 完成文档入库（parse/chunk/embed/store）
2. 完成向量检索与引用拼装
3. 在 `/chat` 中接入检索与工具路由
4. 增加基础评测样本和回归脚本
