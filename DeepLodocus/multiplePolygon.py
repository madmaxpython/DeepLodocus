import numpy as np
from matplotlib.lines import Line2D
from matplotlib.artist import Artist
from matplotlib.widgets import PolygonSelector

def dist(x, y):
    """
    Return the distance between two points.
    """
    d = x - y
    return np.sqrt(np.dot(d, d))


def dist_point_to_segment(p, s0, s1):
    """
    Get the distance of a point to a segment.
      *p*, *s0*, *s1* are *xy* sequences
    This algorithm from
    http://geomalgorithms.com/a02-_lines.html
    """
    v = s1 - s0
    w = p - s0
    c1 = np.dot(w, v)
    if c1 <= 0:
        return dist(p, s0)
    c2 = np.dot(v, v)
    if c2 <= c1:
        return dist(p, s1)
    b = c1 / c2
    pb = s0 + b * v
    return dist(p, pb)


class PolygonInteractor:
    """
    A polygon editor.

    Key-bindings

      't' toggle vertex markers on and off.  When vertex markers are on,
          you can move them, delete them

      'd' delete the vertex under point

      'i' insert a vertex at point.  You must be within epsilon of the
          line connecting two existing vertices

    """

    showverts = True
    epsilon = 5  # max pixel distance to count as a vertex hit

    def __init__(self, ax, poly, contour, animated_artists=()):
        if poly.figure is None:
            raise RuntimeError('You must first add the polygon to a figure '
                               'or canvas before defining the interactor')
        self.ax = ax
        canvas = poly.figure.canvas
        self.poly = poly

        self.line = contour

        self._ind = None  # the active vert

        canvas.mpl_connect('draw_event', self.on_draw)
        canvas.mpl_connect('button_press_event', self.on_button_press)
        canvas.mpl_connect('key_press_event', self.on_key_press)
        canvas.mpl_connect('button_release_event', self.on_button_release)
        canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas = canvas

        self._artists = []
        for a in animated_artists:
            self.add_artist(a)
        #self.add_artist(self.line)

    def add_artist(self, art):
        if art.figure != self.canvas.figure:
            raise RuntimeError
        art.set_animated(True)
        self._artists.append(art)

    def on_draw(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.ax.draw_artist(self.poly)
        self.ax.draw_artist(self.line)
        self._draw_animated()
        self.canvas.blit(self.ax.bbox)
        # do not need to blit here, this will fire before the screen is
        # updated

    def _draw_animated(self):
        """Draw all of the animated artists."""
        fig = self.canvas.figure
        for a in self._artists:
            fig.draw_artist(a)

    def get_ind_under_point(self, event):
        """
        Return the index of the point closest to the event position or *None*
        if no point is within ``self.epsilon`` to the event position.
        """
        # display coords
        xy = np.asarray(self.poly.xy)
        xyt = self.poly.get_transform().transform(xy)
        xt, yt = xyt[:, 0], xyt[:, 1]
        d = np.hypot(xt - event.x, yt - event.y)
        indseq, = np.nonzero(d == d.min())
        ind = indseq[0]

        if d[ind] >= self.epsilon:
            ind = None

        return ind

    def on_button_press(self, event):
        """Callback for mouse button presses."""
        if not self.showverts:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        self._ind = self.get_ind_under_point(event)

    def on_button_release(self, event):
        """Callback for mouse button releases."""
        if not self.showverts:
            return
        if event.button != 1:
            return
        self._ind = None

    def on_key_press(self, event):
        """Callback for key presses."""
        if not event.inaxes:
            return
        if event.key == 't':
            self.showverts = not self.showverts
            self.line.set_visible(self.showverts)
            if not self.showverts:
                self._ind = None
        elif event.key == 'd':
            ind = self.get_ind_under_point(event)
            if ind is not None:
                self.poly.xy = np.delete(self.poly.xy,
                                         ind, axis=0)
                self.line.set_data(zip(*self.poly.xy))
        elif event.key == 'i':
            xys = self.poly.get_transform().transform(self.poly.xy)
            p = event.x, event.y  # display coords
            for i in range(len(xys) - 1):
                s0 = xys[i]
                s1 = xys[i + 1]
                d = dist_point_to_segment(p, s0, s1)
                if d <= self.epsilon:
                    self.poly.xy = np.insert(
                        self.poly.xy, i+1,
                        [event.xdata, event.ydata],
                        axis=0)
                    self.line.set_data(zip(*self.poly.xy))
                    break
        if self.line.stale:
            self.canvas.draw_idle()

    def on_mouse_move(self, event):
        """Callback for mouse movements."""
        if not self.showverts:
            return
        if self._ind is None:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        x, y = event.xdata, event.ydata

        self.poly.xy[self._ind] = x, y
        if self._ind == 0:
            self.poly.xy[-1] = x, y
        elif self._ind == len(self.poly.xy) - 1:
            self.poly.xy[0] = x, y
        self.line.set_data(zip(*self.poly.xy))

        self.canvas.restore_region(self.background)
        self._draw_animated()
        self.canvas.draw_idle()
        # self.ax.draw_artist(self.poly)
        # self.ax.draw_artist(self.line)
        self.canvas.blit(self.ax.bbox)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    import cv2
    import random

    def AreaSelector(TITLE_WINDOW, VIDEO_PATH, frame):
        fig, ax = plt.subplots()
        ax.invert_yaxis()
        fig.canvas.manager.set_window_title('Calibration Step')
        fig.suptitle(TITLE_WINDOW, fontsize=16)

        imgplot = plt.imshow(frame)

        lineprops = {'color': 'red', 'linewidth': 4, 'alpha': 0.8}
        lsso = PolygonSelector(ax=ax, onselect=onSelect, lineprops=lineprops)
        plt.show()
        plt.close("all")
        return coord



def onSelect(x):
    global coord
    if len(x) != 0:
        plt.close()
    coord = x
    return coord
if __name__ == '__main__':
    videopath = "/Users/maximeteixeira/Desktop/DeepLodocusGit/DeepLodocus/Datas/3_9BR.h264.transcode.mp4"
    cap = cv2.VideoCapture(videopath)
    randomnb = random.randint(0, 300)
    cap.set(1, randomnb)

    ret, frame = cap.read()

    poly = Polygon(AreaSelector("lasso", videopath, frame), animated=True)
    poly2 = Polygon(AreaSelector("lasso", videopath, frame), animated=True)


    xc1, yc1 = zip(*poly.xy)
    poly_contour = Line2D(xc1, yc1, marker='x', markerfacecolor='r',
                          animated=True)


    xc2, yc2 = zip(*poly2.xy)
    poly_contour2 = Line2D(xc2, yc2, marker='x', markerfacecolor='r',
                          animated=True)

    fig, ax = plt.subplots()

    ax.add_patch(poly)
    ax.add_line(poly_contour)

    ax.add_patch(poly2)
    ax.add_line(poly_contour2)
    p = PolygonInteractor(ax, poly, poly_contour, [poly, poly2, poly_contour, poly_contour2])
    p2 = PolygonInteractor(ax, poly2, poly_contour2, [poly, poly2, poly_contour, poly_contour2])

    ax.set_title('Click and drag a point to move it')
    plt.imshow(frame)
    plt.show()