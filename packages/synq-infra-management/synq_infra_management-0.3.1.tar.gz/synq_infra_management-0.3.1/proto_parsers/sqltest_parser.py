import re
from synq.datachecks.sqltests.v1.sql_tests_pb2 import SqlTest
from synq.entities.v1.annotation_pb2 import Annotation
from synq.platforms.v1.data_platforms_pb2 import (
    DataPlatformIdentifier,
    SnowflakeIdentifier,
)


class sqlTestParser:
    def __init__(self, local_tests, synq_tests) -> None:
        self.local_tests = local_tests
        self.synq_tests = synq_tests
        self.new_tests = []
        self.deleted_tests = []

    def find_new_tests(self):
        # Find new tests in local file.
        for synq_test in self.local_tests:
            for existing_test in self.synq_tests.sql_tests:
                if self.compare_tests(synq_test, existing_test):
                    self.new_tests.append(synq_test)
                    break
        return self.new_tests

    def find_deployed_tests(self):
        # Find deployed tests in Synq
        for existing_test in self.synq_tests.sql_tests:
            for synq_test in self.local_tests:
                if self.compare_tests(existing_test, synq_test):
                    self.deleted_tests.append(existing_test)
                    break
        return self.deleted_tests

    def compare_tests(self, test_to_check, existing_test):
        # Compare deployed tests and local tests.
        match_counter = 0
        if test_to_check.id == existing_test.id:
            match_counter += 1
        if test_to_check.sql_expression in existing_test.sql_expression.replace(
            "\n", " "
        ).replace("   ", " ").replace("  ", " "):
            match_counter += 1
        if test_to_check.recurrence_rule[-15:] == existing_test.recurrence_rule[-15:]:
            match_counter += 1
        if match_counter == 3:
            return False
        else:
            return True
