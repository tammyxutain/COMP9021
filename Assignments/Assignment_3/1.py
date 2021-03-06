class Point():
    def __init__(self,point):
        self.x = point[0]
        self.y = point[1]

    def __repr__(self):
        return '({},{})'.format(self.x, self.y)

class Vector():
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.x = end_point.x - start_point.x
        self.y = end_point.y - start_point.y
        self.length = (self.x**2 + self.y**2)**(1/2)
        

def cross_product(A, B):  #defin the cross product, A,B are vector 
    return A.x * B.y - B.x * A.y      
        
def available_coloured_pieces(file): #transfer the xml documents to the list of points
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(file, "html.parser")
    pieces={}
    for position in soup.find_all('path'):
        a=((position.get('d')).replace('M','')).replace('z','').split('L')
        colour = position.get('fill')
        point=[]
        for i in a:
            i = i.split(' ')
            i = [int(i) for i in i if i ]
            point.append(Point(i))
        pieces[colour] = point
    return pieces

def product_result(polygon): #get all cross_product in the polygon
    product_result=[]
    for i in range(-2,len(polygon)-2):
        ab = Vector(polygon[i], polygon[i+1])
        bc = Vector(polygon[i+1], polygon[i+2])

        r = cross_product(ab,bc)
        product_result.append(r)
    return(product_result)
    
def if_cross(a, b, c, d): #input Point()
    ac = Vector(a,c)
    ad = Vector(a,d)
    bc = Vector(b,c)
    bd = Vector(b,d)
    ca = Vector(c,a)
    da = Vector(d,a)
    cb = Vector(c,b)
    db = Vector(d,b)
    return (cross_product(ac, ad) * cross_product(bc, bd) <= 0) \
        and (cross_product(ca, cb) * cross_product(da, db) <= 0)
    
    
def are_valid (pieces):
    for colour in pieces:
        result=product_result(pieces[colour])  #use cross product(judge clockwise)
        #print(result)
        for i in range(len(result)-1):
            if result[i]*result[i+1] <= 0:
                return False
     
        for m in range(len(pieces[colour])-1): # comfirm the line not across
            a = pieces[colour][m]
            b = pieces[colour][m+1]
            if m+2 < len(pieces[colour])-1:
                for n in range(m+2, len(pieces[colour])-1):
                    c = pieces[colour][n]
                    d = pieces[colour][n+1]
                    if if_cross(a,b,c,d):
                            return False       
    return True
            

def reverse(colour): #slip the piece
    for point in colour:
        
        point.x,point.y = point.y,point.x
    
    colour = colour[::-1]
    return colour    

def print_Point(colour):
    for i in colour:
        print('({},{})'.format(i.x,i.y),end=' ')
    print()

        
def get_config(A_colour):
    result = [A_colour]
    B_colour = turn_90(A_colour)

    for _ in range(3):
        for i in result:
            if not equal(i,B_colour):
                continue
            else:
                turn_90(B_colour)
                continue
            result.append(B_colour)

    B_colour = reverse(B_colour)
    for _ in range(4):
        for i in result:
            if not equal(i,B_colour):
                continue
            else:
                turn_90(B_colour)
                continue
            result.append(B_colour)
    return result
   
def equal(a,b):
    for i in a:
        for j in b:
            if i.x != j.x or i.y != j.y:
                return False
    return True


    B_colour = reverse(B_colour)
    for _ in range(4):
       for i in range(len(A_colour)):
        if A_colour[i].x != B_colour[i].x or A_colour[i].y != B_colour[i].y:
            B_colour = turn_90(B_colour)
        else:
            return True 

    return False
                           
def are_identical_sets_of_coloured_pieces(piece_A, piece_B):
    if len(piece_A) != len(piece_B):  #the number of pirece must be same
        return False
    else:
        for A_colour in piece_A:       #test same color of two pirece whether identical
            for B_colour in piece_B:
                if A_colour != B_colour:
                    continue
                else:
                    if not is_identical(piece_A[A_colour], piece_B[B_colour]):
                        return False
    return True
    
def reset_position(piece):
    goal_x = None
    goal_y = None
    for i in piece:
        if goal_x == None:
            goal_x = i.x
        if goal_y == None:
            goal_y = i.y
        goal_x = min(goal_x,i.x)
        goal_y = min(goal_y,i.y)
        
    for n in piece:
        n.x -= goal_x
        n.y -= goal_y

    start_point=[]                  #let the start point be (0,min)
    for j in range(len(piece)):
        if piece[j].x == 0:
            start_point.append(j)
            
    temp = piece[start_point[0]].y
    result = start_point[0]
    for x in start_point:
        if piece[x].y < temp:
            result = x
  
    piece = piece[result:] + piece[0:result]
    return piece          

def turn_90(piece):
    piece = reset_position(piece)
    for i in piece:
        temp = i.x
        i.x = -i.y
        i.y = temp
    piece = reset_position(piece)
    return piece

def area(piece):
    
    total_area = 0
    
    for p in piece:
        colour = piece[p]
        area = 0
        for i in range(-2,len(colour)-2):   #point in the same ploygon
            area += 0.5*cross_product(colour[i], colour[i+1])
        total_area += abs(area)
    return abs(total_area)           
                     
  
