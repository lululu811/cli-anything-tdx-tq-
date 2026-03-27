#!/usr/bin/env python
"""
TDX TQ SDK CLI - 通达信量化接口命令行工具

Usage:
    cli-anything-tdx-tq [OPTIONS] COMMAND [ARGS]...

Commands:
    init            初始化连接
    close           关闭连接
    market          行情数据相关命令
    stock           股票信息相关命令
    sector          板块数据相关命令
    financial       财务数据相关命令
    formula         公式调用相关命令
    subscribe       订阅相关命令
    trading         交易相关命令
    export          导出数据
    config          配置管理
    status          查看状态
"""

import sys
import os
import json
import click
from typing import Optional, List
from pathlib import Path

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))

from .core.session import session
from .core.config import config
from .core.export import export_dataframe, export_dict
from .utils.output import format_output


@click.group()
@click.version_option(version='1.0.0', prog_name='cli-anything-tdx-tq')
@click.option('--tdx-path', envvar='TDX_PATH', help='通达信安装路径')
@click.pass_context
def cli(ctx, tdx_path: Optional[str]):
    """
    TDX TQ SDK CLI - 通达信量化接口命令行工具

    基于 TQ 策略模式，提供完整的命令行接口。

    前置条件:
    1. 通达信客户端已启动并登录
    2. 通达信安装在 D:\\new_tdx64 或通过 --tdx-path 指定
    """
    ctx.ensure_object(dict)
    if tdx_path:
        config.tdx_path = tdx_path
    ctx.obj['config'] = config


@cli.command()
@click.pass_context
def init(ctx):
    """初始化连接"""
    try:
        session.initialize()
        click.echo(click.style("连接已建立", fg='green'))
    except Exception as e:
        click.echo(click.style(f"初始化失败：{e}", fg='red'), err=True)
        ctx.exit(1)


@cli.command()
@click.pass_context
def close(ctx):
    """关闭连接"""
    try:
        session.close()
        click.echo(click.style("连接已关闭", fg='green'))
    except Exception as e:
        click.echo(click.style(f"关闭失败：{e}", fg='red'), err=True)
        ctx.exit(1)


# ==================== 行情数据命令组 ====================

@cli.group()
def market():
    """行情数据相关命令"""
    pass


