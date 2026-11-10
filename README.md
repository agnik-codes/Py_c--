# Cab Pool Matcher

## 1. Project Overview

Cab Pool Matcher is a command-line application developed using Python for the SUTT Backend Developer Recruitment Assignment.

The application helps students travelling to the same destination at the same time share cabs. Students can submit ride requests, wait in priority queues, and get assigned to available cabs.

The main objective is to ensure that students are assigned seats based on their academic year, with senior students receiving higher priority.

## 2. Features

- Register new student ride requests.
- Support two destinations: Delhi and Jaipur.
- Support four time slots: Morning, Afternoon, Evening, and Night.
- Maintain separate priority queues for each destination and time-slot combination.
- Give priority to senior students (Year 5 before Year 4, Year 3, Year 2, and Year 1).
- Maintain first-come, first-served order among students belonging to the same year.
- View all waiting students and their priority order.
- View all cabs, including their drivers, destinations, time slots, passenger lists, and departure status.
- Preview possible cab matches without changing the waiting queue.
- Dispatch cabs by assigning the most senior eligible students to available seats.
- Save and restore application data using JSON.

## 3. Technologies Used

- **Python 3:** Main programming language.
- **CSV:** Used to store and load initial cab information.
- **JSON:** Used to save and restore application state.
- **heapq:** Used to implement priority queues.
- **datetime:** Used to record request submission times.

All modules used belong to Python's standard library. No external packages are required.

## 4. Project Structure

```text
cab_pool_matcher/
│
├── main.py
├── models.py
├── queue_manager.py
├── cab_manager.py
├── storage.py
├── cabs.csv
├── data.json
├── README.md
└── .gitignore
```

### Description of Files

| File | Description |
|---|---|
| `main.py` | Contains the main application menu and handles user interaction. |
| `models.py` | Defines the RideRequest and Cab classes. |
| `queue_manager.py` | Implements and manages priority queues for student requests. |
| `cab_manager.py` | Handles cab matching, previewing, and dispatching. |
| `storage.py` | Handles saving and loading application data using JSON. |
| `cabs.csv` | Contains the initial cab information. |
| `data.json` | Stores the saved application state and is generated automatically. |
| `.gitignore` | Specifies files and folders that Git should ignore. |

## 5. Requirements

- Python 3 installed on the system.
- A terminal or command-line interface.
- Git (recommended for version control).

No additional Python packages need to be installed.

## 6. How to Run the Application

1. Clone or download the repository.
2. Open the project folder in the terminal.
3. Execute the following command:

```bash
python3 main.py
```

4. The application menu will appear in the terminal.
5. Select the desired option and follow the instructions.

On Windows, use:

```bash
python main.py
```

## 7. Cab Data Format (CSV)

The application loads cab information from the `cabs.csv` file instead of hard-coding cab details into the program.

The CSV file follows this structure:

```csv
driver,seats,destination,time_slot
Rahul,4,Delhi,Morning
Amit,3,Jaipur,Afternoon
Priya,4,Delhi,Evening
Neha,4,Jaipur,Night
```

### CSV Fields

- **driver:** Name of the cab driver.
- **seats:** Total passenger capacity of the cab (1–4).
- **destination:** Destination of the cab (Delhi or Jaipur).
- **time_slot:** Scheduled time slot (Morning, Afternoon, Evening, or Night).

### Why CSV Was Chosen

CSV was chosen for storing the initial cab information because:

- Cab information is naturally tabular, with each cab having the same set of fields.
- CSV files are simple, lightweight, and easy to read.
- They can be opened and edited using spreadsheet applications such as Microsoft Excel or Google Sheets.
- Python provides a built-in `csv` module, so no external dependencies are required.
- It is easy to add, remove, or modify cab entries without changing the Python source code.

## 8. Priority Queue Implementation

The application maintains a separate priority queue for every destination and time-slot combination.

For example:
- Delhi, Morning
- Delhi, Evening
- Jaipur, Morning
- Jaipur, Night

Students are prioritised according to the following order:

1. Year 5
2. Year 4
3. Year 3
4. Year 2
5. Year 1

If two students belong to the same year, the student who submitted the request earlier receives priority.

The application uses Python's built-in `heapq` module to implement priority queues.

The priority tuple used is:

```python
(-request.year, request.request_order, request)
```

The negative year value ensures that students from higher years receive priority because Python's `heapq` implements a min-heap.

The request order is used as a tie-breaker to ensure that students from the same year are served in registration order.

This also avoids directly comparing two RideRequest objects.

