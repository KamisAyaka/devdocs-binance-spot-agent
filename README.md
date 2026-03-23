# DevDocs Binance Spot Agent

面向开发者文档场景的 Agent 项目初始化仓库，当前阶段聚焦于：

- 搭建可持续迭代的后端目录结构
- 明确第一周的开发任务拆解
- 沉淀第一版技术方案草稿

项目目标是逐步实现一个针对 Binance Spot API 文档的智能助手，支持文档问答、网页检索、工具调用、引用返回和基础执行轨迹展示。

## 当前仓库内容

- `app/`: 后端应用主目录
- `docs/`: 项目文档，包括任务拆解与技术方案
- `scripts/`: 后续放置本地脚本、数据处理脚本
- `tests/`: 测试目录
- `learning-plan.md`: 一个月学习与交付计划

## 推荐目录结构

```text
.
├── README.md
├── learning-plan.md
├── app
│   ├── agents
│   ├── api
│   ├── core
│   ├── db
│   ├── models
│   ├── retrieval
│   ├── schemas
│   ├── services
│   └── tools
├── docs
│   ├── tech-design-draft.md
│   └── week-1-breakdown.md
├── scripts
└── tests
```

## 模块职责

- `app/api`: FastAPI 路由层，对外暴露 `health`、`chat`、`ingest` 等接口
- `app/core`: 配置、日志、异常、中间件等基础设施
- `app/services`: 业务编排层，承接接口与 Agent/检索模块
- `app/agents`: LangGraph 或 Agent 工作流节点与状态定义
- `app/tools`: 网页搜索、网页抓取等工具封装
- `app/retrieval`: 文档切块、向量检索、引用拼装
- `app/schemas`: 请求响应 Schema
- `app/models`: 模型调用抽象层
- `app/db`: SQLite/PostgreSQL 适配及数据访问
- `tests`: 单测、集成测试、评测脚本

## 当前阶段交付物

- 项目目录结构初始化
- [第一周任务拆解](/Users/firefly/Desktop/learnagent/devdocs-binance-spot-agent/docs/week-1-breakdown.md)
- [技术方案草稿](/Users/firefly/Desktop/learnagent/devdocs-binance-spot-agent/docs/tech-design-draft.md)
- [Day 1 完成清单](/Users/firefly/Desktop/learnagent/devdocs-binance-spot-agent/docs/day-1-checklist.md)

## 第一周目标

- 完成 FastAPI 应用骨架
- 跑通配置加载、日志和异常处理
- 抽象模型调用层
- 接入 2 个基础工具：网页搜索、网页抓取

## 后续建议开发顺序

1. 先补 `pyproject.toml`、`main.py`、配置模块和健康检查接口
2. 再补模型层和工具层的抽象接口
3. 第 2 周再接入文档入库、切块和检索链路

## 依赖管理

项目使用 [pyproject.toml](/Users/firefly/Desktop/learnagent/devdocs-binance-spot-agent/pyproject.toml) 作为 Python 项目的统一配置入口，负责：

- 项目元信息
- 运行时依赖
- 开发依赖
- `pytest` 与 `ruff` 等工具配置

后续可使用支持 `pyproject.toml` 的工具进行依赖安装和开发环境管理。

## 本地启动

先准备环境变量文件：

```bash
cp .env.example .env
```

安装依赖后，可通过 `uvicorn` 启动当前最小服务：

```bash
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

启动后可访问：

- `GET /health`
- `GET /config`
- `GET /docs`

Day 4 起已接入请求追踪和统一错误处理：

- 响应头包含 `X-Request-ID` 与 `X-Process-Time-MS`
- 异常响应统一为 `{"success": false, "error": {...}}` 结构

Day 5 已完成模型层抽象：

- 统一模型输入输出结构：`ChatMessage`、`ModelRequest`、`ModelResponse`
- 抽象接口：`ModelClient`
- 预留 OpenAI 兼容适配器：`OpenAICompatibleModelClient`

## 环境变量约定

项目统一使用 `DEVDOCS_` 前缀管理环境变量，配置入口位于：

- [config.py](/Users/firefly/Desktop/learnagent/devdocs-binance-spot-agent/app/core/config.py)
- [.env.example](/Users/firefly/Desktop/learnagent/devdocs-binance-spot-agent/.env.example)

当前已纳入配置管理的字段包括：

- 运行环境：`DEVDOCS_APP_ENV`、`DEVDOCS_DEBUG`、`DEVDOCS_LOG_LEVEL`
- 模型相关：`DEVDOCS_MODEL_PROVIDER`、`DEVDOCS_MODEL_NAME`、`DEVDOCS_MODEL_BASE_URL`
- 存储相关：`DEVDOCS_DATABASE_URL`
- 功能开关：`DEVDOCS_ENABLE_WEB_SEARCH`

## 参考文档

- [第一周任务拆解](/Users/firefly/Desktop/learnagent/devdocs-binance-spot-agent/docs/week-1-breakdown.md)
- [技术方案草稿](/Users/firefly/Desktop/learnagent/devdocs-binance-spot-agent/docs/tech-design-draft.md)
- [学习计划](/Users/firefly/Desktop/learnagent/devdocs-binance-spot-agent/learning-plan.md)
