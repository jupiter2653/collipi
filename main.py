import tkinter as tk
from math import sqrt, log, cos, sin, pi

class Main(tk.Frame):
    """Main frame"""

    def __init__(self, window , _d, _dt, _circle, _sparkles, **kwargs):
        tk.Frame.__init__(self, window, **kwargs)
        self.pack(fill=tk.BOTH, expand=True)
        self.sim = Simulation(self, _d, _dt, _sparkles)
        self.graph = Graph(self,_circle)
        self.chocs = 0



class Graph(tk.Canvas):
    """Representation"""

    def __init__(self, _parent, _circle):
        self.size = 480
        self.p = _parent
        super().__init__(_parent, background="black",width=self.size ,height=self.size)
        self.pack(fill=tk.BOTH, side="right", expand=True)
        self.r = 200
        self.create_oval(self.size/2-self.r,self.size/2-self.r,self.size/2+self.r,self.size/2+self.r,outline="white")
        self.v = (self.p.b1.v, self.p.b2.v)
        self.s = -self.r/(self.v[0]*sqrt(self.p.b1.m))
        self.t = self.create_text(self.size/2,15,text="0",anchor=tk.CENTER,fill="white",font=('Times', '12'))
        self.circle = _circle

    def update(self):
        if self.circle:
            id = self.create_line(self.size/2 + self.v[0]*sqrt(self.p.b1.m)*self.s,
                                self.size/2 - self.v[1]*sqrt(self.p.b2.m)*self.s,
                                self.size/2 + self.p.b1.v*sqrt(self.p.b1.m)*self.s,
                                self.size/2 - self.p.b2.v*sqrt(self.p.b2.m)*self.s,fill="white")
            self.v = (self.p.b1.v, self.p.b2.v)
        self.delete(self.t)
        self.t = self.create_text(self.size/2,15,text=str(self.p.chocs),anchor=tk.CENTER,fill="white",font=('Times', '12'))


class Simulation(tk.Canvas):
    """docstring for Simulation."""

    def __init__(self, _parent, _d, _dt, _sparkles):
        self.size = (800,480)
        self.p = _parent
        self.liney = self.size[1]-100
        self.dt = _dt
        self.d = _d
        self.l = 0
        self.size0 = 50
        self.doSparkles = _sparkles
        self.sparkleList = []

        super().__init__(_parent, background="black",width=self.size[0] ,height=self.size[1])
        self.pack(fill=tk.BOTH, side="left", expand=True)

        self.p.b1 = Bloc(100**self.d, -0.1, 300, self, "white")
        self.p.b2 = Bloc(1, 0, 100, self, "red")

        self.b1 = self.p.b1
        self.b2 = self.p.b2

        self.sc = 1/2*(self.b1.m*self.b1.v**2+self.b2.m*self.b2.v**2)

        self.drawSim()

    def drawSim(self):
        self.update()


        self.delete(self.l)
        self. l = self.create_line(0, self.liney, self.size[0], self.liney, fill="white")

        if self.b2.pos <= self.size[0]+10:
            self.simulate(self.dt)

        self.b1.draw()
        self.b2.draw()

        for sparkle in self.sparkleList:
            sparkle.draw()

        self.after(1,self.drawSim)

    def simulate(self,dt):
        for i in range(int(1/dt)):
            if self.b2.pos+self.b2.size >= self.b1.pos:
                self.p.chocs += 1

                m1, m2 = self.b1.m, self.b2.m
                mc = self.b1.m*self.b1.v +self.b2.m*self.b2.v
                ec = self.sc

                self.b1.v = (2*sqrt(m1/m2)*mc + sqrt((mc**2)*-4 + 8*ec*((m1/m2)+1)))/(2*((m1/m2)+1)*sqrt(m1))
                self.b2.v = (mc-m1*self.b1.v)/m2
                self.p.graph.update()
                self.sparkle(self.b1.pos)

            self.b1.move(dt)
            self.b2.move(dt)

    def sparkle(self, x):
        if self.doSparkles:
            for o in [pi/4, 0, -pi/4, pi/2 ,3*pi/4, pi, -3*pi/4, -pi/2]:
                self.sparkleList.append(Sparkle(x, o, "pink", self))
            if len(self.sparkleList) >= 32:
                self.sparkleList = self.sparkleList[:32]

class Bloc():
    """Moving bloc"""

    def __init__(self, _m, _v0, _pos0, _c, _color):
        self.m = _m
        self.v = _v0
        self.pos = _pos0
        self.c = _c
        self.size = self.getSize()
        self.color = _color
        self.id = 0

    def draw(self):
        self.c.delete(self.id)
        self.id = self.c.create_rectangle(self.pos, self.c.liney, self.pos+self.size, self.c.liney-self.size,fill=self.color)

    def move(self,dt):
        if self.pos <= 0:
            self.v *= -1
            self.c.p.chocs += 1
            self.c.p.graph.update()
            self.c.sparkle(0)
        self.pos += self.v*dt

    def getSize(self):
        return self.c.size0*2**(log(self.m, 100))



class Sparkle():
    """Glowing sparkle"""

    def __init__(self, x, o, _color, _c):
        d = 15
        l = 5
        self.color = _color
        self.c = _c
        self.lt = 100
        y = _c.liney-self.c.size0/2
        self.line = [x+d*cos(o), y-d*sin(o),x+(d+l)*cos(o),y-(d+l)*sin(o)]
        self.id = 0

    def draw(self):
        self.lt -= 1
        self.c.delete(self.id)
        if self.lt >= 0:
            self.id = self.c.create_line(*self.line, fill=self.color, width=2)
        else:
            self.c.sparkleList.remove(self)


root = tk.Tk()
main = Main(root, 2, 0.1, True, True)
main.mainloop()
