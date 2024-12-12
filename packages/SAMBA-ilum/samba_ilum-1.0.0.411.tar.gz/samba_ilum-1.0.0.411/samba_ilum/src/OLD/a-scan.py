# SAMBA_ilum Copyright (C) 2024 - Closed source


import numpy as np
import shutil
import os


passo = replace_passo   # Variação no módulo do vetores de rede em Angs.
range = replace_range   # Range de variação (em Angs.) com relação ao parâmetro de rede [param -range, param +range]


"""
#----------------------------------------------------------------
# Testando a compatibilidade do arquivo POSCAR ------------------
#----------------------------------------------------------------
poscar = open('POSCAR', "r")
VTemp = poscar.readline().split()
poscar.close()
#-------------
crit = 0
for k in range(len(VTemp)):
    try:
       inteiro = int(VTemp[k])
       if (k > 0 and k < 3): crit += 1
    except ValueError:
       if (k == 0):  crit += 1
    #------------------------------
    if (len(VTemp) < 3 or crit < 3):
       print(f' ')
       print(f'========================================')
       print(f'Verifique o arquivo POSCAR utilizado!   ')
       print(f'INCOMPATIBILIDADE com o código detectada')
       print(f'========================================')
       print(f' ')
       #==========
       sys.exit()   
       #=========
"""


#==========================================================================
# Obtendo os vetores de rede da Heteroestrutura ===========================
#==========================================================================
contcar = open('CONTCAR', "r")
#-----------------------------
VTemp = contcar.readline()
VTemp = contcar.readline();  param = float(VTemp)
VTemp = contcar.readline().split();  A1x = float(VTemp[0])*param;  A1y = float(VTemp[1])*param;  A1z = float(VTemp[2])*param
VTemp = contcar.readline().split();  A2x = float(VTemp[0])*param;  A2y = float(VTemp[1])*param;  A2z = float(VTemp[2])*param
VTemp = contcar.readline().split();  A3x = float(VTemp[0])*param;  A3y = float(VTemp[1])*param;  A3z = float(VTemp[2])*param
VTemp = contcar.readline()
VTemp = contcar.readline().split(); nions = 0
for i in np.arange(len(VTemp)):
    nions += int(VTemp[i])
#--------------
contcar.close()
#--------------


#==========================================================================
# Obtendo o fator percentual de multiplicação dos vetores de Rede =========
#==========================================================================
A1 = np.array([float(A1x), float(A1y), float(A1z)])*param;  module_a1 = float(np.linalg.norm(A1))
A2 = np.array([float(A2x), float(A2y), float(A2z)])*param;  module_a2 = float(np.linalg.norm(A2))
A3 = np.array([float(A3x), float(A3y), float(A3z)])*param;  module_a3 = float(np.linalg.norm(A3))
#------------------------------------------------------------------------------------------------
if (module_a1 <= module_a2):
   fator = ((module_a1 +passo)/module_a1) -1
   vector = 'A1'
if (module_a2 < module_a1):
   fator = ((module_a2 +passo)/module_a2) -1
   vector = 'A2'
# if ((type_lattice = 3) and (module_a3 < module_a1) or (module_a3 < module_a2)):
#    fator = ((module_a3 +passo)/module_a3) -1
#    vector = 'A3'
#------------------------------------------------------------


n_passos = (range/passo)
#------------------------------------------------------------
if ((n_passos -int(n_passos)) == 0): n_passos = int(n_passos)
if ((n_passos -int(n_passos)) != 0): n_passos = int(n_passos) +1 


n_passos = int(range/passo)
number = 0


#============================================================
# Gerando os arquivos POSCAR para cada valor de a (param) ===
#============================================================

for i in np.arange(1,(n_passos)+1):
    #----------
    number += 1
    i = n_passos +1 -i
    fator_new = float(1 -(i*fator))
    #---------------------------------------------
    dir_temp = str(fator_new);  os.mkdir(dir_temp)
    if os.path.isfile('vdw_kernel.bindat'): shutil.copyfile('vdw_kernel.bindat', dir_temp + '/vdw_kernel.bindat')
    shutil.copyfile('contcar_update.py', dir_temp + '/contcar_update.py')
    shutil.copyfile('energy_scan.py', dir_temp + '/energy_scan.py')
    shutil.copyfile('KPOINTS', dir_temp + '/KPOINTS')
    shutil.copyfile('POTCAR', dir_temp + '/POTCAR')
    shutil.copyfile('INCAR', dir_temp + '/INCAR')
    #--------------------------------------------
    contcar = open('CONTCAR', "r")
    poscar_new = open(dir_temp + '/POSCAR', "w") 
    VTemp = contcar.readline();  poscar_new.write(f'{VTemp}')
    VTemp = contcar.readline();  poscar_new.write(f'{VTemp}')
    #--------------------------------------------------------
    VTemp = contcar.readline().split();  poscar_new.write(f'{float(VTemp[0])*fator_new} {float(VTemp[1])*fator_new} {float(VTemp[2])*fator_new} \n')
    VTemp = contcar.readline().split();  poscar_new.write(f'{float(VTemp[0])*fator_new} {float(VTemp[1])*fator_new} {float(VTemp[2])*fator_new} \n')
    VTemp = contcar.readline().split();  poscar_new.write(f'{float(VTemp[0])*fator_new} {float(VTemp[1])*fator_new} {float(VTemp[2])*fator_new} \n')
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    VTemp = contcar.readline();  poscar_new.write(f'{VTemp}')
    VTemp = contcar.readline();  poscar_new.write(f'{VTemp}')
    VTemp = contcar.readline();  poscar_new.write(f'Direct \n')
    #---------------------------------------------------------
    for j in np.arange(nions):
        VTemp = contcar.readline();  poscar_new.write(f'{VTemp}')
    #--------------
    contcar.close()   
    poscar_new.close()
    #-----------------


