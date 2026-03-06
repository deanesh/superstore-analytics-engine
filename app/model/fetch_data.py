from pipeline.pipeline import SuperstorePipeline


def get_analysis():

    file_path = "data/indian_superstore_data.xlsx"

    pipeline = SuperstorePipeline(file_path)

    df, rfm, model, fig_sales, fig_returns = pipeline.run()

    return df, rfm, fig_sales, fig_returns