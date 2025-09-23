import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Crear una malla de coordenadas
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)

# Definir dos funciones
Z1 = np.sin(np.sqrt(X**2 + Y**2))
Z2 = np.cos(X) * np.sin(Y)

# Crear figura y ejes
fig, axs = plt.subplots(2, 2, figsize=(10, 8), subplot_kw={"projection": None})

# --- Gráfico superior izquierdo (3D de Z1)
ax1 = fig.add_subplot(2, 2, 1, projection="3d")
surf1 = ax1.plot_surface(X, Y, Z1, cmap="viridis")
ax1.set_title("Superficie 3D - Función Z1")
fig.colorbar(surf1, ax=ax1, shrink=0.5, aspect=8)

# --- Gráfico superior derecho (3D de Z2)
ax2 = fig.add_subplot(2, 2, 2, projection="3d")
surf2 = ax2.plot_surface(X, Y, Z2, cmap="plasma")
ax2.set_title("Superficie 3D - Función Z2")
fig.colorbar(surf2, ax=ax2, shrink=0.5, aspect=8)

# --- Gráfico inferior izquierdo (curvas de nivel de Z1)
ax3 = fig.add_subplot(2, 2, 3)
contour1 = ax3.contourf(X, Y, Z1, cmap="viridis")
ax3.set_title("Curvas de nivel - Z1")
fig.colorbar(contour1, ax=ax3)

# --- Gráfico inferior derecho (curvas de nivel de Z2)
ax4 = fig.add_subplot(2, 2, 4)
contour2 = ax4.contourf(X, Y, Z2, cmap="plasma")
ax4.set_title("Curvas de nivel - Z2")
fig.colorbar(contour2, ax=ax4)

# Ajustar espaciado
plt.tight_layout()
plt.show()