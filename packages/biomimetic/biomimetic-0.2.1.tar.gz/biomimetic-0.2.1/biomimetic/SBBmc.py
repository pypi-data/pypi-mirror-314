import numpy as np
from .SBmc import SimpleBiomimeticCell


class SimpleBiasBiomimeticCell(SimpleBiomimeticCell):
    def __init__(Cell, index, inputSize, memorySize, outputSize):
        super().__init__(index, inputSize, memorySize, outputSize)
        Cell.fireFlag = False
    
    def __str__(Cell):
        return f"SBBmc({Cell.index}, {Cell.inputSize}, {Cell.outputSize}, {Cell.activationFlag}, {Cell.fireFlag})"

    def fire(Cell, fireFlag: bool):
        Cell.fireFlag = fireFlag
        return Cell.outputArray if Cell.activationFlag and Cell.fireFlag else np.zeros(Cell.outputArray.shape) != 0


if __name__ == "__main__":
    # Test 1: Initialization
    cell = SimpleBiasBiomimeticCell(1, 3, 2, 2)
    print("Test 1: Initialization")
    print(cell)

    # Test 2: Learning
    print("\nTest 2: Learning")
    cell.learn([[1, 1, 1], [0, 1, 0]])
    print("Weight Array After Learning:")
    print(cell.weightArray)

    # Test 3: Activation with Matching Input
    print("\nTest 3: Activation with Matching Input")
    activations = cell.activate([1, 1, 1])
    print("Activations:", activations)
    print("Activation Flag:", cell.activationFlag)
    print(cell)

    # Test 4: Fire with fireFlag = False
    print("\nTest 4: Fire with fireFlag = False")
    cell.output([0, 1])
    output = cell.fire(False)
    print("Output Array:", output)
    print(cell)

    # Test 5: Fire with fireFlag = True
    print("\nTest 5: Fire with fireFlag = True")
    output = cell.fire(True)
    print("Output Array:", output)
    print(cell)

    # Test 6: Fire Without Activation
    print("\nTest 6: Fire Without Activation")
    cell.activate([0, 0, 0])  # No matching input
    output = cell.fire(True)
    print("Output Array (No Activation):", output)
    print(cell)
