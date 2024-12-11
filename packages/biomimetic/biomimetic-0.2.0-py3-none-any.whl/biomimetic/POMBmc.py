import numpy as np
from SBmc import SimpleBiomimeticCell


class ParallelOMBiomimeticCell(SimpleBiomimeticCell):
    def __init__(Cell, index, inputSize, memorySize, outputSize, outputNums):
        super().__init__(index, inputSize, memorySize, outputSize)
        Cell.outputNums = outputNums
        Cell.outputsArray = np.zeros((outputNums, outputSize))

    def __str__(Cell):
        return f"POMBmc({Cell.index}, {Cell.inputSize}, {Cell.outputSize}, {Cell.activationFlag}, {Cell.outputNums})"

    def output(Cell, targetValues: np.array):
        Cell.outputsArray = np.array(targetValues)

    def fire(Cell):
        return Cell.outputsArray if Cell.activationFlag else np.zeros(Cell.outputsArray.shape) != 0


if __name__ == "__main__":
    # Test 1: Initialization
    cell = ParallelOMBiomimeticCell(1, 3, 2, 2, 3)
    print("Test 1: Initialization")
    print(cell)

    # Test 2: Learning and Activation
    print("\nTest 2: Learning and Activation")
    cell.learn([[1, 1, 1], [0, 1, 0]])
    activations = cell.activate([1, 1, 1])
    print("Activations:", activations)
    print("Activation Flag:", cell.activationFlag)
    print(cell)

    # Test 3: Output and Fire with Activation
    print("\nTest 3: Output and Fire with Activation")
    cell.output([[0, 1], [1, 0], [1, 1]])
    output = cell.fire()
    print("Output Array After Fire:", output)

    # Test 4: Fire Without Activation
    print("\nTest 4: Fire Without Activation")
    cell.activate([0, 0, 0])
    print("Activation Flag:", cell.activationFlag)
    output = cell.fire()
    print("Output Array After Fire (No Activation):", output)
    print(cell)
