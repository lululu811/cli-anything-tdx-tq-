# TDX-TQ-SDK CLI Harness

## 软件架构文档 (SOP)

### 软件名称
tdx-tq-sdk

### 软件描述
通达信 TQ 策略版本 Python SDK，提供完善的量化交易数据接口封装。

### 前置条件
1. 通达信客户端已启动并登录
2. 通达信安装在 `D:\new_tdx64`
3. TQ 策略模块位于 `D:\new_tdx64\PYPlugins\sys\tqcenter.py`

### 核心功能域

#### 1. 行情数据域 (Market Data)
- 获取 K 线数据 (get_market_data)
- 获取实时行情快照 (get_market_snapshot)
- 获取除权除息数据 (get_divid_factors)

#### 2. 股票信息域 (Stock Info)
- 获取股票基础信息 (get_stock_info)
- 获取股票更多信息 (get_more_info)
- 获取股本信息 (get_share_info, get_gb_info)

#### 3. 板块数据域 (Sector Data)
- 获取板块列表 (get_sector_list)
- 获取板块成分股 (get_stock_list_in_sector)
- 管理自定义板块 (create_sector, delete_sector, rename_sector, clear_sector)

#### 4. 财务数据域 (Financial Data)
- 获取专业财务数据 (get_financial_data)
- 获取股票交易数据 (get_gpjy_value)
- 获取板块交易数据 (get_bkjy_value)
- 获取市场交易数据 (get_scjy_value)

#### 5. 公式调用域 (Formula)
- 调用指标公式 (formula_zb)
- 调用选股公式 (formula_xg)
- 调用专家公式 (formula_exp)
- 批量执行公式 (formula_process_mul, formula_process_mul_xg, formula_process_mul_zb)

#### 6. 订阅服务域 (Subscription)
- 订阅行情数据 (subscribe_quote, subscribe_hq)
- 取消订阅 (unsubscribe_hq)
- 获取订阅列表 (get_subscribe_hq_stock_list)

#### 7. 交易管理域 (Trading)
- 下单 (order_stock)
- 发送消息/文件/预警 (send_message, send_file, send_warn)

### 数据模型

#### 输入参数
- 股票代码：格式 `600487.SH`, `000001.SZ`
- 时间格式：`YYYYMMDD` 或 `YYYYMMDDHHMMSS`
- 周期类型：`tick`, `1m`, `5m`, `1d`, `1w`, `1mon` 等
- 复权类型：`none`, `front`, `back`

#### 输出格式
- 市场数据：`Dict[str, pd.DataFrame]` - 以字段名为键的 DataFrame 字典
- 股票信息：`Dict[str, Any]` - 信息字典
- 列表数据：`List[str]` - 股票代码列表

### 异常类型
- `TdxError`: 基础异常
- `TdxInitError`: 初始化错误
- `TdxDataError`: 数据获取错误
- `TdxParamError`: 参数错误

### CLI 设计原则

1. **命令分组**: 按功能域组织命令组
2. **输出模式**: 支持 `--json` 输出供 Agent 消费
3. **状态管理**: 支持会话模式保持连接
4. **错误处理**: 统一的错误输出格式
