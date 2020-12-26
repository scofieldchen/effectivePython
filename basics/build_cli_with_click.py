# 如何用click创建命令行界面？

import click
from click.types import DateTime


# 入门
# 1. 调用@click_command()装饰一个函数，将函数变为'Command'对象
# 2. 调用@click.option()或者@click.argument()装饰函数，添加命令行参数
#     option -> 关键词参数，可选，argument -> 缩减版option，类似位置参数
# 3. 调用被装饰的函数
# @click.command()
# @click.option("-c", "--count", default=3, help="打印次数")
# @click.argument("name")
# def main(count, name):
#     """将名字打印到控制台"""
#     for i in range(count):
#         click.echo(f"hello {name}")
#         # click.echo(click.style(f"hello {name}", fg="red", bold=True))


# 如何校验参数？
# click提供很多参数类型，部分可直接用于参数检验，包括类型和取值范围，非常方便
@click.command()
@click.option("--choice", type=click.Choice(["a", "b", "c"], case_sensitive=False))
@click.option("--datetime", type=click.DateTime(formats=["%Y-%m-%d", "%Y-%m-%d %H:%M:%S"]))
@click.option("--intrng", type=click.IntRange(min=1, max=100))
@click.option("--interval", nargs=2, type=float, default=(0, 0))
def main(choice, datetime, intrng, interval):
    click.echo(choice)
    click.echo(datetime)
    click.echo(type(datetime))
    click.echo(intrng)
    click.echo(interval)


if __name__ == "__main__":
    main()
