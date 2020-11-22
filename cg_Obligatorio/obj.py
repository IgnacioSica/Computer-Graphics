class Obj:

    v = [[0.0,0.0,0.0]]
    vn = [[0.0,0.0,0.0]]
    vt = []
    faces = []
    drawData = []
    drawV = []
    drawN = []

    def __init__(self, name):
        self.name = name

    def parse(self, path):
        f = open(path, "r")
        for l in f:
            l = l.strip('\n')

            if l.find("v ") >= 0:
                ver = l.split(" ")
                verF = [float(x) for x in ver[1:]]
                self.v.append(verF)

            elif l.find("vn ") >= 0:
                norm = l.split(" ")
                normF = [float(x) for x in norm[1:]]
                self.vn.append(normF)

            elif l.find("vt ") >= 0:
                text = l.split(" ")
                textF = [float(x) for x in text[1:]]
                self.vt.append(textF)

            elif l.find("f ") >= 0:
                face = l.split(" ")
                for vnt in face[1:]:
                    faceI = [int(x) for x in vnt.split('/')]
                    self.faces.append(faceI)

        for f in self.faces:
            self.drawV.append(self.v[f[0]])
            self.drawN.append(self.vn[f[1]])
            self.drawData.append(self.vt[f[2]])