## 9. Finding Matches and Dispatching Cabs

### Finding Matches

The matching operation checks available cabs and identifies waiting students who could be assigned seats based on their destination, time slot, and priority.

This operation is only a preview. It does not remove students from the waiting queue or assign them to a cab.

### Dispatching a Cab

When a cab is dispatched:

1. The application identifies an available cab for the selected destination and time slot.
2. It retrieves students from the corresponding priority queue.
3. Students are selected according to seniority.
4. Students are assigned seats up to the available capacity of the cab.
5. Assigned students are removed from the waiting queue.
6. The cab is marked as departed.

A cab can leave even if all its seats are not occupied.

## 10. Brownie Points: Data Persistence

The application uses a JSON file named `data.json` to save its current state.

The saved information includes:

- Students who are still waiting.
- Students assigned to each cab.
- Cab details and passenger lists.
- Departure status of every cab.
- Request order and submission information.

When the application is started again, it loads the saved information so that the previous state can be restored.

The request order is preserved so that students belonging to the same academic year retain their original first-come, first-served priority after restarting the application.

### Why JSON Was Chosen

JSON was chosen for saving application data because:

- JSON is human-readable and easy to understand.
- It supports structured data such as dictionaries, lists, and nested objects.
- It is suitable for storing information about cabs along with their passenger lists.
- Python provides a built-in `json` module, so no external package is required.
- It is easier to inspect and debug compared to binary serialization formats.

JSON was preferred over pickle because the saved information should be readable by humans and should not depend on Python-specific binary serialization.

### Why Both CSV and JSON Are Used

CSV is used for the initial cab information because it is simple tabular data with fixed columns.

JSON is used for application persistence because the application's changing state contains nested information, such as cabs containing multiple passengers, as well as waiting requests and departure statuses.

Thus, each format is used for the type of data it handles most conveniently.

## 11. Tricky Situations and Their Handling

### 1. Half-Empty Cab

A cab can be dispatched even when it does not have enough passengers to fill all its seats.

It takes only the available eligible waiting students, up to its seat capacity. The remaining seats stay empty.

### 2. No Cabs Left

If all suitable cabs have departed or no matching open cab is available, new requests remain in the waiting queue.

The application displays an appropriate message. Student requests are never silently deleted.

### 3. Students from the Same Year

The request order is included in the priority tuple along with the year.

This ensures that when two students belong to the same academic year, the student who registered earlier receives priority.

### 4. Large Number of Students

The priority queue allows the application to manage a large number of ride requests efficiently.

The time complexities of important operations are discussed below.

## 12. Time Complexity Analysis

Let:

- `N` = Number of waiting students in a particular queue.
- `C` = Total number of cabs.
- `K` = Number of students assigned to a cab (maximum 4).

| Operation | Time Complexity | Explanation |
|---|---|---|
| Add one request | O(log N) | Insertion into a heap takes logarithmic time. |
| Add 1,000 requests | O(1000 log 1000) | Each request is inserted into the priority queue. |
| Find a matching cab | O(C) | Cabs are checked one by one until a suitable cab is found. |
| Dispatch one cab | O(C + K log N) | Finding a cab takes O(C), and removing K students from the heap takes O(K log N). |

Since a cab has at most four seats, K is at most 4.

Getting all requests in sorted priority order requires O(N log N) time because the heap entries are sorted for display.

## 13. Input Validation

The application checks user input to avoid invalid ride requests.

The supported values are:

- Destinations: Delhi and Jaipur.
- Time slots: Morning, Afternoon, Evening, and Night.
- Academic years: 1 to 5.
- Cab seats: 1 to 4.

Invalid inputs should display a friendly error message instead of causing the application to crash.

## 14. Version Control

Git and GitHub are used for version control and project submission.

The repository includes the Python source files, sample cab CSV file, README, and `.gitignore`.

The `.gitignore` file excludes unnecessary generated files such as:

- `.venv/`
- `__pycache__/`
- `*.pyc`
- `data.json`
- `.DS_Store`

The sample `cabs.csv` file is kept in the repository because it is required to initialise the cab information.

## 15. Conclusion

Cab Pool Matcher demonstrates the use of Python classes, priority queues, file handling, and data persistence to solve a practical cab-sharing problem.

The application ensures that students are assigned seats according to seniority while maintaining first-come, first-served order among students in the same year.

The project also demonstrates modular code organisation and the use of Git for version control.

## Author

Developed as part of the **SUTT Backend Developer Recruitment – Cab Pool Matcher Assignment**.

By **Agnik Roy**
