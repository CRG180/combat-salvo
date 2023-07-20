import csv
import itertools
from datetime import datetime
from homogeneous_salvo_model import Force, Engagement


# ... (The previous definitions of Force and Engagement classes)

def read_doe_parameters_from_csv(file_path):
    doe_parameters = []
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name_A = row["name_A"]
            num_units_A = int(row["num_units_A"])
            aimed_offense_A = int(row["aimed_offense_A"])
            num_missiles_A = int(row["num_missiles_A"])
            defense_capability_A = int(row["defense_capability_A"])
            defense_staying_A = int(row["defense_staying_A"])

            name_B = row["name_B"]
            num_units_B = int(row["num_units_B"])
            aimed_offense_B = int(row["aimed_offense_B"])
            num_missiles_B = int(row["num_missiles_B"])
            defense_capability_B = int(row["defense_capability_B"])
            defense_staying_B = int(row["defense_staying_B"])

            force_A = Force(
                name=name_A,
                num_units=num_units_A,
                aimed_offense=aimed_offense_A,
                num_missiles=num_missiles_A,
                defense_capability=defense_capability_A,
                defense_staying=defense_staying_A,
            )

            force_B = Force(
                name=name_B,
                num_units=num_units_B,
                aimed_offense=aimed_offense_B,
                num_missiles=num_missiles_B,
                defense_capability=defense_capability_B,
                defense_staying=defense_staying_B,
            )

            doe_parameters.append((force_A, force_B))
    return doe_parameters



def write_results_to_file(results):
    # Get the current date and time in a specific format
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_name = f"doe_results_{current_datetime}.csv"

    with open(output_file_name, "w", newline="") as csvfile:
        fieldnames = ["Experiment", "Side A", "Side B", "Winner", "Salvos Fired"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for idx, (a, b) in enumerate(results, start=1):
            battle = Engagement(a, b)
            battle.iter_engagement()

            writer.writerow({
                "Experiment": idx,
                "Side A": f"{a.name}: {a.num_units} units",
                "Side B": f"{b.name}: {b.num_units} units",
                "Winner": a.name if a > b else b.name,
                "Salvos Fired": battle.iter
            })

if __name__ == "__main__":
    import os
    current_directory = os.getcwd()
    print("Current Working Directory:", current_directory)
    
    doe_parameters = read_doe_parameters_from_csv("data/doe_input.csv")

    results = []

    for idx, (a, b) in enumerate(doe_parameters, start=1):
        print(f"Running Experiment {idx} - {a.name} vs {b.name}")
        battle = Engagement(a, b)
        battle.iter_engagement()

        results.append((a, b))

    write_results_to_file(results)