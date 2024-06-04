import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List

"""
input:
    v1 (np.array) : vector n-dim in standard basis
    U: (np.array) : orthogornal matrix 
    
output: 
    v2 (np.array):  vector n-dim in U basis
    
Math intuition: Orthogornal matrix U rotate v1 into v2

Options: 
    Define theta --> Find v2 and matrix U
"""

class Input:
    def _read_vector_input(self) -> np.array:
        inp_vec = input("Enter vector: \n")
        return np.array(list(map(eval, inp_vec.split())))
        
    def _read_matrix_input(self) -> np.array:
        print("Enter matrix: \n")
        lines = []
        while True:
            line = input()
            if not line.strip():
                break
            lines.append(line)
        return np.array([list(map(eval, line.split())) for line in lines])
    

class Validator:
    
    def length(self, a: List[int]) -> float:
        return sum([a[i]**2 for i in range(len(a))]) **(1/2)
    
    def orthogonal(self, u1: np.array, u2: np.array) -> None:
            if u1 @ u2 != 0: 
                raise "Error, basis U contains unorthogonal vectors"
    
    def valid(self, U: np.array, v: np.array):
        if U.shape[0] != v.shape[0]: 
            raise "Error, vector v and matrix U are not in the same R space"
        
        for i in range(U.shape[0]):
            if self.length(U[i]) != 1.0: 
                raise "Error, basis U contains unorthogonal vectors"
            if i == U.shape[0]-1: continue
            self.orthogonal(U[i], U[i+1])
            
class Logic:
    
    def compute(self, U: np.array, v1: np.array) -> None:
        v1 = np.array([1/2, 3])
        v2 = v1 @ U.T
        self.vis(v1, v2)
    
    def vis(self, v1: np.array, v2: np.array) -> None:
    
        origin = np.array([0, 0])
        fig, ax = plt.subplots()
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.grid(True)

        quiver_v1 = ax.quiver(*origin, *v1, angles='xy', scale_units='xy', scale=1, color='red')
        quiver_v2 = ax.quiver(*origin, *v2, angles='xy', scale_units='xy', scale=1, color='blue')
        
        def interpolate_vectors(v1, v2, t):
            return v1 * (1 - t) + v2 * (t)

        def update(frame):
            t = frame / 100 
            v_interpolated = interpolate_vectors(v1, v2, t)
            quiver_v1.set_UVC(v_interpolated[0], v_interpolated[1])
            return quiver_v1,

        ani = FuncAnimation(fig, update, frames=101, interval=50, blit=True)
        plt.show()

class Visualization:
    def __init__(self, input_loader: Input, validator: Validator, logic: Logic):
        self._menu_options = {
            "1": ("Option 1: input matrix U and vector v1", self._option1),
            "2": ("Option 2: input vector v1 and vector v2", self._option2),
            "3": ("Option 3: input rotation theta", self._option3),
            "4": ("Option 4: ", self._option4),
        }
        self.input_loader = input_loader
        self._validator = validator
        self._logic = logic
    
    def _option1(self) -> None:
        self.U = self.input_loader._read_matrix_input()
        self.v1 = self.input_loader._read_vector_input()
        
        self._validator.valid(self.U, self.v1)
        self._logic.compute(self.U, self.v1)
        
        
    def _option2(self):
        ...
    
    def _option3(self):
        ...
        
    def _option4(self):
        ...

    def _print_menu(self):
        for key, (description, _) in self._menu_options.items():
            print(f"{key}. {description}")
    
    def run(self):
        while True:
            self._print_menu()
            choice = input("Choose an option: ")

            if choice in self._menu_options:
                _, action = self._menu_options[choice]
                if action: action()
                else: break
            else:
                print("Invalid choice!")

            input("Press Enter to continue...")
            
            
if __name__ == "__main__":
    input_loader = Input()
    validator = Validator()
    logic = Logic()
    vis = Visualization(input_loader=input_loader, validator=validator, logic=logic)
    vis.run()