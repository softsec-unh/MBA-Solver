#/usr/bin/python3


def generate_sub_dataset():
    """generate a sub-dataset of the entire dataset.
    """
    linear_dataset = "../dataset/pldi_dataset_linear_MBA.txt"
    poly_dataset = "../dataset/pldi_dataset_poly_MBA.txt"
    nonpoly_dataset = "../dataset/pldi_dataset_nonpoly_MBA.txt"

    datasets = [linear_dataset, poly_dataset, nonpoly_dataset]
    subNameList = ["pldi_dataset_linear_MBA.txt", "pldi_dataset_poly_MBA.txt", "pldi_dataset_nonpoly_MBA.txt"]
    for (i, dataset) in enumerate(datasets):
        linenum = 0
        fw = open(subNameList[i], "w")
        print("#complex,groundtruth", file=fw)
        with open(dataset, "r") as fr:
            for line in fr:
                if "#" not in line:
                    linenum += 1
                    if linenum % 50 == 3:
                        print(line, end="", file=fw)

        fw.close()

    return None
 
if __name__ == "__main__":
    generate_sub_dataset()



