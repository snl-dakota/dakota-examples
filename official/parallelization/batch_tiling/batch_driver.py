import dakota.interfacing as di
from flux.job import JobspecV1, FluxExecutor
import concurrent.futures
import os
import pathlib
import sys
from typing import List, Dict


def create_workdir(workdir_base: str, eval_num: int) -> pathlib.Path:
    """Create tagged work directory

    workdir_base: untagged workdirectory name
    eval_num: evaluation number for tag

    return: name of tagged workdir
    """
    workdir = pathlib.Path(workdir_base + f".{eval_num}")
    workdir.mkdir(parents=True, exist_ok=True)
    return workdir


def write_parameters_file(parameters_file: pathlib.Path, parameters: List[str]) -> None:
    """Write parameters to parameters file"""
    with open(parameters_file, "w") as f:
        f.write("".join(parameters))


def create_job_spec(workdir: pathlib.Path, parameters_file: str , results_file: str) -> JobspecV1:
    """Create a Flux jobspec that can be used by Flux's asynch API"""
    # from_command creates a job spec from a command and set of resource requirements
    jobspec = JobspecV1.from_command(
            command=["text_book_par", parameters_file, results_file],
            num_tasks=8
        )
    # A few other attributes must be set explicitly (they aren't constructor arguments)
    jobspec.cwd = str(workdir)
    jobspec.environment = dict(os.environ)
    jobspec.stdout = "stdout.txt"
    jobspec.stderr = "stderr.txt"
    return jobspec


def read_eval_result(results_file: pathlib.Path) -> str:
    """Read the results file and return the contents as a string"""
    with open(results_file, "r") as f:
        return f.read()


def main():
    batch_params_file = sys.argv[1]
    batch_results_file = sys.argv[2]

    splitter = di.BatchSplitter(batch_params_file)
    num_evals = len(splitter)

    parameters_file = "params.in"
    results_file = "results.out"
    workdir_base = "workdir"

    eval_workdir_map = {}
    for i, params in enumerate(splitter):
        eval_num = splitter.eval_nums[i]
        eval_workdir_map[eval_num] = create_workdir(workdir_base, eval_num)
        write_parameters_file(eval_workdir_map[eval_num] / parameters_file, params)

    failed = set()
    with FluxExecutor() as executor:
        futures = {
                executor.submit(create_job_spec(workdir, parameters_file, results_file)): eval_num 
                for eval_num, workdir in eval_workdir_map.items()
                }
        for future in concurrent.futures.as_completed(futures):
            if future.exception():
                eval_num = futures[future]
                print(f"Eval {eval_num} raised exception {future.exception()}", file=sys.stderr)
                failed.add(eval_num)

    with open(batch_results_file, "w") as f:
        for eval_num, workdir in eval_workdir_map.items():
            if eval_num in failed:
                f.write("FAIL\n")
            else:
                eval_result = read_eval_result(workdir / results_file)
                f.write(eval_result)
            f.write("#\n")


if __name__ == "__main__":
    main()

