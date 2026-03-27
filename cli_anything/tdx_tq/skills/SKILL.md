---
name: tdx-tq-sdk
description: 通达信 TQ SDK CLI - 通达信量化接口命令行工具
version: 1.0.0
---

# TDX TQ SDK CLI Skill

通达信量化接口命令行工具，基于 TQ 策略模式，提供完整的股票数据获取和分析功能。

## 前置条件

1. **通达信客户端**：必须已启动并登录
2. **通达信安装**：默认路径 `D:\new_tdx64`
3. **Python 环境**：Python 3.8+

## 安装

```bash
cd D:/TDX-SKILL/tdx-tq-sdk/cli_agent
pip install -e .
```

## 命令组

### market - 行情数据

获取股票 K 线数据、实时行情、除权除息数据等。

#### market get - 获取 K 线数据

```bash
cli-anything-tdx-tq market get -s <股票代码> [选项]
```

**参数：**
- `-s, --stocks`: 股票代码列表，逗号分隔（必填）
- `-p, --period`: 周期，可选 tick/1m/5m/1d/1w/1mon（默认：1d）
- `-c, --count`: 获取数量（默认：60）
- `-d, --dividend`: 复权类型，可选 none/front/back（默认：front）
- `-o, --output`: 输出文件路径
- `--json`: 以 JSON 格式输出

**示例：**
```bash
# 获取亨通光电 60 条日线数据
cli-anything-tdx-tq market get -s 600487.SH -c 60

# 获取前复权数据
cli-anything-tdx-tq market get -s 600487.SH -d front

# 获取多只股票数据
cli-anything-tdx-tq market get -s 600487.SH,000001.SZ,600519.SH

# 输出 JSON 格式
cli-anything-tdx-tq market get -s 600487.SH --json
```

#### market snapshot - 获取实时行情快照

```bash
cli-anything-tdx-tq market snapshot -s <股票代码> [选项]
```

**参数：**
- `-s, --stock`: 股票代码（必填）
- `--json`: 以 JSON 格式输出

**示例：**
```bash
cli-anything-tdx-tq market snapshot -s 600487.SH
cli-anything-tdx-tq market snapshot -s 600487.SH --json
```

#### market divid - 获取除权除息数据

```bash
cli-anything-tdx-tq market divid -s <股票代码> [选项]
```

**参数：**
- `-s, --stock`: 股票代码（必填）
- `--start`: 开始时间 YYYYMMDD
- `--end`: 结束时间 YYYYMMDD
- `--json`: 以 JSON 格式输出

**示例：**
```bash
cli-anything-tdx-tq market divid -s 600487.SH
cli-anything-tdx-tq market divid -s 600487.SH --start 20230101 --end 20241231
```

### stock - 股票信息

获取股票基础信息、更多信息等。

#### stock info - 获取股票基础信息

```bash
cli-anything-tdx-tq stock info -s <股票代码> [选项]
```

**参数：**
- `-s, --stock`: 股票代码（必填）
- `--json`: 以 JSON 格式输出

**示例：**
```bash
cli-anything-tdx-tq stock info -s 600487.SH
cli-anything-tdx-tq stock info -s 600487.SH --json
```

#### stock more - 获取股票更多信息

```bash
cli-anything-tdx-tq stock more -s <股票代码> [选项]
```

**参数：**
- `-s, --stock`: 股票代码（必填）
- `-f, --fields`: 指定字段，逗号分隔
- `--json`: 以 JSON 格式输出

**示例：**
```bash
cli-anything-tdx-tq stock more -s 600487.SH
cli-anything-tdx-tq stock more -s 600487.SH -f HisHigh,HisLow,ZTPrice
```

### sector - 板块数据

获取板块列表、板块成分股等。

#### sector list - 获取板块列表

```bash
cli-anything-tdx-tq sector list [选项]
```

**参数：**
- `-t, --type`: 板块类型，0=行业/1=概念/2=风格（默认：0）
- `--json`: 以 JSON 格式输出

**示例：**
```bash
# 获取行业板块
cli-anything-tdx-tq sector list

# 获取概念板块
cli-anything-tdx-tq sector list -t 1
```

#### sector stocks - 获取板块成分股

```bash
cli-anything-tdx-tq sector stocks -s <板块名称> [选项]
```

**参数：**
- `-s, --sector`: 板块名称（必填）
- `--json`: 以 JSON 格式输出

