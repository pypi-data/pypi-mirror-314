# SAMBA_ilum Copyright (C) 2024 - Closed source


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Observação:  Introduzir o vácuo original no arquivo POSCAR final
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


import numpy as np
import shutil
import os
#--------------------------
import plotly.offline as py
import plotly.graph_objects as go
#--------------------------------
import scipy.interpolate as interp
from scipy.interpolate import griddata
#-------------------------------------
import matplotlib as mpl
from matplotlib import cm
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.colors as mcolors


n_d = 301  # O dados do xy-scan serão interpolados para um grid de (n_d x n_d) pontos


#========================================================
# Obtendo a área no plano XY da Heteroestrutura =========
#========================================================
poscar = open('POSCAR.0', 'r')
VTemp = poscar.readline().split()
VTemp = poscar.readline();  param = float(VTemp)
#-----------------------------------------------
A1 = poscar.readline().split();  A1x = float(A1[0])*param; A1y = float(A1[1])*param; A1z = float(A1[2])*param;  mA1 = np.linalg.norm(A1)
A2 = poscar.readline().split();  A2x = float(A2[0])*param; A2y = float(A2[1])*param; A2z = float(A2[2])*param;  mA2 = np.linalg.norm(A2)
A3 = poscar.readline().split();  A3x = float(A3[0])*param; A3y = float(A3[1])*param; A3z = float(A3[2])*param;  mA3 = np.linalg.norm(A3)
#---------------------------------------------------------------------------------------------------------------------------------------
A1 = np.array([A1x, A1y])
A2 = np.array([A2x, A2y])
#---------------------------
# Área da célula no plano XY
Area = np.linalg.norm(np.cross(A1, A2))
#--------------------------------------
poscar.close()
#-------------


#=====================================================
# Extraindo informações do arquivo energy_scan.txt ===
#=====================================================
file0 = np.loadtxt('energy_scan.txt', dtype=str)
file0.shape
#-----------------------
date_shift  = file0[:,0]
date_E   = np.array(file0[:,1],dtype=float)
E_min    = min(date_E)
E_max    = max(date_E)
Delta_E_meV = ((E_max -E_min)*1000)/Area
Delta_E_J   = ((E_max -E_min)*1.6021773e-19)/(Area*1e-20)
line     = np.argmin(date_E)
delta    = date_shift[line]
#------------------------------------------
delta_min = delta.replace('_', ' ').split()
a1_min = float(delta_min[0])
a2_min = float(delta_min[1])
x_min = (a1_min*A1x) + (a2_min*A2x)
y_min = (a1_min*A1y) + (a2_min*A2y)
#----------------------------------
if (a1_min == -0.0): a1_min = 0.0
if (a2_min == -0.0): a2_min = 0.0
if (x_min == -0.0):  x_min = 0.0
if (y_min == -0.0):  y_min = 0.0
#-------------------------------


#===============================================
# Criando o arquivo energy_scan_shift.txt ======
#===============================================
file0 = np.loadtxt('energy_scan.txt', dtype=str)
file0.shape
#----------------------
date_shift = file0[:,0]
date_E = np.array(file0[:,1],dtype=float)
#----------------------------------------
file = open('energy_scan_shift.txt', "w")
shift = [-2, -1, 0, +1, +2]
#-------------------------------
for i in range(len(date_shift)):
    #--------------------------------------------------
    shift_temp = date_shift[i].replace('_',' ').split()
    shift_A1 = float(shift_temp[0])
    shift_A2 = float(shift_temp[1])
    #------------------------------
    for j in range(len(shift)):
        for k in range(len(shift)):
            t_shift_A1 = shift_A1 -a1_min +shift[j]
            t_shift_A2 = shift_A2 -a2_min +shift[k]
            if (t_shift_A1 >= 0.0  and t_shift_A1 <= 1.0):
               if (t_shift_A2 >= 0.0  and t_shift_A2 <= 1.0): 
                  file.write(f'{shift_A1 -a1_min +shift[j]}_{shift_A2 -a2_min + shift[k]} {date_E[i]} \n')
#-----------
file.close()
#-----------


