<!-- markdownlint-disable -->

# API Overview

## Modules

- [`oqtant_client`](./oqtant_client.md#module-oqtant_client)
- [`schemas`](./schemas.md#module-schemas)
- [`schemas.job`](./schemas.job.md#module-schemasjob)
- [`schemas.optical`](./schemas.optical.md#module-schemasoptical)
- [`schemas.output`](./schemas.output.md#module-schemasoutput)
- [`schemas.quantum_matter`](./schemas.quantum_matter.md#module-schemasquantum_matter)
- [`schemas.rf`](./schemas.rf.md#module-schemasrf)
- [`settings_dev`](./settings_dev.md#module-settings_dev)
- [`simulator`](./simulator.md#module-simulator)
- [`simulator.qm_potential`](./simulator.qm_potential.md#module-simulatorqm_potential)
- [`simulator.simulator`](./simulator.simulator.md#module-simulatorsimulator)
- [`simulator.three_dim`](./simulator.three_dim.md#module-simulatorthree_dim)
- [`simulator.wave_function`](./simulator.wave_function.md#module-simulatorwave_function)
- [`start_notebook`](./start_notebook.md#module-start_notebook)
- [`util`](./util.md#module-util)
- [`util.auth`](./util.auth.md#module-utilauth)
- [`util.exceptions`](./util.exceptions.md#module-utilexceptions)

## Classes

- [`oqtant_client.OqtantClient`](./oqtant_client.md#class-oqtantclient): Python class for interacting with Oqtant
- [`job.OqtantJob`](./schemas.job.md#class-oqtantjob): A class that represents a job submitted to Oqtant
- [`optical.Barrier`](./schemas.optical.md#class-barrier): Class that represents a painted optical barrier.
- [`optical.Landscape`](./schemas.optical.md#class-landscape): Class that represents a dynamic painted-potential optical landscape constructed
- [`optical.Laser`](./schemas.optical.md#class-laser): Class that represents a terminator laser with a single pulse.
- [`optical.Pulse`](./schemas.optical.md#class-pulse): Class that represents a terminator laser pulse
- [`optical.Snapshot`](./schemas.optical.md#class-snapshot): A class that represents a painted optical landscape/potential at a single
- [`output.AxisType`](./schemas.output.md#class-axistype)
- [`output.OqtantNonPlotOutput`](./schemas.output.md#class-oqtantnonplotoutput)
- [`output.OqtantOutput`](./schemas.output.md#class-oqtantoutput): A class that represents the output of a job submitted to Oqtant
- [`output.OqtantPlotOutput`](./schemas.output.md#class-oqtantplotoutput)
- [`output.OutputImageType`](./schemas.output.md#class-outputimagetype)
- [`quantum_matter.OqtantLogin`](./schemas.quantum_matter.md#class-oqtantlogin): OqtantLogin(access_token: 'str | None' = None)
- [`quantum_matter.QuantumMatter`](./schemas.quantum_matter.md#class-quantummatter): A class that represents user inputs to create and manipulate quantum matter
- [`quantum_matter.QuantumMatterFactory`](./schemas.quantum_matter.md#class-quantummatterfactory): An abstract factory for creating instances of the QuantumMatter schema classes
- [`rf.ConversionError`](./schemas.rf.md#class-conversionerror)
- [`rf.RfEvap`](./schemas.rf.md#class-rfevap): A class that represents the forced RF evaporation that cools atoms to quantum degeneracy.
- [`rf.RfSequence`](./schemas.rf.md#class-rfsequence): A class that represents a sequence of radio frequency powers/frequencies in time
- [`rf.RfShield`](./schemas.rf.md#class-rfshield): A class that represents an RF shield (at fixed frequency and power)
- [`settings_dev.Settings`](./settings_dev.md#class-settings)
- [`qm_potential.QMPotential`](./simulator.qm_potential.md#class-qmpotential): 'QMPotential' represents the quantum matter object potential (combination of magnetic trap/snapshot/barriers)
- [`simulator.Simulator`](./simulator.simulator.md#class-simulator): 'Simulator' Defines methods for evolution and plotting of the system described by the Oqtant simulator.
- [`simulator.TimeSpan`](./simulator.simulator.md#class-timespan): TimeSpan(start: float, end: float)
- [`three_dim.ThreeDimGrid`](./simulator.three_dim.md#class-threedimgrid): 'ThreeDimGrid' Defines a two dimensional grid space in cylindrical coordinates with axial symmetry.
- [`wave_function.WaveFunction`](./simulator.wave_function.md#class-wavefunction): 'WaveFunction' Defines representation for a wavefunction
- [`exceptions.JobError`](./util.exceptions.md#class-joberror)
- [`exceptions.JobPlotFitError`](./util.exceptions.md#class-jobplotfiterror)
- [`exceptions.JobPlotFitMismatchError`](./util.exceptions.md#class-jobplotfitmismatcherror)
- [`exceptions.JobReadError`](./util.exceptions.md#class-jobreaderror)
- [`exceptions.JobWriteError`](./util.exceptions.md#class-jobwriteerror)
- [`exceptions.OqtantAuthorizationError`](./util.exceptions.md#class-oqtantauthorizationerror)
- [`exceptions.OqtantError`](./util.exceptions.md#class-oqtanterror)
- [`exceptions.OqtantJobError`](./util.exceptions.md#class-oqtantjoberror)
- [`exceptions.OqtantJobListLimitError`](./util.exceptions.md#class-oqtantjoblistlimiterror)
- [`exceptions.OqtantJobParameterError`](./util.exceptions.md#class-oqtantjobparametererror)
- [`exceptions.OqtantJobUnsupportedTypeError`](./util.exceptions.md#class-oqtantjobunsupportedtypeerror)
- [`exceptions.OqtantJobValidationError`](./util.exceptions.md#class-oqtantjobvalidationerror)
- [`exceptions.OqtantRequestError`](./util.exceptions.md#class-oqtantrequesterror)
- [`exceptions.OqtantTokenError`](./util.exceptions.md#class-oqtanttokenerror)
- [`exceptions.SimSubmitError`](./util.exceptions.md#class-simsubmiterror)
- [`exceptions.SimValueError`](./util.exceptions.md#class-simvalueerror)
- [`exceptions.VersionWarning`](./util.exceptions.md#class-versionwarning)

## Functions

- [`oqtant_client.get_client`](./oqtant_client.md#function-get_client): Method to get both an authentication token and an instance of OqtantClient
- [`oqtant_client.get_oqtant_client`](./oqtant_client.md#function-get_oqtant_client): Method to create a new OqtantClient instance.
- [`job.print_keys`](./schemas.job.md#function-print_keys): Print the keys of a nested dictionary or list
- [`output.Gaussian_dist_2D`](./schemas.output.md#function-gaussian_dist_2d): Method to sample a 2D Gaussian distribution with given parameters on a grid of coordinates
- [`output.TF_dist_2D`](./schemas.output.md#function-tf_dist_2d): Method to sample a 2D Thomas-Fermi distribution with given parameters on a grid of coordinates
- [`output.bimodal_dist_2D`](./schemas.output.md#function-bimodal_dist_2d): Method to sample a bimodal (Thomas-Fermi + Gaussian) distribution with given parameters on a grid of coordinates
- [`output.in_trap_check`](./schemas.output.md#function-in_trap_check)
- [`output.round_sig`](./schemas.output.md#function-round_sig): Method to round a number to a specified number of significant digits
- [`start_notebook.get_running_ports`](./start_notebook.md#function-get_running_ports): Get running ports of Jupyter servers
- [`auth.generate_challenge`](./util.auth.md#function-generate_challenge): Method to generate a base64 string to serve as an auth0 challenge
- [`auth.generate_random`](./util.auth.md#function-generate_random): Method to generate a random base64 string
- [`auth.get_authentication_url`](./util.auth.md#function-get_authentication_url): Method to generate the auth0 authentication url
- [`auth.get_token`](./util.auth.md#function-get_token): Method to get an authentication token from auth0 after a user authenticates
- [`auth.get_user_token`](./util.auth.md#function-get_user_token): Method to initiate the user authentication process
- [`auth.login`](./util.auth.md#function-login): Route to initiate the authentication process
- [`auth.main`](./util.auth.md#function-main): Main route to handle user authentication
- [`auth.notebook_login`](./util.auth.md#function-notebook_login): Method to get an authenticate widget


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
