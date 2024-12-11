import numpy as np
from SBmc import SimpleBiomimeticCell


class ParallelMOBiomimeticCell(SimpleBiomimeticCell):
    def __init__(Cell, index, inputNums, inputSize, memorySize, outputSize):
        super().__init__(index, inputSize, memorySize, outputSize)
        Cell.inputNums = inputNums
        Cell.inputArrays = np.zeros((inputNums, inputSize))
        Cell.weightArrays = np.zeros((inputNums, memorySize, inputSize))
        Cell.activationFlags = np.zeros(inputNums, dtype=bool)

    def __str__(Cell):
        return f"PMOBmc({Cell.index}, {Cell.inputSize}, {Cell.outputSize}, {Cell.activationFlags}, {Cell.inputNums})"

    def learn(Cell, featuresValues: np.array):
        Cell.weightArrays = np.array(featuresValues)

    def activate(Cell, inputValues: np.array):
        Cell.inputArrays = inputValues
        activationSheet = []
        for i in range(Cell.inputNums):
            matches = np.logical_not(np.logical_xor(Cell.weightArrays[i], Cell.inputArrays[i])).all(axis=1)
            activationSheet.append(matches.astype(int))
            Cell.activationFlags[i] = np.any(matches)
        return np.array(activationSheet)

    def fire(Cell):
        return Cell.outputArray if np.all(Cell.activationFlags) else np.zeros(Cell.outputArray.shape) != 0


if __name__ == "__main__":
    # Test 1: Initialization
    cell = ParallelMOBiomimeticCell(1, 2, 3, 2, 2)
    print("Test 1: Initialization")
    print(cell)

    # Test 2: Learning and Activation
    print("\nTest 2: Learning and Activation")
    cell.learn([[[1, 1, 1], [0, 1, 0]], [[1, 0, 1], [0, 0, 1]]])
    activations = cell.activate([[1, 1, 1], [1, 0, 1]])
    print("Activation Sheet:", activations)
    print("Activation Flags:", cell.activationFlags)
    print(cell)

    # Test 3: Fire with Activation
    print("\nTest 3: Fire with Activation")
    cell.output([1, 0])
    output = cell.fire()
    print("Output Array After Fire:", output)

    # Test 4: Fire Without Activation
    print("\nTest 4: Fire Without Activation")
    cell.activate([[0, 0, 0], [0, 0, 0]])
    output = cell.fire()
    print("Output Array After Fire (No Activation):", output)
    print(cell)
  