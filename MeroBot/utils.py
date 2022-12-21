def save_bank_records(filename, banks):
    with open(filename, mode="w") as file:
            for index, bank in enumerate(banks):
                file.write(f"{bank} ---------------<<bank index>>---> [{index}]\n")