import sympy as sp
import numpy as np
import plotly.graph_objects as go

class TaylorSeriesPlotter:
    def __init__(self, function, variable='x'):
        self.function = sp.sympify(function)
        self.variable = sp.Symbol(variable)

    def taylor_series(self, center, order):
        return sp.series(self.function, self.variable, center, order).removeO()

    def diff_area(self, x_vals, y_original, y_taylor):
        area = []
        for i in range(1, len(x_vals)):
            x_area = [x_vals[i-1], x_vals[i], x_vals[i], x_vals[i-1]]
            y_area = [y_taylor[i-1], y_taylor[i], y_original[i], y_original[i-1]]

            # 차이 계산 (절댓값 사용)]
            color = "rgba(0, 0, 255, 0.2)" if y_original[i] > y_taylor[i] else "rgba(255, 0, 0, 0.2)"
            area.append(go.Scatter(
                x=x_area,
                y=y_area,
                fill='toself',
                mode='lines',
                line_width=0,
                fillcolor=color,
                showlegend=False
            ))
        return area

    def plot_comparison(self, center, orders, x_range=(-10, 10), num_points=500):
        x_vals = np.linspace(x_range[0], x_range[1], num_points)
        original_func = sp.lambdify(self.variable, self.function, modules="numpy")
        y_original = original_func(x_vals)

        fig = go.Figure()

        # Original function trace
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_original,
            mode='lines',
            name='Original Function',
            line=dict(color='blue'),
            customdata=np.stack([y_original, np.zeros_like(y_original)], axis=-1),  # [y_original, 0] 저장
            hovertemplate='x: %{x}<br>Original y: %{customdata[0]}<br>Difference: %{customdata[1]}<extra></extra>'  # 차이를 계산하여 표시
        ))

        for order in orders:
            taylor_expr = self.taylor_series(center, order)
            taylor_func = sp.lambdify(self.variable, taylor_expr, modules="numpy")
            y_taylor = taylor_func(x_vals)

            # 차이 계산 (절댓값 사용)
            diff = abs(y_original - y_taylor)  # 절댓값 차이 계산
            fig.add_trace(go.Scatter(
                x=x_vals,
                y=y_taylor,
                mode='lines',
                name=f'Taylor Series (Order {order})',
                line=dict(color='red'),
                customdata=np.stack([y_taylor, diff], axis=-1),  # [y_taylor, diff] 저장
                hovertemplate='x: %{x}<br>Taylor y: %{customdata[0]}<br>Difference: %{customdata[1]}<extra></extra>'  # 차이 표시
            ))

            area = self.diff_area(x_vals, y_original, y_taylor)
            for diff in area:
                fig.add_trace(diff)

        fig.update_layout(
            title=f"Taylor Series Approximation Comparison (Center: {center})",
            xaxis_title="x",
            yaxis_title="f(x)",
            legend_title="Functions",
            template="plotly_white",
            yaxis=dict(range=[-10, 10])
        )

        fig.show()

if __name__ == "__main__":
    try:
        function_input = input("function (ex: sin(x), exp(x), log(1+x)): ")
        function = sp.sympify(function_input)

        center_input = input("the center of the series: ")
        center = float(center_input)

        orders_input = input("degree (ex: 2,4,6): ")
        orders = list(map(int, orders_input.split(',')))

        plotter = TaylorSeriesPlotter(function)
        plotter.plot_comparison(center=center, orders=orders)

    except (sp.SympifyError, ValueError) as e:
        print(f"Error: {e}. Please check your inputs and try again.")
