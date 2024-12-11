"""Spec for Text Search Result styling."""

from .base_styling import ResultColumnStyling


class ResultTextStyling(ResultColumnStyling):
    """Style text search result columns.

    Specify styling options for text search result columns,
    including color specifications and data column mapping.

    Args:
        color_spec (Optional[ColorSpec]): Spec for coloring columns.
        data_column (Optional[TemplatedStringItem]): Name of column in pandas
            dataframe(s) used for color spec if a gradient is used. Optional for
            single colors.

    Examples:
        ??? example "Changing the color of a text search result item"
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
                    search.ResultTextItem(
                        data_column="score",
                        styling=search.ResultTextStyling(
                            color_spec=color.Palette.ASHES_GREY,
                        )
                    ),
                ],
            )

            Dashboard(content=search_widget)
            ```
    """
