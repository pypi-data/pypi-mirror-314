import matplotlib.pyplot as plt

class Plotter:
    """
    A simple plotter class for plotting points and lines. Based on matplotlib.

    Methods
    -------
    set_color(color)
        Sets the color for plotting points and lines.
    set_marker_size(size)
        Sets the size of the markers used for plotting points.
    set_line_width(width)
        Sets the width of the lines used for plotting lines.
    plot_point(x, y)
        Plots a point at the given x and y coordinates.
    plot_line(p1, p2)
        Plots a line between the points p1 and p2.
    show()
        Displays the plot.
    save(filename)
        Saves the plot to a file.
    """
    def __init__(self):
        self._fig, self._ax = plt.subplots()
        self._color = 'blue'
        self._marker_size = 5
        self._line_width = 1
        self._ax.axis('off')  # Hide the axes by default

    def set_color(self, color):
        self._color = color

    def set_marker_size(self, size):
        self._marker_size = size

    def set_line_width(self, width):
        self._line_width = width

    def plot_point(self, p):
        x, y = p
        self._ax.plot(x, y, color=self._color, marker='o', markersize=self._marker_size)

    def plot_line(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        self._ax.plot([x1, x2], [y1, y2], color=self._color, linewidth=self._line_width)

    def show(self):
        plt.show()

    def save(self, filename):
        self._fig.savefig(filename)

if __name__ == "__main__":
    # Example usage:
    plotter = Plotter()
    plotter.set_color('red')
    plotter.set_marker_size(10)
    plotter.plot_point((1, 2))
    plotter.set_line_width(2)
    plotter.plot_line((1, 2), (3, 4))
    plotter.save('plot.png')
    plotter.show()