for i in np.arange(1,2):
    #----------
    number += 1
    fator_new = 1.0
    #---------------------------------------------
    dir_temp = str(fator_new);  os.mkdir(dir_temp)
    if os.path.isfile('vdw_kernel.bindat'): shutil.copyfile('vdw_kernel.bindat', dir_temp + '/vdw_kernel.bindat')
    shutil.copyfile('contcar_update.py', dir_temp + '/contcar_update.py')
    shutil.copyfile('energy_scan.py', dir_temp + '/energy_scan.py')
    shutil.copyfile('KPOINTS', dir_temp + '/KPOINTS')
    shutil.copyfile('POTCAR', dir_temp + '/POTCAR')
    shutil.copyfile('INCAR', dir_temp + '/INCAR')
    #--------------------------------------------
    contcar = open('CONTCAR', "r")
    poscar_new = open(dir_temp + '/POSCAR', "w") 
    VTemp = contcar.readline();  poscar_new.write(f'{VTemp}')
    VTemp = contcar.readline();  poscar_new.write(f'{VTemp}')
    #--------------------------------------------------------
    VTemp = contcar.readline().split();  poscar_new.write(f'{float(VTemp[0])*fator_new} {float(VTemp[1])*fator_new} {float(VTemp[2])*fator_new} \n')
    VTemp = contcar.readline().split();  poscar_new.write(f'{float(VTemp[0])*fator_new} {float(VTemp[1])*fator_new} {float(VTemp[2])*fator_new} \n')
    VTemp = contcar.readline().split();  poscar_new.write(f'{float(VTemp[0])*fator_new} {float(VTemp[1])*fator_new} {float(VTemp[2])*fator_new} \n')
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    VTemp = contcar.readline();  poscar_new.write(f'{VTemp}')
    VTemp = contcar.readline();  poscar_new.write(f'{VTemp}')
    VTemp = contcar.readline();  poscar_new.write(f'Direct \n')
    #----------------------------------------------------------
    for j in np.arange(nions):
        VTemp = contcar.readline();  poscar_new.write(f'{VTemp}')
    #--------------
    contcar.close()   
    poscar_new.close()
    #-----------------


for i in np.arange(1,(n_passos)+1):
    #----------
    number += 1
    fator_new = float(1 +(i*fator))
    #---------------------------------------------
    dir_temp = str(fator_new);  os.mkdir(dir_temp)
    if os.path.isfile('vdw_kernel.bindat'): shutil.copyfile('vdw_kernel.bindat', dir_temp + '/vdw_kernel.bindat')
    shutil.copyfile('contcar_update.py', dir_temp + '/contcar_update.py')
    shutil.copyfile('energy_scan.py', dir_temp + '/energy_scan.py')
    shutil.copyfile('KPOINTS', dir_temp + '/KPOINTS')
    shutil.copyfile('POTCAR', dir_temp + '/POTCAR')
    shutil.copyfile('INCAR', dir_temp + '/INCAR')
    #--------------------------------------------
    contcar = open('CONTCAR', "r")
    poscar_new = open(dir_temp + '/POSCAR', "w") 
    VTemp = contcar.readline();  poscar_new.write(f'{VTemp}')
    VTemp = contcar.readline();  poscar_new.write(f'{VTemp}')
    #--------------------------------------------------------
    VTemp = contcar.readline().split();  poscar_new.write(f'{float(VTemp[0])*fator_new} {float(VTemp[1])*fator_new} {float(VTemp[2])*fator_new} \n')
    VTemp = contcar.readline().split();  poscar_new.write(f'{float(VTemp[0])*fator_new} {float(VTemp[1])*fator_new} {float(VTemp[2])*fator_new} \n')
    VTemp = contcar.readline().split();  poscar_new.write(f'{float(VTemp[0])*fator_new} {float(VTemp[1])*fator_new} {float(VTemp[2])*fator_new} \n')
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    VTemp = contcar.readline();  poscar_new.write(f'{VTemp}')
    VTemp = contcar.readline();  poscar_new.write(f'{VTemp}')
    VTemp = contcar.readline();  poscar_new.write(f'Direct \n')
    #----------------------------------------------------------
    for j in np.arange(nions):
        VTemp = contcar.readline();  poscar_new.write(f'{VTemp}')
    #--------------
    contcar.close()   
    poscar_new.close()
    #-----------------
