class Stat:
    areaCovered: 0
    maxArea: 1
    bumpedIntoWall: []
    leftRightRatio: 1
    releaseFromWall: bool

    def __init__(self, ac, ma, biw, rfw, lrr):
        self.maxArea = ac
        self.areaCovered = ac
        self.bumpedIntoWall = biw
        self.releaseFromWall = rfw
        self.leftRightRatio = lrr

    def __str__(self):
        msg = "Area covered: " + str(self.areaCovered) + "\n WallCollisions: " + str(
            self.bumpedIntoWall) + "\n Left Right Ratio: " + str(self.leftRightRatio)
        return msg
