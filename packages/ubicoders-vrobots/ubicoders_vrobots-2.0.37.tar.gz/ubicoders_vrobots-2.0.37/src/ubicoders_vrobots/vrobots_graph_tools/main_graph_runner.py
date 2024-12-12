from .graph_srv_plotly import graph_server_plotly
from .graph_srv_pyqt import graph_server_pyqt
from .graph_srv_matplotlib import graph_server_matplotlib


def main_graph_runner(
    backend="web",
    port=12750,
    data_length=250,
    interval=200,
    title="Real-Time Data Visualization",
    y_label="",
):
    """
    Main graph runner backend: "web", "pyqt", "matplotlib"
    """
    if backend == "web":
        graph_server_plotly(
            port=port,
            data_length=data_length,
            interval=interval,
            title=title,
            y_label=y_label,
        )

    if backend == "pyqt":
        graph_server_pyqt(port=port, data_length=data_length)

    if backend == "matplotlib":
        graph_server_matplotlib(port=port, data_length=data_length)


if __name__ == "__main__":
    main_graph_runner(backend="pyqt")
