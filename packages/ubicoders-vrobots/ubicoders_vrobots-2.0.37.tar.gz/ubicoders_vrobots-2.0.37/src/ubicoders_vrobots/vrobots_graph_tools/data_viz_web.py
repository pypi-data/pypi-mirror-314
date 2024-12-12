from collections import deque
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging, sys
import numpy as np

log = logging.getLogger("werkzeug")
log.disabled = True  # Disables all werkzeug logs
cli = sys.modules["flask.cli"]
cli.show_server_banner = lambda *x: None


class DataVizWeb:
    def __init__(self, title="Real-Time Data Visualization", y_label="", interval=100):
        self.app = Dash(__name__)
        self.title = title
        self.y_label = y_label
        self.interval = interval
        self.data_queue = deque(maxlen=250)
        self._setup_layout()
        self._setup_callbacks()

    def _setup_layout(self):
        """Define the app layout."""
        self.app.layout = html.Div(
            [
                html.H1(self.title),
                dcc.Graph(id="live-graph"),
                dcc.Interval(
                    id="interval-component", interval=self.interval, n_intervals=0
                ),
            ]
        )

    def _setup_callbacks(self):
        """Define the callback for updating the graph."""

        @self.app.callback(
            Output("live-graph", "figure"), Input("interval-component", "n_intervals")
        )
        def update_graph_live(n):
            if (self.data_queue is None) or (len(self.data_queue) == 0):
                return go.Figure()
            stacked_data = np.vstack(self.data_queue)
            times, x_data, y_data, z_data = (
                stacked_data[:, 0],
                stacked_data[:, 1],
                stacked_data[:, 2],
                stacked_data[:, 3],
            )

            fig = make_subplots(
                rows=3,
                cols=1,
                shared_xaxes=False,
                subplot_titles=(
                    f"{self.y_label} - X",
                    f"{self.y_label} - Y",
                    f"{self.y_label} - Z",
                ),
            )

            fig.add_trace(
                go.Scatter(
                    x=times, y=x_data, mode="lines+markers", name=f"{self.y_label} Axis"
                ),
                row=1,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=times, y=y_data, mode="lines+markers", name=f"{self.y_label} Axis"
                ),
                row=2,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=times, y=z_data, mode="lines+markers", name=f"{self.y_label} Axis"
                ),
                row=3,
                col=1,
            )

            fig.update_layout(
                height=800,
                title_text=self.title,
                showlegend=False,
                yaxis=dict(dtick=1),  # X axis
                yaxis2=dict(dtick=1),  # Y axis
                yaxis3=dict(dtick=1),  # Z axis
            )
            fig.update_xaxes(title_text="Time", row=3, col=1)

            return fig

    def clear_data(
        self,
    ):
        self.data_queue.clear()

    def append_data(self, data_point):
        """Append data to the shared queue."""
        self.data_queue.append(data_point)

    def run(self, debug=True):
        """Run the Dash server."""
        print(
            "\033[92m" + "Plot server is running on http://localhost:8050/" + "\033[0m"
        )
        self.app.run_server(debug=debug, use_reloader=False)