def is_solution(tangram, shape):
    if area(tangram) != area(shape):   #total area is equal
        return False

    for i in tangram:                  #judge each of two pieces whether overliped or not
        for j in tangram:
            if i != j:
                unions = union(tangram[i],tangram[j])
                if unions == False:
                    return False
                else:
                    if unions == 'not union':
                        continue

    for k in tangram:                # determine if every points is in the shape 
        if not is_in_shape(tangram[k],shape):
            return False   
    return True

def is_in_shape(piece, shape):
    for i in shape:
        shape_point = shape[i]
        true_list=[]
    for q in piece:
        true_list.append(point_in_shape(q,shape_point))

    if False in true_list:
        return False
    return True

def point_in_shape(q,shape_point):   #judge the single point if in the piece 
    flag = False
    for p in range(len(shape_point)):
        p1 = shape_point[p-1]
        p2 = shape_point[p]
        
        if q.x == p1.x and q.y == p1.y:
            return True

        if cross_product(Vector(p1,q),Vector(q,p2)) == 0:
            if min(p1.y, p2.y) <= q.y <= max(p1.y, p2.y):
                if min(p1.x, p2.x) <= q.x <= max(p1.x, p2.x):
                    return True
                else:
                    continue
            
        if min(p1.y, p2.y) <= q.y < max(p1.y, p2.y):

            if p1.x == p2.x:
                if q.x <= p1.x:
                    flag = not flag

            else:
                if q.x <= max(p1.x, p2.x):
                    if q.y == p1.y:
                        if q.x < p1.x:
                            flag = not flag
                    else:               #q0 is the x坐标 point on the line when q0.y = qy                                                                            
                        q0 = (p1.x - p2.x) * (q.y - p1.y) / (p1.y - p2.y) + p1.x
                        if q0 > q.x:
                            flag = not flag

                        if q0 == q.x:
                            return True
    return flag                  
    

def collinear(A_colour, B_colour):
    new_A = []
    for i in range(-1, len(A_colour)-1):
        new_A.append(A_colour[i])
        for j in range(-2, len(B_colour)-2):
            
            #two lines ai-ai+1, bi-bi+1 are collinear
            if cross_product(Vector(A_colour[i], A_colour[i+1]), Vector(B_colour[j], B_colour[j+1])) != 0 \
               or cross_product(Vector(A_colour[i], A_colour[i+1]), Vector(B_colour[j], A_colour[i])) != 0: 
                continue
            else:             
                min_a = min(A_colour[i].x, A_colour[i+1].x)
                max_a = max(A_colour[i].x, A_colour[i+1].x)
                if min_a < B_colour[j].x < max_a and min_a < B_colour[j+1].x < max_a:
               #     is the the line ab print('在范围内')
                    if abs(A_colour[i].x - B_colour[j].x) < abs(A_colour[i].x - B_colour[j+1].x):

                        new_A.append(B_colour[j])
                        new_A.append(B_colour[j+1])
                        
                    else:

                        new_A.append(B_colour[j+1])
                        new_A.append(B_colour[j])

                elif min_a < B_colour[j].x < max_a:

                    new_A.append(B_colour[j])

                elif min_a < B_colour[j+1].x < max_a:
                    new_A.append(B_colour[j+1])
    return new_A 
##
##
def union(A_colour, B_colour):
    import copy

    if cross_product(Vector(A_colour[0], A_colour[1]), Vector(A_colour[1], A_colour[2])) < 0:
        A_colour = A_colour[::-1]
    if cross_product(Vector(B_colour[0], B_colour[1]), Vector(B_colour[1], B_colour[2])) < 0:
        B_colour = B_colour[::-1]        
    A = copy.deepcopy(collinear(A_colour, B_colour))
    B = copy.deepcopy(collinear(B_colour, A_colour))

    count = 0
    for i in A:
        for j in B:
            if i.x == j.x and i.y == j.y:
                count += 1
    if count <= 1:
        return 'not union'

    if count >=3:
        return False

    a = None

    i = 0
    j = 0
    for i in range(0,len(A)):    
        if a == None:
            for j in B:
                if A[i].x == j.x and A[i].y == j.y:
                    a = i
                    break
            
    b = None

    i = 0
    j = 0
    for i in range(0,len(A)):
        if b == None:
            for j in B:
                if A[i].x == j.x and A[i].y == j.y:
                    if  i != a:
                        b = i
                        if b != a + 1:
                            a = len(A) - 1
                            b = 0
                else:
                    continue
                break

    i = 0
    j = 0
    for j in range(0,len(B)):
        if B[j].x == A[a].x and B[j].y == A[a].y:         
            c = j
            break
        
    if B[c-1].x != A[b].x or B[c-1].y != A[b].y:
        return False
    return True

def solve(pieces, shape):
    pieces_list = [[],[],None]
    config = []
    for i in pieces: #append colour into piece_list[0], just colour no position
        pieces_list[0].append(i)          #initialization of piece_list

    for i in pieces_list[0]:        #select the first colour in piece_list
        shape = pieces[i]
        
        
    
