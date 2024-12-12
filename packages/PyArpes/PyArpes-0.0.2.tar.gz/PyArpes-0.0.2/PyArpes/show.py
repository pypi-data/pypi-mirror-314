
import numpy as np
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from math import cos, sin, pi


class Igor(object, ):
    def __init__(self) -> None:

        """
        =======================================================================
        PACKAGE: Data Post-Processing Package for ARPES Data
        Author: Bin CAO <binjacobcao@gmail.com> 
        Guangzhou Municipal Key Laboratory of Materials Informatics, Advanced Materials Thrust,
        Hong Kong University of Science and Technology (Guangzhou), Guangzhou 511400, Guangdong, China
        =======================================================================
        Please feel free to open issues on GitHub:
        https://github.com/Bin-Cao/MultiBgolearn
        or 
        contact Bin Cao (bcao686@connect.hkust-gz.edu.cn) with any issues, comments, or suggestions 
        regarding the usage of this code.
        """
        os.makedirs('arpes_plots', exist_ok=True)
    

    def dispersion(self,file_loc, Columns_range=None, E_photon=25, work_function=4.28, E_Bind=0, alpha=1, beta=-8.11399, 
               Rows=834, R_Start=-2.2675, R_Delta=0.003, R_Units='Kinetic Energy [eV]',
               Columns=489, C_Start=-17.6403, C_Delta=0.0682412, C_Units='Y-Scale [deg]', 
               cmap='coolwarm', fontsize=16):
        """
        Visualize the ARPES dispersion data as a colormap.

        Reference:
            Zhang H, Pincelli T, Jozwiak C, et al. Angle-resolved photoemission spectroscopy[J]. Nature Reviews Methods Primers, 2022, 2(1): 54.

        Parameters:
            file_loc (str): Path to the data file containing the ARPES data.
            Columns_range (list, optional): Range of column values to display (e.g., [-14, 15]).
            E_photon (float): Energy of incident photon in eV (default is 25 eV).
            work_function (float): Work function of the instrument in eV (default is 4.28 eV).
            E_Bind (float): Binding energy of electrons in eV (default is 0 eV).
            alpha (float): Angle alpha in degrees (default is 1°).
            beta (float): Angle beta in degrees (default is -8.11399°).
            Rows (int): Number of rows (N) in the data (default is 834).
            R_Start (float): Starting value for rows (energy in eV) (default is -2.2675 eV).
            R_Delta (float): Step size for rows (energy step in eV) (default is 0.003 eV).
            R_Units (str): Units for rows (default is 'Kinetic Energy [eV]').
            Columns (int): Number of columns (M) in the data (default is 489).
            C_Start (float): Starting value for columns (Y-scale angle in degrees) (default is -17.6403°).
            C_Delta (float): Step size for columns (angle step in degrees) (default is 0.0682412°).
            C_Units (str): Units for columns (default is 'Y-Scale [deg]').
            cmap (str): Colormap style for the plot (default is 'coolwarm').
            fontsize (int): Font size for labels, title, and ticks (default is 14).

        Returns:
            None: Displays the plot and saves it to files.
        
        E.g.,
            PyArpes.Igor().dispersion(file_loc = './data.txt')
        """
        
        # Calculate the photoelectron energy based on photon energy, work function, and binding energy
        Ein = E_photon - work_function - E_Bind
        
        # Read the data from the file
        try:
            data = np.loadtxt(file_loc)
        except Exception as e:
            print(f"Error reading file: {e}")
            return

        # Ensure the data dimensions match the provided parameters
        if data.shape != (Rows, Columns):
            print(f"Error: Data dimensions {data.shape} do not match the specified dimensions ({Rows}, {Columns}).")
            return

        # Generate row and column axis values
        row_values = np.linspace(R_Start, R_Start + (Rows - 1) * R_Delta, Rows)
        col_values = np.linspace(C_Start, C_Start + (Columns - 1) * C_Delta, Columns)
        
        # Filter columns based on Columns_range if specified
        if Columns_range is not None:
            col_min, col_max = Columns_range
            col_indices = np.where((col_values >= col_min) & (col_values <= col_max))[0]
            data_filtered = data[:, col_indices]
            col_values_filtered = col_values[col_indices]
        else:
            data_filtered = data
            col_values_filtered = col_values
        
        # Plot the data using the chosen colormap
        plt.figure(figsize=(10, 6))
        mesh = plt.pcolormesh(col_values_filtered, row_values, data_filtered, shading='auto', cmap=cmap)
        cbar = plt.colorbar(mesh)
        cbar.set_label('Intensity', fontsize=fontsize, fontweight='bold', family='Arial')

        # Set font style and sizes for labels and title
        plt.xlabel(C_Units, fontsize=fontsize, fontweight='bold', family='Arial')
        plt.ylabel(R_Units, fontsize=fontsize, fontweight='bold', family='Arial')
        plt.title('Dispersion', fontsize=fontsize, fontweight='bold', family='Arial')

        # Adjust the tick labels to be larger
        plt.xticks(fontsize=fontsize)
        plt.yticks(fontsize=fontsize)

        # Colorbar index settings (making sure it's bold and larger)
        cbar.ax.tick_params(labelsize=fontsize, labelcolor='black', width=1, size=7)

        # Save and show the plot
        plt.tight_layout()
        plt.savefig('./arpes_plots/dispersion_plot_degree.png', dpi=500)
        plt.savefig('./arpes_plots/dispersion_plot_degree.svg', dpi=500)
        plt.show()

        # Convert degrees to radians for angle-based calculations
        col_values_filtered_rad = np.radians(col_values_filtered)
        
        # Calculate Kxin using the provided formula 
        Kxin = 0.512 * np.sqrt(Ein) * (np.cos(np.radians(beta)) * np.sin(np.radians(alpha)) + 
                                    np.sin(np.radians(beta)) * np.cos(col_values_filtered_rad) * np.cos(np.radians(alpha)))

        # Plot the dispersion in K space
        plt.figure(figsize=(10, 6))
        mesh = plt.pcolormesh(Kxin, row_values, data_filtered, shading='auto', cmap=cmap)
        cbar = plt.colorbar(mesh)
        cbar.set_label('Intensity', fontsize=fontsize, fontweight='bold', family='Arial')

        # Set font style and sizes for labels and title
        plt.xlabel('Kxin', fontsize=fontsize, fontweight='bold', family='Arial')
        plt.ylabel(R_Units, fontsize=fontsize, fontweight='bold', family='Arial')
        plt.title('Dispersion in K', fontsize=fontsize, fontweight='bold', family='Arial')

        # Adjust the tick labels to be larger
        plt.xticks(fontsize=fontsize)
        plt.yticks(fontsize=fontsize)

        # Colorbar index settings
        cbar.ax.tick_params(labelsize=fontsize, labelcolor='black', width=1, size=7)

        # Save and show the plot
        plt.tight_layout()
        plt.savefig('./arpes_plots/dispersion_plot_K.png', dpi=500)
        plt.savefig('./arpes_plots/dispersion_plot_K.svg', dpi=500)
        plt.show()





