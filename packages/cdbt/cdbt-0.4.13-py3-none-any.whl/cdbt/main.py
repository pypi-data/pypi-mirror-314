import json
import os
import re
import shutil
import subprocess
import sys
import typing as t

import pyperclip
from click.core import Command
from click.core import Context
from dotenv import find_dotenv
from dotenv import load_dotenv

load_dotenv(find_dotenv("../.env"))
load_dotenv(find_dotenv(".env"))


class ColdBoreCapitalDBT:

    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode
        self.dbt_ls_test_mode_output = None
        self.dbt_test_mode_command_check_value = None
        self.exclude_seed_snapshot = "resource_type:snapshot resource_type:seed"

        self.dbt_execute_command_output = ""

    def build(self, ctx: Context, full_refresh, select, fail_fast, threads):
        flags = {
            "select": select,
            "fail_fast": fail_fast,
            "threads": threads,
            "full_refresh": full_refresh,
        }
        args = self._create_common_args(flags)
        try:
            run_result = self.execute_dbt_command_stream("build", args)
        except subprocess.CalledProcessError as e:
            self.handle_cmd_line_error(e)

        if not run_result:
            raise DbtError("DBT build failed with errors.")

    def trun(self, ctx: Context, full_refresh, select, fail_fast, threads):
        flags = {
            "select": select,
            "fail_fast": fail_fast,
            "threads": threads,
            "full_refresh": full_refresh,
        }
        args = self._create_common_args(flags)
        args = args + ["--exclude", self.exclude_seed_snapshot]
        try:
            run_result = self.execute_dbt_command_stream("build", args)
        except subprocess.CalledProcessError as e:
            self.handle_cmd_line_error(e)

        if not run_result:
            raise DbtError("DBT build failed with errors.")

    def run(self, ctx: Context, full_refresh, select, fail_fast, threads):
        flags = {
            "select": select,
            "fail_fast": fail_fast,
            "threads": threads,
            "full_refresh": full_refresh,
        }
        args = self._create_common_args(flags)
        try:
            run_result = self.execute_dbt_command_stream("run", args)
        except subprocess.CalledProcessError as e:
            self.handle_cmd_line_error(e)

        if not run_result:
            raise DbtError("DBT build failed with errors.")

    def test(self, ctx: Context, select, fail_fast, threads):
        flags = {"select": select, "fail_fast": fail_fast, "threads": threads}
        args = self._create_common_args(flags)
        try:
            run_result = self.execute_dbt_command_stream("test", args)
        except subprocess.CalledProcessError as e:
            self.handle_cmd_line_error(e)

        if not run_result:
            raise DbtError("DBT build failed with errors.")

    def unittest(self, ctx: Context, select, fail_fast):
        select = f"{select},tag:unit-test"  # Comma is an and condition.
        flags = {"select": select, "fail_fast": fail_fast}
        args = self._create_common_args(flags)
        try:
            run_result = self.execute_dbt_command_stream("test", args)
        except subprocess.CalledProcessError as e:
            self.handle_cmd_line_error(e)

        if not run_result:
            raise DbtError("DBT build failed with errors.")

    def compile(self, ctx: Context, select):
        # We ignore the ctx object as compile has no threads.
        try:
            self.execute_dbt_command_stream("compile", [])
        except subprocess.CalledProcessError as e:
            self.handle_cmd_line_error(e)

    def clip_compile(self, ctx: Context, select):
        # We ignore the ctx object as compile has no threads.
        try:
            self.execute_dbt_command_stream("compile", ["-s", select])
            results = self.dbt_execute_command_output
            # Copy to clipboard
            results = self.extract_sql_code(results)
            pyperclip.copy(results)
        except subprocess.CalledProcessError as e:
            self.handle_cmd_line_error(e)

    def recce(self, ctx: Context):
        print("Downloading production artifacts.")
        current_dir = os.getcwd()
        # Initialize variables
        target_path = None
        logs = None
        # Check if current directory ends with 'transform'
        if current_dir.endswith('transform'):
            target_path = os.path.join('target-base')
            logs = os.path.join('logs')
        elif os.path.isdir(os.path.join(current_dir, 'transform')):
            target_path = os.path.join('transform', 'target-base')
            logs = os.path.join('transform', 'logs')
        else:
            raise FileNotFoundError("No 'transform' directory found in the current execution directory.")
        os.makedirs(target_path, exist_ok=True)

        # Delete all files in target_path
        for file_name in os.listdir(target_path):
            file_path = os.path.join(target_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)


        # Pull artifacts from Snowflake. These are the latest production artifacts.
        try:
            if not self.test_mode:
                subprocess.run(
                    ["dbt", "run-operation", "get_last_artifacts"], check=True
                )
        except subprocess.CalledProcessError as e:
            self.handle_cmd_line_error(e)

        # Copy files from logs to target_path
        if os.path.isdir(logs):
            for file_name in os.listdir(logs):
                full_file_path = os.path.join(logs, file_name)
                if os.path.isfile(full_file_path):
                    shutil.copy(full_file_path, target_path)
        else:
            raise FileNotFoundError(f"'logs' directory not found at expected path: {logs}")

        # Start recce server
        try:
            if not self.test_mode:
                subprocess.run(
                    ["dbt", "docs", "generate"], check=True
                )
                subprocess.run(
                    ["recce", "server"], check=True
                )
        except subprocess.CalledProcessError as e:
            self.handle_cmd_line_error(e)

    def handle_cmd_line_error(self, e):
        print(f'Failure while running command: {" ".join(e.cmd)}')
        print(e.stderr)
        print(e.stdout)
        raise Exception(f"Failure while running command: {' '.join(e.cmd)}")
        # sys.exit(e.returncode)

    def sbuild(self, ctx: Context, full_refresh, threads):
        print("Starting a state build based on local manifest.json")
        artifact_dir = "_artifacts"
        target_dir = "target"
        # Path to the artifacts file that will be generated by the dbt compile command representing the current state.
        manifest_path = os.path.join("./", target_dir, "manifest.json")
        # Path to the artifact file that represents the prior build state.
        manifest_artifact_path = os.path.join("./", artifact_dir, "manifest.json")

        self.execute_state_based_build(
            ctx,
            artifact_dir,
            manifest_artifact_path,
            manifest_path,
            full_refresh,
            threads,
            roll_back_manifest_flag=True,
        )

    def pbuild(self, ctx: Context, full_refresh, threads, skip_download):
        print("Starting a state build based on production manifest.json")
        artifact_dir = "logs"
        target_dir = "target"
        # Pull artifacts from Snowflake. These are the latest production artifacts.
        try:
            if not self.test_mode and not skip_download:
                subprocess.run(
                    ["dbt", "run-operation", "get_last_artifacts"], check=True
                )
        except subprocess.CalledProcessError as e:
            self.handle_cmd_line_error(e)

        manifest_path = os.path.join("", target_dir, "manifest.json")
        manifest_artifact_path = os.path.join("", artifact_dir, "manifest.json")

        self.execute_state_based_build(
            ctx,
            artifact_dir,
            manifest_artifact_path,
            manifest_path,
            full_refresh,
            threads,
            roll_back_manifest_flag=False,
        )

    def gbuild(self, ctx: Context, main, full_refresh, threads):
        """
        Build based off of a Git diff of changed models.

        Args:
            ctx:
            full_refresh:
            threads:

        Returns:

        """
        if main:
            print("Building based on changes from main branch.")
            result = subprocess.run(
                ["git", "diff", "main", "--name-only"],
                stdout=subprocess.PIPE,
                text=True,
            )
        else:
            result = subprocess.run(
                ["git", "diff", "--name-only"], stdout=subprocess.PIPE, text=True
            )

        modified_files = result.stdout.splitlines()

        sql_files = [
            file.split("/")[-1].replace(".sql", "")
            for file in modified_files
            if "models" in file and file.endswith(".sql")
        ]

        # Construct state commands
        build_children = ctx.obj.get("build_children", False)
        build_children_count = ctx.obj.get("build_children_count", None)
        build_parents = ctx.obj.get("build_parents", False)
        build_parent_count = ctx.obj.get("build_parents_count", None)
        if build_children:
            if build_children_count:
                for i in range(len(sql_files)):
                    sql_files[i] = f"{sql_files[i]}+{build_children_count}"
            else:
                for i in range(len(sql_files)):
                    sql_files[i] = f"{sql_files[i]}+"

        if build_parents:
            if build_parent_count:
                for i in range(len(sql_files)):
                    sql_files[i] = f"{build_parent_count}+{sql_files[i]}"
            else:
                for i in range(len(sql_files)):
                    sql_files[i] = f"+{sql_files[i]}"

        select_list = " ".join(sql_files)

        full_refresh = self._scan_for_incremental_full_refresh(
            state_flags=["--select", select_list],
            exclude_flags=None,
            full_refresh=full_refresh,
        )

        args = [
            "--select",
            select_list,
            "--exclude",
            "resource_type:seed,resource_type:snapshot",
        ]
        if threads:
            args.append("--threads")
            args.append(str(threads))

        if full_refresh:
            args.append("--full-refresh")

        self.execute_dbt_command_stream("build", args)

    def lightdash_start_preview(self, ctx, select, preview_name, l43):
        # Check to make sure the LIGHTDASH_PROJECT env variable is set
        if not os.getenv("LIGHTDASH_PROJECT"):
            print(
                "LIGHTDASH_PROJECT environment variable not set. Set this key to the ID of the project you will "
                "promote charts to."
            )
            sys.exit(1)
        else:
            print(f"Building for LIGHTDASH_PROJECT: {os.getenv('LIGHTDASH_PROJECT')}")

        self._check_lightdash_for_updates()
        if not preview_name:
            # If no preview name, use the current name of the git branch
            result = subprocess.run(
                ["git", "branch", "--show-current"], stdout=subprocess.PIPE, text=True
            )
            preview_name = result.stdout.strip()

        args = ["lightdash", "start-preview", "--name", preview_name]

        if l43:
            args = args + ["-s", "tag:l3 tag:l4"]

        if select:
            args = args + ["--select", select]

        try:
            print(f'Running command: {" ".join(args)}')
            subprocess.run(args, check=True)
        except subprocess.CalledProcessError as e:
            self.handle_cmd_line_error(e)

    @staticmethod
    def _check_lightdash_for_updates():
        api_str = 'curl -s "https://app.lightdash.cloud/api/v1/health"'

        try:
            result = subprocess.run(
                api_str, shell=True, check=True, text=True, capture_output=True
            )
            # Convert to JSON
            result_json = json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Failure while running command: {api_str}")
            print(e.stderr)
            print(e.stdout)
            sys.exit(e.returncode)

        api_version = result_json["results"]["version"]

        result = subprocess.run(
            ["lightdash", "--version"], check=True, text=True, capture_output=True
        )

        current_version = result.stdout.strip()

        if api_version != current_version:
            print(
                f"API version {api_version} does not match current version {current_version}. Upgrading."
            )
            args = ["npm", "install", "-g", f"@lightdash/cli@{api_version}"]
            subprocess.run(args, check=True)
        else:
            print(
                f"API version {api_version} matches current version {current_version}."
            )

    def pre_commit(self, ctx):
        args = ["pre-commit", "run", "--all-files"]

        try:
            subprocess.run(args, check=True)
        except subprocess.CalledProcessError as e:
            self.handle_cmd_line_error(e)

    def format(self, ctx: Context, select, all=False, main=False):
        """
        Scan for files that have changed since the last commit and pass them to sqlfluff fix command for cleanup.

        Args:
            ctx: Context object.
        """
        print("Scanning for changed files since last commit.")
        # Set the env path to the .sqlfluffignore
        os.environ["SQLFLUFF_CONFIG"] = "../.sqlfluffignore"
        try:
            if main:
                # Check against main.
                result = subprocess.run(
                    ["git", "diff", "--name-only", "main"],
                    stdout=subprocess.PIPE,
                    text=True,
                    check=True,
                )
            else:
                # Check against last commit.
                result = subprocess.run(
                    ["git", "diff", "--name-only"],
                    stdout=subprocess.PIPE,
                    text=True,
                    check=True,
                )
            changed_files = result.stdout.splitlines()
        except subprocess.CalledProcessError as e:
            print(f'Failure while running git command: {" ".join(e.cmd)}')
            print(e.stderr)
            print(e.stdout)
            sys.exit(e.returncode)

        # Filter SQL files
        sql_files = [file for file in changed_files if file.endswith(".sql")]

        # Filter out any files that are not in the models directory
        sql_files = [file for file in sql_files if "models" in file]

        if not sql_files and not all:
            print("No SQL files have changed since the last commit.")
            return

        if all:
            sql_files = ["./models"]

        for sql_file in sql_files:
            try:
                print(f"Running sqlfluff fix on {sql_file}")
                subprocess.run(
                    ["sqlfluff", "fix", sql_file, "--config", "../.sqlfluff"],
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                print(f"Failure while running sqlfluff fix command on {sql_file}")
                print(e.stderr)
                print(e.stdout)
                # Optionally, we might not want to exit immediately but continue fixing other files
                # sys.exit(e.returncode)

        print("Sqlfluff fix completed for all changed SQL files.")

    def execute_state_based_build(
        self,
        ctx: Context,
        artifact_dir: str,
        manifest_artifact_path: str,
        manifest_path: str,
        full_refresh: bool,
        threads: int,
        roll_back_manifest_flag: bool,
    ):
        if roll_back_manifest_flag and not self.test_mode:
            print(
                f"Making a backup of the current manifest.json at {manifest_path} to {manifest_artifact_path}"
            )
            # Move the manifest from ./target to ./_artifacts. This becomes the prior state. Only used for local state
            # build. Not used for pdbuild (production build).
            shutil.move(manifest_path, manifest_artifact_path)
        # Execute dbt compile
        try:
            if not self.test_mode:
                subprocess.run(["dbt", "compile"], check=True)
        except subprocess.CalledProcessError as e:
            self.handle_cmd_line_error(e)

        # Construct state commands
        build_children = ctx.obj.get("build_children", False)
        build_children_count = ctx.obj.get("build_children_count", None)
        build_parents = ctx.obj.get("build_parents", False)
        build_parent_count = ctx.obj.get("build_parents_count", None)
        state_modified_str = "state:modified"
        if build_children:
            state_modified_str = f"{state_modified_str}+"
            if build_children_count:
                state_modified_str = f"{state_modified_str}{build_children_count}"
        if build_parents:
            state_modified_str = f"+{state_modified_str}"
            if build_parent_count:
                state_modified_str = f"{build_parent_count}{state_modified_str}"

        state_flags = [
            "--select",
            state_modified_str,
            "--state",
            os.path.join("", artifact_dir) + "/",
        ]
        exclude_flags = ["--exclude", self.exclude_seed_snapshot]
        # Get a list of models and their config

        full_refresh = self._scan_for_incremental_full_refresh(
            state_flags, exclude_flags, full_refresh
        )

        run_result = None
        # Execute dbt build excluding snapshots and seeds
        # Rest the args.
        args = self._create_common_args({"threads": threads})
        args = args + state_flags + exclude_flags
        if full_refresh:
            args = args + ["--full-refresh"]

        try:
            run_result = self.execute_dbt_command_stream("build", args)
        except subprocess.CalledProcessError as e:
            print(f'Failure while running command: {" ".join(e.cmd)}')
            print(e.stderr)
            print(e.stdout)
            if roll_back_manifest_flag and not self.test_mode:
                self.roll_back_manifest(e, manifest_artifact_path, manifest_path)
            else:
                sys.exit(e.returncode)

        if not run_result:
            e = "DBT build failed with errors."
            self.roll_back_manifest(e, manifest_artifact_path, manifest_path)
            raise DbtError("DBT build failed with errors.")

    def _scan_for_incremental_full_refresh(
        self, state_flags, exclude_flags, full_refresh
    ):
        if state_flags and exclude_flags:
            args = state_flags + exclude_flags
        elif state_flags and not exclude_flags:
            args = state_flags
        elif exclude_flags and not state_flags:
            args = exclude_flags
        else:
            args = []

        args = args + ["--output-keys", "name resource_type config"]
        models_json = self.dbt_ls_to_json(args)
        if not full_refresh:
            for model in models_json:
                if model["config"]["materialized"] == "incremental":
                    full_refresh = True
                    print(
                        f'Found incremental build model: {model["name"]}. Initiating full refresh.'
                    )
                    break
        return full_refresh

    def dbt_ls_to_json(self, args):
        cmd = ["dbt", "ls", "--output", "json"]
        cmd = cmd + args
        try:
            if self.test_mode:
                output = self.dbt_ls_test_mode_output
            else:
                output = subprocess.run(
                    cmd, check=True, text=True, capture_output=True
                ).stdout
        except subprocess.CalledProcessError as e:
            print(e.stderr)
            print(e.stdout)
            print(" ".join(cmd))
            sys.exit(e.returncode)
        # The results come back with a few header lines that need to be removed, then a series of JSON string with a
        # format like: {"name": "active_patient_metrics", "resource_type": "model", "config":
        # {"materialized": "incremental"}} RE removes the header stuff and finds the json lines.
        json_lines = re.findall(r"^{.*$", output, re.MULTILINE)
        # Split lines and filter to get only JSON strings
        models_json = [json.loads(line) for line in json_lines]
        return models_json

    @staticmethod
    def _create_common_args(flags: t.Dict[str, t.Any]) -> t.List[str]:
        threads = flags.get("threads", None)
        select = flags.get("select", None)
        fail_fast = flags.get("fail_fast", None)
        full_refresh = flags.get("full_refresh", None)
        args = []
        if threads:
            args.append("--threads")
            args.append(str(threads))
        if select:
            args.append("--select")
            args.append(select)
        if fail_fast:
            args.append("--fail-fast")
        if full_refresh:
            args.append("--full-refresh")
        return args

    @staticmethod
    def roll_back_manifest(e, manifest_artifact_path, manifest_path):
        print(f"DBT build failed. Rolling back manifest state with error\n {e}")
        # Move the manifest.json from _artifacts back to target dir. If the build failed, we want to rebuild against this
        # state, not the one generated by the compile command.
        shutil.move(manifest_artifact_path, manifest_path)
        sys.exit(e.returncode)

    @staticmethod
    def execute_dbt_command_capture(command: str, args: t.List[str]) -> str:
        """
        Executes a DBT command and captures the output without streaming to the stdout.
        Args:
            command: The DBT command to run.
            args: A list of args to pass into the command.

        Returns:
            A string containing the results of the command.
        """
        cmd = ["dbt", command] + args
        try:
            output = subprocess.run(
                cmd, check=True, text=True, capture_output=True
            ).stdout
        except subprocess.CalledProcessError as e:
            print(f'Failure while running command: {" ".join(cmd)}')
            print(e.stderr)
            print(e.stdout)
            sys.exit(e.returncode)
        return output

    def execute_dbt_command_stream(self, command: str, args: t.List[str]) -> bool:
        """
        Execute a dbt command with the given arguments. This function will stream the output of the command in real-time
        Args:
            command: The DBT command to run.
            args: A list of args to pass into the command.

        Returns:
            True if successful, False if error.
        """

        dbt_command = ["dbt", command] + args
        print(f'Running command: {" ".join(dbt_command)}')
        if self.test_mode:
            self.dbt_test_mode_command_check_value = dbt_command
            return True
        else:
            stderr, stdout = self.subprocess_stream(dbt_command)

            # Check for errors using a regex method if necessary
            if self.contains_errors(stdout + stderr):
                return False

            return True

    def subprocess_stream(self, args):
        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Ensure outputs are in text mode rather than bytes
        )
        # Real-time output streaming
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                print(output.rstrip())  # Print each line of the output
                self.dbt_execute_command_output += output.rstrip() + "\n"
        # Capture and print any remaining output after the loop
        stdout, stderr = process.communicate()
        if stdout:
            print(stdout.strip())
        # Check exit code
        if process.returncode != 0:
            print(f"Command resulted in an error: {stderr}")
            raise subprocess.CalledProcessError(
                returncode=process.returncode, cmd=args, output=stderr
            )
        return stderr, stdout

    @staticmethod
    def extract_sql_code(log: str) -> str:
        """
        Extract the SQL code from the given log string.

        Parameters:
        log (str): The log string containing the header info and SQL code.

        Returns:
        str: The extracted SQL code.
        """
        # Split the log by lines
        lines = log.splitlines()

        # Iterate over the lines and find the first empty line
        sql_start_index = 0
        for i, line in enumerate(lines):
            if line.startswith("\x1b["):
                sql_start_index = i + 1

        # Join the lines from the first empty line to the end
        sql_code = "\n".join(lines[sql_start_index:])

        return sql_code

    @staticmethod
    def contains_errors(text):
        pattern = r"([2-9]|\d{2,})\s+errors?"
        error_flag = bool(re.search(pattern, text))
        return error_flag


class DbtError(Exception):
    def __init__(self, message):
        self.message = "DBT build failed with errors."

    def __str__(self):
        return self.message


class MockCtx(Context):
    def __init__(
        self,
        command: t.Optional["Command"] = None,
    ) -> None:
        self.obj = {
            "build_children": False,
            "build_children_count": None,
            "parents_children": False,
            "build_parent_count": None,
        }


if __name__ == "__main__":
    cdbt = ColdBoreCapitalDBT()
    mock_ctx = MockCtx(Command("Duck"))
    mock_ctx.obj["build_children"] = True
    # cdbt.build(full_refresh=False, select=None, fail_fast=False)
    # cdbt.trun(full_refresh=False, select=None, fail_fast=False)
    # cdbt.run(full_refresh=False, select=None, fail_fast=False)
    # cdbt.test(select=None, fail_fast=False)
    # cdbt.compile()
    # cdbt.sbuild(ctx=None, full_refresh=False)
    # cdbt.pbuild(ctx=MockCtx(Command('Duck')), full_refresh=False)
    # cdbt.gbuild(ctx=mock_ctx, full_refresh=False, threads=8)
    cdbt.format(ctx=mock_ctx, select=None, all=True, main=False)
    sys.exit(0)
