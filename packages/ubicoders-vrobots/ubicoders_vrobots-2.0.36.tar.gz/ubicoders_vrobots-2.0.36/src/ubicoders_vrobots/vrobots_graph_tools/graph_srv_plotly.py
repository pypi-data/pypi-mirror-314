import asyncio
from collections import deque
from .data_viz_web import DataVizWeb
from .graph_udp_server import start_udp_server


async def graph_server_plotly_core(
    port=12750,
    data_length=250,
    interval=100,
    title="Real-Time Data Visualization",
    y_label="",
):
    # if interval < 100 throw an error
    if interval < 100:
        print("Graph update interval should be greater than 100")
        return

    data_app = DataVizWeb(title=title, y_label=y_label, interval=interval)
    data_app.data_queue = deque(maxlen=data_length)

    dash_task = asyncio.to_thread(data_app.run)
    udp_task = start_udp_server(data_app.data_queue, port=port)

    await asyncio.gather(dash_task, udp_task)


def graph_server_plotly(
    port=12750,
    data_length=250,
    interval=100,
    title="Real-Time Data Visualization",
    y_label="",
):
    asyncio.run(
        graph_server_plotly_core(
            port=port,
            data_length=data_length,
            interval=interval,
            title=title,
            y_label=y_label,
        )
    )


if __name__ == "__main__":
    graph_server_plotly()
