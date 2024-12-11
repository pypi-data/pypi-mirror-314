from datetime import datetime

import yaml, glob, os
import synq.datachecks.sqltests.v1.sql_tests_service_pb2 as sql_tests_service_pb2

from synq.datachecks.sqltests.v1.sql_tests_pb2 import SqlTest
from synq.entities.v1.annotation_pb2 import Annotation
from synq.platforms.v1.data_platforms_pb2 import (
    DataPlatformIdentifier,
    SnowflakeIdentifier,
)


class SqlTestManager:
    def __init__(self, test_def_file_or_directory, *yaml_files_or_directory) -> None:
        self.test_def_file_or_directory = test_def_file_or_directory

        if os.path.isdir(self.test_def_file_or_directory):
            test_def_file = os.path.join(
                self.test_def_file_or_directory, "tests_def.yaml"
            )
            if not os.path.exists(test_def_file):
                raise FileNotFoundError(
                    f"Test definitions file 'tests_def.yaml' not found in {self.test_def_file_or_directory}"
                )
        else:
            test_def_file = self.test_def_file_or_directory

        self.test_definitions = self.open_yaml(test_def_file)

        self.sql_tests = self.load_sql_tests()

    def load_sql_tests(self):
        if os.path.isdir(self.test_def_file_or_directory):
            yaml_files = glob.glob(
                os.path.join(self.test_def_file_or_directory, "*_data.yaml")
            )
        else:
            yaml_files = self.test_def_file_or_directory

        sql_tests = []
        for file_path in yaml_files:
            sql_tests.extend(self.open_yaml(file_path))
        return sql_tests

    @staticmethod
    def open_yaml(file_path):
        with open(file_path, "r") as file:
            return yaml.safe_load(file) or []

    @staticmethod
    def set_recurrence_rule(schedule=None):
        """
        Configures the recurrence rule for the given schedule.
        Defaults to 'daily at midnight' if schedule is missing or invalid.
        Supports:
        - 'hourly'
        - 'daily'
        - Specific times like '2pm', '9am', etc.
        """
        base_date = "20240101"

        if not schedule:
            return f"DTSTART:{base_date}T000000Z\nRRULE:FREQ=DAILY"

        schedule = schedule.strip().lower()

        if schedule == "hourly":
            return f"DTSTART:{base_date}T000000Z\nRRULE:FREQ=HOURLY"

        try:
            if schedule.endswith("am") or schedule.endswith("pm"):
                hour = datetime.strptime(schedule, "%I%p").strftime("%H")
                return f"DTSTART:{base_date}T{hour}0000Z\nRRULE:FREQ=DAILY"
            else:
                raise ValueError(f"Invalid schedule format: {schedule}")
        except ValueError as e:
            return f"DTSTART:{base_date}T000000Z\nRRULE:FREQ=DAILY"

    def generate_sql(self, test_name, column, table, schema, database, values=None):
        fully_qualified_table = f"{database}.{schema}.{table}"

        for test in self.test_definitions:
            if test["id"] == test_name:
                sql = test["sql"].replace("{.Column}", column)
                sql = sql.replace("{.Table}", fully_qualified_table)

                for item in self.sql_tests:
                    if "columns" in item:
                        for col in item["columns"]:
                            if col["name"] == column:
                                where_a = col.get("where_a")
                                where_b = col.get("where_b")

                                if where_a is not None:
                                    sql = sql.replace("{.WhereA}", str(where_a))
                                if where_b is not None:
                                    sql = sql.replace("{.WhereB}", str(where_b))
                                break

                if values:
                    sql = sql.replace("{.Values}", values)

                return sql

    def get_annotations_sql_tests_def(self, test_name):
        # Get tagging from tests_def.yaml and apply to SQL Tests.
        for test in self.test_definitions:
            if test["id"] == test_name:
                annotation_type = Annotation(
                    name="synq.sqltest.type",
                    values=[test["tags"].get("type", "default_type")],
                )
        return [annotation_type]

    def get_annotations_core(
        self,
        organisation,
        product_name,
        database,
        schema,
        table,
        column,
        test_name,
        id,
        tag,
        dynamic_tags,
    ):
        # Get tagging from the source, apply tags for engine, account and database
        for tagging in self.sql_tests:
            if (
                product_name
                + "."
                + database
                + "."
                + schema
                + "."
                + table
                + "."
                + column
                + "."
                + test_name
                == id
            ):
                try:
                    value_tag = Annotation(
                        name="synq.sqltest." + tag,
                        values=[tagging["tags"].get(tag, dynamic_tags.get(tag))],
                    )
                except KeyError as e:
                    raise Exception(
                        f"Tag '{tag}' not found in the tagging dictionary: {e}\n### Every tag needs to be filled ###"
                    )
                except TypeError as e:
                    raise Exception(
                        f"Tag '{tag}' not found in the tagging dictionary: {e}\n### Read the documentation and make sure all tags are defined ###"
                    )

        return [value_tag]

    def get_annotations_tags(
        self,
        product_name,
        database,
        schema,
        table,
        column,
        test_name,
        id,
        tag,
        test_tag,
    ):
        # Get tags from the TAG section of core_data.yaml file.
        for tagging in self.sql_tests:
            if (
                product_name
                + "."
                + database
                + "."
                + schema
                + "."
                + table
                + "."
                + column
                + "."
                + test_name
                == id
            ):
                try:
                    value_tag = Annotation(
                        name="synq.sqltest." + tag,
                        values=[str(test_tag)],
                    )
                except KeyError as e:
                    raise Exception(
                        f"Tag '{tag}' not found in the tagging dictionary: {e}\n### Every tag needs to be filled ###"
                    )
                except TypeError as e:
                    raise Exception(
                        f"Tag '{tag}' not found in the tagging dictionary: {e}\n### Read the documentation and make sure all tags are defined ###"
                    )
        return [value_tag]

    @staticmethod
    def get_test_values(test_name, engine="snowflake"):
        try:
            for test_statement, values in test_name.items():
                test_name = test_statement
                for check, value in values.items():
                    test_values = value
        except:
            test_values = None
        return test_name, test_values, engine

    @staticmethod
    def get_test_id(product_name, database, schema, table, column, test_name):
        # Build the ID from table, coluns and test_name provided.
        return (
            product_name
            + "."
            + database
            + "."
            + schema
            + "."
            + table
            + "."
            + column
            + "."
            + test_name
        )

    @staticmethod
    def get_test_name(product_name, database, schema, table, column, test_name):
        # Build the final SQL Test name
        return (
            "API - "
            + product_name
            + "."
            + database
            + "."
            + schema
            + "."
            + table
            + "."
            + column
            + "."
            + test_name
        )

    def create_sql_class(self, tagging=None):
        # Main function, used to parse the local tests stored in YAML files.
        final_tests = []
        if tagging is None:
            tagging = ["owner", "product", "environment", "pagerduty_service"]
        for test_object in self.sql_tests:
            if "account" not in test_object or "database" not in test_object:
                print(
                    f"Skipping test due to missing 'account' or 'database': {test_object}"
                )
                continue
            database = SnowflakeIdentifier(
                account=test_object["account"], database=test_object["database"]
            )
            platform = DataPlatformIdentifier(snowflake=database)
            table = test_object["table"]
            schedule = test_object.get("schedule", "daily")
            schema = test_object["schema"]
            product_name = test_object["tags"]["product"]
            for testable_column in test_object["columns"]:
                for test_name in testable_column["tests"]:
                    test_name, test_values, engine = self.get_test_values(test_name)
                    sql_test = SqlTest()
                    sql_test.platform.CopyFrom(platform)

                    sql_test.id = self.get_test_id(
                        product_name,
                        database.database,
                        schema,
                        table,
                        testable_column["name"],
                        test_name,
                    )

                    sql_test.name = self.get_test_name(
                        product_name,
                        database.database,
                        schema,
                        table,
                        testable_column["name"],
                        test_name,
                    )

                    sql_test.sql_expression = self.generate_sql(
                        test_name,
                        testable_column["name"],
                        table,
                        schema,
                        database.database,
                        test_values,
                    )

                    sql_test.recurrence_rule = self.set_recurrence_rule(schedule)
                    annotations_def = self.get_annotations_sql_tests_def(test_name)
                    sql_test.annotations.extend(annotations_def)

                    organisation = os.getenv("ORGANISATION")
                    dynamic_tags = {
                        "organisation": organisation,
                        "platform": engine,
                        "account": database.account,
                        "database": database.database,
                        "schema": schema,
                        "table": table,
                    }

                    for tag in dynamic_tags:
                        sql_test.annotations.extend(
                            self.get_annotations_core(
                                organisation,
                                product_name,
                                database.database,
                                schema,
                                table,
                                testable_column["name"],
                                test_name,
                                sql_test.id,
                                tag.lower(),
                                dynamic_tags=dynamic_tags,
                            )
                        )

                    for tag in tagging:
                        if tag == "pagerduty_service":
                            test_tag_value = test_object["tags"].get(tag, "false")
                        else:
                            if tag not in test_object["tags"]:
                                raise KeyError(
                                    f"Tag '{tag}' is missing in the YAML file"
                                )
                            test_tag_value = test_object["tags"][tag]

                        if isinstance(test_tag_value, bool):
                            test_tag_value = str(test_tag_value).lower()
                        elif isinstance(test_tag_value, str):
                            test_tag_value = test_tag_value.lower()

                        sql_test.annotations.extend(
                            self.get_annotations_tags(
                                product_name,
                                database.database,
                                schema,
                                table,
                                testable_column["name"],
                                test_name,
                                sql_test.id,
                                tag.lower(),
                                test_tag_value,
                            )
                        )

                    sql_test.save_failures = True
                    final_tests.append(sql_test)
        return final_tests

    def compare_and_update_tests(yaml_items, deployed_items):
        # Compare local tests with already deployed tests.
        tests_to_update = []
        for yaml_test in yaml_items:
            yaml_test_id = yaml_test.id

            deployed_test = next(
                (test for test in deployed_items if test.id == yaml_test_id), None
            )
            if deployed_test:
                yaml_schedule = yaml_test.recurrence_rule
                deployed_schedule = deployed_test.recurrence_rule

                yaml_tags = {
                    annotation.name: annotation.values
                    for annotation in yaml_test.annotations
                }

                deployed_tags = {
                    annotation.name: annotation.values
                    for annotation in deployed_test.annotations
                }

                if (
                    yaml_test.sql_expression != deployed_test.sql_expression
                    or yaml_tags != deployed_tags
                    or yaml_schedule != deployed_schedule
                ):
                    tests_to_update.append(yaml_test)

        return tests_to_update

    def get_tests_to_deploy_and_delete(parser, accounts):
        # Filter SQL tests to deploy or delete, searches for anything different between the local file and the deployed tests
        if isinstance(accounts, str):
            accounts = [accounts]

        yaml_items = parser.find_new_tests()
        yaml_account_ids = {item.platform.snowflake.account for item in yaml_items}
        invalid_accounts = yaml_account_ids - set(accounts)

        if invalid_accounts:
            raise ValueError(
                f"Account ID mismatch detected. The YAML file contains accounts that do not match the expected accounts: {accounts}. Found in YAML: {invalid_accounts}"
            )

        yaml_items_filtered = [
            item for item in yaml_items if item.platform.snowflake.account in accounts
        ]
        yaml_test_ids = {item.id for item in yaml_items_filtered}

        deployed_items = [
            item
            for item in parser.find_deployed_tests()
            if item.platform.snowflake.account in accounts
        ]

        deployed_test_ids = {item.id for item in deployed_items}

        tests_to_deploy = [
            test for test in yaml_items_filtered if test.id not in deployed_test_ids
        ]
        tests_to_delete = [
            test_id for test_id in deployed_test_ids if test_id not in yaml_test_ids
        ]

        tests_to_update = SqlTestManager.compare_and_update_tests(
            yaml_items, deployed_items
        )

        tests_to_deploy.extend(tests_to_update)

        return tests_to_deploy, tests_to_delete

    def deploy_tests(stub, tests_to_deploy):
        # Function to update or add SQL Tests into Synq
        response = stub.BatchUpsertSqlTests(
            sql_tests_service_pb2.BatchUpsertSqlTestsRequest(sql_tests=tests_to_deploy)
        )
        # checks for any inconsistencies when applying.
        if "failed to get input tables" in str(response):
            print(f"Error occurred during deployment: {response}")
            raise SystemExit(1)
        elif "rpc error:" in str(response):
            print(f"Error occurred during deployment: {response}")
            raise SystemExit(1)

    def delete_tests(stub, tests_to_delete):
        # Function to delete SQL Tests in Synq.
        delete_response = stub.BatchDeleteSqlTests(
            sql_tests_service_pb2.BatchDeleteSqlTestsRequest(ids=tests_to_delete)
        )
        if "rpc error:" in str(delete_response):
            print(f"Error occurred during the delete: {delete_response}")
            raise SystemExit(1)

    def plan(tests_to_deploy, tests_to_delete, response):
        changes = {}
        additions_count = 0
        updates_count = 0
        deletions_count = len(tests_to_delete)
        YELLOW = "\033[93m"
        GREEN = "\033[92m"
        RED = "\033[91m"
        BOLD = "\033[1m"
        END = "\033[0m"

        if tests_to_deploy:
            for test in tests_to_deploy:
                existing_tests = [t for t in response.sql_tests if t.id == test.id]
                if len(existing_tests) > 0:
                    existing_test = existing_tests[0]
                    updates = []

                    if test.sql_expression != existing_test.sql_expression:
                        updates.append(
                            f"  {YELLOW} ~ [WARNING] {END}{BOLD}SQL expression will be updated.{END} \n"
                            f"     SQL Expression = {existing_test.sql_expression} {YELLOW} --> {END} {test.sql_expression}"
                        )

                    if test.recurrence_rule != existing_test.recurrence_rule:

                        def extract_schedule_details(rule):
                            freq = rule.split("\n")[1].split("FREQ=")[-1]
                            dtstart = rule.split("\n")[0].split("DTSTART:")[-1]
                            time = dtstart.split("T")[-1][:4]
                            formatted_time = f"{int(time[:2]) % 12 or 12}{'am' if int(time[:2]) < 12 else 'pm'}"
                            return f"{freq} - {formatted_time}"

                        updates.append(
                            f"  {YELLOW} ~ [WARNING] {END}{BOLD}Recurrence rule will be updated.{END} \n"
                            f"     Schedule = {extract_schedule_details(existing_test.recurrence_rule)} "
                            f"{YELLOW} --> {END} {extract_schedule_details(test.recurrence_rule)}"
                        )

                    yaml_tags = {a.name: a.values for a in test.annotations}

                    deployed_tags = {
                        a.name: a.values for a in existing_test.annotations
                    }
                    if yaml_tags != deployed_tags:
                        tag_updates = []
                        for key in yaml_tags:
                            if yaml_tags[key] != deployed_tags.get(key):
                                deployed_value = deployed_tags.get(key, [])
                                deployed_value_str = (
                                    deployed_value[-1] if deployed_value else "None"
                                )
                                tag_updates.append(
                                    f"     {key} = {deployed_value_str} {YELLOW} --> {END} {yaml_tags[key][-1]}"
                                )
                        updates.append(
                            f"  {YELLOW} ~ [WARNING] {END}{BOLD}Tags will be updated.{END} \n"
                            + "\n".join(tag_updates)
                        )

                    if updates:
                        changes[test.id] = updates
                        updates_count += 1
                else:
                    additions_count += 1
                    changes[test.id] = [
                        f"  {GREEN} + {END} Will be added. \n SQL Expression = {test.sql_expression} \n "
                        f"Tags: \n"
                        f"{''.join(f'  {x.name}: {x.values[-1]}\n' for x in test.annotations)}"
                        f"Schedule = {test.recurrence_rule.split('\n')[1].split('FREQ=')[-1]}"
                    ]

        if tests_to_delete:
            changes[""] = [
                f"{BOLD} {test_id} {END} \n {RED} - [WARNING] {END}Will be deleted"
                for test_id in tests_to_delete
            ]

        if not tests_to_deploy and not tests_to_delete:
            print("No changes to make. Everything is up-to-date.")
        else:
            for test_id, updates in changes.items():
                print(f"\n {BOLD}{test_id}{END}")
                for update in updates:
                    print(update)

        print(f"\n{BOLD}Plan Summary:{END}")
        print(f"{GREEN}+ {additions_count} to add{END}")
        print(f"{YELLOW}~ {updates_count} to update{END}")
        print(f"{RED}- {deletions_count} to delete{END}")

        return changes

    def apply(stub, tests_to_deploy, tests_to_delete, response):
        changes = {}
        additions_count = 0
        updates_count = 0
        deletions_count = len(tests_to_delete)

        YELLOW = "\033[93m"
        GREEN = "\033[92m"
        RED = "\033[91m"
        BOLD = "\033[1m"
        END = "\033[0m"

        if tests_to_deploy:
            for test in tests_to_deploy:
                existing_tests = [t for t in response.sql_tests if t.id == test.id]
                if len(existing_tests) > 0:
                    existing_test = existing_tests[0]
                    updates = []

                    if test.sql_expression != existing_test.sql_expression:
                        updates.append(
                            f"  {YELLOW} ~ {END} {BOLD}SQL expression updated.{END} \n"
                            f"     SQL Expression = {existing_test.sql_expression} {YELLOW} --> {END} {test.sql_expression}"
                        )

                    if test.recurrence_rule != existing_test.recurrence_rule:

                        def extract_schedule_details(rule):
                            freq = rule.split("\n")[1].split("FREQ=")[-1]
                            dtstart = rule.split("\n")[0].split("DTSTART:")[-1]
                            time = dtstart.split("T")[-1][:4]
                            formatted_time = f"{int(time[:2]) % 12 or 12}{'am' if int(time[:2]) < 12 else 'pm'}"
                            return f"{freq} - {formatted_time}"

                        updates.append(
                            f"  {YELLOW} ~ {END} {BOLD}Recurrence updated.{END} \n"
                            f"     Schedule = {extract_schedule_details(existing_test.recurrence_rule)} "
                            f"{YELLOW} --> {END} {extract_schedule_details(test.recurrence_rule)}"
                        )

                    yaml_tags = {a.name: a.values for a in test.annotations}
                    deployed_tags = {
                        a.name: a.values for a in existing_test.annotations
                    }

                    if yaml_tags != deployed_tags:
                        tag_updates = []
                        for key in yaml_tags:
                            if yaml_tags[key] != deployed_tags.get(key):
                                deployed_value = deployed_tags.get(key, [])
                                deployed_value_str = (
                                    deployed_value[-1] if deployed_value else "None"
                                )
                                tag_updates.append(
                                    f"     {key} = {deployed_value_str} {YELLOW} --> {END} {yaml_tags[key][-1]}"
                                )
                        updates.append(
                            f"  {YELLOW} ~ [WARNING] {END}{BOLD}Tag updated.{END} \n"
                            + "\n".join(tag_updates)
                        )

                    if updates:
                        changes[test.id] = updates
                        updates_count += 1
                else:
                    additions_count += 1
                    changes[test.id] = [
                        f"  {GREEN} + {END} Test added. \n SQL Expression = {test.sql_expression} \n "
                        f"Tags: \n"
                        f"{''.join(f'  {x.name}: {x.values[-1]}\n' for x in test.annotations)}"
                        f"Schedule = {test.recurrence_rule.split('\n')[1].split('FREQ=')[-1]}"
                    ]

            # Deploy the tests
            print(f"{BOLD}Applying changes...{END}")
            SqlTestManager.deploy_tests(stub, tests_to_deploy)

        if tests_to_delete:
            changes[""] = [
                f"{BOLD} {test_id} {END} \n {RED} - {END} Test deleted \n"
                for test_id in tests_to_delete
            ]
            # Delete the tests
            print(f"{BOLD}Deleting tests...{END}\n")
            SqlTestManager.delete_tests(stub, tests_to_delete)

        if not tests_to_deploy and not tests_to_delete:
            print("No changes to make. Everything is up-to-date.")
        else:
            for test_id, updates in changes.items():
                print(f"\n {BOLD}{test_id}{END}")
                for update in updates:
                    print(update)

        print(f"\n{BOLD}Apply complete!{END}")
        print(f"\n{BOLD}Apply Summary:{END}")
        print(f"{GREEN}+ {additions_count} added{END}")
        print(f"{YELLOW}~ {updates_count} updated{END}")
        print(f"{RED}- {deletions_count} deleted{END}")
