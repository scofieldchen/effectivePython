"""
整合flask和bokeh，实现数据可视化。
"""
import numpy as np
import pandas as pd
import datetime as dt

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import gridplot

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap


BALTYPES = [
    ("total", "总余额"),
    ("free", "可用余额"),
    ("used", "冻结余额")
]
FREQS = [
    ("5T", "5分钟"),
    ("15T", "15分钟"),
    ("30T", "30分钟"),
    ("H", "1小时"),
    ("4H", "4小时"),
    ("D", "1天")
]


app = Flask(__name__)
app.config["SECRET_KEY"] = "you will never guess"
bootstrap = Bootstrap(app)


class MyForm(FlaskForm):
    coin = StringField("币种", validators=[DataRequired()])
    baltype = SelectField("余额类型", validators=[DataRequired()],
                          choices=BALTYPES)
    freq = SelectField("频率", validators=[DataRequired()],
                       choices=FREQS, default="1天")
    start = DateField("开始日期", validators=[DataRequired()],
                      default=dt.datetime.now() - dt.timedelta(days=10),
                      format="%Y-%m-%d")
    end = DateField("结束日期", validators=[DataRequired()],
                    default=dt.datetime.now(),
                    format="%Y-%m-%d")
    submit = SubmitField("提交")


def load_data(filename, coin, start, end, baltype="total", freq="D"):
    """加载数据

    Args:
        filename(str): 存储数据的csv文件
        coin(str): 币种，如'BTC','USDT'
        start(str): 开始日期
        end(str): 结束日期
        baltype(str): 余额类型，'total','free','used'
        freq(str): 频率，默认为天
    
    Returns:
        pd.DataFrame
    """
    df = pd.read_csv(filename, index_col="datetime", parse_dates=True)
    bal = df.loc[df["coin"] == coin.upper(), baltype.lower()]
    bal = bal.asfreq(freq, method="ffill")
    bal_chg = bal.diff()
    bal_df = pd.concat({"value": bal, "change": bal_chg}, axis=1)
    bal_df.fillna(0, inplace=True)
    return bal_df[start:end]


def cal_width(data):
    """自动计算柱状图宽度，当x轴是datetime类型，最小
    单位是毫秒"""
    mindate, maxdate = data.index[0], data.index[-1]
    milliseconds = (maxdate - mindate).total_seconds() * 1000
    if milliseconds == 0:
        milliseconds = 86400000
    return 0.8 * milliseconds / len(data.index)


def create_plot(data):
    """创建Figure对象
    
    Args:
        data(df): 时间序列数据，包含'datetime'索引

    Returns:
        bokeh.figure对象
    """
    source = ColumnDataSource(data)

    p1 = figure(title="账户余额", x_axis_type="datetime",
                width=600, height=300)
    p1.line(x="datetime", y="value", source=source, line_width=2)
    
    p2 = figure(title="余额变化", x_axis_type="datetime",
                width=600, height=300, x_range=p1.x_range)
    width = cal_width(data)
    p2.vbar(x="datetime", top="change", source=source, width=width)
    
    grid = gridplot([p1, p2], ncols=1)
    
    return grid


@app.route("/chart", methods=["GET", "POST"])
def chart():
    form = MyForm()
    
    if request.method == "POST":
        df = load_data("data.csv", coin=request.form.get("coin"),
                       start=request.form.get("start"),
                       end=request.form.get("end"),
                       baltype=request.form.get("baltype"),
                       freq=request.form.get("freq"))
        if df is not None and not df.empty:
            p = create_plot(df)
            script, div = components(p)
            return render_template("chart.html", form=form,
                                   script=script, div=div)

    return render_template("chart.html", form=form)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