#===========================================================
# Extraindo informações do arquivo energy_scan_shift.txt ===
#===========================================================
file0 = np.loadtxt('energy_scan_shift.txt', dtype=str)
file0.shape
#----------------------
date_shift = file0[:,0]
date_E = np.array(file0[:,1],dtype=float)
E_min    = min(date_E)
#---------------------


#-------------------------------------
file = open('xy-scan_direct.dat', "w")
#-------------------------------------
for i in range(len(date_shift)):
    VTemp = str(date_shift[i])
    VTemp = VTemp.replace('_', ' ')
    file.write(f'{VTemp} {((date_E[i] -E_min)*1000)/Area} \n')
#-----------
file.close()
#-----------


#----------------------------------------
file = open('xy-scan_cartesian.dat', "w")
#----------------------------------------
for i in range(len(date_shift)):
    VTemp = str(date_shift[i])
    VTemp = VTemp.replace('_', ' ').split()
    Coord_X = ((float(VTemp[0])*A1x) + (float(VTemp[1])*A2x))
    Coord_Y = ((float(VTemp[0])*A1y) + (float(VTemp[1])*A2y))
    file.write(f'{Coord_X} {Coord_Y} {((date_E[i] -E_min)*1000)/Area} \n')
#-----------
file.close()
#-----------


#===================================================
# Plot 3D - Coordenadas Cartesianas (.html) ========
#===================================================
label1 = '\u0394' + 'X' + ' (' + '\u212B' + ')'
label2 = '\u0394' + 'Y' + ' (' + '\u212B' + ')'
label3 = 'E-Emin' + ' (meV/' + '\u212B' + '\u00B2' + ')'
#------------------------------------------------------------
file2 = np.loadtxt('xy-scan_cartesian.dat')
file2.shape
#------------------
eixo1c = file2[:,0]
eixo2c = file2[:,1]
eixo3c = file2[:,2]
#---------------------------
# Create meshgrid for (x, y):
x = np.linspace(min(eixo1c), max(eixo1c), n_d)
y = np.linspace(min(eixo2c), max(eixo2c), n_d)
x_grid, y_grid = np.meshgrid(x, y)
# Grid data:
e2_grid = griddata((eixo1c, eixo2c), eixo3c, (x_grid, y_grid), method = 'cubic', fill_value=np.nan)


#============================================================
# Obtendo as coordenadas do ponto de E_mínima ===============
#============================================================
e2_grid[np.isnan(e2_grid)] = np.inf
min_idx = np.unravel_index(np.argmin(e2_grid), e2_grid.shape)   # Encontrando o índice do menor valor de energia no e_grid
delta_X = x_grid[min_idx]                                       # Encontrando o correspondente valor de delta_X
delta_Y = y_grid[min_idx]                                       # Encontrando o correspondente valor de delta_Y
E_min   = e2_grid[min_idx]                                      # Encontrando o correspondente valor de E_min
# print(min_idx, delta_X, delta_Y, E_min)
#----------------------------------------
fig = go.Figure()
fig.add_trace(go.Surface(x = x_grid, y = y_grid, z = e2_grid, name = 'xy-scan', opacity = 0.8, showscale = False, colorscale='jet'))
fig.update_layout(title = 'xy-scan', scene = dict(xaxis_title = label1, yaxis_title = label2, zaxis_title = label3, aspectmode = 'cube'), margin = dict(r = 20, b = 10, l = 10, t = 10))
fig.update_layout(xaxis_range=[min(eixo1c), max(eixo1c)])
fig.update_layout(yaxis_range=[min(eixo2c), max(eixo2c)])
fig.write_html('xy-scan_3D_cartesian.html')


