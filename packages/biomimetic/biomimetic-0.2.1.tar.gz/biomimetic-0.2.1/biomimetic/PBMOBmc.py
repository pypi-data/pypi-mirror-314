import numpy as np
from .PMOBmc import ParallelMOBiomimeticCell


class ParallelMOBiasBiomimeticCell(ParallelMOBiomimeticCell):
    def __init__(Cell, index, inputNums, inputSize, memorySize, outputSize):
        super().__init__(index, inputNums, inputSize, memorySize, outputSize)
        Cell.fireFlag = False

    def __str__(Cell):
        return f"PBMOBmc({Cell.index}, {Cell.inputSize}, {Cell.outputSize}, {Cell.activationFlags}, {Cell.fireFlag}, {Cell.inputNums})"

    def fire(Cell, fireFlag: bool):
        Cell.fireFlag = fireFlag
        return Cell.outputArray if np.all(Cell.activationFlags) and Cell.fireFlag else np.zeros(Cell.outputArray.shape)


if __name__ == "__main__":
    # Test 1: Initialization
    cell = ParallelMOBiasBiomimeticCell(1, 2, 3, 2, 2)
    print("Test 1: Initialization")
    print(cell)

    # Test 2: Fire with fireFlag = False
    print("\nTest 2: Fire with fireFlag = False")
    cell.learn([[[1, 1, 1], [0, 1, 0]], [[1, 0, 1], [0, 0, 1]]])
    cell.activate([[1, 1, 1], [1, 0, 1]])
    cell.output([1, 0])
    output = cell.fire(False)
    print("Output Array:", output)
    print(cell)

    # Test 3: Fire with fireFlag = True
    print("\nTest 3: Fire with fireFlag = True")
    output = cell.fire(True)
    print("Output Array:", output)
    print(cell)
