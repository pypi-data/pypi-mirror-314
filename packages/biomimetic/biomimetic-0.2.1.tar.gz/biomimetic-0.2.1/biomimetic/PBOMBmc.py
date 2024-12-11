import numpy as np
from .POMBmc import ParallelOMBiomimeticCell


class ParallelOMBiasBiomimeticCell(ParallelOMBiomimeticCell):
    def __init__(Cell, index, inputSize, memorySize, outputSize, outputNums):
        super().__init__(index, inputSize, memorySize, outputSize, outputNums)
        Cell.fireFlags = np.zeros(outputNums, dtype=bool)

    def __str__(Cell):
        return f"PBOMBmc({Cell.index}, {Cell.inputSize}, {Cell.outputSize}, {Cell.activationFlag}, {Cell.fireFlags}, {Cell.outputNums})"

    def fire(Cell, fireFlags: np.array):
        Cell.fireFlags = fireFlags

        if not Cell.activationFlag: return np.zeros(Cell.outputsArray.shape) != 0
        
        result = np.zeros_like(Cell.outputsArray)
        for i in range(Cell.outputNums):
            if Cell.fireFlags[i]:
                result[i] = Cell.outputsArray[i]
            else:
                result[i] = np.zeros(Cell.outputsArray[i].shape) != 0

        return np.array(result)


if __name__ == "__main__":
    # Test 1: Initialization
    cell = ParallelOMBiasBiomimeticCell(1, 3, 2, 2, 3)
    print("Test 1: Initialization")
    print(cell)

    # Test 2: Fire with fireFlags all False
    print("\nTest 2: Fire with fireFlags = False")
    cell.learn([[1, 1, 1], [0, 1, 0]])
    cell.activate([1, 1, 1])
    cell.output([[0, 1], [1, 0], [1, 1]])
    output = cell.fire(np.array([False, False, False]))
    print("Output Array:", output)
    print(cell)

    # Test 3: Fire with fireFlag = True
    print("\nTest 3: Fire with fireFlags = True")
    output = cell.fire(np.array([True, True, True]))
    print("Output Array:", output)
    print(cell)
    
    # Test 4: Fire with fireFlag = True
    print("\nTest 4: Fire with mixed fireFlags")
    output = cell.fire(np.array([False, False, True]))
    print("Output Array:", output)
    print(cell)
