"""
"Implementación de sistemas multiagentes aplicado a la limpieza"

Por: Daniel Yamamoto

Fecha de entrega: 10/11/2021
"""

from matplotlib import pyplot as plt
from numpy.core.numeric import count_nonzero

import matplotlib.patches as mpl_patches
import numpy as np
import time

# Crea plot del tablero
def plotMaze(maze, fig, name_fig, time, por_dirty, tot_moves):
    fig.clf()
    ax = fig.add_subplot(1, 1, 1)
    ax.matshow(maze, cmap=plt.cm.bone)
    ax.title.set_text(name_fig)
    ax.set_xticks([])
    ax.set_yticks([])
    # Texto dentro de la gráfica
    textstr = []
    textstr.append("Used time: {0:.1f}sec".format(time))
    textstr.append("Clean porcentage: {0:.2f}%".format(por_dirty))
    textstr.append("Total moves: {0}".format(tot_moves))
    # Propiedades del cuadro de texto
    handles = [mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", lw=0, alpha=0)] * 3
    # Asigna el texto en un cuadro fijo
    ax.legend(handles, textstr, loc='best', fontsize='small', fancybox=True, framealpha=1, handlelength=0, handletextpad=0)
    # Dibujamos el plot
    plt.xlabel("Axis X", fontsize=14)
    plt.ylabel("Axis Y", fontsize=14)
    plt.draw()
    plt.pause(0.000001)

# Creación del tablero
def create_board(num_row, num_col, por_dirty_spaces):
    # Inicialización de la matriz
    board = np.zeros((num_row, num_col))
    # Calculamos los espacios sucios
    num_dirty = num_row * num_col * (por_dirty_spaces / 100)
    count = 1
    # Asignamos los espacios sucios
    while count < num_dirty:
        x = np.random.randint(num_col)
        y = np.random.randint(num_row)
        if board[y, x] == 0:
            count = count + 1
            board[y, x] = 1
    return board

# Inicializa los agentes en la posición 1,1
def init_agents(num_agents, board):
    agents = np.zeros((num_agents, 2), dtype=int)
    for i in range(num_agents):
        agents[i] = [1, 1]
    return agents, board

# Movimiento de los agentes
def do_action(agents, board, num_agents):
    num_row, num_col = board.shape
    cur_pos = agents[num_agents, :]
    ran_x = np.random.randint(-1, 2)
    ran_y = np.random.randint(-1, 2)
    row_possible = cur_pos[0] + ran_y >= 0 and cur_pos[0] + ran_y < num_row
    col_possible = cur_pos[1] + ran_x >= 0 and cur_pos[1] + ran_x < num_col
    if row_possible and col_possible:
        row_possible = cur_pos[0] + ran_y
        col_possible = cur_pos[1] + ran_x
        board[cur_pos[0], cur_pos[1]] = 0
        agents[num_agents, :] = [row_possible, col_possible]
    return agents, board

# Ciclo de los movimientos de los agentes
def run_time(agents, board, num_agents, max_time, por_dirty):
    # Plot inicial
    fig = plt.figure(figsize = (8, 8))
    plotMaze(board, fig, "Board dirty", 0, por_dirty, 0)
    plt.pause(1)
    # Inicialización del tiempo
    t = time.time()
    all_clean = False
    elapsed, tot_moves, por_clean = 0, 0, 0
    num_row, num_col = board.shape
    
    while elapsed < max_time and all_clean == False:
        for n in range(num_agents):
            agents, board = do_action(agents, board, n)
            tot_moves = tot_moves + 1
        # Copia del board
        boardCopy = board.copy()
        for n in range(num_agents):
            boardCopy[agents[n, 0], agents[n, 1]] = 2
        # Comprobamos si el table ya esta limpio
        if np.all((board == 0)):
            all_clean = True
        # Calculamos el porcentaje de limpieza
        por_clean = count_nonzero(board == 1)
        por_clean = por_clean / (num_col * num_row) * 100
        # Actualizamos el tiempo
        elapsed = time.time() - t
        # Actualizamos el plot
        plotMaze(board, fig, "Board with agents", elapsed, 100 - por_clean, tot_moves)
    plt.pause(3)
    return board, elapsed, tot_moves, por_clean

def main():
    num_agents = 10
    num_row, num_col = 20, 20
    por_dirty = 50
    max_time = 20
    # Inicialización del tablero
    board = create_board(num_row, num_col, por_dirty)
    # Inicialización de los agentes
    agents, board = init_agents(num_agents, board)
    # Run time
    board, tot_time, tot_moves, por_dirty = run_time(agents, board, num_agents, max_time, por_dirty)
    print(f'Used time {round(tot_time, 2)} of {max_time} seconds')
    print(f'Clean porcentage: {100 - por_dirty} %' )
    print(f'Total moves: {tot_moves}' )

if __name__ == '__main__':
    main()