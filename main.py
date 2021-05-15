import tkinter as tk
from math import sqrt

class Main(tk.Frame):
    """Main frame"""

    def __init__(self, window , **kwargs):
        tk.Frame.__init__(self, window, **kwargs)
        self.pack(fill=tk.BOTH, expand=True)
        self.sim = Simulation(self)
        self.graph = Graph(self)
        self.chocs = 0



class Graph(tk.Canvas):
    """Representation"""

    def __init__(self, _parent):
        self.size = 480
        self.p = _parent
        super().__init__(_parent, background="white",width=self.size ,height=self.size)
        self.pack(fill=tk.BOTH, side="right", expand=True)
        self.r = 200
        self.create_oval(self.size/2-self.r,self.size/2-self.r,self.size/2+self.r,self.size/2+self.r)
        self.v = (self.p.b1.v, self.p.b2.v)
        self.s = -self.r/(self.v[0]*sqrt(self.p.b1.m))

    def update(self):
        id = self.create_line(self.size/2 + self.v[0]*sqrt(self.p.b1.m)*self.s,
                            self.size/2 + self.v[1]*sqrt(self.p.b2.m)*self.s,
                            self.size/2 + self.p.b1.v*sqrt(self.p.b1.m)*self.s,
                            self.size/2 + self.p.b2.v*sqrt(self.p.b2.m)*self.s)

        self.v = (self.p.b1.v, self.p.b2.v)
        print(self.p.chocs)
        return id


class Simulation(tk.Canvas):
    """docstring for Simulation."""

    def __init__(self, _parent):
        self.size = (800,480)
        self.p = _parent
        self.liney = self.size[1]-100

        self.l = 0

        super().__init__(_parent, background="black",width=self.size[0] ,height=self.size[1])
        self.pack(fill=tk.BOTH, side="left", expand=True)

        self.p.b1 = Bloc(100, -0.1, 200, 100, self)
        self.p.b2 = Bloc(1, 0, 50, 100, self)

        self.b1 = self.p.b1
        self.b2 = self.p.b2

        self.sc = 1/2*(self.b1.m*self.b1.v**2+self.b2.m*self.b2.v**2)

        self.drawSim()

    def drawSim(self):
        self.update()


        self.delete(self.l)
        self. l = self.create_line(0, self.liney, self.size[0], self.liney, fill="white")


        if self.b2.pos+self.b2.size >= self.b1.pos:
            self.p.chocs += 1

            m1, m2 = self.b1.m, self.b2.m
            mc = self.b1.m*self.b1.v +self.b2.m*self.b2.v
            ec = self.sc

            self.b1.v = (2*sqrt(m1/m2)*mc + sqrt((mc**2)*-4 + 8*ec*((m1/m2)+1)))/(2*((m1/m2)+1)*sqrt(m1))
            self.b2.v = (mc-m1*self.b1.v)/m2
            self.p.graph.update()

        self.b1.move()
        self.b2.move()

        self.b1.draw()
        self.b2.draw()
        self.after(1,self.drawSim)

class Bloc():
    """Moving bloc"""

    def __init__(self, _m, _v0, _pos0, _size, _c):
        self.m = _m
        self.v = _v0
        self.pos = _pos0
        self.size = _size
        self.c = _c
        self.id = 0

    def draw(self):
        self.c.delete(self.id)
        self.id = self.c.create_rectangle(self.pos, self.c.liney, self.pos+self.size, self.c.liney-self.size, outline="white",fill="pink")

    def move(self):
        if self.pos <= 0:
            self.v *= -1
            self.c.p.chocs +=1
            self.c.p.graph.update()

        self.pos += self.v



root = tk.Tk()
main = Main(root)
main.mainloop()
