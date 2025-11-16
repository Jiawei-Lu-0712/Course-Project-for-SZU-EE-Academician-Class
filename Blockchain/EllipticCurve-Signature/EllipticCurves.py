from FieldElement import FieldElemet, BitcoinFieldElement
import hashlib
from random import randrange


class EllipticPoint:
    def __init__(self, x, y, a, b):
        '''
        x, y, a, b 分别对应椭圆曲线公式上的参数
        '''
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        if x is None and y is None:
            return
        #验证x,y是否在曲线上，也就是将x,y带入公式后左右两边要想等
        if self.y ** 2 != self.x ** 3 + self.a * self.x + self.b:
            raise ValueError(f"x:{self.x}, y:{self.y} is no a elliptic point")
    """重载类的魔法属性方法，判断点相同、不同、相加、相乘等"""
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y or self.a != other.a or self.b != other.b

    def __repr__(self):
        return f"x:{self.x}, y:{self.y}, a:{self.a}, b:{self.b}"

    def __add__(self, other):
        #首先判断给定点在该椭圆曲线上
        if self.a != other.a or self.b != other.b:
            raise ValueError(f"given point is no on the same elliptic curve")

        # 如果本身是零元，那么实现I + A = A
        if self.x is None and self.y is None:
            return other

        # 如果输入点是零元，那么加法结果就是本身：
        if other.x is None and other.y is None:
            return self

        # 如果输入点与当前点互为相反数，也就是关于x轴对称，那么返回无限远交点I
        if self.x == other.x and self.y != other.y: # 这里针对有限群里面的点进行了修改
            return self.__class__(None, None, self.a, self.b)

        '''
        如果当前点与给定点形成的直线与椭圆曲线有三个交点，首先我们要计算A(x1,y1),B(x2,y2)所形成直线的斜率
        s = (y2-y1)/(x2-x1), 于是A,B所形成的直线方程就是 y = s * (x-x1) + y1,
        由于椭圆曲线的方程为 y^2 = x^2 + a*x + b，由于直线与曲线相交，假设叫点的坐标为x', y'
        由于交点在直线上，因此满足 y' = s * (x' - x1) + y1, 同时又满足y' ^ 2 = x' ^ 3 + a * x' + b,
        将左边带入到右边就有：
        (s * (x' - x1)) ^ 2 = x' ^ 3 + a * x' + b
        把公式左边挪到右边然后进行化简后就有：
        x ^3 - (s^2) * (x^2) + (a + 2*(s^2)*x1 - 2*s*y1)*x + b - (s^2)*(x1^2)+2*s*x1*y1-(y1 ^2) = 0  (公式1）
        如果我们把第三个交点C的坐标设置为(x3, y3)，于是A，B,C显然能满足如下公式：
        (x-x1)*(x-x2)*(x-x3) = 0
        将其展开后为：
        x^3 - (x1 + x2 + x3) * (x^2) + (x1*x2 + x1*x3 + x2+x3)*x - x1*x2*x3 = 0  （公式2）
        我们把公式1 和公式2中对应项的系数一一对应起来，也就是两个公式中x^3的系数是1，公式1中x^2的系数是(s^2)，
        公式2中x^2的系数为(x1 + x2 + x3)，于是对应起来：
        s^2 <-> (x1 + x2 + x3)  （#1）
        公式1中x对应系数为(a + 2*(s^2)*x1 - 2*s*y1), 公式2中x对应系数为(x1*x2 + x1*x3 + x2+x3)，于是对应起来：
        (a + 2*(s^2)*x1 - 2*s*y1) <-> (x1*x2 + x1*x3 + x2+x3)
        公式1中常数项为b - (s^2)*(x1^2)+2*s*x1*y1-(y1 ^2), 公式2中常数项为 x1*x2*x3，对应起来就是：
        b - (s^2)*(x1^2)+2*s*x1*y1-(y1 ^2) <-> x1*x2*x3
        
        根据代数理论中中的Vieta定律，如果如果两个多项式的根要相同，他们对应项的系数必须相等，于是有：
        s^2 = (x1 + x2 + x3)  （#1）
        (a + 2*(s^2)*x1 - 2*s*y1) = (x1*x2 + x1*x3 + x2+x3)
        b - (s^2)*(x1^2)+2*s*x1*y1-(y1 ^2) = x1*x2*x3
        于是我们可以从(#1)中把x3 解出来：
        x3 = s^2 - x1 - x2 
        然后把x3放入直线方程将y3解出来：
        y3 = -(s(x3-x1)+y1) = s * (x1 - x3) - y1
        '''
        """这里概括一下：定义一条直线与椭圆曲线有三个交点（这三个点可以三点不重合、其中两点重合以及有无穷远点），这三种情况可以画图理解"""
        if self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            x3 = s ** 2 - self.x - other.x
            y3 = s * (self.x - x3) - self.y
            return self.__class__(x3, y3, self.a, self.b)
        '''
        如果self.x == other.x and self.y == other.y ,这种情况下对应椭圆曲线上一点的切线，这时
        我们要计算切线与曲线的另一个交点。根据微积分，函数f(x)在给定点x处的切线对应斜率就是f'(x)，
        椭圆曲线函数为y^2 = x^3 + a*x + b, 左右两步对x求导有：
        2y*(d(y)/d(x)) = 3x^2 + a, d(y)/d(x)就是f'(x),我们需要将其计算出来，也就有:
        s = d(y)/d(x) = (3*x^2+a)/(2*y),接下来的计算跟上面一样，只不过把x2换成x1,于是有：
        x3 = s^2 - 2*x1, y3 = s * (x1 - x3) - y1
        '''
        if self == other : #这里针对有限群的元素进行修改
            s = (3 * self.x ** 2 + self.a) / (2 * self.y)  #修改bug
            x3 = s ** 2 - 2 * self.x
            y3 = s * (self.x - x3) - self.y
            return self.__class__(x3, y3, self.a, self.b)

        '''
        还有最后一种情况，直线不但与y轴平行，而且还是曲线的切线，有就是一根竖直线与曲线在源头处相切，这也是为什么要椭圆曲线引入无穷远点的原因，两条平行线（y轴、平行y轴的直线）在无穷远点相交，PS：黎曼几何
        这个点也是y坐标为0的点
        '''
        if self == other and 0 * self.x: #这里的修改可以应对有限群元素的情况
            return self.__class__(None, None, self.a, self.b)
    #这里使用二倍乘法
    def __rmul__(self, scalar):
        result = self.__class__(None, None, self.a, self.b)
        current = self
        while scalar:
            if scalar & 1:
                result += current
            current += current
            scalar >>= 1
        return result

