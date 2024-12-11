"""Module to Reports in PDF Format"""

import datetime
import logging

import pandas as pd

import o7pdf.pandas_chart as pdc
import o7pdf.pandas_table as pdt
from o7pdf.colors import PdfColors
from o7pdf.template import Template

logger = logging.getLogger(__name__)


# pylint: disable=singleton-comparison


# *************************************************
#
# *************************************************
def record_type_sort(record_type: str) -> int:
    if record_type == "Usage":
        return 1
    if record_type == "Other":
        return 2
    if record_type == "Total":
        return 100
    if record_type == "Tax":
        return 99

    return 10


# *************************************************
#
# *************************************************
def color_delta_bg(diff: float) -> int:
    if diff > 5.0:
        return PdfColors.R600

    if diff < -5.0:
        return PdfColors.G600

    return PdfColors.N0


# *************************************************
#
# *************************************************
def color_delta_fg(diff: float) -> int:
    if diff > 5.0:
        return PdfColors.N0

    if diff > 1.0:
        return PdfColors.R600

    if diff < -5.0:
        return PdfColors.N0

    if diff < -1.0:
        return PdfColors.G600

    return PdfColors.N10


# *************************************************
# https://pyfpdf.github.io/fpdf2/fpdf/
# *************************************************
class ReportAwsCost(Template):
    """Class temaplate to generate PDF Report"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title = "AWS Montly Cost Report"

        self.first_month: str = None
        self.last_month_long: str = None
        self.last_month: str = None
        self.previous_month: str = None
        self.previous_month_long: str = None
        self.months: list[datetime.date] = []

        self.df_usage: pd.DataFrame = None
        self.df_totals: pd.DataFrame = None
        self.df_accounts: pd.DataFrame = None

    # *************************************************
    #
    # *************************************************
    def chart_last_year(
        self, df_totals_last_year: pd.DataFrame, width: float = 80, height: float = 50
    ):
        """Fill Check historic charts"""

        series = [
            pdc.SerieParam(
                name="Usage",
                color=PdfColors.BM500,
                data="Usage",
                type="bar",
                y_axis="left",
                is_stacked=True,
            ),
        ]

        chart = pdc.PandasChart(
            df=df_totals_last_year,
            series=series,
            width=width,
            height=height,
            pdf=self,
            font_size=6,
            title="Last Year Montly Usage (USD)",
        )
        chart_max = df_totals_last_year["Usage"].max() * 1.2
        chart.axis["left"].min = 0
        chart.axis["left"].max = (int(chart_max / 10) + 1) * 10
        chart.param.spacing = 0.40
        chart.param.x_label_step = 3
        chart.generate()

    # *************************************************
    #
    # *************************************************
    def table_last_year(self, df_year_totals: pd.DataFrame):
        """Fill Check historic charts"""

        columns = [pdt.ColumnParam(name="Month", width=10, data="month", align="C", merge=False)]

        for record_type in df_year_totals.columns:
            if record_type == "month":
                continue

            columns.append(
                pdt.ColumnParam(
                    name=record_type,
                    width=12,
                    data=record_type,
                    align="R",
                    merge=False,
                    text_format="{:,.2f}",
                    footer="sum",
                )
            )

        pdt.PandasTable(
            df=df_year_totals.reset_index(), columns=columns, pdf=self, font_size=6
        ).generate()

    # *************************************************
    #
    # *************************************************
    def table_usage_by_dimension(
        self, df_usage: pd.DataFrame, dimension: str, dimension_width: int = 15, months: int = 2
    ):
        """Table of Account Usage"""

        print(f"table_usage_by_dimension dimension={dimension}")

        months = [month.strftime("%Y-%m") for month in self.months[-months:]]
        group_name = f"Last {len(months)} Month"
        # print(months)

        # ------------------------------------------
        # Compile Usage Details for dimension
        # ------------------------------------
        df_pivot = df_usage.pivot_table(
            values=["amount"],
            index=[dimension],
            columns=["month"],
            aggfunc="sum",
            fill_value=0.0,
        )
        df_pivot.columns = df_pivot.columns.droplevel()
        df_pivot["total"] = df_pivot.sum(axis=1)
        df_pivot = df_pivot.sort_values(by="total", ascending=False)
        df_pivot = df_pivot.fillna(0.0)

        previous_month = months[0]

        columns = [
            pdt.ColumnParam(
                name=dimension,
                width=dimension_width,
                data=dimension,
                align="L",
                merge=False,
                text_trim=True,
            ),
            pdt.ColumnParam(
                name="12 Months",
                width=15,
                data="total",
                text_format="{:,.2f}$",
                cell_format="WEIGHT",
                align="R",
                footer="sum",
            ),
            pdt.ColumnParam(
                name=previous_month,
                width=12,
                data=previous_month,
                text_format="{:,.2f}$",
                cell_format="WEIGHT",
                align="R",
                footer="sum",
                group=group_name,
            ),
        ]

        previous_month = months[0]
        if previous_month not in df_pivot.columns:
            df_pivot[previous_month] = 0.0

        for month in months[1:]:
            delta_col = f"{month}_d"
            delta_col_bg = f"{delta_col}_bg"
            delta_col_fg = f"{delta_col}_fg"

            if month not in df_pivot.columns:
                df_pivot[month] = 0.0

            df_pivot[delta_col] = df_pivot[month] - df_pivot[previous_month]
            df_pivot[delta_col_bg] = df_pivot[delta_col].apply(color_delta_bg)
            df_pivot[delta_col_fg] = df_pivot[delta_col].apply(color_delta_fg)
            previous_month = month

            columns.append(
                pdt.ColumnParam(
                    name=month,
                    width=12,
                    data=month,
                    text_format="{:,.2f}$",
                    cell_format="WEIGHT",
                    align="R",
                    footer="sum",
                    group=group_name,
                )
            )
            columns.append(
                pdt.ColumnParam(
                    name="+/-",
                    width=10,
                    data=delta_col,
                    text_format="{:,.0f}",
                    cell_format="DELTA_PLUS",
                    color_bg=delta_col_bg,
                    color_fg=delta_col_fg,
                    align="C",
                    footer="sum",
                    group=group_name,
                )
            )

        # print(df_pivot.iloc[0])
        # import pprint
        # pprint.pprint(columns)
        # exit(0)

        pdt.PandasTable(
            df=df_pivot.reset_index(),
            columns=columns,
            pdf=self,
            font_size=6,
        ).generate()

    # *************************************************
    #
    # *************************************************
    def text_summary(self, df_year_totals: pd.DataFrame):
        # year_totals = df_year_totals.sum()

        last_month_totals = df_year_totals.iloc[-1]

        if len(df_year_totals) > 1:
            previous_month_totals = df_year_totals.iloc[-2]
            usage_delta = last_month_totals["Usage"] - previous_month_totals["Usage"]
        else:
            usage_delta = 0

        with self.local_context():
            self.set_font("OpenSans", size=6)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text=f"__{self.last_month_long} Usage__",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        with self.local_context():
            self.set_font("OpenSans", size=20)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text=f"**{last_month_totals['Usage']:.2f} USD** ",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        with self.local_context():
            self.set_font("OpenSans", size=6)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text=f"__Delta to {self.previous_month_long}:__",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        cell_color = PdfColors.R600 if usage_delta >= 0 else PdfColors.G600
        cell_text = (
            f"**+ {usage_delta:.2f} USD**" if usage_delta >= 0 else f"**{usage_delta:.2f} USD**"
        )
        with self.local_context():
            self.set_font("OpenSans", size=10)
            self.set_text_color(**cell_color)
            self.cell(
                text=cell_text,
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

    # *************************************************
    #
    # *************************************************
    def get_totals_per_account(self, account: str = None):
        print(f"get_totals_per_account account={account}")

        df_totals = (
            self.df_totals[self.df_totals["account"] == account].copy()
            if account
            else self.df_totals
        )

        df_totals = df_totals.groupby(["month", "RECORD_TYPE"])["amount"].sum()
        df_totals = df_totals.reset_index().pivot_table(
            values=["amount"],
            index=["month"],
            columns=["RECORD_TYPE"],
            aggfunc="sum",
            fill_value=0.0,
            margins=False,
        )
        df_totals.columns = df_totals.columns.droplevel()
        df_totals["Total"] = df_totals.sum(axis=1)
        df_totals = df_totals.reindex(sorted(df_totals.columns, key=record_type_sort), axis=1)

        return df_totals

    # *************************************************
    #
    # *************************************************
    def compile_data(self, dfs: dict[pd.DataFrame]):
        """Compile the data for the report"""

        # Sanatize Data
        dfs["totals"]["date"] = dfs["totals"]["date"].apply(lambda x: pd.Timestamp(x))
        dfs["usage"]["date"] = dfs["usage"]["date"].apply(lambda x: pd.Timestamp(x))

        last_month = dfs["totals"]["date"].max()
        last_month = last_month.replace(day=1) - pd.DateOffset(months=1)

        self.months = [(last_month.replace(day=1) - pd.DateOffset(months=i)) for i in range(12)][
            ::-1
        ]

        previous_month = self.months[-2]
        first_month = self.months[0]
        # print(self.months)
        # print(f"First Month -> {first_month}")
        # print(f"Previous Month -> {previous_month}")
        # print(f"Last Month -> {last_month}")

        df_accounts = dfs["accounts"]

        # ------------------------------------
        # Clean Up Totals
        # ------------------------------------
        df_totals = dfs["totals"]
        # df_totals = df_totals[df_totals["date"].dt.between(first_month, last_month)].copy()
        df_totals = df_totals[
            (df_totals["date"] >= first_month) & (df_totals["date"] <= last_month)
        ].copy()
        df_totals["month"] = df_totals["date"].dt.strftime("%Y-%m")

        df_totals = df_totals.merge(
            df_accounts[["Id", "Name"]], left_on="LINKED_ACCOUNT", right_on="Id", how="left"
        )
        df_totals["account"] = df_totals["LINKED_ACCOUNT"].astype(str) + " - " + df_totals["Name"]
        df_totals = df_totals.drop(columns=["Id", "Name"])

        self.df_totals = df_totals

        # print(df_totals)

        # ------------------------------------
        # Clean Up Usage
        # ------------------------------------
        df_usage = dfs["usage"]
        df_usage = df_usage[
            (df_usage["date"] >= first_month) & (df_usage["date"] <= last_month)
        ].copy()
        df_usage["month"] = df_usage["date"].dt.strftime("%Y-%m")

        df_usage = df_usage.merge(
            df_accounts[["Id", "Name"]], left_on="LINKED_ACCOUNT", right_on="Id", how="left"
        )
        df_usage["account"] = df_usage["LINKED_ACCOUNT"].astype(str) + " - " + df_usage["Name"]
        df_usage = df_usage.drop(columns=["Id", "Name"])
        # print(df_usage)
        self.df_usage = df_usage

        self.df_accounts = (
            df_usage.groupby(["account"])["amount"]
            .sum()
            .reset_index()
            .sort_values(by="amount", ascending=False)
        )
        # print(self.df_accounts)

        self.last_month_long = last_month.strftime("%B %Y")
        self.previous_month_long = previous_month.strftime("%B %Y")

        self.first_month = first_month.strftime("%Y-%m")
        self.last_month = last_month.strftime("%Y-%m")
        self.previous_month = previous_month.strftime("%Y-%m")

        print(f"First Month -> {self.first_month}")
        print(f"Previous Month -> {self.previous_month}")
        print(f"Last Month -> {self.last_month}")
        print(f"Last Month -> {self.last_month_long}")

        return self

    # *************************************************
    #
    # *************************************************
    def generate_organization_page(self):
        print("generate_organization_page")

        start_y = self.get_y()
        middle = self.w / 2
        df_year_totals = self.get_totals_per_account()

        self.text_summary(df_year_totals)
        self.ln(5)
        self.chart_last_year(df_year_totals, width=70, height=30)
        self.set_xy(middle, start_y)
        self.table_last_year(df_year_totals)

        self.ln(10)
        start_y = self.get_y()

        self.set_xy(self.l_margin, start_y)
        self.table_usage_by_dimension(self.df_usage, dimension="account", dimension_width=40)

        self.set_xy(middle, start_y)
        self.table_usage_by_dimension(self.df_usage, dimension="SERVICE", dimension_width=40)

    # *************************************************
    #
    # *************************************************
    def generate_account_page(self, account: str):
        print(f"generate_account_page account={account}")

        self.add_page()
        self.section_title(f"Account: {account}")

        start_y = self.get_y()
        middle = self.w / 2
        self.set_xy(20, start_y)

        df_year_totals = self.get_totals_per_account(account=account)

        self.text_summary(df_year_totals)
        self.ln(5)
        self.chart_last_year(df_year_totals, width=70, height=30)
        self.set_xy(middle, start_y)
        self.table_last_year(df_year_totals)

        start_y = 90

        df_usage = self.df_usage[self.df_usage["account"] == account]

        self.set_xy(self.l_margin, start_y)
        self.table_usage_by_dimension(
            df_usage=df_usage, dimension="SERVICE", dimension_width=40, months=6
        )

    # *************************************************
    #
    # *************************************************
    def generate(self, dfs: dict[pd.DataFrame]):
        """Return Report from the notes in Pdf format"""

        print("Generate Cost Report")

        # import o7util.pandas
        # o7util.pandas.dfs_to_excel(dfs=dfs, filename="tests/sechub-data-xx.xlsx")

        self.compile_data(dfs)

        self.title = f"AWS Cost Report - {self.last_month_long}"

        self.alias_nb_pages()
        self.add_page()
        self.report_head()

        self.generate_organization_page()

        for account in self.df_accounts["account"]:
            self.generate_account_page(account)

        return self


# if __name__ == "__main__":
#     import o7util.pandas

#     dfs = o7util.pandas.dfs_from_excel("tests/aws-cost-data.xlsx")
#     obj = ReportAwsCost(filename="cache/aws_cost.pdf")
#     obj.generate(dfs=dfs)
#     obj.save()

#     dfs = o7util.pandas.dfs_from_excel("tests/aws-cost-data-big.xlsx")
#     obj = ReportAwsCost(filename="cache/aws_cost-big.pdf")
#     obj.generate(dfs=dfs)
#     obj.save()
