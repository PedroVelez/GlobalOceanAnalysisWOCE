import pandas as pd
import matplotlib.pyplot as plt

file_in = './Cuencas/SouthMadagascar.csv'
file_out = './Cuencas/SouthMadagascarNEUVO.csv'

file_bg1 = './Cuencas/SACentralAntartica.csv'
file_bg2 = './Cuencas/SouthAfrica.csv'


df = pd.read_csv(file_in)
bg1 = pd.read_csv(file_bg1)
bg2 = pd.read_csv(file_bg2)

lon = df['lon'].values
lat = df['lat'].values

# === PLOT ===
fig, ax = plt.subplots()
ax.plot(lon,lat,c='blue')
sc = ax.scatter(lon, lat, picker=True)

ax.plot(bg1['lon'], bg1['lat'],c='red')
ax.scatter(bg1['lon'], bg1['lat'],
           c='red', s=10, alpha=0.5, label='Fondo 1')
ax.plot(bg2['lon'], bg2['lat'],c='gray')
ax.scatter(bg2['lon'], bg2['lat'],
           c='gray', s=10, alpha=0.5, label='Fondo 2')


selected_idx = None

def on_pick(event):
    global selected_idx
    selected_idx = event.ind[0]

def on_motion(event):
    global selected_idx
    if selected_idx is None:
        return
    if event.xdata is None or event.ydata is None:
        return

    lon[selected_idx] = event.xdata
    lat[selected_idx] = event.ydata
    sc.set_offsets(list(zip(lon, lat)))
    fig.canvas.draw_idle()

def on_release(event):
    global selected_idx
    selected_idx = None

def on_key(event):
    if event.key == 'g':
        df['lon'] = lon
        df['lat'] = lat
        df.to_csv(file_out, index=False)
        print(f"Guardado en {file_out}")

fig.canvas.mpl_connect('pick_event', on_pick)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('key_press_event', on_key)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Arrastra puntos con el ratón | Pulsa 'g' para guardar")

plt.show()