import tkinter as tk
from math import sqrt, log

class Main(tk.Frame):
    """Main frame"""

    def __init__(self, window , _d, _dt, _circle, **kwargs):
        tk.Frame.__init__(self, window, **kwargs)
        self.pack(fill=tk.BOTH, expand=True)
        self.sim = Simulation(self, _d, _dt)
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
                                self.size/2 + self.v[1]*sqrt(self.p.b2.m)*self.s,
                                self.size/2 + self.p.b1.v*sqrt(self.p.b1.m)*self.s,
                                self.size/2 + self.p.b2.v*sqrt(self.p.b2.m)*self.s,fill="white")
            self.v = (self.p.b1.v, self.p.b2.v)
        self.delete(self.t)
        self.t = self.create_text(self.size/2,15,text=str(self.p.chocs),anchor=tk.CENTER,fill="white",font=('Times', '12'))


class Simulation(tk.Canvas):
    """docstring for Simulation."""

    def __init__(self, _parent, _d, _dt):
        self.size = (800,480)
        self.p = _parent
        self.liney = self.size[1]-100
        self.dt = _dt
        self.d = _d
        self.l = 0

        super().__init__(_parent, background="black",width=self.size[0] ,height=self.size[1])
        self.pack(fill=tk.BOTH, side="left", expand=True)

        self.p.b1 = Bloc(100**self.d, -0.1, 300, self)
        self.p.b2 = Bloc(1, 0, 100, self)

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
            self.b1.move(dt)
            self.b2.move(dt)

class Bloc():
    """Moving bloc"""

    def __init__(self, _m, _v0, _pos0, _c):
        self.m = _m
        self.v = _v0
        self.pos = _pos0
        self.size = self.getSize()
        self.c = _c
        self.id = 0

    def draw(self):
        self.c.delete(self.id)
        self.id = self.c.create_rectangle(self.pos, self.c.liney, self.pos+self.size, self.c.liney-self.size, outline="white",fill="pink")

    def move(self,dt):
        if self.pos <= 0:
            self.v *= -1
            self.c.p.chocs += 1
            self.c.p.graph.update()
        self.pos += self.v*dt

    def getSize(self):
        return 20*2**(log(self.m, 100))


root = tk.Tk()
main = Main(root, 4, 0.01, False)
main.mainloop()
