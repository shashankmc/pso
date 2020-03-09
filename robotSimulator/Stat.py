class Stat:
    areaCovered: 0
    maxArea: 1
    bumpedIntoWall: []
    dvCount: []

    def __init__(self, ac, ma, biw, dvCount):
        self.maxArea = ma
        self.areaCovered = ac
        self.bumpedIntoWall = biw
        self.dvCount = dvCount

    def __str__(self):
        msg = "Area covered: " + str(self.areaCovered) + "\n WallCollisions: " + str(
            self.bumpedIntoWall) + "\n dvCount: " + str(self.dvCount)
        return msg
