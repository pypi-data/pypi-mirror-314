class MiniObjLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.mtl_file_path = None

        self.v = []
        self.vn = []
        self.vt = []
        self.fv = []
        self.fvn = []
        self.fvt = []

        self.mtl = []
        self.mtl_f_map = {}

    def readlines(self):
        # read all lines
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        # strip start and end whitespace
        lines = [line.strip() for line in lines]
        return lines

    def parse_each_face(self, face: str):
        components = face.split("/")
        vertex_index = int(components[0])
        if len(components) == 2:
            texture_index = int(components[1]) if components[1] != "" else -1
            normal_index = -1
        elif len(components) == 3:
            texture_index = int(components[1]) if components[1] != "" else -1
            normal_index = int(components[2]) if components[2] != "" else -1
        return vertex_index, texture_index, normal_index
        
    def parse_lines(self, lines: list[str]):
        current_mtl = None
        # parse lines
        for line in lines:
            if line.startswith("v "):
                # parse vertex
                vertex = line.split(" ")[1:]
                # map string to float
                vertex = [float(v) for v in vertex]
                self.v.append(vertex)
            elif line.startswith("vn "):
                # parse vertex normal
                vertex_normal = line.split(" ")[1:]
                vertex_normal = [float(vn) for vn in vertex_normal]
                self.vn.append(vertex_normal)
            elif line.startswith("vt "):
                # parse vertex texture
                vertex_texture = line.split(" ")[1:]
                vertex_texture = [float(vt) for vt in vertex_texture]
                self.vt.append(vertex_texture)
            elif line.startswith("usemtl "):
                # parse material
                material = line.split(" ")[1]
                current_mtl = material
                self.mtl.append(material)
                if material not in self.mtl_f_map:
                    self.mtl_f_map[material] = []
            elif line.startswith("f "):
                # parse face
                points = line.split(" ")[1:]
                fv = []
                fvt = []
                fvn = []
                for point in points:
                    vertex_index, texture_index, normal_index = self.parse_each_face(point)
                    fv.append(vertex_index)
                    if texture_index != -1:
                        fvt.append(texture_index)
                    if normal_index != -1:
                        fvn.append(normal_index)
                
                current_face_index = len(self.fv)
                self.mtl_f_map[current_mtl].append(current_face_index)
                
                self.fv.append(fv)
                self.fvt.append(fvt)
                self.fvn.append(fvn)

    def load(self):
        lines = self.readlines()
        self.parse_lines(lines)


        
    