#===========================================================================
# Obtendo as coordenadas do ponto de E_mínima na forma direta ==============
#===========================================================================
a = np.array([A1x, A1y, A1z])
b = np.array([A2x, A2y, A2z])
c = np.array([A3x, A3y, A3z])
T = np.linalg.inv(np.array([a, b, c]).T)  # Definindo a matriz de transformação
#------------------------------------------------------------------------------
r = np.array([delta_X, delta_Y, 0.0])        # Definindo o vetor posição cartesiano do átomo
#------------------------------------
f = np.dot(T, r)           # Calculando a correspondenre posição em coordenadas fracionárias    # ??????????????????? Esta correto ???????????????????
for m in range(3):                                                                              # ?????? Ao invés de 'f' não deveria ser 'f[m]' ??????
    f = np.where(f < 0, f + 1, f)                                                               # ??????????????????? Esta correto ???????????????????
    f = np.where(f > 1, f - 1, f)
#--------------------------------
for m in range(3):
    # f[m] = round(f[m], 6)
    if (f[m] > 0.9999 or f[m] < 0.0001):
       f[m] = 0.0
#------------------------------------
delta_A1 = float(f[0])
delta_A2 = float(f[1])


#=======================================================
# Plot 2D - Coordenadas Cartesianas (Mapa de cores) ====
#=======================================================
n_contour = 100
#------------------------------------
mod_x = abs(max(eixo1c) -min(eixo1c))
mod_y = abs(max(eixo2c) -min(eixo2c))
#----------------------------------------------------------------
cmap_gray = (mpl.colors.ListedColormap(['darkgray', 'darkgray']))
#-----------------------
fig, ax = plt.subplots()
cp = plt.contourf(x_grid, y_grid, e2_grid, levels = n_contour, cmap = 'jet', alpha = 1.0, antialiased = True)
plt.quiver(0, 0, A1x, A1y, angles='xy', scale_units='xy', scale=1, color='black', label='A$_1$')
plt.quiver(0, 0, A2x, A2y, angles='xy', scale_units='xy', scale=1, color='black', label='A$_2$')
plt.text((A1x/2), (A1y/2), "A$_1$", fontsize=10, color="black")
plt.text((A2x/2), (A2y/2), "A$_2$", fontsize=10, color="black")
# plt.scatter(delta_X, delta_Y, c='black', marker='o', s=2)
# plt.scatter(x_min, y_min, c='black', marker='o', s=2)
cbar = fig.colorbar(cp, orientation = 'vertical', shrink = 1.0)
#-------------------
plt.title('xy-scan')
plt.xlabel('$\Delta$X' + '$\ ({\AA})$')
plt.ylabel('$\Delta$Y' + '$\ ({\AA})$')
cbar.set_label('$E-E_{min}\ $(meV/${\AA^2})$')
#---------------------------------------------
ax.set_box_aspect(mod_y/mod_x)
#------------------------------------------------------------------------------
plt.savefig('xy-scan_cartesian.png', dpi = 600, bbox_inches='tight', pad_inches = 0)
# plt.savefig('xy-scan_cartesian.pdf', dpi = 600, bbox_inches='tight', pad_inches = 0)
# plt.savefig('xy-scan_cartesian.eps', dpi = 600, bbox_inches='tight', pad_inches = 0)
# plt.savefig('xy-scan_cartesian.svg', dpi = 600, bbox_inches='tight', pad_inches = 0)


#--------------------------------------------------
shutil.copyfile(str(delta) + '/POSCAR', 'POSCAR')
shutil.copyfile(str(delta) + '/CONTCAR', 'CONTCAR')
#----------------------------------------------------


#=====================================================
info = open('info_xy-scan.dat', "w", encoding='utf-8')
info.write(f'====================================================== \n')
info.write(f'Displacement carried out over the 2nd material lattice   \n')
#------------------------------------------------------------------
info.write(f'Displacement_XY = ({x_min}, {y_min}) in Å \n')
info.write(f'Displacement_XY = ({a1_min}*A1, {a2_min}*A2) \n')
#----------------------------------------------------------------
# info.write(f'Displacement_XY = ({delta_X}, {delta_Y}) in Å \n')
# info.write(f'Displacement_XY = ({delta_A1}*A1, {delta_A2}*A2) \n')
info.write(f'------------------------------------------------------ \n')
info.write(f'ΔE = {Delta_E_meV:.12f} meV/Å^2  or  {Delta_E_J:.12f} J/m^2 \n')
info.write(f'====================================================== \n')
info.close()
#===========
