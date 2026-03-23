# 技术方案草稿

## 1. 项目定位

项目名称：`DevDocs Binance Spot Agent`

目标是构建一个围绕 Binance Spot API 文档的开发者智能助手，提供：

- 文档问答
- API 使用解释
- 检索增强回答
- 网页搜索补充
- 带引用的响应
- 基础执行轨迹和日志

## 2. MVP 范围

第一阶段只做最小可演示版本，范围限定为：

- 一个 FastAPI 后端服务
- 一个 `/chat` 接口
- 一个 `/ingest` 接口
- 一个 `/health` 接口
- 一套文档切块与向量检索能力
- 两个工具：网页搜索、网页抓取
- 一条基础工作流：问题路由 -> 检索/搜索 -> 生成 -> 引用整理 -> 返回

不在第一阶段做：

- 复杂前端
- 长期记忆
- 多知识库租户
- 复杂权限系统
- 在线增量训练

## 3. 技术选型

### 后端框架

- FastAPI

原因：

- 上手快
- 类型提示友好
- 适合快速定义接口和依赖注入

### Agent 编排

- LangGraph

原因：

- 比单纯链式调用更适合表达路由、分支、重试和回退
- 更贴合后续面试里的 Workflow 表达

### 模型接入

- OpenAI 兼容接口

原因：

- 方便切换不同模型供应商
- 可以先做统一适配层，再逐步替换底层实现

### 检索

- Chroma 或 FAISS

建议：

- 本地开发优先 Chroma，简单直观
- 如果只追求轻量依赖，也可以先用 FAISS

### 数据存储

- SQLite

原因：

- 第一阶段只需要轻量持久化
- 减少部署复杂度

## 4. 系统分层

```text
API Layer
  -> Service Layer
    -> Agent Workflow
      -> Retrieval / Tools / Model Adapter
        -> Storage / External APIs
```

各层职责：

- API Layer：参数校验、鉴权预留、响应封装
- Service Layer：业务编排和调用聚合
- Agent Workflow：路由、状态流转、失败回退
- Retrieval / Tools / Model Adapter：核心能力模块
- Storage / External APIs：数据库、向量库、搜索服务、网页抓取

## 5. 核心流程

### 5.1 Chat 流程

```text
User Question
  -> Router
  -> Retrieve Docs or Search Web
  -> Build Context
  -> Generate Answer
  -> Attach Citations
  -> Return Response
```

### 5.2 Ingest 流程

```text
Source Docs
  -> Parse
  -> Chunk
  -> Embed
  -> Store Vector + Metadata
```

## 6. 推荐目录设计

```text
app/
  api/         # 路由层
  core/        # 配置、日志、异常、中间件
  services/    # 业务编排
  agents/      # LangGraph 状态与节点
  tools/       # 搜索、抓取等工具
  retrieval/   # 切块、embedding、向量检索、citation
  schemas/     # 请求/响应结构
  models/      # 模型调用抽象
  db/          # 数据访问与持久化
```

## 7. 关键数据结构建议

### ChatRequest

- `question`
- `session_id`
- `top_k`
- `use_web_search`

### ChatResponse

- `answer`
- `citations`
- `steps`
- `latency_ms`
- `request_id`

### Citation

- `source_type`
- `title`
- `url`
- `snippet`
- `score`

## 8. 第一版接口设计

### `GET /health`

用途：

- 健康检查

### `POST /chat`

用途：

- 用户提问，返回回答、引用和执行摘要

### `POST /ingest`

用途：

- 导入指定文档源并完成入库

### `GET /config`

用途：

- 开发阶段查看当前运行配置的部分摘要
- 仅用于开发排查，禁止返回密钥等敏感信息

## 8.1 配置严格模式提醒

- 当前配置层保留了默认值，目标是降低早期开发阻力
- 在进入测试环境联调前，需要改为严格模式
- 严格模式要求：关键字段（如模型 API Key、模型 Base URL、数据库连接）缺失时，应用启动直接报错退出
- 错误信息必须包含缺失字段名，避免运行期才暴露问题

## 9. 非功能性要求

- 所有请求带 request id
- 接口有基础超时控制
- 工具调用记录耗时和状态
- 日志结构统一
- 回答尽量返回引用，避免无来源断言

## 10. 风险点

- 文档质量不稳定会直接影响回答质量
- 网页搜索结果波动大，可能影响可复现性
- 如果工作流过早复杂化，会拖慢 MVP 交付

## 11. 当前技术决策

- 先做单体服务，不拆微服务
- 先做同步主链路，必要时再局部异步化
- 先做会话级短期记忆，不做长期记忆
- 先保证引用可追溯，再追求复杂推理能力

## 12. 下一步落地顺序

1. 补 `pyproject.toml` 和基础依赖
2. 创建 `app/main.py`
3. 建立 `core/config.py`、`core/logging.py`、`core/exceptions.py`
4. 增加 `api/routes/health.py` 与 `api/routes/chat.py`
5. 定义模型层与工具层接口
6. 再进入文档入库和检索链路