"""传入参数，y^2=x^3+7 mod 233 ,测试两点相加。PS：y^2=x^3+7是secp256k1的特定椭圆曲线"""
a = FieldElemet(0, 223)
b = FieldElemet(7, 223)
x = FieldElemet(192, 223)
y = FieldElemet(105, 223)

p = EllipticPoint(x, y, a, b)

print(f"p + p is :{p+p}")

x = FieldElemet(47,  223)
y = FieldElemet(71, 223)
p = EllipticPoint(x, y, a, b)
for s in range(1, 21):
    result = s * p
    print(f"{s} * [(47,71) over 233]  = [({result.x.num},{result.y.num}) over 233]")

"""测试有限域内，椭圆曲线某一点P的阶数n，即nP=O(无穷远点），判断(n+1)P=P,可得n的值"""
a = FieldElemet(0, 223)
b = FieldElemet(7, 223)
x = FieldElemet(15, 223)
y = FieldElemet(86, 223)

p = EllipticPoint(x, y, a, b)
p1 = p + p
n = 1
while p1 != p:
    p1 += p
    n += 1

print(f"order of the group is {n}")       #打印该有限群里面的点

"""给出secp256k1签名算法的数据，y^2=x^3+7，以及N和基点G的坐标"""

A = 0
B = 7
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141


class BitcoinEllipticPoint(EllipticPoint):
    #重载类的魔法属性

    def __init__(self, x, y, a = None, b = None):
        a, b = BitcoinFieldElement(A), BitcoinFieldElement(B)
        if type(x) == int:
            super().__init__(x = BitcoinFieldElement(x), y = BitcoinFieldElement(y), a = a, b = b)
        else:
            super().__init__(x = x, y = y, a = a, b = b)

    def __rmul__(self, scalar):
        scalar = scalar % N
        return super().__rmul__(scalar)
    """定义验证签名函数,"""
    def verify(self, z, sig):
        s_invert = pow(sig.s, N- 2, N) #费马小定理计算s的逆
        u = z * s_invert % N
        v = sig.r * s_invert % N
        total = u * G + v * self
        return total.x.num == sig.r

G = BitcoinEllipticPoint(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
                         0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)


"""定义签名认证函数，我们签名：r=kG.x，s=(z+r*e)*k^-1=(z+ekG)*k^-1;
那验证用公钥P=eG,计算(z*s^-1*G + r*s^-1*P)=(z*G+r*P)*s^-1=(zG+kGeG)*[k(z+ekG)^-1]=kG(z+ekG)*(z+ekG)^-1=kG

上面公式比较长，但其实就是，通过原数据z，公钥P=eG算出kG的过程
 """
def verify_signature(r, s, z, P):
    s_invert = pow(s, N - 2, N)  # 使用费马小定理直接找到s的逆元素
    u = z * s_invert % N  # u = z / s
    v = r * s_invert % N # v = r / s
    return (u * G + v * P).x.num == r # 检验x坐标对应数值是否等于 r

"""生成签名"""

class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s
    def __repr__(self):
        return f"Signature({hex(self.r)}, {hex(self.s)})"
#将私钥、签名信息通过哈希函数得到哈希值，并用16进制表示
private_key_str = "this is my secret key"
message_str = "message I want to send"
e = "0x" + hashlib.sha256(private_key_str.encode('utf-8')).hexdigest()
z = "0x" + hashlib.sha256(message_str.encode('utf-8')).hexdigest()
e = int(e, 16)
z = int(z, 16)

k = randrange(10000)        #随机选一个整数k

r = (k * G).x.num           #kG=(x,y),r=x (mod n)
k_invert = pow(k, N - 2, N) #费马小定理计算k的逆，k^-1指k*k^-1==1 mod p
print(e.to_bytes(32, 'big'))

P = e * G                   #这个是公钥，需要用于验证签名
s = (z + r * e) * k_invert % N
#输出签名（r，s），并发布公钥让大家验证签名
print(f"r is {hex(r)}")
print(f"s is {hex(s)}")
print(f"public key is: {P}")
#验证签名
verify_res = verify_signature(r = r, s = s, z = z, P = P)
print(f"verify result is {verify_res}")


