import numpy as np


class SimpleBiomimeticCell:
    def __init__(Cell, index, inputSize, memorySize, outputSize):
        Cell.index = index
        Cell.inputSize = inputSize
        Cell.outputSize = outputSize
        Cell.inputArray = np.zeros((1, inputSize))
        Cell.weightArray = np.zeros((memorySize, inputSize))
        Cell.outputArray = np.zeros((1, outputSize))
        Cell.activationFlag = False

    def __str__(Cell):
        return f"SBmc({Cell.index}, {Cell.inputSize}, {Cell.outputSize}, {Cell.activationFlag})"

    def learn(Cell, featuresValue: np.array):
        Cell.weightArray = np.array(featuresValue)

    def output(Cell, targetValue: np.array):
        Cell.outputArray = np.array(targetValue)

    def activate(Cell, inputValue: np.array):
      Cell.inputArray = np.array(inputValue)
      matches = np.logical_not(np.logical_xor(Cell.weightArray, Cell.inputArray)).all(axis=1)
      activations = matches.astype(int)
      Cell.activationFlag = np.any(matches)
      return activations
    
    def fire(Cell):
        return Cell.outputArray if Cell.activationFlag else np.zeros(Cell.outputArray.shape) != 0


if __name__ == "__main__":
    # Test 1: Initialization
    cell = SimpleBiomimeticCell(1, 3, 2, 2)
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

    # Test 4: Activation with Non-Matching Input
    print("\nTest 4: Activation with Non-Matching Input")
    activations = cell.activate([0, 0, 0])
    print("Activations:", activations)
    print("Activation Flag:", cell.activationFlag)
    print(cell)

    # Test 5: Output and Fire with Activation
    print("\nTest 5: Output and Fire with Activation")
    cell.activate([1, 1, 1])
    cell.output([0, 1])
    output = cell.fire()
    print("Output Array After Fire:", output)
    print(cell)

    # Test 6: Output and Fire Without Activation
    print("\nTest 6: Output and Fire Without Activation")
    cell.activate([0, 0, 0])
    output = cell.fire()
    print("Output Array After Fire (No Activation):", output)
    print(cell)
