import numpy as np
from .UBmc import UniversalBiomimeticCell


class UniversalBiasBiomimeticCell(UniversalBiomimeticCell):
    def __init__(Cell, index, inputNums, inputSize, memorySize, outputSize, outputNums):
        super().__init__(index, inputNums, inputSize, memorySize, outputSize, outputNums)
        Cell.fireFlags = np.zeros(outputNums, dtype=bool)

    def __str__(Cell):
        return f"UBBmc({Cell.index}, {Cell.inputSize}, {Cell.outputSize}, {Cell.activationFlags}, {Cell.fireFlags}, {Cell.inputNums}, {Cell.outputNums})"

    def fire(Cell, fireFlags: np.array):
        Cell.fireFlags = fireFlags

        if not np.all(Cell.activationFlags):
            return np.zeros(Cell.outputsArray.shape) != 0
        
        result = np.zeros_like(Cell.outputsArray)
        for i in range(Cell.outputNums):
            if Cell.fireFlags[i]:
                result[i] = Cell.outputsArray[i]
            else:
                result[i] = np.zeros(Cell.outputsArray[i].shape) != 0

        return result


if __name__ == "__main__":
    from UBBmc import UniversalBiasBiomimeticCell
    import numpy as np

    # Test 1: Initialization
    cell = UniversalBiasBiomimeticCell(1, 2, 3, 2, 2, 2)
    print("Test 1: Initialization")
    print(cell)

    # Test 2: Fire with fireFlags all False
    print("\nTest 2: Fire with fireFlags all False")
    cell.learn([[[1, 1, 1], [0, 1, 0]], [[1, 0, 1], [0, 0, 1]]])
    cell.activate([[1, 1, 1], [1, 0, 1]])
    cell.output([[1, 0], [0, 1]])
    output = cell.fire(np.array([False, False]))
    print("Output Array:", output)
    print(cell)

    # Test 3: Fire with fireFlags all True
    print("\nTest 3: Fire with fireFlags all True")
    output = cell.fire(np.array([True, True]))
    print("Output Array:", output)
    print(cell)

    # Test 4: Fire with mixed fireFlags
    print("\nTest 4: Fire with mixed fireFlags")
    output = cell.fire(np.array([True, False]))
    print("Output Array:", output)
    print(cell)
