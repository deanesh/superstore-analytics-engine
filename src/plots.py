import matplotlib.pyplot as plt
import seaborn as sns


def sales_trend(df):

    fig, ax = plt.subplots(figsize=(10,5))

    df.resample("ME", on="Order Date")["Sales"].sum().plot(ax=ax)

    ax.set_title("Monthly Sales Trend")
    ax.set_ylabel("Sales")

    return fig


def return_rate_plot(df):

    fig, ax = plt.subplots(figsize=(8,5))

    rate = df.groupby("Category")["Returned"].apply(lambda x: (x == "Yes").mean() * 100)

    sns.barplot(x=rate.index, y=rate.values, ax=ax)

    ax.set_ylabel("Return Rate %")
    ax.set_title("Return Rate by Category")

    return fig