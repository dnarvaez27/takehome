# Take Home Project

Challenge: A directory contains multiple files and directories of non-uniform file and directory names. Create a program that traverses a base directory and creates an index file that can be used to quickly lookup files by name, size, and content type.

# Installation

There are two installation methods using Docker or using Poetry.

<details>
  <summary>Using Docker</summary>

**Build the Docker image**

```
docker build --tag 'python3.11_poetry' .
```

**Run the Docker image**

```
docker run --name david-narvaez-takehome -ti --rm 'python3.11_poetry'
```

</details>

<details>
<summary>Using Poetry virtual env</summary>

> Be sure to have Python 3.11 and Poetry (at least v1.5.1) installed in your system

**Install the dependencies**

```
poetry install
```

Run the command line

```
poetry run python main.py
```

</details>

# Usage

At this point you should have an active command line terminal asking for input. The menu asks for three possible options:

- `r`: Refresh the index with files using a given a directory relative path (should be done at least once to fill the index)
- `s`: Performa a search query using the already filled index (refer here for [Query reference](https://whoosh.readthedocs.io/en/latest/querylang.html))
- `q`: Exit the interactive shell.

The Index schema is the following:

```json
{
  "filename": "[string] Name of the file without extension",
  "extension": "[string] Extension of the file",
  "size": "[number] Size in bytes of the file",
  "path": "[string] Absolute path to the file"
}
```

### Example Queries

<details>
  <summary>Look for all files whose name have at least one word starting with the <code>user</code> prefix.</summary>

```
filename:user*
```

Alternatively you can omit the `filename:` prefix as the filename is the default field to search for

```
user*
```

</details>

<details>
  <summary>Look for all files whose size is less than or equal to 100 bytes</summary>

```
size:[TO 100]
```

</details>

<details>
  <summary>Look for all JSON files</summary>

```
extension:json
```

</details>

# How does it works

**Index refreshing**

The application traverses all the directories and files in the given path. For each of those files it gathers information about the file (size and extension).

This is done in multiple processes to improve performance (depends on the configuration and the quantity of files). To adjust the concurrent processes update the `TRAVERSAL_PROCESSES` constant in the `main.py` file.

Once this information is gathered and structured, it uploads that information to the index. Missing fields are skipped from being indexed, that is why it is not possible to search for entries based on a missing field (e.g. all files with no extension).

**Search**

The hard work of the implementation is left to the Whoosh library. The quantity of results is limited to improve performance of the operation. If this value needs to be modified, change the value of the constant `MAX_SEARCH_RESULTS` in the `main.py` file.

---

**Why Whoosh?**

- It is an out of the box solution for index and text-search functionality in python, so we don't reinvent the wheel.
- Its query language is similar to what Apache Lucene offers so it is very powerful.
- Requires minimal dependencies and it is pure python which is simpler to port to multiple OSs and architectures.
