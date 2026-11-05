from config import config
from collections import deque
from types import SimpleNamespace
import matplotlib.pyplot as plt
from matplotlib import patches

def showBoard(objects):
    """Draws all objects as circles with fading trails. Returns True if the window was closed. (objects: list of objects
    to be drawn, sizeModifier: size of the board)."""
    #! This function contains the only code written in any part by AI, all other code is my own.

    if not hasattr(showBoard, "_s"):
        fig, ax = plt.subplots(figsize=(8, 8))
        half = config["boardConfigs"]["boardSize"] / 2
        fig.patch.set_facecolor(config["boardConfigs"]["backgroundColor"])
        ax.set(facecolor=config["boardConfigs"]["backgroundColor"], xlim=(-half, half), ylim=(-half, half),
               xticks=[], yticks=[], aspect='equal')
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.add_patch(patches.Rectangle((-half, -half), config["boardConfigs"]["boardSize"], config["boardConfigs"]["boardSize"],
                                       linewidth=2, edgecolor=config["boardConfigs"]["borderColor"], facecolor='none'))
        plt.tight_layout()
 
        # per-object artists + trail history live in s.entries, keyed by id(obj)
        s = showBoard._s = SimpleNamespace(fig=fig, ax=ax, entries={}, bg=None) # type: ignore
 
        def draw_animated():
            # circles first, then trails: matches the original z-order (patches under lines)
            for part in ('circle', 'trail'):
                for e in s.entries.values():
                    ax.draw_artist(e[part])
 
        def on_draw(event):
            # fires on every full draw (first frame, window resize): re-cache the static background
            if fig.canvas.supports_blit:
                s.bg = fig.canvas.copy_from_bbox(fig.bbox) # type: ignore
            draw_animated()
 
        s.draw_animated = draw_animated
        fig.canvas.mpl_connect('draw_event', on_draw)
        plt.show(block=False)
 
    s = showBoard._s # type: ignore
    fig, ax, entries = s.fig, s.ax, s.entries
    if not plt.fignum_exists(fig.number):
        return True
 
    seen = set()
    for obj in objects:
        x, y = obj.getPosition()
        x /= config["boardConfigs"]["sizeModifier"]
        y /= config["boardConfigs"]["sizeModifier"]
        color = getattr(obj, "color", config["boardConfigs"]["defaultColor"])
        key = id(obj)
        seen.add(key)
 
        e = entries.get(key)
        if e is None:
            e = entries[key] = {
                'obj': obj,  # strong ref: stops id() being recycled by a new object while this entry lives
                'circle': ax.add_patch(patches.Circle((x, y), config["boardConfigs"]["radius"], edgecolor=config["boardConfigs"]["edgeColor"],
                                                      linewidth=1, animated=True)),
                'trail': ax.plot([], [], linewidth=1, alpha=0.2, animated=True)[0],
                'xs': deque(maxlen=int(config["boardConfigs"]["trailLength"])),
                'ys': deque(maxlen=int(config["boardConfigs"]["trailLength"])),
            }
        e['xs'].append(x)
        e['ys'].append(y)
        e['circle'].center = (x, y)
        e['circle'].set_facecolor(color)
        e['trail'].set_data(e['xs'], e['ys'])
        e['trail'].set_color(color)
 
    for key in entries.keys() - seen:  # objects that no longer exist
        e = entries.pop(key)
        e['circle'].remove()
        e['trail'].remove()
 
    canvas = fig.canvas
    if s.bg is None or not canvas.supports_blit:
        canvas.draw()  # full draw; on_draw caches the background and draws the animated artists
    else:
        canvas.restore_region(s.bg)
        s.draw_animated()
        canvas.blit(fig.bbox)
    canvas.flush_events()
 
    return not plt.fignum_exists(fig.number)

if __name__ == "__main__":
    from gravity_simulation import main
    main()