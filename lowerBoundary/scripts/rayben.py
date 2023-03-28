"""
To run and plot using e.g. 4 processes:
    $ mpiexec -n 4 python3 rayben.py
    $ mpiexec -n 4 python3 plot.py snapshots/*.h5
    $ mpiexec -n 4 python3 plot.py snapshots/*.h5 --output=asdf
"""

import numpy as np
import dedalus.public as d3
import logging
logger = logging.getLogger(__name__)
from sys import argv
from os import system
import os
from time import time


# input parameters
try:
    assert len(argv) in [7,9]
    logRaf,logPrf,s,res,stop_sim_time,Lx = [float(t) for t in argv[1:7]]
    cont = len(argv)==7
    if not cont: Ra0,Pr0 = [10**float(t) for t in argv[7:9]]
    else: Ra0,Pr0 = 1,1
    Raf,Prf = 10**logRaf,10**logPrf


except Exception as e:
    print(e)
    print('input: logRaf,logPrf,speed,res,stop_sim_time,Lx,logRa0,logPr0')
    print('or:    logRaf,logPrf,speed,res,stop_sim_time,Lx                  (if continuing from an existing run)')
    exit(1)


# Parameters
Lz = 1
Nx,Nz = int(Lx*res),int(res)
dealias = 3/2
timestepper = d3.RK222
max_timestep = 0.125
dtype = np.float64


# Bases
coords = d3.CartesianCoordinates('x', 'z')
dist = d3.Distributor(coords, dtype=dtype)
xbasis = d3.RealFourier(coords['x'], size=Nx, bounds=(0, Lx), dealias=dealias)
zbasis = d3.ChebyshevT(coords['z'], size=Nz, bounds=(0, Lz), dealias=dealias)

# Fields
myRa  = dist.Field(name='myRa',  bases=(xbasis,zbasis))
myPr  = dist.Field(name='myPr',  bases=(xbasis,zbasis))
myLx  = dist.Field(name='myLx',  bases=(xbasis,zbasis))
myRes = dist.Field(name='myRes', bases=(xbasis,zbasis))

p = dist.Field(name='p', bases=(xbasis,zbasis))
b = dist.Field(name='b', bases=(xbasis,zbasis))
u = dist.VectorField(coords, name='u', bases=(xbasis,zbasis))
tau_p = dist.Field(name='tau_p')
tau_b1 = dist.Field(name='tau_b1', bases=xbasis)
tau_b2 = dist.Field(name='tau_b2', bases=xbasis)
tau_u1 = dist.VectorField(coords, name='tau_u1', bases=xbasis)
tau_u2 = dist.VectorField(coords, name='tau_u2', bases=xbasis)

# Substitutions
x, z = dist.local_grids(xbasis, zbasis)
ex, ez = coords.unit_vector_fields(dist)
lift_basis = zbasis.derivative_basis(1)
lift = lambda A: d3.Lift(A, lift_basis, -1)
grad_u = d3.grad(u) + ez*lift(tau_u1) # First-order reduction
grad_b = d3.grad(b) + ez*lift(tau_b1) # First-order reduction

# Problem
# First-order form: "div(f)" becomes "trace(grad_f)"
# First-order form: "lap(f)" becomes "div(grad_f)"
problem = d3.IVP([p, myRa, myPr, myRes, myLx, b, u, tau_p, tau_b1, tau_b2, tau_u1, tau_u2], namespace=locals())

def func(x): return x/abs(x) if x!=0 else 0

problem.add_equation("dt(myRa)  = func(Raf-myRa)*s*myRa")      # assuming Ra<Raf
problem.add_equation("dt(myPr)  = func(Prf-myPr)*s*myPr")      # assuming Pr>Prf
problem.add_equation("dt(myRes) = 0")
problem.add_equation("dt(myLx)  = 0")

problem.add_equation("trace(grad_u) + tau_p = 0")
problem.add_equation("dt(b) - div(grad_b) + lift(tau_b2)                  = ((myRa * myPr)**(-1/2)-1)*div(grad_b) - u@grad(b)")
problem.add_equation("dt(u) - div(grad_u) + grad(p) - b*ez + lift(tau_u2) = ((myRa / myPr)**(-1/2)-1)*div(grad_u) - u@grad(u)")
problem.add_equation("(grad_b@ez)(z=0)  = -Lz")     # fixed flux
problem.add_equation("(grad_b@ez)(z=Lz) = -Lz")     # fixed flux
problem.add_equation("u(z=0) = 0")                  # no slip
problem.add_equation("u(z=Lz) = 0")                 # no slip
problem.add_equation("integ(p) = 0") # Pressure gauge

# Solver
solver = problem.build_solver(timestepper)
solver.stop_sim_time = stop_sim_time

# Initial conditions
if not cont:
    myRa.fill_random('g', seed=42, distribution='normal', scale=1e-3) # Random noise
    myRa['g'] = Ra0
    myPr.fill_random('g', seed=42, distribution='normal', scale=1e-3) # Random noise
    myPr['g'] = Pr0
    myLx.fill_random('g', seed=42, distribution='normal', scale=1e-3) # Random noise
    myLx['g'] = Lx
    myRes.fill_random('g', seed=42, distribution='normal', scale=1e-3) # Random noise
    myRes['g'] = res

    b.fill_random('g', seed=40, distribution='normal', scale=1e-3) # Random noise
    b['g'] *= z * (Lz - z) # Damp noise at walls
    b['g'] += Lz - z # Add linear background
    file_handler_mode = 'overwrite'
else:
    latest = max([int(t.split('_s')[1].split('.')[0]) for t in os.listdir('checkpoints') if t[-3:] == '.h5'])
    solver.load_state('checkpoints/checkpoints_s%s.h5' % latest)
    initial_timestep = 2e-2
    myLx['g'] = Lx
    myRes['g'] = res
    file_handler_mode = 'append'

# Analysis
snapshots = solver.evaluator.add_file_handler('snapshots', sim_dt=5, max_writes=50, mode=file_handler_mode)
snapshots.add_task(b,     name='b')
snapshots.add_task(myRa,  name='myRa')
snapshots.add_task(myPr,  name='myPr')
snapshots.add_task(myLx,  name='myLx')
snapshots.add_task(myRes, name='myRes')
checkpoints = solver.evaluator.add_file_handler('checkpoints', sim_dt=5, max_writes=1, mode=file_handler_mode)
checkpoints.add_tasks(solver.state)



# CFL
CFL = d3.CFL(solver, initial_dt=max_timestep, cadence=10, safety=0.5, threshold=0.05, max_change=1.5, min_change=0.5, max_dt=max_timestep)
CFL.add_velocity(u)


# Main loop
try:
    logger.info('Starting main loop')
    while solver.proceed:
        timestep = CFL.compute_timestep()
        solver.step(timestep)
        if (solver.iteration-1) % 10 == 0:
            open('progress.txt','a').write('Iteration=%i, Time=%e, dt=%e\n' %(solver.iteration, solver.sim_time, timestep))
except:
    logger.error('Exception raised, triggering end of main loop.')
    raise
finally:
    solver.log_stats()