@market.command('get')
@click.option('--stocks', '-s', required=True, help='股票代码列表，逗号分隔')
@click.option('--period', '-p', default='1d', help='周期 (tick,1m,5m,1d,1w,1mon)')
@click.option('--count', '-c', default=60, type=int, help='获取数量')
@click.option('--dividend', '-d', type=click.Choice(['none', 'front', 'back']), default='front', help='复权类型')
@click.option('--output', '-o', help='输出文件路径')
@click.option('--json', 'as_json', is_flag=True, help='以 JSON 格式输出')
@click.pass_context
def market_get(ctx, stocks: str, period: str, count: int, dividend: str, output: Optional[str], as_json: bool):
    """获取 K 线数据"""
    try:
        session.ensure_initialized()
        stock_list = [s.strip() for s in stocks.split(',')]
        data = session.tdx.get_market_data(
            stock_list=stock_list,
            period=period,
            count=count,
            dividend_type=dividend
        )

        if output:
            export_dict(data, output, format='csv')
            click.echo(click.style(f"数据已导出到 {output}", fg='green'))
        else:
            if as_json:
                result = {}
                for key, df in data.items():
                    result[key] = df.to_dict('records')
                click.echo(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                for key, df in data.items():
                    click.echo(f"\n=== {key} ===")
                    click.echo(df.to_string())
    except Exception as e:
        click.echo(click.style(f"获取数据失败：{e}", fg='red'), err=True)
        ctx.exit(1)


@market.command('snapshot')
@click.option('--stock', '-s', required=True, help='股票代码')
@click.option('--json', 'as_json', is_flag=True, help='以 JSON 格式输出')
@click.pass_context
def market_snapshot(ctx, stock: str, as_json: bool):
    """获取实时行情快照"""
    try:
        session.ensure_initialized()
        snapshot = session.tdx.get_market_snapshot(stock)

        if as_json:
            click.echo(json.dumps(snapshot, ensure_ascii=False, indent=2))
        else:
            for k, v in snapshot.items():
                click.echo(f"{k}: {v}")
    except Exception as e:
        click.echo(click.style(f"获取行情失败：{e}", fg='red'), err=True)
        ctx.exit(1)


@market.command('divid')
@click.option('--stock', '-s', required=True, help='股票代码')
@click.option('--start', help='开始时间 (YYYYMMDD)')
@click.option('--end', help='结束时间 (YYYYMMDD)')
@click.option('--json', 'as_json', is_flag=True, help='以 JSON 格式输出')
@click.pass_context
def market_divid(ctx, stock: str, start: str, end: str, as_json: bool):
    """获取除权除息数据"""
    try:
        session.ensure_initialized()
        data = session.tdx.get_divid_factors(
            stock_code=stock,
            start_time=start or '',
            end_time=end or ''
        )

        if as_json:
            click.echo(json.dumps(data.to_dict('records'), ensure_ascii=False, indent=2))
        else:
            click.echo(data.to_string())
    except Exception as e:
        click.echo(click.style(f"获取数据失败：{e}", fg='red'), err=True)
        ctx.exit(1)


# ==================== 股票信息命令组 ====================

@cli.group()
def stock():
    """股票信息相关命令"""
    pass


@stock.command('info')
@click.option('--stock', '-s', required=True, help='股票代码')
@click.option('--json', 'as_json', is_flag=True, help='以 JSON 格式输出')
@click.pass_context
def stock_info(ctx, stock: str, as_json: bool):
    """获取股票基础信息"""
    try:
        session.ensure_initialized()
        info = session.tdx.get_stock_info(stock)

        if as_json:
            click.echo(json.dumps(info, ensure_ascii=False, indent=2))
        else:
            for k, v in info.items():
                click.echo(f"{k}: {v}")
    except Exception as e:
        click.echo(click.style(f"获取信息失败：{e}", fg='red'), err=True)
        ctx.exit(1)


@stock.command('more')
@click.option('--stock', '-s', required=True, help='股票代码')
@click.option('--fields', '-f', help='指定字段，逗号分隔')
@click.option('--json', 'as_json', is_flag=True, help='以 JSON 格式输出')
@click.pass_context
def stock_more(ctx, stock: str, fields: Optional[str], as_json: bool):
    """获取股票更多信息（52 周高低点、涨跌幅等）"""
    try:
        session.ensure_initialized()
        field_list = [f.strip() for f in fields.split(',')] if fields else None
        info = session.tdx.get_more_info(stock, field_list=field_list or [])

        if as_json:
            click.echo(json.dumps(info, ensure_ascii=False, indent=2))
        else:
            for k, v in info.items():
                click.echo(f"{k}: {v}")
    except Exception as e:
        click.echo(click.style(f"获取信息失败：{e}", fg='red'), err=True)
        ctx.exit(1)


# ==================== 板块数据命令组 ====================

@cli.group()
def sector():
    """板块数据相关命令"""
    pass


@sector.command('list')
@click.option('--type', '-t', 'list_type', type=click.Choice(['0', '1', '2']), default='0',
             help='板块类型 (0=行业，1=概念，2=风格)')
@click.option('--json', 'as_json', is_flag=True, help='以 JSON 格式输出')
@click.pass_context
def sector_list(ctx, list_type: str, as_json: bool):
    """获取板块列表"""
    try:
        session.ensure_initialized()
        sectors = session.tdx.get_sector_list(list_type=int(list_type))

        if as_json:
            click.echo(json.dumps(sectors, ensure_ascii=False, indent=2))
        else:
            for i, sector in enumerate(sectors, 1):
                click.echo(f"{i}. {sector}")
    except Exception as e:
        click.echo(click.style(f"获取板块失败：{e}", fg='red'), err=True)
        ctx.exit(1)


@sector.command('stocks')
@click.option('--sector', '-s', required=True, help='板块名称')
@click.option('--json', 'as_json', is_flag=True, help='以 JSON 格式输出')
@click.pass_context
def sector_stocks(ctx, sector: str, as_json: bool):
    """获取板块成分股"""
    try:
        session.ensure_initialized()
        stocks = session.tdx.get_stock_list_in_sector(sector)

        if as_json:
            click.echo(json.dumps(stocks, ensure_ascii=False, indent=2))
        else:
            click.echo(f"板块：{sector}")
            click.echo(f"成分股数量：{len(stocks)}")
            for i, stock in enumerate(stocks, 1):
                click.echo(f"{i}. {stock}")
    except Exception as e:
        click.echo(click.style(f"获取成分股失败：{e}", fg='red'), err=True)
        ctx.exit(1)


# ==================== 财务数据命令组 ====================

@cli.group()
def financial():
    """财务数据相关命令"""
    pass


@financial.command('get')
@click.option('--stocks', '-s', required=True, help='股票代码列表，逗号分隔')
@click.option('--fields', '-f', required=True, help='字段列表，逗号分隔 (如 FN1,FN4,FN6)')
@click.option('--start', help='开始时间 (YYYYMMDD)')
@click.option('--end', help='结束时间 (YYYYMMDD)')
@click.option('--json', 'as_json', is_flag=True, help='以 JSON 格式输出')
@click.pass_context
def financial_get(ctx, stocks: str, fields: str, start: Optional[str], end: Optional[str], as_json: bool):
    """获取专业财务数据"""
    try:
        session.ensure_initialized()
        stock_list = [s.strip() for s in stocks.split(',')]
        field_list = [f.strip() for f in fields.split(',')]

        data = session.tdx.get_financial_data(
            stock_list=stock_list,
            field_list=field_list,
            start_time=start or '',
            end_time=end or ''
        )

        if as_json:
            result = {}
            for code, df in data.items():
                result[code] = df.to_dict('records')
            click.echo(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for code, df in data.items():
                click.echo(f"\n=== {code} ===")
                click.echo(df.to_string())
    except Exception as e:
        click.echo(click.style(f"获取数据失败：{e}", fg='red'), err=True)
        ctx.exit(1)


# ==================== 公式调用命令组 ====================

@cli.group()
def formula():
    """公式调用相关命令"""
    pass


@formula.command('zb')
@click.option('--name', '-n', required=True, help='指标公式名称')
@click.option('--args', '-a', default='', help='公式参数，逗号分隔')
@click.option('--stock', '-s', help='股票代码')
@click.option('--json', 'as_json', is_flag=True, help='以 JSON 格式输出')
@click.pass_context
def formula_zb(ctx, name: str, args: str, stock: Optional[str], as_json: bool):
    """调用通达信指标公式"""
    try:
        session.ensure_initialized()
        result = session.tdx.formula_zb(
            formula_name=name,
            formula_arg=args
        )

        if as_json:
            click.echo(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for k, v in result.items():
                click.echo(f"{k}: {v}")
    except Exception as e:
        click.echo(click.style(f"调用公式失败：{e}", fg='red'), err=True)
        ctx.exit(1)


@formula.command('xg')
@click.option('--name', '-n', required=True, help='选股公式名称')
@click.option('--args', '-a', default='', help='公式参数，逗号分隔')
@click.option('--stocks', '-s', help='股票列表，逗号分隔')
@click.option('--json', 'as_json', is_flag=True, help='以 JSON 格式输出')
@click.pass_context
def formula_xg(ctx, name: str, args: str, stocks: Optional[str], as_json: bool):
    """调用通达信选股公式"""
    try:
        session.ensure_initialized()
        stock_list = [s.strip() for s in stocks.split(',')] if stocks else []
        result = session.tdx.formula_xg(
            formula_name=name,
            formula_arg=args
        )

        if as_json:
            click.echo(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for k, v in result.items():
                click.echo(f"{k}: {v}")
    except Exception as e:
        click.echo(click.style(f"调用公式失败：{e}", fg='red'), err=True)
        ctx.exit(1)


# ==================== 配置命令组 ====================

@cli.group()
def config_cmd():
    """配置管理"""
    pass


@config_cmd.command('show')
@click.pass_context
def config_show(ctx):
    """显示当前配置"""
    cfg = ctx.obj.get('config', config)
    status = cfg.get_status()

    for k, v in status.items():
        icon = "✓" if v else "✗" if k.endswith('_exists') else ""
        click.echo(f"{k}: {v} {icon}")


@config_cmd.command('set')
@click.option('--tdx-path', help='通达信安装路径')
@click.pass_context
def config_set(ctx, tdx_path: Optional[str]):
    """设置配置"""
    if tdx_path:
        config.tdx_path = tdx_path
        click.echo(click.style(f"通达信路径已设置为：{tdx_path}", fg='green'))


# ==================== 状态命令 ====================

@cli.command()
@click.option('--json', 'as_json', is_flag=True, help='以 JSON 格式输出')
@click.pass_context
def status(ctx, as_json: bool):
    """查看当前状态"""
    result = {
        'session_initialized': session.is_initialized,
        'config': config.get_status()
    }

    if as_json:
        click.echo(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        click.echo("=== TDX TQ SDK Status ===")
        click.echo(f"Session initialized: {session.is_initialized}")
        click.echo(f"\nConfig:")
        for k, v in config.get_status().items():
            icon = "[OK]" if v else "[X]" if k.endswith('_exists') else ""
            click.echo(f"  {k}: {v} {icon}")


def main():
    """CLI 入口点"""
    cli(obj={})


if __name__ == '__main__':
    main()
