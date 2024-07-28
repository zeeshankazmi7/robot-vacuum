from tabulate import tabulate
import math

def inputSize():
    # defining valid size options
    validNums = [2, 3, 4, 5]
    size = 0
    while True:
        try:
            # asking for size input from user
            size = int(input("Enter size: "))
            if size in validNums:
                # returning valid size
                return size
            print("\nInvalid input. Please enter a size between 2 and 5\n")
        except:
            print("\nInvalid input. Please enter a size between 2 and 5\n")
        
def validCoordinates(input, tableSize):
    # checking if input length is sufficient
    if len(input) < 5:
        return False
    
    points = 0
    # checking if input format is valid
    if input[0] == "(":
        points += 1
    if input[4] == ")":
        points += 1
    if int(input[1]) <= tableSize and int(input[3]) <= tableSize:
        points += 1
    if int(input[1]) >= 0 and int(input[3]) >= 0:
        points += 1

    # verifying all conditions are met
    if points == 4:
        return True
    else:
        return False

def displayEnvironment(environment):
    # displaying environment in grid format
    return tabulate(environment, tablefmt="grid")

def selectDirtTile(environment, size):
    while True:
        try:
            # asking for dirt count from user
            dirtCount = int(input("Enter dirt count: "))
        except:
            print("\nInvalid input. Please enter a number.\n")
        else:
            break
    
    for i in range(0, dirtCount):
        # asking for dirt coordinates
        coordinates = input("Enter coordinates of dirt {}: ".format(i+1))
        coordinates = coordinates.replace(" ", "")
        while validCoordinates(coordinates, size) != True:
            coordinates = input("Invalid coordinates. Please try again: ")
            coordinates = coordinates.replace(" ", "")
        
        # placing dirt at specified coordinates
        environment[int(coordinates[1])][int(coordinates[3])] = "Dirt"

    return environment
    
def createEnvironment(size):
    # creating a clean environment grid
    environment = [['Clean' for _ in range(size)] for _ in range(size)]
    return environment

def getDirtyCoordinates(environment):
    # finding all dirty coordinates in the environment
    dirty_coordinates = []
    for i in range(len(environment)):
        for j in range(len(environment)):
            if environment[i][j] == "Dirt":
                dirty_coordinates.append((i, j))
            
        return dirty_coordinates

class Cleaner:
    def __init__(self, environment, size):
        # initializing cleaner with environment and size
        self.environment = environment
        self.currentPosition = self.cleanerPosition(size)

    def cleanerPosition(self, size):
        # asking for initial position of the cleaner
        coordinates = input("Enter coordinate of Roomba: ")
        coordinates = coordinates.replace(" ", "")
        while validCoordinates(coordinates, size) != True:
            coordinates = input("Invalid coordinates. Please try again: ")
            coordinates = coordinates.replace(" ", "")
        
        return ((int(coordinates[1]), int(coordinates[3])))

    def left(self):
        # moving cleaner left if not at edge
        x, y = self.currentPosition
        if y > 0:
            self.currentPosition = (x, y - 1)
            print(f"Moved left. Current position: ({x}, {y})")
        else:
            print("Cannot move left. Reached the edge.")

    def right(self):
        # moving cleaner right if not at edge
        x, y = self.currentPosition
        if y < len(self.environment) - 1:
            self.currentPosition = (x, y + 1)
            print(f"Moved right. Current position: ({x}, {y})")
        else:
            print("Cannot move right. Reached the edge.")

    def up(self):
        # moving cleaner up if not at edge
        x, y = self.currentPosition
        if x > 0:
            self.currentPosition = (x - 1, y)
            print(f"Moved up. Current position: ({x}, {y})")
        else:
            print("Cannot move up. Reached the edge.")

    def down(self):
        # moving cleaner down if not at edge
        x, y = self.currentPosition
        if x < len(self.environment) - 1:
            self.currentPosition = (x + 1, y)
            print(f"Moved down. Current position: ({x}, {y})")
        else:
            print("Cannot move down. Reached the edge.")

    def clean(self):
        # cleaning dirt if present at current position
        x, y = self.currentPosition
        if self.environment[x][y] == "Dirt":
            self.environment[x][y] = "Clean"
            print("Cleaned dirt at position:", self.currentPosition)
        else:
            print("No dirt to clean at position:", self.currentPosition)

    def checkGoalState(self):
        # checking if environment is clean
        for row in self.environment:
            if "Dirt" in row:
                return False
        return True

    def findNearestDirtyTile(self):
        # finding nearest dirty tile to cleaner
        minDistance = math.inf
        nearestTile = None
        for i in range(len(self.environment)):
            for j in range(len(self.environment[i])):
                if self.environment[i][j] == "Dirt":
                    distance = abs(self.currentPosition[0] - i) + abs(self.currentPosition[1] - j)
                    if distance < minDistance:
                        minDistance = distance
                        nearestTile = (i, j)
        return nearestTile

def main():
    # main function to run the cleaning simulation
    size = inputSize()
    environment = createEnvironment(size)
    cleaner = Cleaner(environment, size)
    
    environment = selectDirtTile(environment, size)

    print("Initial Environment:")
    print(displayEnvironment(environment))

    while not cleaner.checkGoalState():
        nearestDirtyTile = cleaner.findNearestDirtyTile()
        if nearestDirtyTile:
            targetX, targetY = nearestDirtyTile
            currentX, currentY = cleaner.currentPosition
            if currentX < targetX:
                cleaner.down()
            elif currentX > targetX:
                cleaner.up()
            elif currentY < targetY:
                cleaner.right()
            elif currentY > targetY:
                cleaner.left()
            else:
                cleaner.clean()
        else:
            print("No more dirty tiles found. Exiting...")
            break

        print("Current Environment:")
        print(displayEnvironment(environment))

    if cleaner.checkGoalState():
        print("All waste responsibly collected. Task completed!")

main()

