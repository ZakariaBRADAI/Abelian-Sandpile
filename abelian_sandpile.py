def topple(grid, x_topple, y_topple):
    """Defines the topple rule."""

    nb_topples = grid[x_topple, y_topple] // 4
    grid[x_topple, y_topple] %= 4
    grid = pour(grid, x_topple, y_topple, nb_topples)
    return grid


def pour(grid, x_topple, y_topple, nb_topples):
    """Pours toppeling grains on the neighbor cases."""

    if x_topple > 0:
        grid[x_topple - 1, y_topple] += nb_topples

    if x_topple < grid.shape[0] - 1:
        grid[x_topple + 1, y_topple] += nb_topples

    if y_topple > 0:
        grid[x_topple, y_topple - 1] += nb_topples

    if y_topple < grid.shape[1] - 1:
        grid[x_topple, y_topple + 1] += nb_topples

    return grid


def stabilize(grid):
    """Defines the stabilization of a sandpile."""

    unstable_indexes = np.array(np.where(grid >= 4))

    while len(unstable_indexes[0]) > 0:
        for i in range(0, len(unstable_indexes[0])):
            x_topple = unstable_indexes[0, i]
            y_topple = unstable_indexes[1, i]
            grid = topple(grid, x_topple, y_topple)

        unstable_indexes = np.array(np.where(grid >= 4))

    return grid


class AbelianSandpile:

    
    def __init__(self, grid):
        self.grid = grid
        self.abelian_grid = grid
        self.shape = self.grid.shape

        self.avalanches_size = 0 #np.array([])
        self.topple_profil = np.zeros(self.shape)

        if self.shape[0] == self.shape[1]:
            self.geometry = "square"

        else:
            self.geometry = "rectangle"

        self.beta_grid = np.zeros(self.shape)

        match self.geometry:
            case "square":
                for i in range(0, self.shape[0]):
                    self.beta_grid[i, 0] += 1
                    self.beta_grid[0, i] += 1
                    self.beta_grid[i, -1] += 1
                    self.beta_grid[-1, i] += 1
            case "rectangle":
                for i in range(0, self.shape[0]):
                    self.beta_grid[i, 0] += 1
                    self.beta_grid[i, -1] += 1

                for j in range(0, self.shape[1]):
                    self.beta_grid[0, j] += 1
                    self.beta_grid[-1, j] += 1

        self.thermical_algorithm()

    def stabilze_abelian_grid(self):
        '''
        Also defines the stabilization of the abelian grid
        but counts the number and size of avalanches.

        Used during the perturbation processus.
        '''

        unstable_indexes = np.array(np.where(self.abelian_grid >= 4))
    
        while len(unstable_indexes[0]) > 0:
            self.avalanches_size += unstable_indexes.size
            for i in range(0, len(unstable_indexes[0])):
                x_topple = unstable_indexes[0, i]
                y_topple = unstable_indexes[1, i]
                self.abelian_grid = topple(self.abelian_grid, x_topple, y_topple)
                self.topple_profil[x_topple, y_topple] += 1
                #self.avalanches_size = np.append(self.avalanches_size, len(unstable_indexes[0]))
            
                
            unstable_indexes = np.array(np.where(self.abelian_grid >= 4))
            ###
    

    def __add__(self, other):
        """
        Defines the addition of sandpiles.
        By default the addition of two sandpiles returns
        the addition of their abelian grids.
        """

        if hasattr(other, "abelian_grid"):
            return stabilize(self.abelian_grid + other.abelian_grid)

        else:
            raise TypeError("can only add abelian sandpile to another abelian sandpile")

    def beta_operator(self):
        """Computes beta operator application on the sandpile"""

        self.abelian_grid = stabilize(self.abelian_grid + self.beta_grid)

    def thermical_algorithm(self):
        """Computes Dhar's thermical algorithm"""

        mask = np.copy(self.abelian_grid)
        self.beta_operator()

        while not (np.array_equal(self.abelian_grid, mask)):
            mask = np.copy(self.abelian_grid)
            self.beta_operator()

    def perturb(self, N=50000):
        '''Defines ther perturbation processus on the sandpile.'''
        
        mean_hight = [np.mean(self.abelian_grid)]
        tab_avalanches_size = []
        self.avalanches_size = 0
        for i in range(N):
            x_perturb = np.random.randint(0, self.shape[0])
            y_perturb = np.random.randint(0, self.shape[1])
            self.abelian_grid[x_perturb, y_perturb] += 1
            self.stabilze_abelian_grid()
            mean_hight.append(np.mean(self.abelian_grid))
            tab_avalanches_size.append(self.avalanches_size)
            self.avalanches_size = 0 
            
        avalanches_frequency = []

        
        
        for size in tab_avalanches_size:
            avalanches_frequency.append( tab_avalanches_size.count(size))

        tab_avalanches_size = np.array(tab_avalanches_size)
        avalanches_frequency = np.array(avalanches_frequency)
        mean_hight = np.array(mean_hight)
        
        return mean_hight, tab_avalanches_size, avalanches_frequency

    def plot_grid(self):
        '''Plots the abelian grid of the sandpile.'''

        plt.figure()
        plt.imshow(self.abelian_grid, cmap='Greys')
        plt.colorbar()
        plt.show()    
