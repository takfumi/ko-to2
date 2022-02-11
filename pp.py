import numpy as np
import cv2
import math


IMAGE_PATH = "./ko-to6.jpg" # 読み込む画像

def main():
    image  = cv2.imread(IMAGE_PATH) # 画像読み込み
    image2 = cv2.imread(IMAGE_PATH) # 画像読み込み
    image3 = cv2.imread(IMAGE_PATH) # 画像読み込み

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # グレースケール化
    cv2.imwrite("./ou6.png", gray)
    outLineImage = cv2.Canny(gray, 100, 200, apertureSize = 3)   # 輪郭線抽出
    cv2.imwrite("./outLine6.png", outLineImage)    # ファイル保存

    
    for i in range(500,100,-1):
    
        houghPList = hough_lines_p(image2, outLineImage,i)  # 確率的ハフ変換による直線抽出
        cv2.imwrite("./out_houghP9_%d.png" % i, image2)        # ファイル保存
        #draw_cross_points(image2, houghPList)             # 直線リストから交点を描画
        #cv2.imwrite("./result_houghP_cros7.png", image2)  # ファイル保存
        
        

        d = makeLinearEquation(image3,houghPList) # エンドライン,サイドライン区別
        cv2.imwrite("./outline6_%d.png" % i, image3)      # ファイル保存
        print("返り値:",d)
        print("しきい値:",i)
        if d == 1:
           break
        


# 確率的ハフ変換で直線を抽出する関数
def hough_lines_p(image, outLineImage,i):
    lineList = []
    # 確率的ハフ変換で直線を抽出
    lines = cv2.HoughLinesP(outLineImage, rho=1, theta=np.pi/200, threshold=i, minLineLength=0, maxLineGap=200)
    print("hough_lines_p: ", len(lines))
    #print(lines)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        #print(line[0])
        lineList.append((x1, y1, x2, y2))
        cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2) # 緑色で直線を引く

    #print(lineList)

    return lineList


# 交点を描画する関数
def draw_cross_points(image, lineList):
    size = len(lineList)

    cnt = 0
    for i in range(size-1):
        for j in range(i+1, size):
            pointA = (lineList[i][0], lineList[i][1])
            pointB = (lineList[i][2], lineList[i][3])
            pointC = (lineList[j][0], lineList[j][1])
            pointD = (lineList[j][2], lineList[j][3])
            ret, cross_point = calc_cross_point(pointA, pointB, pointC, pointD) # 交点を計算
            if ret:
                # 画像の範囲外のものは除外
                if (cross_point[0] >= 0) and (cross_point[0] <= image.shape[1]) and (cross_point[1] >= 0) and (cross_point[1] <= image.shape[0]) :
                    
                    cv2.circle(image, (cross_point[0],cross_point[1]), 2, (255,0,0), 3) # 交点を青色で描画
                    cnt = cnt + 1
    #print("draw_cross_points:", cnt)


# 線分ABと線分CDの交点を求める関数
def calc_cross_point(pointA, pointB, pointC, pointD):
    cross_points = (0,0)
    bunbo = (pointB[0] - pointA[0]) * (pointD[1] - pointC[1]) - (pointB[1] - pointA[1]) * (pointD[0] - pointC[0])

    # 直線が平行な場合
    if (bunbo == 0):
        return False, cross_points

    vectorAC = ((pointC[0] - pointA[0]), (pointC[1] - pointA[1]))
    r = ((pointD[1] - pointC[1]) * vectorAC[0] - (pointD[0] - pointC[0]) * vectorAC[1]) / bunbo
    s = ((pointB[1] - pointA[1]) * vectorAC[0] - (pointB[0] - pointA[0]) * vectorAC[1]) / bunbo

    # 線分AB、線分AC上に存在しない場合
    if (r <= 0) or (1 <= r) or (s <= 0) or (1 <= s):
        return False, cross_points

    # rを使った計算の場合
    distance = ((pointB[0] - pointA[0]) * r, (pointB[1] - pointA[1]) * r)
    cross_points = (int(pointA[0] + distance[0]), int(pointA[1] + distance[1]))

    return True, cross_points

