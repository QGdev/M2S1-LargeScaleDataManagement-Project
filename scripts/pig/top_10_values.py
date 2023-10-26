def find_top_values(file_path):
    top_values = []

    with open(file_path, 'r') as file:
        for line in file:
            elements = line.split('\t')

            # Skip incorrect lines
            if len(elements) < 2:
                continue

            # Skip incorrect pagerank values (non-existent, or not a number)
            try:
                pr_value = float(elements[1])
            except ValueError:
                continue

            top_values.append((elements[0].strip(), pr_value))

    # Sort the list
    top_values.sort(key=lambda x: x[1], reverse=True)

    # Keep to 10 values
    top_values = top_values[:10]

    return top_values


if __name__ == '__main__':
    path = './out/pagerank_data_3/part-r-00000.txt'
    results = find_top_values(path)
    print("Top 10 Values and IRIs:")
    for i, (iri, value) in enumerate(results, start=1):
        print(f"{i}. IRI: {iri}, Value: {value}")
