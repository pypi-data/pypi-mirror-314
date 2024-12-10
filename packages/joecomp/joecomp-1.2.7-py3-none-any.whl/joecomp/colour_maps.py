from matplotlib.colors import LinearSegmentedColormap

blueOrangeCMAP = LinearSegmentedColormap.from_list('my_CMAP', (
    # Edit this gradient at https://eltos.github.io/gradient/#219EBC-8ECAE6-FFFFFF-FFB703-FB8500
    (0.000, (0.129, 0.620, 0.737)),
    (0.250, (0.557, 0.792, 0.902)),
    (0.500, (1.000, 1.000, 1.000)),
    (0.750, (1.000, 0.718, 0.012)),
    (1.000, (0.984, 0.522, 0.000))))

# Colour map from Dr Adrien Houge
HUGE_CMAP_LIST = ['#EDE0D4', '#E6CCB2', '#DDB892', '#B08968', '#7F5539', '#9C6644']
latteCMAP = LinearSegmentedColormap.from_list("Cmap", HUGE_CMAP_LIST, N = 200)