def line(List):#ラインの統合
    size = len(List)
    print(size)
    maxx = 0
    maxy = 0
    minx = 0
    miny = 0
    lineList = []
    print(List)
    
    for i in range(size):
        a = 0
        c = i
        if len(List)<=i:
           break
        maxx = List[i][2]
        maxy = List[i][3]
        minx = List[i][0]
        miny = List[i][1]
        print(i)
       
        if List[i][3]-List[i][1]!=0 and List[i][2]-List[i][0]!=0:
           a = math.floor(((List[i][3]-List[i][1]) / (List[i][2]-List[i][0]))*100)
           print(a)
        elif List[i][3]-List[i][1]==0: # X軸に平行
             a = 0
        elif List[i][2]-List[i][0]==0: # Y軸に平行
             a = 1
        
        for j in (i+1,100):
            b = 0
            c = c + 1
            print(c)
            print(List)
            if c>=len(List):
               break
            if List[c][3]-List[c][1]!=0 and List[c][2]-List[c][0]!=0:
               b = math.floor(((List[c][3]-List[c][1]) / (List[c][2]-List[c][0]))*100)
               print("b",b)
           
            elif List[i][3]-List[i][1]==0: # X軸に平行
                 b = 0
            elif List[i][2]-List[i][0]==0: # Y軸に平行
                 b = 1
            
            if a == b:
               if minx >= List[c][0]:
                  minx = List[c][0]
               elif miny >= List[c][1]:
                  miny = List[c][1]
               elif maxx <= List[c][2]:
                  maxx = List[c][2]
               elif maxy <= List[c][3]:
                  mmaxy = List[c][1]
               
               List.remove(List[c])
               c = c - 1
            lineList.append((minx,miny,maxx,maxy))
            
    return lineList