**示例：**
```bash
cli-anything-tdx-tq sector stocks -s 半导体
cli-anything-tdx-tq sector stocks -s 人工智能 --json
```

### financial - 财务数据

获取专业财务数据。

#### financial get - 获取专业财务数据

```bash
cli-anything-tdx-tq financial get -s <股票列表> -f <字段列表> [选项]
```

**参数：**
- `-s, --stocks`: 股票代码列表，逗号分隔（必填）
- `-f, --fields`: 字段列表，逗号分隔（必填），如 FN1(EPS),FN4(BPS),FN6(ROE)
- `--start`: 开始时间 YYYYMMDD
- `--end`: 结束时间 YYYYMMDD
- `--json`: 以 JSON 格式输出

**常用字段：**
- FN1: 每股收益 (EPS)
- FN4: 每股净资产 (BPS)
- FN6: 净资产收益率 (ROE)
- FN230: 营业收入
- FN232: 净利润

**示例：**
```bash
cli-anything-tdx-tq financial get -s 600487.SH -f FN1,FN4,FN6
cli-anything-tdx-tq financial get -s 600487.SH -f FN230,FN232 --start 20230101 --end 20241231
```

### formula - 公式调用

调用通达信指标公式、选股公式。

#### formula zb - 调用指标公式

```bash
cli-anything-tdx-tq formula zb -n <公式名> [选项]
```

**参数：**
- `-n, --name`: 指标公式名称（必填）
- `-a, --args`: 公式参数，逗号分隔
- `-s, --stock`: 股票代码
- `--json`: 以 JSON 格式输出

**示例：**
```bash
# 调用 MA 指标
cli-anything-tdx-tq formula zb -n MA -a 5,10,20

# 调用 KDJ 指标
cli-anything-tdx-tq formula zb -n KDJ -a 9,3,3
```

#### formula xg - 调用选股公式

```bash
cli-anything-tdx-tq formula xg -n <公式名> [选项]
```

**参数：**
- `-n, --name`: 选股公式名称（必填）
- `-a, --args`: 公式参数，逗号分隔
- `-s, --stocks`: 股票列表，逗号分隔
- `--json`: 以 JSON 格式输出

**示例：**
```bash
cli-anything-tdx-tq formula xg -n KDJ -a 9,3,3
```

### config - 配置管理

#### config show - 显示当前配置

```bash
cli-anything-tdx-tq config show
```

#### config set - 设置配置

```bash
cli-anything-tdx-tq config set --tdx-path D:\new_tdx64
```

### status - 查看状态

```bash
cli-anything-tdx-tq status [--json]
```

## 全局选项

| 选项 | 说明 |
|------|------|
| `--help` | 显示帮助信息 |
| `--version` | 显示版本号 |
| `--tdx-path` | 通达信安装路径（可通过 TDX_PATH 环境变量设置） |

## 输出格式

### JSON 模式

所有命令都支持 `--json` 选项，输出 JSON 格式数据：

```bash
cli-anything-tdx-tq stock info -s 600487.SH --json
```

输出示例：
```json
{
  "Code": "600487.SH",
  "Name": "亨通光电",
  "Industry": "通信设备",
  "Area": "江苏",
  ...
}
```

## 使用场景

### 场景 1：获取单只股票数据

```bash
# 获取日线数据
cli-anything-tdx-tq market get -s 600487.SH -c 100 --json > data.json
```

### 场景 2：获取板块成分股

```bash
# 获取半导体板块所有股票
cli-anything-tdx-tq sector stocks -s 半导体 --json > semiconductor.json
```

### 场景 3：批量获取财务数据

```bash
# 获取多只股票的 EPS 和 ROE
cli-anything-tdx-tq financial get -s 600487.SH,000001.SZ,600519.SH -f FN1,FN6 --json
```

## 注意事项

1. **前置条件**：必须先启动并登录通达信客户端
2. **股票代码格式**：6 位数字 + 市场后缀，如 `600487.SH`
3. **时间格式**：YYYYMMDD，如 `20240101`
4. **数据周期**：tick, 1m, 5m, 1d, 1w, 1mon 等
5. **复权类型**：none(不复权), front(前复权), back(后复权)

## 故障排除

### 初始化失败

确保通达信客户端已启动并登录，检查路径配置：
```bash
cli-anything-tdx-tq config show
```

### 模块未找到

重新安装：
```bash
cd D:/TDX-SKILL/tdx-tq-sdk/cli_agent
pip install -e .
```
