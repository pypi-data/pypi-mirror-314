import numpy as np
from PBOMBmc import ParallelOMBiasBiomimeticCell


class ParallelOMModeBiasBiomimeticCell(ParallelOMBiasBiomimeticCell):
    def __init__(Cell, index, inputSize, memorySize, outputSize, outputNums, modeCount):
        super().__init__(index, inputSize, memorySize, outputSize, outputNums)
        Cell.modeCount = modeCount
        Cell.currentMode = 0
        Cell.weightCube = np.zeros((modeCount, memorySize, inputSize))

    def __str__(Cell):
        return f"PMBOMBmc({Cell.index}, {Cell.inputSize}, {Cell.outputSize}, {Cell.activationFlag}, {Cell.fireFlags}, {Cell.outputNums}, {Cell.modeCount})"

    def learn(Cell, weightCube: np.array):
        Cell.weightCube = np.array(weightCube)

    def learnMode(Cell, weightSheet: np.array, modeIndex: int):
        Cell.weightCube[modeIndex] = np.array(weightSheet)

    def activate(Cell, inputValue: np.array, modeIndex: int):
        Cell.currentMode = modeIndex
        modeWeights = Cell.weightCube[Cell.currentMode]
        matches = np.logical_not(np.logical_xor(modeWeights, inputValue)).all(axis=1)
        activations = matches.astype(int)
        Cell.activationFlag = np.any(matches)
        return activations


if __name__ == "__main__":
    # Test 1: Initialization
    cell = ParallelOMModeBiasBiomimeticCell(1, 3, 4, 2, 3, 2)  # 2 modes, 3 outputs
    print("Test 1: Initialization")
    print(cell)

    # Test 2: Learning for Modes
    print("\nTest 2: Learning for Modes")
    weightCube = [
        [[1, 1, 1], [0, 1, 0], [1, 0, 1], [0, 0, 0]],  # Mode 0 weights
        [[0, 0, 1], [1, 1, 0], [0, 1, 1], [1, 0, 0]],  # Mode 1 weights
    ]
    cell.learn(weightCube)
    print("Weight Cube After Learning:")
    print(cell.weightCube)

    # Test 3: Activation in Mode 0
    print("\nTest 3: Activation in Mode 0")
    activations = cell.activate([1, 1, 1], modeIndex=0)
    print("Activations:", activations)
    print("Activation Flag:", cell.activationFlag)

    # Test 4: Fire with Activation and Bias (Mode 0)
    print("\nTest 4: Fire with Activation and Bias (Mode 0)")
    cell.output([[0, 1], [1, 0], [1, 1]])
    output = cell.fire(np.array([False, False, True]))
    print("Output Array:", output)

    # Test 5: Fire with Activation and No Bias (Mode 0)
    print("\nTest 5: Fire with Activation and No Bias (Mode 0)")
    output = cell.fire(np.array([True, True, True]))
    print("Output Array:", output)

    # Test 6.0: Changing Mode 1 weight sheet
    print("\nTest 6.0: Changing Mode 1 weight sheet")
    cell.learnMode([[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 0, 0]], modeIndex=1)
    print("Weight Cube After Learning:")
    print(cell.weightCube)

    # Test 6: Activation in Mode 1
    print("\nTest 6: Activation in Mode 1")
    activations = cell.activate([0, 0, 1], modeIndex=1)
    print("Activations:", activations)
    print("Activation Flag:", cell.activationFlag)

    # Test 7: Fire with Activation and Bias (Mode 1)
    print("\nTest 7: Fire with Activation and Bias (Mode 1)")
    cell.output([[0, 1], [1, 0], [1, 1]])
    output = cell.fire(np.array([True, False, False]))
    print("Output Array:", output)

    # Test 8: Fire with Activation and No Bias (Mode 1)
    print("\nTest 8: Fire with Activation and No Bias (Mode 1)")
    output = cell.fire(np.array([True, True, True]))
    print("Output Array:", output)
