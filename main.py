from takip import create_entry, read_all_entries, update_entry, delete_entry

if __name__ == "__main__":
    create_entry('2023-11-12', 'example', 'GET', 'None')
    update_entry(1, 'Updated error message')
    read_all_entries()

