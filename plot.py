import bpy
import mathutils
import math
from mathutils import Matrix
import time
import json
    
def deselect():
    bpy.ops.object.select_all(action='DESELECT')

def selectObjects(objs):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objs:
        objectToSelect = bpy.data.objects[obj.name]
        objectToSelect.select_set(True)    
        bpy.context.view_layer.objects.active = objectToSelect

def selectObject(obj, add = False, recursive = False):
    if not add:
        bpy.ops.object.select_all(action='DESELECT')
    objectToSelect = bpy.data.objects[obj.name]
    objectToSelect.select_set(True)
    bpy.context.view_layer.objects.active = objectToSelect
    if recursive:
        for child in obj.children:
            selectObject(child, True, True)
            
def getAllChildrenArr(parentObjs):
    children = []
    for parent in parentObjs:
        if len(parent.children):
            children.extend(getAllChildrenArr([parent]))
    return children


def getChildrenArr(parentObjs, depth):
    children = []
    for parent in parentObjs:
        for child in parent.children:
            if depth > 0:
                children.extend( getChildren(child, depth-1) )
            else:
                children.append(child)
    return children

def getChildren(parentObj, depth):
    return getChildrenArr([parentObj],depth)

def getFamily(parentObjs):
    part = []
    if isinstance(parentObjs, list):
        part.extend(parentObjs)
    else:
        part.append(parentObjs)
    al = []
    while len(part):
        part = getChildrenArr(part,0)    
        al.extend(part)
    return al

def getUpperObject(parentObj):
    if not parentObj:
        return None
    print("**** Getting the uppermost of:"+str(parentObj.name))
    mh = -20.0
    upmost = None
    parentUp = parentObj.matrix_world.translation[2]
    print("Parent:"+str(parentObj.matrix_world.translation[2]))
    for child in getChildren(parentObj, 0):
        if child:
            childUp = child.matrix_world.translation[2]
            print("Candidate:"+str(child.matrix_world.translation[2]))
            if (childUp - parentUp) > mh:
                upmost = child
                mh = childUp - parentUp
    print("wins:"+str(upmost.matrix_world.translation))
    return upmost

def deleteSelected():
    bpy.ops.object.delete(True)

def delete(obj):
    selectObject(obj, False, True)
    bpy.ops.object.delete(True)

def selectAll():
    bpy.ops.object.select_all(action='SELECT')
    
def deselect():
    bpy.ops.object.select_all(action='DESELECT')

def selectObject(obj, add = False, recursive = False):
    if not obj:
        return
    if not add:
        bpy.ops.object.select_all(action='DESELECT')
    objectToSelect = bpy.data.objects[obj.name]
    objectToSelect.select_set(True)    
    bpy.context.view_layer.objects.active = objectToSelect
    if recursive:
        for child in obj.children:
            selectObject(child, True, True)

def selectObjects(objs):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objs:
        objectToSelect = bpy.data.objects[obj.name]
        objectToSelect.select_set(True)    
        bpy.context.view_layer.objects.active = objectToSelect

def createCube(size):
    bpy.ops.mesh.primitive_cube_add()
    box = bpy.context.active_object
    bpy.ops.transform.resize(value=(size, size, size))
    return box

def createSphere(size):
    bpy.ops.mesh.primitive_ico_sphere_add()
    sphere = bpy.context.active_object
    bpy.ops.transform.resize(value=(size, size, size))
    #setattr(sphere, "fios", "0")
    return sphere

def upit(what, amnt):
    # one blender unit in x-direction
    bpy.ops.transform.translate(value=(0.0, 0.0, amnt), orient_type='GLOBAL')
    pass

def getUpperObject(parentObj):
    if not parentObj:
        return None
    mh = -20.0
    upmost = None
    parentUp = parentObj.matrix_world.translation[2]
    parentX = parentObj.matrix_world.translation[0]
    for child in getChildren(parentObj, 0):
        if child:
            childUp = child.matrix_world.translation[2]
            childX = child.matrix_world.translation[0]
            if abs(childX-parentX)<0.01: #epsilon
                if (childUp - parentUp) > mh:
                    upmost = child
                    mh = childUp - parentUp
    if mh<0:
        return None
    return upmost

