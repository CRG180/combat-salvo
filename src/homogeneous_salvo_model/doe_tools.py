
import csv
import itertools
import os
from datetime import datetime
import multiprocessing
from homogeneous_salvo_model import Force, Engagement

class DOESimulation:
    """
    A class to represent a Design of Experiments simulation for a homogeneous salvo model.

    ...

    Attributes
    ----------
    input_file_path : str
        The path to the input CSV file containing the DOE parameters.
    output_file_path : str, optional
        The path to the output CSV file for writing the results.
    doe_parameters : list
        A list of tuples containing pairs of Force objects representing the DOE parameters.
    results : list
        A list to store the results of simulations.

    Methods
    -------
    __init__(self, input_file_path, output_file_path=None)
        Initializes a new instance of the DOESimulation class.

    read_doe_parameters(self)
        Reads the DOE parameters from the input CSV file.

    run_simulations(self)
        Runs the simulations sequentially (non-parallel) and stores the results.

    run_simulations_parallel(self)
        Runs the simulations using parallel processing and stores the results.

    write_results_to_file(self, include_input_parameters=False)
        Writes the simulation results to a CSV file.

    display_results(self, include_input_parameters=False)
        Displays the simulation results in the terminal.
    """
    def __init__(self, input_file_path, output_file_path=None):
        """
        Initializes a new instance of the DOESimulation class.

        Parameters
        ----------
        input_file_path : str
            The path to the input CSV file containing the DOE parameters.
        output_file_path : str, optional
            The path to the output CSV file for writing the results. If not provided, a default filename
            will be generated based on the current date and time.
        """
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.doe_parameters = []
        self.results = []  # Store the results of simulations

        if not self.output_file_path:
            # If output_file_path is not provided, use the same directory as input_file_path
            # with a different file name for the output CSV file
            output_file_name = f"doe_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            self.output_file_path = os.path.join(os.path.dirname(input_file_path), output_file_name)

    def read_doe_parameters(self):
        """
        Reads the DOE parameters from the input CSV file.
        """
        with open(self.input_file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                force_A = Force(
                    name=row["name_A"],
                    num_units=int(row["num_units_A"]),
                    aimed_offense=int(row["aimed_offense_A"]),
                    num_missiles=int(row["num_missiles_A"]),
                    defense_capability=int(row["defense_capability_A"]),
                    defense_staying=int(row["defense_staying_A"]),
                )

                force_B = Force(
                    name=row["name_B"],
                    num_units=int(row["num_units_B"]),
                    aimed_offense=int(row["aimed_offense_B"]),
                    num_missiles=int(row["num_missiles_B"]),
                    defense_capability=int(row["defense_capability_B"]),
                    defense_staying=int(row["defense_staying_B"]),
                )

                self.doe_parameters.append((force_A, force_B))

    def run_simulations(self):
        """
        Runs the simulations sequentially (non-parallel) and stores the results.
        """
        for idx, (a, b) in enumerate(self.doe_parameters, start=1):
            battle = Engagement(a, b)
            battle.iter_engagement()
            self.results.append((a, b, battle.iter))
        print(f"Simulation completed {idx} runs.")

    def run_simulations_parallel(self):
        """
        Runs the simulations using parallel processing and stores the results.
        """
        with multiprocessing.Pool() as pool:
            def run_single_simulation(experiment):
                a, b = experiment
                battle = Engagement(a, b)
                battle.iter_engagement()
                return a, b, battle.iter

            self.results = pool.map(run_single_simulation, self.doe_parameters)

        # Process the results as needed (e.g., write to CSV file or display in terminal)
        # ...

    def write_results_to_file(self, include_input_parameters=False):
        """
        Writes the simulation results to a CSV file.

        Parameters
        ----------
        include_input_parameters : bool, optional
            If True, includes the input parameters of the simulations in the output CSV file. Default is False.
        """
        with open(self.output_file_path, "w", newline="") as csvfile:
            fieldnames = ["Experiment", "Side A", "Side B", "Winner", "Salvos Fired"]
            if include_input_parameters:
                fieldnames.extend(["Side A Parameters", "Side B Parameters"])
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for idx, (a, b, salvos_fired) in enumerate(self.results, start=1):
                row_data = {
                    "Experiment": idx,
                    "Side A": f"{a.name}: {a.num_units} units",
                    "Side B": f"{b.name}: {b.num_units} units",
                    "Winner": a.name if a > b else b.name,
                    "Salvos Fired": salvos_fired,
                }

                if include_input_parameters:
                    row_data["Side A Parameters"] = str(a.__dict__)
                    row_data["Side B Parameters"] = str(b.__dict__)

                writer.writerow(row_data)
        print(f"Results written to {self.output_file_path}")

    def display_results(self, include_input_parameters=False):
        """
        Displays the simulation results in the terminal.

        Parameters
        ----------
        include_input_parameters : bool, optional
            If True, includes the input parameters of the simulations in the terminal output. Default is False.
        """
        print("\nResults:\n")
        for idx, (a, b, salvos_fired) in enumerate(self.results, start=1):
            print(f"Experiment {idx}")
            print(f"Side A: {a.name} - Remaining Units: {a.num_units}")
            print(f"Side B: {b.name} - Remaining Units: {b.num_units}")
            print(f"Winner: {a.name if a > b else b.name}")
            print(f"Salvos Fired: {salvos_fired}")

            if include_input_parameters:
                print(f"Side A Parameters: {a.__dict__}")
                print(f"Side B Parameters: {b.__dict__}")

            print()


if __name__ == "__main__":
    #current_directory = os.getcwd()
    #print("Current Working Directory:", current_directory)

    doe_simulation = DOESimulation("data/doe_input.csv")
    doe_simulation.read_doe_parameters()

    # Example: Run the simulations sequentially (non-parallel)
    doe_simulation.run_simulations()

    # Optional: Display or write the results
   # doe_simulation.display_results(include_input_parameters=True)
    doe_simulation.write_results_to_file(include_input_parameters=True)