# 区別する関数
def makeLinearEquation(image,lineList):
    size = len(lineList)
    #print(lineList)
    endlineList = []
    endlineList1 = []
    endlineList11 = []
    endlineList12 = []
    endlineList2 = []
    sidelineList = []
    cnt = 0
    
    c1 = 0
    c2 = 0
    a = 0
    b = 0
    c11 = 0
    c12 = 0
    
    for i in range(size): #傾き計算
        m = 0
        
        if lineList[i][3]-lineList[i][1]!=0 and lineList[i][2]-lineList[i][0]!=0:
       
           m = (lineList[i][3]-lineList[i][1]) / (lineList[i][2]-lineList[i][0])
           
        elif lineList[i][3]-lineList[i][1]==0: # X軸に平行
             m = 0
        elif lineList[i][2]-lineList[i][0]==0: # Y軸に平行
             m = 1
       
        #ライン４つに分類
        if np.tan(30*np.pi/180)<m<=np.tan(89*np.pi/180) and m != 1: #エンドライン
           
           c11 = c11 + 1
           endlineList1.append((lineList[i][0],lineList[i][1],lineList[i][2],lineList[i][3]))
           endlineList1=sorted(endlineList1)
           
        elif np.tan(-30*np.pi/180)>m>=np.tan(-89*np.pi/180) and m != 1:
           
           c12 = c12 + 1
           endlineList2.append((lineList[i][0],lineList[i][1],lineList[i][2],lineList[i][3]))
           endlineList2=sorted(endlineList2)
    for i in range(size):#サイドライン
         m = 0
        
         if lineList[i][3]-lineList[i][1]!=0 and lineList[i][2]-lineList[i][0]!=0:
         
            m = (lineList[i][3]-lineList[i][1]) / (lineList[i][2]-lineList[i][0])
           
         elif lineList[i][3]-lineList[i][1]==0: # X軸に平行
                m = 0
         elif lineList[i][2]-lineList[i][0]==0: # Y軸に平行
                m = 1
         #print(m)
         if c11 < c12 and m>=0:
           sidelineList.append((lineList[i][0],lineList[i][1],lineList[i][2],lineList[i][3]))
           endlineList11 = endlineList2
           b = 1

         elif c11 > c12 and m<=0:
           c2 = c2 + 1
           sidelineList.append((lineList[i][0],lineList[i][1],lineList[i][2],lineList[i][3]))
           endlineList11 = endlineList1
           b = 0
    
    size1 = len(endlineList11)
    size2 = len(sidelineList)
    if size1==0 or size2==0:
       return 0
    
    c3 = 0
    crossList = []

    for i in range(size1):
        for j in range(size2):
            pointA = (endlineList11[i][0], endlineList11[i][1])
            pointB = (endlineList11[i][2], endlineList11[i][3])
            pointC = (sidelineList[j][0], sidelineList[j][1])
            pointD = (sidelineList[j][2], sidelineList[j][3])
            ret, cross_point = calc_cross_point(pointA, pointB, pointC, pointD) # 交点を計算
            #print(cross_point)
            if ret:
                # 画像の範囲外のものは除外
                if (cross_point[0] >= 0) and (cross_point[0] <= image.shape[1]) and (cross_point[1] >= 0) and (cross_point[1] <= image.shape[0]) :
                    #endlineList.append((endlineList11[i]))
                    #endlineList=sorted(endlineList)
                    
                    crossList.append((cross_point[0],cross_point[1]))
                    #cv2.line(image,(endlineList[i][0],endlineList[i][1]),(endlineList[i][2],endlineList[i][3]),(255,0,255),2)
                    #cv2.line(image,(sidelineList[j][0],sidelineList[j][1]),(sidelineList[j][2],sidelineList[j][3]),(255,0,255),2)
                    cv2.circle(image, (cross_point[0],cross_point[1]), 5, (255,0,0), 5) # 交点を青色で描画
                    
                    c3 = c3 + 1
    
    print(len(crossList))
    print(endlineList)
    crossList2 = []
    crossList3 = []
    crossList11 = sorted(crossList)
    
    for i in range(100):#中央値をとる
        if len(crossList11) <= i:
               break
        c = i
        cLi = []
        cLi2 = []
        cLi.append((crossList11[i][0],crossList11[i][1]))
        for j in range(i+1,100):
            c = c + 1
            print("i;",i)
            print("j;",j)
            print("c:",c)
            print(crossList11)
            print("数;",len(crossList11))
            
            if len(crossList11) <= c:
               break
            
            if (crossList11[i][0] - 10 <= crossList11[c][0] and crossList11[c][0] < crossList11[c][0] + 10) and (crossList11[c][1] - 10 <= crossList11[c][1] and crossList11[c][1]< crossList11[i][1] + 10):
               
               cLi.append((crossList11[c][0],crossList11[c][1]))
               crossList11.remove(crossList11[c])
               c = c - 1
            
        cLi2 = sorted(cLi)
        print(cLi2)
        if len(cLi2) == 1:
           crossList2.append((cLi2[0]))
        elif len(cLi2) == 2:
             crossList2.append((cLi2[0][0],cLi2[0][1]))
        elif len(cLi2)%2 == 0 and len(cLi2)!=2:
             a = int((len(cLi2)-1)/2)
             crossList2.append((cLi2[a][0],cLi2[a][1]))
        elif len(cLi2)%2 != 0 and len(cLi2)!=1:
             a = int(((len(cLi2)-1)/2)+1)
             crossList2.append((cLi2[a][0],cLi2[a][1]))
        
    print("draw_cross_points:", c3)
    #print(crossList)
    #print(crossList2)
    crossList3 = sorted(crossList2)
    #print(len(crossList))
    #print(crossList3)
    for i in range(len(crossList3)):
        cv2.circle(image, (crossList3[i][0],crossList3[i][1]), 5, (0,255,0), 5) # 交点を緑色で描画
        
    size4 = len(crossList3)
    size5 = len(sidelineList)
    
    if size4<6:
       return 0
    
    #print(sidelineList)
    print(size4)
    print(size5)
    
    sidelineunder = 0
    if b == 0:
       v = size4-1
       for i in range(size5):
           if size5 <= i:
              break
           elif (sidelineList[i][0] <= crossList3[v][0]<= sidelineList[i][2]) and (sidelineList[i][3] <= crossList3[v][1] <= sidelineList[i][1]):
               cv2.line(image,(sidelineList[i][0],sidelineList[i][1]),(sidelineList[i][2],sidelineList[i][3]),(255,0,255),2)
               if lineList[i][3]-lineList[i][1]!=0 and lineList[i][2]-lineList[i][0]!=0:
                  sidelineunder = (lineList[i][3]-lineList[i][1]) * (lineList[i][2]-lineList[i][0])
               elif lineList[i][3]-lineList[i][1]==0: # X軸に平行
                    sidelineunder = 0
               elif lineList[i][2]-lineList[i][0]==0: # Y軸に平行
                    sidelineunder = 1
       aa = crossList3[v-5][0]
       ab = crossList3[v-5][1]
       print(sidelineunder)
       
    elif b == 1:
         v = 0
         for i in range(size5):
           if size5 <= i:
              break
           elif (sidelineList[i][0] <= crossList3[v][0]<= sidelineList[i][2]) and (sidelineList[i][3] <= crossList3[v][1] <= sidelineList[i][1]):
               cv2.line(image,(sidelineList[i][0],sidelineList[i][1]),(sidelineList[i][2],sidelineList[i][3]),(255,0,255),2)
               m = 0
               if lineList[i][3]-lineList[i][1]!=0 and lineList[i][2]-lineList[i][0]!=0:
                  m = (lineList[i][3]-lineList[i][1]) / (lineList[i][2]-lineList[i][0])
               elif lineList[i][3]-lineList[i][1]==0: # X軸に平行
                  m = 0
               elif lineList[i][2]-lineList[i][0]==0: # Y軸に平行
                  m = 1
               print(m)
         aa = crossList3[v+5][0]
         ab = crossList3[v+5][1]
         
    print(aa)
    print(ab)
    aaaa = 0
    upList = []
    for i in range(size5):
        if size5 <= i:
           break
        elif (sidelineList[i][0] <= aa and aa <= sidelineList[i][2]) and (sidelineList[i][1] >= ab and ab >= sidelineList[i][3]):
           upList.append(sidelineList[i])
           m = 0
           if lineList[i][3]-lineList[i][1]!=0 and lineList[i][2]-lineList[i][0]!=0:
                  m = (lineList[i][3]-lineList[i][1]) / (lineList[i][2]-lineList[i][0])
           elif lineList[i][3]-lineList[i][1]==0: # X軸に平行
                m = 0
           elif lineList[i][2]-lineList[i][0]==0: # Y軸に平行
                m = 1
                
           print(m)
           #if np.tan(-2*np.pi/180)+sidelineunder <= m and m <= np.tan(2*np.pi/180)+sidelineunder:
           
           #cv2.line(image,(List[i][0],sidelineList[i][1]),(aa,ab),(255,0,255),2)
           aaaa = aaaa + 1
           #else:
              #return 0
    upList = sorted(upList)
    print("uplist:",upList)
    size6 = len(upList)
    if size6 == 0:
       return 0
    cv2.line(image,(upList[size6-1][0],upList[size6-1][1]),(aa,ab),(255,0,255),2)
    print(size6)
    ac = []
    cv2.line(image,(aa,ab),(crossList3[v][0],crossList3[v][1]),(255,0,255),2)
    print(endlineList)
    print(endlineList11)
    ac = line(endlineList11)
    print(ac)
    print(len(ac))
    print(c11)
    print(c12)
    print("エンドライン:",c11)
    print("サイドライン:",c2)
    print("合計:",c1+c2)
    print("サイドライン本数",aaaa)
    
    return 1

if __name__ == '__main__':
    main()

