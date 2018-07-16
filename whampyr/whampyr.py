# -*- coding: utf-8 -*-

"""Main module."""

from fart import solver_tree


class Whampyr(object):
    def __init__(self, plasma, f, solver_m = solver_tree, **solver_kwargs):
        self.solver_m      = solver_m
        self.plasma        = plasma
        self.disp_func     = f
        self.solver_kwargs = solver_kwargs


    def solve(self, w_domain, **k):
        self.solver = self.solver_m.Solver(self.disp_func,
                                           w_domain,
                                           kpara=k["kpara"], kperp=k["kperp"],
                                           **self.solver_kwargs)
        self.solver.solve()
        return self.solutions()


    def solutions(self):
        return self.solver.zeros







