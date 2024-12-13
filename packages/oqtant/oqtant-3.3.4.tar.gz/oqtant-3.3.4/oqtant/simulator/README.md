# Oqtant Simulator
The Oqtant simulator provides a theoretical simulation of a pure Bose-Einstein condensate in a magnetic trap with the 
same trap frequencies as the Oqtant hardware. The simulator is a useful tool for designing experiments to run on Oqtant 
hardware as it is always available! The simulation runs locally on your computer. 

Simulation jobs require an Oqtant account and use the same workflow as normal jobs, but do NOT count against your 
job quota or daily limit.

## User Authentication
Simulator jobs are run locally and totally free! There is no limit to the number of simulations you may run per day 
with OqtAPI. However, the simulator still requires a valid authentication/token to use QuantumMatterFactory methods. 
These tokens last for 2 hours and may be refreshed by re-evaluating the first 2 cells only. There is no need to restart 
the kernel to refresh your token. Job limits and usage are displayed in every authenticated notebook whether you are 
running simulator or hardware jobs, which may exist in the same notebook (like this one!).

First create a QuantumMatterFactory object and login to Oqtant.
```python
from oqtant.schemas.quantum_matter import QuantumMatterFactory, QuantumMatter
from IPython.display import HTML
from matplotlib import pyplot as plt

# get the login
qmf = QuantumMatterFactory()
qmf.get_login()
```

Next you can create your client.
```python
qmf.get_client()
```

## How to use the Simulator
The use of the simulator is the same as the hardware jobs. The only difference is in the `submit()` function, simply 
pass in the argument `sim=True`. You can then retrieve the result with the same `get_result()` method as a hardware job.

In addition to the standard result data available to hardware run jobs, the simulator also comes with lots of fun 
visualization tools to explore the quantum wavefunction of your simulated BEC. See Walkthrough 6 in the documentation 
for a more thorough introduction to the Oqtant Simulator and to explore all the visualizations available.

### Steps to submit a Simulator Job
1. Create barrier and/or landscape object(s)
2. Instantiate a matter object
3. Submit the simulation job
4. Retrieve the job results
5. View Simulator results

### Example
```python
# Create Barrier object
barrier1 = qmf.create_barrier(
    positions=[0, 0],
    heights=[0, 3],
    widths=[1, 1],
    times=[0, 6],
    shape="GAUSSIAN",
)
barrier1.evolve(duration=4, height=3)

# Instantiate a matter object
sim_matter = qmf.create_quantum_matter(
    barriers=[barrier1, barrier2], lifetime=10, image="IN_TRAP"
)

sim_matter.show_potential([2, 8, 9], ylimits=[0, 8])

# Submitthe simulation job
sim_matter.submit(sim=True)

# Retrieve the job results
sim_matter.get_result()

# View simulator Results
sim_matter.output.plot_it(grid_on=False)
```
