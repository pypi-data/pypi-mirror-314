import numpy as np
from SBBmc import SimpleBiasBiomimeticCell


class SimpleModeBiasBiomimeticCell(SimpleBiasBiomimeticCell):
    def __init__(Cell, index, inputSize, maxMemorySize, outputSize, modeCount):
        super().__init__(index, inputSize, maxMemorySize, outputSize)
        Cell.modeCount = modeCount
        Cell.currentMode = 0
        Cell.weightCube = np.zeros((modeCount, maxMemorySize, inputSize))

    def __str__(Cell):
        return f"SMBBmc({Cell.index}, {Cell.inputSize}, {Cell.outputSize}, {Cell.activationFlag}, {Cell.fireFlag}, {Cell.modeCount})"

    def learn(Cell, weightCube: np.array):
        Cell.weightCube = np.array(weightCube)

    def learnMode(Cell, weightSheet: np.array, modeIndex: int):
        Cell.weightCube[modeIndex] = np.array(weightSheet)

    def activate(Cell, inputValue: np.array, modeIndex: int):
        Cell.currentMode = modeIndex
        Cell.inputArray = inputValue
        modeWeights = Cell.weightCube[Cell.currentMode]
        matches = np.logical_not(np.logical_xor(modeWeights, Cell.inputArray)).all(axis=1)
        activations = matches.astype(int)
        Cell.activationFlag = np.any(matches)
        return activations


if __name__ == "__main__":
    # Test 1: Initialization
    cell = SimpleModeBiasBiomimeticCell(1, 3, 4, 2, 2)  # 2 modes, max memory size = 4
    print("Test 1: Initialization")
    print(cell)

    # Test 2: Learning for All Modes
    print("\nTest 2: Learning for All Modes")
    weightCube = [
        [[1, 1, 1], [0, 1, 0], [1, 0, 1], [0, 0, 0]],  # Mode 0
        [[0, 0, 1], [1, 1, 0], [0, 1, 1], [1, 0, 0]],  # Mode 1
    ]
    cell.learn(weightCube)
    print("Weight Cube After Learning:")
    print(cell.weightCube)

    # Test 3: Activation in Mode 0
    print("\nTest 3: Activation in Mode 0")
    activations = cell.activate([1, 1, 1], modeIndex=0)
    print("Activations (Mode 0):", activations)
    print("Activation Flag (Mode 0):", cell.activationFlag)
    print(cell)

    # Test 4: Activation in Mode 1
    print("\nTest 4: Activation in Mode 1")
    activations = cell.activate([1, 1, 0], modeIndex=1)
    print("Activations (Mode 1):", activations)
    print("Activation Flag (Mode 1):", cell.activationFlag)
    print(cell)

    # Test 5: Learning for a Specific Mode
    print("\nTest 5: Learning for a Specific Mode")
    cell.learnMode([[1, 0, 0], [0, 1, 1], [1, 1, 1], [0, 0, 0]], modeIndex=1)
    print("Weight Cube After Mode-Specific Learning (Mode 1):")
    print(cell.weightCube)

    # Test 6: Fire with Activation in Mode 0
    print("\nTest 6: Fire with Activation in Mode 0")
    cell.activate([1, 1, 1], modeIndex=0)
    cell.output([0, 1])
    output = cell.fire(True)
    print("Output Array (Mode 0):", output)
    print(cell)

    # Test 7: Fire with Activation in Mode 0
    print("\nTest 7: Fire with Activation and False Bias in Mode 0")
    cell.activate([1, 1, 1], modeIndex=0)
    output = cell.fire(False)
    print("Output Array (Mode 0):", output)
    print("Cell - Making Activation/Bias distinction visible:", cell)
    print(cell)

    # Test 8: Fire Without Activation in Mode 1
    print("\nTest 8: Fire Without Activation in Mode 1")
    cell.learnMode([[0, 0, 1], [1, 1, 0], [0, 1, 1], [1, 0, 0]], modeIndex=1)
    cell.activate([0, 0, 0], modeIndex=1)
    output = cell.fire(True)
    print("Output Array (Mode 1 - No Activation):", output)
    print(cell)
