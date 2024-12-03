def process_table(table):
    processed_table = []
    for row in table.rows:
        processed_row = [cell.text.strip() for cell in row.cells]
        processed_table.append(processed_row)
    return processed_table
