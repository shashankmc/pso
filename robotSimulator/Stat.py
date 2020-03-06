
class Stat:
    areaCovered:0
    bumpedIntoWall:0

    def __init__(self, ac, biw):
        self.areaCovered = ac
        self.bumpedIntoWall = biw

    def __str__(self):
        msg = "Area covered: " + str(self.areaCovered)+ "\n WallCollisions: " +str(self.bumpedIntoWall)
        return msg