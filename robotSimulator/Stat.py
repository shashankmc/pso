class Stat:
    areaCovered: 0
    maxArea: 1
    bumpedIntoWall: []
    releaseFromWall=0
    cappedOutput:[]
    dvCount:[]

    def __init__(self, ac, ma, biw, rfw, cop, dvCount):
        self.maxArea = ac
        self.areaCovered = ac
        self.bumpedIntoWall = biw
        self.releaseFromWall = rfw
        self.cappedOutput = cop
        self.dvCount = dvCount

    def __str__(self):
        msg = "Area covered: " + str(self.areaCovered) + "\n WallCollisions: " + str(
            self.bumpedIntoWall)+"\n Capped Outputs: " + str(self.cappedOutput)
        return msg
