# KaWAT: Kata.ai Word Analogy Task

KaWAT contains word analogy task for Indonesian. The raw data is stored under
`syntax` and `semantic` directory for syntactic and semantic analogy questions
respectively. To convert the raw data into Google's Analogy Task format, you
must build the dataset by (make sure to have Python 3.6 in your `PATH`):

    make

The build results will be stored under `build` directory. Invoke `make help` to
see other available commands.
