"""Spec for Number Search Result styling."""

from .base_styling import ResultColumnStyling


class ResultNumberStyling(ResultColumnStyling):
    """Style number search result columns.

    Specify styling options for number search result columns,
    including color specifications and data column mapping.

    Examples:
        ??? example "Changing the color of a number search result item"
            ```py linenums="1"
            #
            import pandas as pd
            from engineai.sdk.dashboard.dashboard import Dashboard
            from engineai.sdk.dashboard.widgets import search
            from engineai.sdk.dashboard.styling import color


            data = pd.DataFrame(
                data=[
                    {"key": "AAPL", "name": "Apple", "score": 10},
                    {"key": "MSFT", "name": "Microsoft", "score": 5},
                ]
            )

            search_widget = search.Search(
                data=data,
                selected_text_column="name",
                items=[
                    search.ResultTextItem(data_column="key"),
                    search.ResultNumberItem(
                        data_column="score",
                        styling=search.ResultNumberStyling(
                            color_spec=color.Palette.BABY_BLUE,
                        )
                    ),
                ],
            )

            Dashboard(content=search_widget)
            ```
    """