class solution():
    def __init__(self, c, x, y):
        self.c = c
        self.x = x
        self.y = y
        self.step_size = c
        self.ks = []
        self.t_cnt = False
        self.l_cnt = False 
    
    def activateT(self):
        self.t_cnt = True
        
    def activateL(self):
        self.l_cnt = True

    def createNode(self):
        #deselect all objects
        last_ob = createCube(4/self.c)
        cube1 = last_ob
        return cube1

    def parent(self, a, b, n, l):
        b.parent = a
        b.location = (0, 25*(self.x*self.y), l)
        b.matrix_parent_inverse = a.matrix_world.inverted()
        a.rotation_euler = (0, a.rotation_euler[1] + math.radians(360/self.c), 0)
        #a.fios += 1

    def adan(self, object, limit = None):
        if not object or not object.parent:
            return object
        ad = object
        while ad and ad.parent and ad.parent!=limit:
            ad = ad.parent
        return ad

    def initialStep(self):
        createCube(4)

    def rotate(self, offset = 0):
        spheres = []
        for j in range(1, 2):
            selectAll()
            toduplicate = bpy.context.selected_objects
            distance = offset
            sphNumber = len(self.ks)
            sphere = createSphere(2.8 / (1+sphNumber))
            sphere.name = 'sph_'+str(sphNumber)
            if sphere:
                spheres.append(sphere)
            newgroup = self.adan(toduplicate[0])
            self.parent(sphere, newgroup, 1, distance)
            for _ in range(1, self.c):
                selectObjects(toduplicate)
                bpy.ops.object.duplicate()
                if self.adan(bpy.context.selected_objects[0],  sphere):
                    newgroup2 = self.adan(bpy.context.selected_objects[0],  sphere)
                    #spheres.append(newgroup2)
                    newgroup2.location = (0, 0, 0)
                    self.parent(sphere, newgroup2, 1, distance)
        return spheres

    def step(self):
        self.step_size *= 2.6 #+ c/9
        return self.rotate(self.step_size)

    def leafs(self, arr = None):
        if not isinstance(arr, list):
            arr = bpy.data.objects
        if not arr:
            return []
        return  [obj for obj in bpy.data.objects if obj.name.startswith("Cube")]
        
    def build(self):
        s.initialStep()
        gp = None
        gsl = self.x-2
        print("\n\n\n*****************************")
        print("Start  C:" + str(self.c))
        print("  x:" + str(self.x))
        print("  y:" + str(self.y))
        print("       v_jump:" + str(gsl))
        print("*****************************")
        for i in range(0, self.x*self.y):
            d = {}
            print("K:---------------->" + str(i))
            d["l"] = 0
            d["t"] = 0
            d["_t"] = []
            d["_tryT"] = []
            d["pk"] = 0
            line = i%(self.x-1)
            column = i%(self.x)
            newSpheres = s.step()
            deselect()
            for sph in newSpheres:
                if self.l_cnt and (i%self.x<(self.x-1)):
                    print("applying l")
                    upsph = getUpperObject(sph)
                    delete(upsph)
                    d["l"] = 1
                    if self.ks:
                        d["l"] = self.ks[-1]["pk"]
                    print("\t\tleafs L:" + str(d["l"]))
                    
                if self.t_cnt and (i>=(self.x-1)) and (i<(self.x*self.y)-1):
                    print("applying t")
                    gp = s.adan(sph)
                    selectObject(gp)
                    grandsons = getChildren(gp, gsl)
                    aa = len(self.leafs())
                    for gs in grandsons:
                        if gs:
                            upgs = getUpperObject(gs)
                            if upgs:
                                a = len(self.leafs())
                                #d["_tryT"].append(upgs.name)
                                delete(upgs)
                                b = len(self.leafs())
                                d["_t"].append(a-b)
                                k_amm = len(self.ks)
                                try_tt = self.ks[k_amm-self.x]["pk"]
                                d["_tryT"].append(try_tt)
                                
                    bb = len(self.leafs())
                    d["t"] += aa-bb
                    print("\t\tleafs T:" + str(d["t"]))

                t = len(self.leafs())
                print("\tK:" + str(t))
                if self.ks:
                    d["pk"] = (self.ks[-1]["pk"] * self.c) + (- d["t"] - d["l"])
                else:
                    d["pk"] = self.c - 1
            d["R_k"] = len(self.leafs())
            print("K-Dict:"+json.dumps(d, indent=2))
            self.ks.append(d)
            if column==(self.x-1):
                print("\n\n\n\n\n\n")

        cube_objs = [obj for obj in bpy.data.objects if obj.name.startswith("Cube")]
        selectObjects(cube_objs)
        print("*****************************")
        print("Final k = " + str(len(cube_objs)))
        print("*****************************\n\n")

x = 3
y = 2
c = 6

bpy.ops.object.select_all(action='SELECT')
deleteSelected()
bpy.ops.object.select_all(action='DESELECT')

s = solution(c, x, y)
s.activateT()
s.activateL()
s.build()
