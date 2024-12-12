import json

# build: python -m build
# upload to pypi: python -m twine upload dist/*

'''
TODO
add level loading
'''
class Blocks:
    def __init__(self):
        self.BLOCK = 0
        self.SPIKE = 1
        self.YELLOW_ORB = 2
        self.BLUE_ORB = 4
        self.PINK_ORB = 3
        self.GREEN_ORB = 5
        self.UPSIDE_DOWN_GRAVITY_PORTAL = 6
        self.REGULAR_GRAVITY_PORTAL = 7
        self.SPEED_PORTALl = 9
        self.FADING_BLOCK = 10
        self.YELLOW_PAD = 11

class TrideDashLevel():
    def __init__(self):
        self.data = {}
        self.objects = []
        self.version = 2
        self.songname = ""
        self.artist = ""
        self.creator = ""
        self.levelname = ""
    def load(self, level_data):
        if level_data.find("§") != -1:
            self.version = 2
            data = str(level_data).split("§")
            song = data[0]
            self.songname = song.split(":")[1]
            artist = data[1]
            self.artist = artist.split(":")[1]
            creator = data[2]
            self.creator = creator.split(":")[1]
            leveldata = data[3]
            l = leveldata.split("\n")
            l.pop(0)
            l.pop(0)
            l.pop(-1)
            l.pop(-1)
            for data in l:
                id = int(str(data.split(";")[0]).split(":")[1])
                pos = data.split(";")[1].split(":")[1]
                rot = float(data.split(";")[2].split(":")[1][1:len(data.split(";")[2].split(":")[1])])
                if id == 8:
                    pass
                else:

                    # TODO: connect ids to their tdremake cousins
                    x = pos.split(",")[0]
                    x = x[2:len(x)]
                    x = float(x)
                    y = pos.split(",")[1]
                    y = float(y[1:-1])
                    list4 = {"objID": id, "position": [x, y], "rotation": rot, "data": {}}
                    self.objects.append(list4)
        else:
            # t d remake
            self.version = 2
            self.data = json.loads(level_data)
    def placeBlock(self, x, y, rotation,  type: int, data: list={}):
        self.objects.append({
            "objID": type,
            "position": [
                x, y
            ],
            "rotation": rotation,
            "data": data
        })
    def editBlock(self, index, data):
        self.objects[index] = data
    def export(self):
        self.data = {"levelName": self.levelname, "songName": self.songname, "artistName": "", "creator": self.creator, "objects":self.objects}
        return json.dumps(self.data)
def newLevel(levelname, creator, songname="Airship Serenity.wav") -> TrideDashLevel:
    l = TrideDashLevel()
    l.creator = creator
    l.levelname = levelname
    l.songname = songname
    return l