#!/usr/bin/env python
import os
import subprocess
import time
import json
import numpy as np
import matplotlib.pyplot as plt
from ase.eos import EquationOfState
from ase import Atoms as AseAtoms
from ase.units import kJ
from ase.constraints import ExpCellFilter
from ase.optimize.fire import FIRE
import ase.units
from jarvis.db.figshare import data
from jarvis.core.atoms import Atoms, ase_to_atoms
from jarvis.io.vasp.inputs import Poscar
from jarvis.core.kpoints import Kpoints3D as Kpoints
from jarvis.analysis.defects.vacancy import Vacancy
from jarvis.analysis.defects.surface import Surface
import pandas as pd
import h5py
import shutil
import glob
import io
import logging
import contextlib
import re
from sklearn.metrics import mean_absolute_error
from chipsff.calcs import setup_calculator
from chipsff.utils import (
    collect_data,
    log_job_info,
    save_dict_to_json,
    load_dict_from_json,
    get_vacancy_energy_entry,
    get_surface_energy_entry,
)

# dft_3d = data("dft_3d")
# vacancydb = data("vacancydb")
# surface_data = data("surfacedb")


class MaterialsAnalyzer:
    def __init__(
        self,
        jid=None,
        calculator_type=None,
        chemical_potentials_file=None,
        film_jid=None,
        substrate_jid=None,
        film_index=None,
        substrate_index=None,
        bulk_relaxation_settings=None,
        phonon_settings=None,
        properties_to_calculate=None,
        use_conventional_cell=False,
        surface_settings=None,
        defect_settings=None,
        phonon3_settings=None,
        md_settings=None,
        calculator_settings=None,  # New parameter for calculator-specific settings
        dataset=[],
        id_tag="jid",
    ):
        self.calculator_type = calculator_type
        self.use_conventional_cell = use_conventional_cell
        self.chemical_potentials_file = chemical_potentials_file
        self.bulk_relaxation_settings = bulk_relaxation_settings or {}
        self.dataset = dataset
        if not self.dataset:
            self.dataset = data("dft_3d")
        self.id_tag = id_tag
        self.phonon_settings = phonon_settings or {
            "dim": [2, 2, 2],
            "distance": 0.2,
        }
        self.properties_to_calculate = properties_to_calculate or []
        self.surface_settings = surface_settings or {}
        self.defect_settings = defect_settings or {}
        self.film_index = film_index or "1_1_0"
        self.substrate_index = substrate_index or "1_1_0"
        self.phonon3_settings = phonon3_settings or {
            "dim": [2, 2, 2],
            "distance": 0.2,
        }
        self.md_settings = md_settings or {
            "dt": 1,
            "temp0": 3500,
            "nsteps0": 1000,
            "temp1": 300,
            "nsteps1": 2000,
            "taut": 20,
            "min_size": 10.0,
        }
        self.calculator_settings = calculator_settings or {}
        if jid:
            self.jid = jid
            # Load atoms for the given JID
            self.atoms = self.get_atoms(jid)
            # Get reference data for the material
            self.reference_data = self.get_entry(jid)
            # Set up the output directory and log file
            self.output_dir = f"{jid}_{calculator_type}"
            os.makedirs(self.output_dir, exist_ok=True)
            self.log_file = os.path.join(self.output_dir, f"{jid}_job_log.txt")
            # Initialize job_info dictionary
            self.job_info = {
                "jid": jid,
                "calculator_type": calculator_type,
            }
            self.calculator = self.setup_calculator()
            self.chemical_potentials = self.load_chemical_potentials()
        elif film_jid and substrate_jid:
            # Ensure film_jid and substrate_jid are strings, not lists
            if isinstance(film_jid, list):
                film_jid = film_jid[0]
            if isinstance(substrate_jid, list):
                substrate_jid = substrate_jid[0]

            self.film_jid = film_jid
            self.substrate_jid = substrate_jid

            # Include Miller indices in directory and file names
            self.output_dir = f"Interface_{film_jid}_{self.film_index}_{substrate_jid}_{self.substrate_index}_{calculator_type}"
            os.makedirs(self.output_dir, exist_ok=True)
            self.log_file = os.path.join(
                self.output_dir,
                f"Interface_{film_jid}_{self.film_index}_{substrate_jid}_{self.substrate_index}_job_log.txt",
            )
            self.job_info = {
                "film_jid": film_jid,
                "substrate_jid": substrate_jid,
                "film_index": self.film_index,
                "substrate_index": self.substrate_index,
                "calculator_type": calculator_type,
            }
            self.calculator = self.setup_calculator()
            self.chemical_potentials = self.load_chemical_potentials()
        else:
            raise ValueError(
                "Either 'jid' or both 'film_jid' and 'substrate_jid' must be provided."
            )

        # Set up the logger
        self.setup_logger()

    def get_entry(self, jid=""):
        for entry in self.dataset:
            if entry[self.id_tag] == jid:
                return entry
        raise ValueError(f"JID {jid} not found in the database")

    def setup_logger(self):

        self.logger = logging.getLogger(
            self.jid or f"{self.film_jid}_{self.substrate_jid}"
        )
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler(self.log_file)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def setup_calculator(self):
        calc_settings = self.calculator_settings
        calc = setup_calculator(self.calculator_type, calc_settings)
        self.log(
            f"Using calculator: {self.calculator_type} with settings: {calc_settings}"
        )
        return calc

    def log(self, message):
        """Log information to the job log file."""
        log_job_info(message, self.log_file)

    def get_atoms(self, jid):
        dat = self.get_entry(jid=jid)
        # dat = get_jid_data(jid=jid, dataset="dft_3d")
        return Atoms.from_dict(dat["atoms"])

    def load_chemical_potentials(self):
        if os.path.exists(self.chemical_potentials_file):
            with open(self.chemical_potentials_file, "r") as f:
                return json.load(f)
        else:
            return {}

    def save_chemical_potentials(self):
        with open(self.chemical_potentials_file, "w") as f:
            json.dump(self.chemical_potentials, f, indent=4)

    def capture_fire_output(self, ase_atoms, fmax, steps, verbose=True):
        """Capture the output of the FIRE optimizer."""
        log_stream = io.StringIO()
        if verbose:
            dyn = FIRE(ase_atoms)
            dyn.run(fmax=fmax, steps=steps)
        else:
            with contextlib.redirect_stdout(log_stream):
                dyn = FIRE(ase_atoms)
                dyn.run(fmax=fmax, steps=steps)
        output = log_stream.getvalue().strip()

        final_energy = None
        if output:
            last_line = output.split("\n")[-1]
            match = re.search(
                r"FIRE:\s+\d+\s+\d+:\d+:\d+\s+(-?\d+\.\d+)", last_line
            )
            if match:
                final_energy = float(match.group(1))

        return final_energy, dyn.nsteps

    def relax_structure(self):
        """Perform structure relaxation and log the process."""
        self.log(f"Starting relaxation for {self.jid}")

        # Use conventional cell if specified

        if self.use_conventional_cell:
            self.log("Using conventional cell for relaxation.")
            self.atoms = (
                self.atoms.get_conventional_atoms
            )  # or appropriate method

        # Convert atoms to ASE format and assign the calculator
        filter_type = self.bulk_relaxation_settings.get(
            "filter_type", "ExpCellFilter"
        )
        relaxation_settings = self.bulk_relaxation_settings.get(
            "relaxation_settings", {}
        )
        constant_volume = relaxation_settings.get("constant_volume", False)
        ase_atoms = self.atoms.ase_converter()
        ase_atoms.calc = self.calculator

        if filter_type == "ExpCellFilter":
            ase_atoms = ExpCellFilter(
                ase_atoms, constant_volume=constant_volume
            )
        else:
            # Implement other filters if needed
            pass

        # Run FIRE optimizer and capture the output using relaxation settings
        fmax = relaxation_settings.get("fmax", 0.05)
        steps = relaxation_settings.get("steps", 200)
        final_energy, nsteps = self.capture_fire_output(
            ase_atoms, fmax=fmax, steps=steps
        )
        relaxed_atoms = ase_to_atoms(ase_atoms.atoms)
        converged = nsteps < steps

        # Log the final energy and relaxation status
        self.log(
            f"Final energy of FIRE optimization for structure: {final_energy}"
        )
        self.log(
            f"Relaxation {'converged' if converged else 'did not converge'} within {nsteps} steps."
        )

        # Update job info and save the relaxed structure
        self.job_info["relaxed_atoms"] = relaxed_atoms.to_dict()
        self.job_info["final_energy_structure"] = final_energy
        self.job_info["converged"] = converged
        self.log(f"Relaxed structure: {relaxed_atoms}")
        # self.log(f"Relaxed structure: {relaxed_atoms.to_dict()}")
        save_dict_to_json(self.job_info, self.get_job_info_filename())

        return relaxed_atoms if converged else None

    def calculate_formation_energy(self, relaxed_atoms):
        """
        Calculate the formation energy per atom using the equilibrium energy and chemical potentials.
        """
        e0 = self.job_info["equilibrium_energy"]
        composition = relaxed_atoms.composition.to_dict()
        total_energy = e0

        for element, amount in composition.items():
            chemical_potential = self.get_chemical_potential(element)
            if chemical_potential is None:
                self.log(
                    f"Skipping formation energy calculation due to missing chemical potential for {element}."
                )
                continue  # Or handle this appropriately
            total_energy -= chemical_potential * amount

        formation_energy_per_atom = total_energy / relaxed_atoms.num_atoms

        # Log and save the formation energy
        self.job_info["formation_energy_per_atom"] = formation_energy_per_atom
        self.log(f"Formation energy per atom: {formation_energy_per_atom}")
        save_dict_to_json(self.job_info, self.get_job_info_filename())

        return formation_energy_per_atom

    def calculate_element_chemical_potential(self, element, element_jid):
        """
        Calculate the chemical potential of a pure element using its standard structure.
        """
        self.log(
            f"Calculating chemical potential for element: {element} using JID: {element_jid}"
        )
        try:
            # Get standard structure for the element using the provided JID
            element_atoms = self.get_atoms(element_jid)
            ase_atoms = element_atoms.ase_converter()
            ase_atoms.calc = self.calculator

            # Perform energy calculation
            energy = ase_atoms.get_potential_energy() / len(ase_atoms)
            self.log(
                f"Calculated chemical potential for {element}: {energy} eV/atom"
            )
            return energy
        except Exception as e:
            self.log(
                f"Error calculating chemical potential for {element}: {e}"
            )
            return None

    def get_chemical_potential(self, element):
        """Fetch chemical potential from JSON based on the element and calculator."""
        element_data = self.chemical_potentials.get(element, {})
        chemical_potential = element_data.get(f"energy_{self.calculator_type}")

        if chemical_potential is None:
            self.log(
                f"No chemical potential found for {element} with calculator {self.calculator_type}, calculating it now..."
            )
            # Get standard JID for the element from chemical_potentials.json
            element_jid = element_data.get("jid")
            if element_jid is None:
                self.log(
                    f"No standard JID found for element {element} in chemical_potentials.json"
                )
                return None  # Skip this element

            # Calculate chemical potential
            chemical_potential = self.calculate_element_chemical_potential(
                element, element_jid
            )
            if chemical_potential is None:
                self.log(
                    f"Failed to calculate chemical potential for {element}"
                )
                return None
            # Add it to the chemical potentials dictionary
            if element not in self.chemical_potentials:
                self.chemical_potentials[element] = {}
            self.chemical_potentials[element][
                f"energy_{self.calculator_type}"
            ] = chemical_potential
            # Save the updated chemical potentials to file
            self.save_chemical_potentials()

        return chemical_potential

    def calculate_forces(self, atoms):
        """
        Calculate the forces on the given atoms without performing relaxation.
        """
        self.log(f"Calculating forces for {self.jid}")

        # Convert atoms to ASE format and assign the calculator
        ase_atoms = atoms.ase_converter()
        ase_atoms.calc = self.calculator

        # Calculate forces
        forces = ase_atoms.get_forces()  # This returns an array of forces

        # Log and save the forces
        self.job_info["forces"] = (
            forces.tolist()
        )  # Convert to list for JSON serialization
        self.log(f"Forces calculated: {forces}")

        # Save to job info JSON
        save_dict_to_json(self.job_info, self.get_job_info_filename())

        return forces

    def calculate_ev_curve(self, relaxed_atoms):
        """Calculate the energy-volume (E-V) curve and log results."""
        self.log(f"Calculating EV curve for {self.jid}")

        dx = np.arange(-0.06, 0.06, 0.01)  # Strain values
        y = []  # Energies
        vol = []  # Volumes
        strained_structures = []  # To store strained structures

        for i in dx:
            # Apply strain and calculate energy at each strain value
            strained_atoms = relaxed_atoms.strain_atoms(i)
            strained_structures.append(strained_atoms)
            ase_atoms = strained_atoms.ase_converter()
            ase_atoms.calc = self.calculator
            energy = ase_atoms.get_potential_energy()

            y.append(energy)
            vol.append(strained_atoms.volume)

        # Convert data to numpy arrays for processing
        y = np.array(y)
        vol = np.array(vol)

        # Fit the E-V curve using an equation of state (EOS)
        try:
            eos = EquationOfState(vol, y, eos="murnaghan")
            v0, e0, B = eos.fit()

            # Bulk modulus in GPa (conversion factor from ASE units)
            kv = B / kJ * 1.0e24  # Convert to GPa

            # Log important results
            self.log(f"Bulk modulus: {kv} GPa")
            self.log(f"Equilibrium energy: {e0} eV")
            self.log(f"Equilibrium volume: {v0} Å³")

            # Save E-V curve plot
            fig = plt.figure()
            eos.plot()
            ev_plot_filename = os.path.join(
                self.output_dir, "E_vs_V_curve.png"
            )
            fig.savefig(ev_plot_filename)
            plt.close(fig)
            self.log(f"E-V curve plot saved to {ev_plot_filename}")

            # Save E-V curve data to a text file
            ev_data_filename = os.path.join(self.output_dir, "E_vs_V_data.txt")
            with open(ev_data_filename, "w") as f:
                f.write("Volume (Å³)\tEnergy (eV)\n")
                for v, e in zip(vol, y):
                    f.write(f"{v}\t{e}\n")
            self.log(f"E-V curve data saved to {ev_data_filename}")

            # Update job info with the results
            self.job_info["bulk_modulus"] = kv
            self.job_info["equilibrium_energy"] = e0
            self.job_info["equilibrium_volume"] = v0
            save_dict_to_json(self.job_info, self.get_job_info_filename())

        except RuntimeError as e:
            self.log(f"Error fitting EOS for {self.jid}: {e}")
            self.log("Skipping bulk modulus calculation due to fitting error.")
            kv = None  # Set bulk modulus to None or handle this as you wish
            e0, v0 = None, None  # Set equilibrium energy and volume to None

        # Return additional values for thermal expansion analysis
        return vol, y, strained_structures, eos, kv, e0, v0

    def calculate_elastic_tensor(self, relaxed_atoms):
        import elastic
        from elastic import get_elementary_deformations, get_elastic_tensor

        """
        Calculate the elastic tensor for the relaxed structure using the provided calculator.
        """
        self.log(f"Starting elastic tensor calculation for {self.jid}")
        start_time = time.time()

        # Convert atoms to ASE format and assign the calculator
        ase_atoms = relaxed_atoms.ase_converter()
        ase_atoms.calc = self.calculator

        # Get elementary deformations for elastic tensor calculation
        systems = elastic.get_elementary_deformations(ase_atoms)

        # Calculate the elastic tensor and convert to GPa
        cij_order = elastic.elastic.get_cij_order(ase_atoms)
        Cij, Bij = elastic.get_elastic_tensor(ase_atoms, systems)
        elastic_tensor = {
            i: j / ase.units.GPa for i, j in zip(cij_order, Cij)
        }  # Convert to GPa

        # Save and log the results
        self.job_info["elastic_tensor"] = elastic_tensor
        self.log(
            f"Elastic tensor for {self.jid} with {self.calculator_type}: {elastic_tensor}"
        )

        # Timing the calculation
        end_time = time.time()
        self.log(f"Elastic Calculation time: {end_time - start_time} seconds")

        # Save to job info JSON
        save_dict_to_json(self.job_info, self.get_job_info_filename())

        return elastic_tensor

    def run_phonon_analysis(self, relaxed_atoms):
        from phonopy import Phonopy, PhonopyQHA
        from phonopy.file_IO import write_FORCE_CONSTANTS
        from phonopy.phonon.band_structure import BandStructure
        from phonopy.structure.atoms import Atoms as PhonopyAtoms

        """Perform Phonon calculation, generate force constants, and plot band structure & DOS."""
        self.log(f"Starting phonon analysis for {self.jid}")
        phonopy_bands_figname = f"ph_{self.jid}_{self.calculator_type}.png"

        # Phonon generation parameters
        dim = self.phonon_settings.get("dim", [2, 2, 2])
        # Define the conversion factor from THz to cm^-1
        THz_to_cm = 33.35641  # 1 THz = 33.35641 cm^-1

        force_constants_filename = "FORCE_CONSTANTS"
        eigenvalues_filename = "phonon_eigenvalues.txt"
        thermal_props_filename = "thermal_properties.txt"
        write_fc = True
        min_freq_tol_cm = -5.0  # in cm^-1
        distance = self.phonon_settings.get("distance", 0.2)

        # Generate k-point path
        kpoints = Kpoints().kpath(relaxed_atoms, line_density=5)

        # Convert atoms to Phonopy-compatible object
        self.log("Converting atoms to Phonopy-compatible format...")
        bulk = relaxed_atoms.phonopy_converter()
        phonon = Phonopy(
            bulk,
            [[dim[0], 0, 0], [0, dim[1], 0], [0, 0, dim[2]]],
            # Do not set factor here to keep frequencies in THz during calculations
        )

        # Generate displacements
        phonon.generate_displacements(distance=distance)
        supercells = phonon.supercells_with_displacements
        self.log(f"Generated {len(supercells)} supercells for displacements.")

        # Calculate forces for each supercell
        set_of_forces = []
        for idx, scell in enumerate(supercells):
            self.log(f"Calculating forces for supercell {idx+1}...")
            ase_atoms = AseAtoms(
                symbols=scell.symbols,
                positions=scell.positions,
                cell=scell.cell,
                pbc=True,
            )
            ase_atoms.calc = self.calculator
            forces = np.array(ase_atoms.get_forces())

            # Correct for drift force
            drift_force = forces.sum(axis=0)
            for force in forces:
                force -= drift_force / forces.shape[0]

            set_of_forces.append(forces)

        # Generate force constants
        self.log("Producing force constants...")
        phonon.produce_force_constants(forces=set_of_forces)

        # Write force constants to file if required
        if write_fc:
            force_constants_filepath = os.path.join(
                self.output_dir, force_constants_filename
            )
            self.log(
                f"Writing force constants to {force_constants_filepath}..."
            )
            write_FORCE_CONSTANTS(
                phonon.force_constants, filename=force_constants_filepath
            )
            self.log(f"Force constants saved to {force_constants_filepath}")

        # Prepare bands for band structure calculation
        bands = [kpoints.kpts]  # Assuming kpoints.kpts is a list of q-points

        # Prepare labels and path_connections
        labels = []
        path_connections = []
        for i, label in enumerate(kpoints.labels):
            if label:
                labels.append(label)
            else:
                labels.append("")  # Empty string for points without labels

        # Since we have a single path, set path_connections accordingly
        path_connections = [True] * (len(bands) - 1)
        path_connections.append(False)

        # Run band structure calculation with labels
        self.log("Running band structure calculation...")
        phonon.run_band_structure(
            bands,
            with_eigenvectors=False,
            labels=labels,
            path_connections=path_connections,
        )

        # Write band.yaml file (frequencies will be in THz)
        band_yaml_filepath = os.path.join(self.output_dir, "band.yaml")
        self.log(f"Writing band structure data to {band_yaml_filepath}...")
        phonon.band_structure.write_yaml(filename=band_yaml_filepath)
        self.log(f"band.yaml saved to {band_yaml_filepath}")

        # --- Begin post-processing to convert frequencies to cm^-1 while preserving formatting ---
        from ruamel.yaml import YAML

        self.log(
            f"Converting frequencies in {band_yaml_filepath} to cm^-1 while preserving formatting..."
        )
        yaml = YAML()
        yaml.preserve_quotes = True

        with open(band_yaml_filepath, "r") as f:
            band_data = yaml.load(f)

        for phonon_point in band_data["phonon"]:
            for band in phonon_point["band"]:
                freq = band["frequency"]
                if freq is not None:
                    band["frequency"] = freq * THz_to_cm

        with open(band_yaml_filepath, "w") as f:
            yaml.dump(band_data, f)

        self.log(
            f"Frequencies in {band_yaml_filepath} converted to cm^-1 with formatting preserved"
        )
        # --- End post-processing ---

        # Phonon band structure and eigenvalues
        lbls = kpoints.labels
        lbls_ticks = []
        freqs = []
        lbls_x = []
        count = 0
        eigenvalues = []

        for ii, k in enumerate(kpoints.kpts):
            k_str = ",".join(map(str, k))
            if ii == 0 or k_str != ",".join(map(str, kpoints.kpts[ii - 1])):
                freqs_at_k = phonon.get_frequencies(k)  # Frequencies in THz
                freqs_at_k_cm = freqs_at_k * THz_to_cm  # Convert to cm^-1
                freqs.append(freqs_at_k_cm)
                eigenvalues.append(
                    (k, freqs_at_k_cm)
                )  # Store frequencies in cm^-1
                lbl = "$" + str(lbls[ii]) + "$" if lbls[ii] else ""
                if lbl:
                    lbls_ticks.append(lbl)
                    lbls_x.append(count)
                count += 1

        # Write eigenvalues to file with frequencies in cm^-1
        eigenvalues_filepath = os.path.join(
            self.output_dir, eigenvalues_filename
        )
        self.log(f"Writing phonon eigenvalues to {eigenvalues_filepath}...")
        with open(eigenvalues_filepath, "w") as eig_file:
            eig_file.write("k-points\tFrequencies (cm^-1)\n")
            for k, freqs_at_k_cm in eigenvalues:
                k_str = ",".join(map(str, k))
                freqs_str = "\t".join(map(str, freqs_at_k_cm))
                eig_file.write(f"{k_str}\t{freqs_str}\n")
        self.log(f"Phonon eigenvalues saved to {eigenvalues_filepath}")

        # Convert frequencies to numpy array in cm^-1
        freqs = np.array(freqs)

        # Plot phonon band structure and DOS
        the_grid = plt.GridSpec(1, 2, width_ratios=[3, 1], wspace=0.0)
        plt.rcParams.update({"font.size": 18})
        plt.figure(figsize=(10, 5))

        # Plot phonon bands
        plt.subplot(the_grid[0])
        for i in range(freqs.shape[1]):
            plt.plot(freqs[:, i], lw=2, c="b")
        for i in lbls_x:
            plt.axvline(x=i, c="black")
        plt.xticks(lbls_x, lbls_ticks)
        plt.ylabel("Frequency (cm$^{-1}$)")
        plt.xlim([0, max(lbls_x)])

        # Run mesh and DOS calculations
        phonon.run_mesh(
            [40, 40, 40], is_gamma_center=True, is_mesh_symmetry=False
        )
        phonon.run_total_dos()
        tdos = phonon.total_dos
        freqs_dos = (
            np.array(tdos.frequency_points) * THz_to_cm
        )  # Convert to cm^-1
        dos_values = tdos.dos
        min_freq = min_freq_tol_cm  # in cm^-1
        max_freq = max(freqs_dos)

        plt.ylim([min_freq, max_freq])

        # Plot DOS
        plt.subplot(the_grid[1])
        plt.fill_between(
            dos_values,
            freqs_dos,
            color=(0.2, 0.4, 0.6, 0.6),
            edgecolor="k",
            lw=1,
            y2=0,
        )
        plt.xlabel("DOS")
        plt.yticks([])
        plt.xticks([])
        plt.ylim([min_freq, max_freq])
        plt.xlim([0, max(dos_values)])

        # Save the plot
        os.makedirs(self.output_dir, exist_ok=True)
        plot_filepath = os.path.join(self.output_dir, phonopy_bands_figname)
        plt.tight_layout()
        plt.savefig(plot_filepath)
        self.log(
            f"Phonon band structure and DOS combined plot saved to {plot_filepath}"
        )
        plt.close()

        self.log("Calculating thermal properties...")
        phonon.run_mesh(mesh=[20, 20, 20])
        phonon.run_thermal_properties(t_step=10, t_max=1000, t_min=0)
        tprop_dict = phonon.get_thermal_properties_dict()

        # Plot thermal properties
        plt.figure()
        plt.plot(
            tprop_dict["temperatures"],
            tprop_dict["free_energy"],
            label="Free energy (kJ/mol)",
            color="red",
        )
        plt.plot(
            tprop_dict["temperatures"],
            tprop_dict["entropy"],
            label="Entropy (J/K*mol)",
            color="blue",
        )
        plt.plot(
            tprop_dict["temperatures"],
            tprop_dict["heat_capacity"],
            label="Heat capacity (J/K*mol)",
            color="green",
        )
        plt.legend()
        plt.xlabel("Temperature (K)")
        plt.ylabel("Thermal Properties")
        plt.title("Thermal Properties")

        thermal_props_plot_filepath = os.path.join(
            self.output_dir, f"Thermal_Properties_{self.jid}.png"
        )
        plt.savefig(thermal_props_plot_filepath)
        self.log(
            f"Thermal properties plot saved to {thermal_props_plot_filepath}"
        )
        plt.close()

        # Save thermal properties to file
        thermal_props_filepath = os.path.join(
            self.output_dir, thermal_props_filename
        )
        with open(thermal_props_filepath, "w") as f:
            f.write(
                "Temperature (K)\tFree Energy (kJ/mol)\tEntropy (J/K*mol)\tHeat Capacity (J/K*mol)\n"
            )
            for i in range(len(tprop_dict["temperatures"])):
                f.write(
                    f"{tprop_dict['temperatures'][i]}\t{tprop_dict['free_energy'][i]}\t"
                    f"{tprop_dict['entropy'][i]}\t{tprop_dict['heat_capacity'][i]}\n"
                )
        self.log(f"Thermal properties written to {thermal_props_filepath}")

        # Calculate zero-point energy (ZPE)
        zpe = (
            tprop_dict["free_energy"][0] * 0.0103643
        )  # Converting from kJ/mol to eV
        self.log(f"Zero-point energy: {zpe} eV")

        # Save to job info
        self.job_info["phonopy_bands"] = phonopy_bands_figname
        save_dict_to_json(self.job_info, self.get_job_info_filename())

        return phonon, zpe

    def analyze_defects(self):
        """Analyze defects by generating, relaxing, and calculating vacancy formation energy."""
        self.log("Starting defect analysis...")
        generate_settings = self.defect_settings.get("generate_settings", {})
        on_conventional_cell = generate_settings.get(
            "on_conventional_cell", True
        )
        enforce_c_size = generate_settings.get("enforce_c_size", 8)
        extend = generate_settings.get("extend", 1)
        # Generate defect structures from the original atoms
        defect_structures = Vacancy(self.atoms).generate_defects(
            on_conventional_cell=on_conventional_cell,
            enforce_c_size=enforce_c_size,
            extend=extend,
        )

        for defect in defect_structures:
            # Extract the defect structure and related metadata
            defect_structure = Atoms.from_dict(
                defect.to_dict()["defect_structure"]
            )

            # Construct a consistent defect name without Wyckoff notation
            element = defect.to_dict()["symbol"]
            defect_name = f"{self.jid}_{element}"  # Consistent format
            self.log(f"Analyzing defect: {defect_name}")

            # Relax the defect structure
            relaxed_defect_atoms = self.relax_defect_structure(
                defect_structure, name=defect_name
            )

            if relaxed_defect_atoms is None:
                self.log(f"Skipping {defect_name} due to failed relaxation.")
                continue

            # Retrieve energies for calculating the vacancy formation energy
            vacancy_energy = self.job_info.get(
                f"final_energy_defect for {defect_name}"
            )
            bulk_energy = (
                self.job_info.get("equilibrium_energy")
                / self.atoms.num_atoms
                * (defect_structure.num_atoms + 1)
            )

            if vacancy_energy is None or bulk_energy is None:
                self.log(
                    f"Skipping {defect_name} due to missing energy values."
                )
                continue

            # Get chemical potential and calculate vacancy formation energy
            chemical_potential = self.get_chemical_potential(element)

            if chemical_potential is None:
                self.log(
                    f"Skipping {defect_name} due to missing chemical potential for {element}."
                )
                continue

            vacancy_formation_energy = (
                vacancy_energy - bulk_energy + chemical_potential
            )

            # Log and store the vacancy formation energy consistently
            self.job_info[f"vacancy_formation_energy for {defect_name}"] = (
                vacancy_formation_energy
            )
            self.log(
                f"Vacancy formation energy for {defect_name}: {vacancy_formation_energy} eV"
            )

        # Save the job info to a JSON file
        save_dict_to_json(self.job_info, self.get_job_info_filename())
        self.log("Defect analysis completed.")

    def relax_defect_structure(self, atoms, name):
        """Relax the defect structure and log the process."""
        # Convert atoms to ASE format and assign the calculator
        filter_type = self.defect_settings.get("filter_type", "ExpCellFilter")
        relaxation_settings = self.defect_settings.get(
            "relaxation_settings", {}
        )
        constant_volume = relaxation_settings.get("constant_volume", True)
        ase_atoms = atoms.ase_converter()
        ase_atoms.calc = self.calculator

        if filter_type == "ExpCellFilter":
            ase_atoms = ExpCellFilter(
                ase_atoms, constant_volume=constant_volume
            )
        else:
            # Implement other filters if needed
            pass
        fmax = relaxation_settings.get("fmax", 0.05)
        steps = relaxation_settings.get("steps", 200)
        # Run FIRE optimizer and capture the output
        final_energy, nsteps = self.capture_fire_output(
            ase_atoms, fmax=fmax, steps=steps
        )
        relaxed_atoms = ase_to_atoms(ase_atoms.atoms)
        converged = nsteps < 200

        # Log the final energy and relaxation status
        self.log(
            f"Final energy of FIRE optimization for defect structure: {final_energy}"
        )
        self.log(
            f"Defect relaxation {'converged' if converged else 'did not converge'} within 200 steps."
        )

        # Update job info with the final energy and convergence status
        self.job_info[f"final_energy_defect for {name}"] = final_energy
        self.job_info[f"converged for {name}"] = converged

        if converged:
            poscar_filename = os.path.join(
                self.output_dir, f"POSCAR_{name}_relaxed.vasp"
            )
            poscar_defect = Poscar(relaxed_atoms)
            poscar_defect.write_file(poscar_filename)
            self.log(f"Relaxed defect structure saved to {poscar_filename}")

        return relaxed_atoms if converged else None

    def analyze_surfaces(self):
        """
        Perform surface analysis by generating surface structures, relaxing them, and calculating surface energies.
        """
        self.log(f"Analyzing surfaces for {self.jid}")

        indices_list = self.surface_settings.get(
            "indices_list",
            [
                [1, 0, 0],
                [1, 1, 1],
                [1, 1, 0],
                [0, 1, 1],
                [0, 0, 1],
                [0, 1, 0],
            ],
        )
        layers = self.surface_settings.get("layers", 4)
        vacuum = self.surface_settings.get("vacuum", 18)

        for indices in indices_list:
            # Generate surface and check for polarity
            surface = (
                Surface(
                    atoms=self.atoms,
                    indices=indices,
                    layers=layers,
                    vacuum=vacuum,
                )
                .make_surface()
                .center_around_origin()
            )
            if surface.check_polar:
                self.log(
                    f"Skipping polar surface for {self.jid} with indices {indices}"
                )
                continue

            # Write initial POSCAR for surface
            poscar_surface = Poscar(atoms=surface)
            poscar_surface.write_file(
                os.path.join(
                    self.output_dir,
                    f"POSCAR_{self.jid}_surface_{indices}_{self.calculator_type}.vasp",
                )
            )

            # Relax the surface structure
            relaxed_surface_atoms, final_energy = self.relax_surface_structure(
                surface, indices
            )

            # If relaxation failed, skip further calculations
            if relaxed_surface_atoms is None:
                self.log(
                    f"Skipping surface {indices} due to failed relaxation."
                )
                continue

            # Write relaxed POSCAR for surface
            pos_relaxed_surface = Poscar(relaxed_surface_atoms)
            pos_relaxed_surface.write_file(
                os.path.join(
                    self.output_dir,
                    f"POSCAR_{self.jid}_surface_{indices}_{self.calculator_type}_relaxed.vasp",
                )
            )

            # Calculate and log surface energy
            bulk_energy = self.job_info.get("equilibrium_energy")
            if final_energy is None or bulk_energy is None:
                self.log(
                    f"Skipping surface energy calculation for {self.jid} with indices {indices} due to missing energy values."
                )
                continue

            surface_energy = self.calculate_surface_energy(
                final_energy, bulk_energy, relaxed_surface_atoms, surface
            )

            # Store the surface energy with the new naming convention
            surface_name = (
                f"Surface-{self.jid}_miller_{'_'.join(map(str, indices))}"
            )
            self.job_info[surface_name] = surface_energy
            self.log(
                f"Surface energy for {self.jid} with indices {indices}: {surface_energy} J/m^2"
            )

        # Save updated job info
        save_dict_to_json(
            self.job_info,
            os.path.join(
                self.output_dir,
                f"{self.jid}_{self.calculator_type}_job_info.json",
            ),
        )
        self.log("Surface analysis completed.")

    def relax_surface_structure(self, atoms, indices):
        """
        Relax the surface structure and log the process.
        """
        filter_type = self.surface_settings.get("filter_type", "ExpCellFilter")
        relaxation_settings = self.surface_settings.get(
            "relaxation_settings", {}
        )
        constant_volume = relaxation_settings.get("constant_volume", True)
        self.log(
            f"Starting surface relaxation for {self.jid} with indices {indices}"
        )
        start_time = time.time()
        fmax = relaxation_settings.get("fmax", 0.05)
        steps = relaxation_settings.get("steps", 200)
        # Convert atoms to ASE format and assign the calculator
        ase_atoms = atoms.ase_converter()
        ase_atoms.calc = self.calculator
        if filter_type == "ExpCellFilter":
            ase_atoms = ExpCellFilter(
                ase_atoms, constant_volume=constant_volume
            )
        else:
            # Implement other filters if needed
            pass
        # Run FIRE optimizer and capture the output
        final_energy, nsteps = self.capture_fire_output(
            ase_atoms, fmax=fmax, steps=steps
        )
        relaxed_atoms = ase_to_atoms(ase_atoms.atoms)
        converged = nsteps < 200

        # Log relaxation results
        self.log(
            f"Final energy of FIRE optimization for surface structure: {final_energy}"
        )
        self.log(
            f"Surface relaxation {'converged' if converged else 'did not converge'} within {nsteps} steps."
        )

        end_time = time.time()
        self.log(
            f"Surface Relaxation Calculation time: {end_time - start_time} seconds"
        )

        # Update job info and return relaxed atoms if converged, otherwise return None
        self.job_info[f"final_energy_surface_{indices}"] = final_energy
        self.job_info[f"converged_surface_{indices}"] = converged

        # Return both relaxed atoms and the final energy as a tuple
        return (relaxed_atoms if converged else None), final_energy

    def calculate_surface_energy(
        self, final_energy, bulk_energy, relaxed_atoms, surface
    ):
        """
        Calculate the surface energy based on the final energy of the relaxed surface and bulk energy.
        """
        # Calculate the number of bulk units in the surface supercell
        num_units = surface.num_atoms / self.atoms.num_atoms

        # Calculate the surface area using the lattice vectors
        m = relaxed_atoms.lattice.matrix
        surface_area = np.linalg.norm(np.cross(m[0], m[1]))

        # Calculate surface energy in J/m^2
        surface_energy = (
            (final_energy - bulk_energy * num_units)
            * 16.02176565
            / (2 * surface_area)
        )

        return surface_energy

    def run_phonon3_analysis(self, relaxed_atoms):
        from phono3py import Phono3py

        """Run Phono3py analysis, process results, and generate thermal conductivity data."""
        self.log(f"Starting Phono3py analysis for {self.jid}")

        # Set parameters for the Phono3py calculation
        dim = self.phonon3_settings.get("dim", [2, 2, 2])
        distance = self.phonon3_settings.get("distance", 0.2)

        # force_multiplier = 16

        # Convert atoms to Phonopy-compatible object and set up Phono3py
        ase_atoms = relaxed_atoms.ase_converter()
        ase_atoms.calc = self.calculator
        bulk = relaxed_atoms.phonopy_converter()

        phonon = Phono3py(
            bulk, [[dim[0], 0, 0], [0, dim[1], 0], [0, 0, dim[2]]]
        )
        phonon.generate_displacements(distance=distance)
        supercells = phonon.supercells_with_displacements

        # Calculate forces for each supercell
        set_of_forces = []
        for scell in supercells:
            ase_atoms = AseAtoms(
                symbols=scell.get_chemical_symbols(),
                scaled_positions=scell.get_scaled_positions(),
                cell=scell.get_cell(),
                pbc=True,
            )
            ase_atoms.calc = self.calculator
            forces = np.array(ase_atoms.get_forces())
            drift_force = forces.sum(axis=0)
            for force in forces:
                force -= drift_force / forces.shape[0]
            set_of_forces.append(forces)

        # Set the forces and produce third-order force constants
        forces = np.array(set_of_forces).reshape(-1, len(phonon.supercell), 3)
        phonon.forces = forces
        phonon.produce_fc3()

        # Run thermal conductivity calculation
        phonon.mesh_numbers = 30
        phonon.init_phph_interaction()
        phonon.run_thermal_conductivity(
            temperatures=range(0, 1001, 10), write_kappa=True
        )

        # Collect thermal conductivity data
        kappa = phonon.thermal_conductivity.kappa
        self.log(f"Thermal conductivity: {kappa}")

        # Move generated HDF5 files to the output directory
        hdf5_file_pattern = "kappa-*.hdf5"
        for hdf5_file in glob.glob(hdf5_file_pattern):
            shutil.move(hdf5_file, os.path.join(self.output_dir, hdf5_file))

        # Process Phono3py results and save plots
        self.process_phonon3_results()

        # Save updated job info to JSON
        save_dict_to_json(
            self.job_info,
            os.path.join(
                self.output_dir,
                f"{self.jid}_{self.calculator_type}_job_info.json",
            ),
        )
        self.log(f"Phono3py analysis completed for {self.jid}")

    def process_phonon3_results(self):
        """Process Phono3py results and generate plots of thermal conductivity."""
        file_pattern = os.path.join(self.output_dir, "kappa-*.hdf5")
        file_list = glob.glob(file_pattern)

        temperatures = np.arange(10, 101, 10)
        kappa_xx_values = []

        if file_list:
            hdf5_filename = file_list[0]
            self.log(f"Processing file: {hdf5_filename}")

            for temperature_index in temperatures:
                converted_kappa = self.convert_kappa_units(
                    hdf5_filename, temperature_index
                )
                kappa_xx = converted_kappa[0]
                kappa_xx_values.append(kappa_xx)
                self.log(
                    f"Temperature index {temperature_index}, converted kappa: {kappa_xx}"
                )

            # Save results to job_info
            self.job_info["temperatures"] = temperatures.tolist()
            self.job_info["kappa_xx_values"] = kappa_xx_values

            # Plot temperature vs. converted kappa (xx element)
            plt.figure(figsize=(8, 6))
            plt.plot(
                temperatures * 10,
                kappa_xx_values,
                marker="o",
                linestyle="-",
                color="b",
            )
            plt.xlabel("Temperature (K)")
            plt.ylabel("Converted Kappa (xx element)")
            plt.title("Temperature vs. Converted Kappa (xx element)")
            plt.grid(True)
            plt.savefig(
                os.path.join(
                    self.output_dir, "Temperature_vs_Converted_Kappa.png"
                )
            )
            plt.close()
        else:
            self.log("No files matching the pattern were found.")

    def convert_kappa_units(self, hdf5_filename, temperature_index):
        """Convert thermal conductivity kappa from HDF5 file units."""
        with h5py.File(hdf5_filename, "r") as f:
            kappa_unit_conversion = f["kappa_unit_conversion"][()]
            heat_capacity = f["heat_capacity"][:]
            gv_by_gv = f["gv_by_gv"][:]
            gamma = f["gamma"][:]

            converted_kappa = (
                kappa_unit_conversion
                * heat_capacity[temperature_index, 2, 0]
                * gv_by_gv[2, 0]
                / (2 * gamma[temperature_index, 2, 0])
            )

            return converted_kappa

    def calculate_thermal_expansion(self, relaxed_atoms):
        from phonopy import Phonopy, PhonopyQHA
        from phonopy.file_IO import write_FORCE_CONSTANTS
        from phonopy.phonon.band_structure import BandStructure
        from phonopy.structure.atoms import Atoms as PhonopyAtoms

        """Calculate the thermal expansion coefficient using QHA."""

        def log(message):
            with open(self.log_file, "a") as f:
                f.write(message + "\n")
            print(message)

        log("Starting thermal expansion analysis...")

        # Step 1: Calculate finer E-V curve
        vol, y, strained_structures, eos, kv, e0, v0 = self.fine_ev_curve(
            atoms=relaxed_atoms, dx=np.linspace(-0.05, 0.05, 50)  # Denser grid
        )

        # Log Bulk modulus, equilibrium energy, and volume
        log(
            f"Bulk modulus: {kv} GPa, Equilibrium energy: {y[0]} eV, Volume: {vol[0]} Å³"
        )
        self.job_info["bulk_modulus"] = kv
        self.job_info["equilibrium_energy"] = y[0]
        self.job_info["equilibrium_volume"] = vol[0]

        # Step 2: Generate phonons for strained structures
        free_energies, heat_capacities, entropies, temperatures = (
            self.generate_phonons_for_volumes(
                strained_structures,
                calculator=self.calculator,
                dim=[2, 2, 2],
                distance=0.2,
                mesh=[20, 20, 20],
            )
        )

        # Step 3: Perform QHA-based thermal expansion analysis
        alpha = self.perform_qha(
            volumes=vol,
            energies=y,
            free_energies=free_energies,
            heat_capacities=heat_capacities,
            entropies=entropies,
            temperatures=temperatures,
            output_dir=self.output_dir,
        )

        self.log(f"Thermal expansion coefficient calculated: {alpha}")
        save_dict_to_json(
            self.job_info,
            os.path.join(
                self.output_dir,
                f"{self.jid}_{self.calculator_type}_job_info.json",
            ),
        )
        self.log(
            f"Thermal expansion analysis information saved to file: {self.jid}_{self.calculator_type}_job_info.json"
        )

    # Helper Functions Inside the Class
    def fine_ev_curve(self, atoms, dx=np.linspace(-0.05, 0.05, 50)):
        """
        Generate a finer energy-volume curve for strained structures.
        """
        y = []
        vol = []
        strained_structures = []

        for i in dx:
            # Apply strain and get strained atoms
            strained_atoms = atoms.strain_atoms(i)
            ase_atoms = strained_atoms.ase_converter()  # Convert to ASE Atoms
            ase_atoms.calc = self.calculator  # Assign the calculator

            # Get potential energy and volume
            energy = ase_atoms.get_potential_energy()
            y.append(energy)
            vol.append(strained_atoms.volume)

            strained_structures.append(
                strained_atoms
            )  # Save the strained structure

        vol = np.array(vol)
        y = np.array(y)

        # Fit the E-V curve using an equation of state (EOS)
        eos = EquationOfState(vol, y, eos="murnaghan")
        v0, e0, B = eos.fit()
        kv = B / kJ * 1.0e24  # Convert to GPa

        # Log important results
        self.log(f"Bulk modulus: {kv} GPa")
        self.log(f"Equilibrium energy: {e0} eV")
        self.log(f"Equilibrium volume: {v0} Å³")

        # Save E-V curve plot
        fig = plt.figure()
        eos.plot()
        ev_plot_filename = os.path.join(self.output_dir, "E_vs_V_curve.png")
        fig.savefig(ev_plot_filename)
        plt.close(fig)
        self.log(f"E-V curve plot saved to {ev_plot_filename}")

        # Save E-V curve data to a text file
        ev_data_filename = os.path.join(self.output_dir, "E_vs_V_data.txt")
        with open(ev_data_filename, "w") as f:
            f.write("Volume (Å³)\tEnergy (eV)\n")
            for v, e in zip(vol, y):
                f.write(f"{v}\t{e}\n")
        self.log(f"E-V curve data saved to {ev_data_filename}")

        # Update job info with the results
        self.job_info["bulk_modulus"] = kv
        self.job_info["equilibrium_energy"] = e0
        self.job_info["equilibrium_volume"] = v0
        save_dict_to_json(self.job_info, self.get_job_info_filename())

        return vol, y, strained_structures, eos, kv, e0, v0

    def generate_phonons_for_volumes(
        self,
        structures,
        calculator,
        dim=[2, 2, 2],
        distance=0.2,
        mesh=[20, 20, 20],
    ):
        from phonopy import Phonopy, PhonopyQHA
        from phonopy.file_IO import write_FORCE_CONSTANTS
        from phonopy.phonon.band_structure import BandStructure
        from phonopy.structure.atoms import Atoms as PhonopyAtoms

        all_free_energies = []
        all_heat_capacities = []
        all_entropies = []
        temperatures = np.arange(0, 300, 6)  # Define temperature range

        for structure in structures:
            # Convert structure to PhonopyAtoms
            phonopy_atoms = PhonopyAtoms(
                symbols=[str(e) for e in structure.elements],
                positions=structure.cart_coords,
                cell=structure.lattice.matrix,
            )

            # Initialize Phonopy object
            phonon = Phonopy(
                phonopy_atoms, [[dim[0], 0, 0], [0, dim[1], 0], [0, 0, dim[2]]]
            )
            phonon.generate_displacements(distance=distance)

            # Calculate forces for displaced structures
            supercells = phonon.get_supercells_with_displacements()
            forces = []
            for scell in supercells:
                ase_atoms = AseAtoms(
                    symbols=scell.symbols,
                    positions=scell.positions,
                    cell=scell.cell,
                    pbc=True,
                )
                ase_atoms.calc = calculator
                forces.append(ase_atoms.get_forces())

            phonon.produce_force_constants(forces=forces)

            # Post-processing to get thermal properties
            phonon.run_mesh(mesh=mesh)
            phonon.run_thermal_properties(t_min=0, t_step=6, t_max=294)
            tprop_dict = phonon.get_thermal_properties_dict()

            free_energies = tprop_dict["free_energy"]
            heat_capacities = tprop_dict["heat_capacity"]
            entropies = tprop_dict["entropy"]

            all_entropies.append(entropies)
            all_free_energies.append(free_energies)
            all_heat_capacities.append(heat_capacities)

        return (
            np.array(all_free_energies),
            np.array(all_heat_capacities),
            np.array(all_entropies),
            temperatures,
        )

    def perform_qha(
        self,
        volumes,
        energies,
        free_energies,
        heat_capacities,
        entropies,
        temperatures,
        output_dir,
    ):
        from phonopy import Phonopy, PhonopyQHA
        from phonopy.file_IO import write_FORCE_CONSTANTS
        from phonopy.phonon.band_structure import BandStructure
        from phonopy.structure.atoms import Atoms as PhonopyAtoms

        # Debugging: print array sizes
        print(f"Number of temperatures: {len(temperatures)}")
        print(f"Number of free energy data points: {free_energies.shape}")
        print(f"Number of volume data points: {len(volumes)}")

        # Ensure that volumes, free_energies, and temperatures are consistent
        if len(volumes) != len(temperatures):
            raise ValueError(
                "The number of volumes must match the number of temperatures"
            )

        # Initialize the QHA object
        try:
            qha = PhonopyQHA(
                volumes=volumes,
                electronic_energies=energies,
                free_energy=free_energies,
                cv=heat_capacities,
                entropy=entropies,
                temperatures=temperatures,
                eos="murnaghan",  # or another EOS if needed
                verbose=True,
            )
        except IndexError as e:
            print(f"Error in QHA initialization: {e}")
            raise

        # Calculate thermal expansion and save plots
        thermal_expansion_plot = os.path.join(
            output_dir, "thermal_expansion.png"
        )
        volume_temperature_plot = os.path.join(
            output_dir, "volume_temperature.png"
        )
        helmholtz_volume_plot = os.path.join(
            output_dir, "helmholtz_volume.png"
        )

        qha.get_thermal_expansion()

        # Save thermal expansion plot
        qha.plot_thermal_expansion()
        plt.savefig(thermal_expansion_plot)

        # Save volume-temperature plot
        qha.plot_volume_temperature()
        plt.savefig(volume_temperature_plot)

        # Save Helmholtz free energy vs. volume plot
        qha.plot_helmholtz_volume()
        plt.savefig(helmholtz_volume_plot)

        # Optionally save thermal expansion coefficient to a file
        thermal_expansion_file = os.path.join(
            output_dir, "thermal_expansion.txt"
        )
        alpha = qha.write_thermal_expansion(filename=thermal_expansion_file)

        return alpha

    def general_melter(self, relaxed_atoms):
        """Perform MD simulation to melt the structure, then quench it back to room temperature."""
        self.log(
            f"Starting MD melting and quenching simulation for {self.jid}"
        )

        calculator = self.setup_calculator()
        ase_atoms = relaxed_atoms.ase_converter()
        dim = self.ensure_cell_size(
            ase_atoms, min_size=self.md_settings.get("min_size", 10.0)
        )
        supercell = relaxed_atoms.make_supercell_matrix(dim)
        ase_atoms = supercell.ase_converter()
        ase_atoms.calc = calculator

        dt = self.md_settings.get("dt", 1) * ase.units.fs
        temp0 = self.md_settings.get("temp0", 3500)
        nsteps0 = self.md_settings.get("nsteps0", 1000)
        temp1 = self.md_settings.get("temp1", 300)
        nsteps1 = self.md_settings.get("nsteps1", 2000)
        taut = self.md_settings.get("taut", 20) * ase.units.fs
        trj = os.path.join(self.output_dir, f"{self.jid}_melt.traj")

        # Initialize velocities and run the first part of the MD simulation
        from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
        from ase.md.nvtberendsen import NVTBerendsen

        MaxwellBoltzmannDistribution(ase_atoms, temp0 * ase.units.kB)
        dyn = NVTBerendsen(ase_atoms, dt, temp0, taut=taut, trajectory=trj)

        def myprint():
            message = f"time={dyn.get_time() / ase.units.fs: 5.0f} fs T={ase_atoms.get_temperature(): 3.0f} K"
            self.log(message)

        dyn.attach(myprint, interval=20)
        dyn.run(nsteps0)

        # Cool down to room temperature
        dyn.set_temperature(temp1)
        dyn.run(nsteps1)

        # Convert back to JARVIS atoms and save the final structure
        final_atoms = ase_to_atoms(ase_atoms)
        poscar_filename = os.path.join(
            self.output_dir,
            f"POSCAR_{self.jid}_quenched_{self.calculator_type}.vasp",
        )
        from ase.io import write

        write(poscar_filename, final_atoms.ase_converter(), format="vasp")
        self.log(
            f"MD simulation completed. Final structure saved to {poscar_filename}"
        )
        self.job_info["quenched_atoms"] = final_atoms.to_dict()

        return final_atoms

    def calculate_rdf(self, quenched_atoms):
        """Calculate Radial Distribution Function (RDF) for quenched structure and save plot."""
        self.log(f"Starting RDF calculation for {self.jid}")
        ase_atoms = quenched_atoms.ase_converter()
        rmax = 3.5
        nbins = 200

        def perform_rdf_calculation(rmax):
            from ase.ga.utilities import get_rdf

            rdfs, distances = get_rdf(ase_atoms, rmax, nbins)
            plt.figure()
            plt.plot(distances, rdfs)
            plt.xlabel("Distance (Å)")
            plt.ylabel("RDF")
            plt.title(
                f"Radial Distribution Function for {self.jid} ({self.calculator_type})"
            )
            rdf_plot_filename = os.path.join(
                self.output_dir, f"RDF_{self.jid}_{self.calculator_type}.png"
            )
            plt.savefig(rdf_plot_filename)
            plt.close()
            self.job_info["rdf_plot"] = rdf_plot_filename
            self.log(f"RDF plot saved to {rdf_plot_filename}")
            return rdf_plot_filename

        try:
            perform_rdf_calculation(rmax)
        except ValueError as e:
            if "The cell is not large enough" in str(e):
                recommended_rmax = float(str(e).split("<")[1].split("=")[1])
                self.log(f"Error: {e}. Adjusting rmax to {recommended_rmax}.")
                perform_rdf_calculation(recommended_rmax)
            else:
                self.log(f"Error: {e}")
                raise

    def ensure_cell_size(self, ase_atoms, min_size):
        """Ensure that all cell dimensions are at least min_size."""
        cell_lengths = ase_atoms.get_cell().lengths()
        scale_factors = np.ceil(min_size / cell_lengths).astype(int)
        supercell_dims = [max(1, scale) for scale in scale_factors]
        return supercell_dims

    def analyze_interfaces(self):
        """Perform interface analysis using intermat package."""
        if not self.film_jid or not self.substrate_jid:
            self.log(
                "Film JID or substrate JID not provided, skipping interface analysis."
            )
            return

        self.log(
            f"Starting interface analysis between {self.film_jid} and {self.substrate_jid}"
        )

        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # Prepare config
        config = {
            "film_jid": self.film_jid,
            "substrate_jid": self.substrate_jid,
            "film_index": self.film_index,
            "substrate_index": self.substrate_index,
            "disp_intvl": 0.05,
            "calculator_method": self.calculator_type.lower(),
        }

        config_filename = os.path.join(
            self.output_dir,
            f"config_{self.film_jid}_{self.film_index}_{self.substrate_jid}_{self.substrate_index}_{self.calculator_type}.json",
        )

        # Save config file
        save_dict_to_json(config, config_filename)
        self.log(f"Config file created: {config_filename}")

        # Run intermat script using subprocess in self.output_dir
        command = f"run_intermat.py --config_file {os.path.basename(config_filename)}"
        self.log(f"Running command: {command}")

        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                cwd=self.output_dir,  # Set the working directory for the subprocess
            )
            self.log(f"Command output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            self.log(f"Command failed with error: {e.stderr}")
            return

        # After execution, check for outputs in self.output_dir
        main_results_filename = os.path.join(
            self.output_dir, "intermat_results.json"
        )
        if not os.path.exists(main_results_filename):
            self.log(f"Results file not found: {main_results_filename}")
            return

        res = load_dict_from_json(main_results_filename)
        w_adhesion = res.get("wads", [])
        systems_info = res.get("systems", {})

        # Handle intmat.png
        intmat_filename = os.path.join(self.output_dir, "intmat.png")
        if os.path.exists(intmat_filename):
            new_intmat_filename = os.path.join(
                self.output_dir,
                f"intmat_{self.film_jid}_{self.film_index}_{self.substrate_jid}_{self.substrate_index}_{self.calculator_type}.png",
            )
            os.rename(intmat_filename, new_intmat_filename)
            self.job_info["intmat_plot"] = new_intmat_filename
            self.log(f"intmat.png saved as {new_intmat_filename}")
        else:
            self.log("intmat.png not found.")

        if "wads" in res:
            # Save additional plots or data as needed
            self.job_info["interface_scan_results"] = main_results_filename
            self.job_info["w_adhesion"] = w_adhesion
            self.job_info["systems_info"] = systems_info
            self.log(
                f"Interface scan results saved to {main_results_filename}"
            )
            self.log(f"w_adhesion: {w_adhesion}")
            self.log(f"systems_info: {systems_info}")
            save_dict_to_json(self.job_info, self.get_job_info_filename())
        else:
            self.log(f"No 'wads' key in results file: {main_results_filename}")

    def get_job_info_filename(self):
        if hasattr(self, "jid") and self.jid:
            return os.path.join(
                self.output_dir,
                f"{self.jid}_{self.calculator_type}_job_info.json",
            )
        else:
            return os.path.join(
                self.output_dir,
                f"Interface_{self.film_jid}_{self.film_index}_{self.substrate_jid}_{self.substrate_index}_{self.calculator_type}_job_info.json",
            )

    def run_all(self):
        """Run selected analyses based on configuration."""
        # Start timing the entire run
        start_time = time.time()
        if self.use_conventional_cell:
            self.log("Using conventional cell for analysis.")
            self.atoms = self.atoms.get_conventional_atoms
        else:
            self.atoms = self.atoms
        # Relax the structure if specified
        if "relax_structure" in self.properties_to_calculate:
            relaxed_atoms = self.relax_structure()
        else:
            relaxed_atoms = self.atoms

        # Proceed only if the structure is relaxed or original atoms are used
        if relaxed_atoms is None:
            self.log("Relaxation did not converge. Exiting.")
            return

        # Lattice parameters before and after relaxation
        lattice_initial = self.atoms.lattice
        lattice_final = relaxed_atoms.lattice

        # Prepare final results dictionary
        final_results = {}

        # Initialize variables for error calculation
        err_a = err_b = err_c = err_vol = err_form = err_kv = err_c11 = (
            err_c44
        ) = err_surf_en = err_vac_en = np.nan
        form_en_entry = kv_entry = c11_entry = c44_entry = 0

        if "calculate_forces" in self.properties_to_calculate:
            self.calculate_forces(self.atoms)

        # Prepare final results dictionary
        final_results = {}

        # Initialize variables for error calculation
        err_a = err_b = err_c = err_vol = err_form = err_kv = err_c11 = (
            err_c44
        ) = err_surf_en = err_vac_en = np.nan
        form_en_entry = kv_entry = c11_entry = c44_entry = 0

        # Calculate E-V curve and bulk modulus if specified
        if "calculate_ev_curve" in self.properties_to_calculate:
            _, _, _, _, bulk_modulus, _, _ = self.calculate_ev_curve(
                relaxed_atoms
            )
            kv_entry = self.reference_data.get("bulk_modulus_kv", 0)
            final_results["modulus"] = {
                "kv": bulk_modulus,
                "kv_entry": kv_entry,
            }
            err_kv = (
                mean_absolute_error([kv_entry], [bulk_modulus])
                if bulk_modulus is not None
                else np.nan
            )

        # Formation energy
        if "calculate_formation_energy" in self.properties_to_calculate:
            formation_energy = self.calculate_formation_energy(relaxed_atoms)
            form_en_entry = self.reference_data.get(
                "formation_energy_peratom", 0
            )
            final_results["form_en"] = {
                "form_energy": formation_energy,
                "form_energy_entry": form_en_entry,
            }
            err_form = mean_absolute_error([form_en_entry], [formation_energy])

        # Elastic tensor
        if "calculate_elastic_tensor" in self.properties_to_calculate:
            elastic_tensor = self.calculate_elastic_tensor(relaxed_atoms)
            c11_entry = self.reference_data.get("elastic_tensor", [[0]])[0][0]
            c44_entry = self.reference_data.get(
                "elastic_tensor", [[0, 0, 0, [0, 0, 0, 0]]]
            )[3][3]
            final_results["elastic_tensor"] = {
                "c11": elastic_tensor.get("C_11", 0),
                "c44": elastic_tensor.get("C_44", 0),
                "c11_entry": c11_entry,
                "c44_entry": c44_entry,
            }
            err_c11 = mean_absolute_error(
                [c11_entry], [elastic_tensor.get("C_11", np.nan)]
            )
            err_c44 = mean_absolute_error(
                [c44_entry], [elastic_tensor.get("C_44", np.nan)]
            )

        # Phonon analysis
        if "run_phonon_analysis" in self.properties_to_calculate:
            phonon, zpe = self.run_phonon_analysis(relaxed_atoms)
            final_results["zpe"] = zpe
        else:
            zpe = None

        # Surface energy analysis
        if "analyze_surfaces" in self.properties_to_calculate:
            self.analyze_surfaces()
            surf_en, surf_en_entry = [], []
            surface_entries = get_surface_energy_entry(
                self.jid, collect_data()
            )

            indices_list = self.surface_settings.get(
                "indices_list",
                [
                    [1, 0, 0],
                    [1, 1, 1],
                    [1, 1, 0],
                    [0, 1, 1],
                    [0, 0, 1],
                    [0, 1, 0],
                ],
            )

            for indices in indices_list:
                surface_name = (
                    f"Surface-{self.jid}_miller_{'_'.join(map(str, indices))}"
                )
                calculated_surface_energy = self.job_info.get(surface_name, 0)
                try:
                    # Try to match the surface entry
                    matching_entry = next(
                        (
                            entry
                            for entry in surface_entries
                            if entry["name"].strip() == surface_name.strip()
                        ),
                        None,
                    )
                    if (
                        matching_entry
                        and calculated_surface_energy != 0
                        and matching_entry["surf_en_entry"] != 0
                    ):
                        surf_en.append(calculated_surface_energy)
                        surf_en_entry.append(matching_entry["surf_en_entry"])
                    else:
                        print(
                            f"No valid matching entry found for {surface_name}"
                        )
                except Exception as e:
                    # Handle the exception, log it, and continue
                    print(f"Error processing surface {surface_name}: {e}")
                    self.log(
                        f"Error processing surface {surface_name}: {str(e)}"
                    )
                    continue  # Skip this surface and move to the next one
            final_results["surface_energy"] = [
                {
                    "name": f"Surface-{self.jid}_miller_{'_'.join(map(str, indices))}",
                    "surf_en": se,
                    "surf_en_entry": see,
                }
                for se, see, indices in zip(
                    surf_en, surf_en_entry, indices_list
                )
            ]
            err_surf_en = (
                mean_absolute_error(surf_en_entry, surf_en)
                if surf_en
                else np.nan
            )

        # Vacancy energy analysis
        if "analyze_defects" in self.properties_to_calculate:
            self.analyze_defects()
            vac_en, vac_en_entry = [], []
            vacancy_entries = get_vacancy_energy_entry(
                self.jid, collect_data()
            )
            for defect in Vacancy(self.atoms).generate_defects(
                on_conventional_cell=True, enforce_c_size=8, extend=1
            ):
                defect_name = f"{self.jid}_{defect.to_dict()['symbol']}"
                vacancy_energy = self.job_info.get(
                    f"vacancy_formation_energy for {defect_name}", 0
                )
                try:
                    # Try to match the vacancy entry
                    matching_entry = next(
                        (
                            entry
                            for entry in vacancy_entries
                            if entry["symbol"] == defect_name
                        ),
                        None,
                    )
                    if (
                        matching_entry
                        and vacancy_energy != 0
                        and matching_entry["vac_en_entry"] != 0
                    ):
                        vac_en.append(vacancy_energy)
                        vac_en_entry.append(matching_entry["vac_en_entry"])
                    else:
                        print(
                            f"No valid matching entry found for {defect_name}"
                        )
                except Exception as e:
                    # Handle the exception, log it, and continue
                    print(f"Error processing defect {defect_name}: {e}")
                    self.log(
                        f"Error processing defect {defect_name}: {str(e)}"
                    )
                    continue  # Skip this defect and move to the next one
            final_results["vacancy_energy"] = [
                {"name": ve_name, "vac_en": ve, "vac_en_entry": vee}
                for ve_name, ve, vee in zip(
                    [
                        f"{self.jid}_{defect.to_dict()['symbol']}"
                        for defect in Vacancy(self.atoms).generate_defects(
                            on_conventional_cell=True,
                            enforce_c_size=8,
                            extend=1,
                        )
                    ],
                    vac_en,
                    vac_en_entry,
                )
            ]
            err_vac_en = (
                mean_absolute_error(vac_en_entry, vac_en) if vac_en else np.nan
            )

        # Additional analyses
        if (
            "analyze_interfaces" in self.properties_to_calculate
            and self.film_jid
            and self.substrate_jid
        ):
            self.analyze_interfaces()

        if "run_phonon3_analysis" in self.properties_to_calculate:
            self.run_phonon3_analysis(relaxed_atoms)

        if "calculate_thermal_expansion" in self.properties_to_calculate:
            self.calculate_thermal_expansion(relaxed_atoms)

        if "general_melter" in self.properties_to_calculate:
            quenched_atoms = self.general_melter(relaxed_atoms)
            if "calculate_rdf" in self.properties_to_calculate:
                self.calculate_rdf(quenched_atoms)

        # Record lattice parameters
        final_results["energy"] = {
            "initial_a": lattice_initial.a,
            "initial_b": lattice_initial.b,
            "initial_c": lattice_initial.c,
            "initial_vol": lattice_initial.volume,
            "final_a": lattice_final.a,
            "final_b": lattice_final.b,
            "final_c": lattice_final.c,
            "final_vol": lattice_final.volume,
            "energy": self.job_info.get("final_energy_structure", 0),
        }

        # Error calculations
        err_a = mean_absolute_error([lattice_initial.a], [lattice_final.a])
        err_b = mean_absolute_error([lattice_initial.b], [lattice_final.b])
        err_c = mean_absolute_error([lattice_initial.c], [lattice_final.c])
        err_vol = mean_absolute_error(
            [lattice_initial.volume], [lattice_final.volume]
        )

        # Create an error dictionary
        error_dat = {
            "err_a": err_a,
            "err_b": err_b,
            "err_c": err_c,
            "err_form": err_form,
            "err_vol": err_vol,
            "err_kv": err_kv,
            "err_c11": err_c11,
            "err_c44": err_c44,
            "err_surf_en": err_surf_en,
            "err_vac_en": err_vac_en,
            "time": time.time() - start_time,
        }

        print("Error metrics calculated:", error_dat)

        # Create a DataFrame for error data
        df = pd.DataFrame([error_dat])

        # Save the DataFrame to CSV
        unique_dir = os.path.basename(self.output_dir)
        fname = os.path.join(self.output_dir, f"{unique_dir}_error_dat.csv")
        df.to_csv(fname, index=False)

        # Plot the scorecard with errors
        self.plot_error_scorecard(df)

        # Write results to a JSON file
        output_file = os.path.join(
            self.output_dir, f"{self.jid}_{self.calculator_type}_results.json"
        )
        save_dict_to_json(final_results, output_file)

        # Log total time
        total_time = error_dat["time"]
        self.log(f"Total time for run: {total_time} seconds")

        return error_dat

    def plot_error_scorecard(self, df):
        import plotly.express as px

        fig = px.imshow(
            df, text_auto=True, aspect="auto", labels=dict(color="Error")
        )

        # Update layout for larger font sizes
        fig.update_layout(
            font=dict(size=24),  # Adjust the font size
            coloraxis_colorbar=dict(
                title_font=dict(size=18), tickfont=dict(size=18)
            ),
        )

        # Optionally adjust the text font size for cells
        fig.update_traces(textfont=dict(size=18))  # Adjust text size in cells

        unique_dir = os.path.basename(self.output_dir)
        fname_plot = os.path.join(
            self.output_dir, f"{unique_dir}_error_scorecard.png"
        )
        fig.write_image(fname_plot)
        fig.show()
