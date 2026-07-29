#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   data_processor.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: mny-aro- <mny-aro-@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/07/27 23:05:09 by mny-aro-            #+#    #+#            #
#   Updated: 2026/07/30 00:57:13 by mny-aro-           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import typing
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.rank: int = 0
        self.data: list[tuple[int, str]] = []

    def count_rank(self) -> int:
        self.rank += 1
        return self.rank - 1

    @abstractmethod
    def validate(self, data: typing.Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: typing.Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        collect = self.data.pop(0)
        return collect


class NumericProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, bool):
            return False
        if isinstance(data, list):
            is_int = all(
                not isinstance(element, bool)
                and isinstance(element, (int, float))
                for element in data
            )
            return is_int
        elif isinstance(data, (int, float)):
            return True
        else:
            return False

    def ingest(self, data: int | float
               | list[int | float]) -> None:
        if isinstance(data, bool):
            raise ValueError("Improper numeric data")
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                rank = self.count_rank()
                str_item = str(item)
                self.data.append((rank, str_item))
        elif isinstance(data, (int, float)):
            rank = self.count_rank()
            value = str(data)
            self.data.append((rank, value))


class TextProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, list):
            is_str_list = all(isinstance(element, str)
                              for element in data)
            return is_str_list
        elif isinstance(data, str):
            return True
        else:
            return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            for item in data:
                rank = self.count_rank()
                self.data.append((rank, item))
        elif isinstance(data, str):
            rank = self.count_rank()
            self.data.append((rank, data))


class LogProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        def is_valid_dict(d: typing.Any) -> bool:
            if not isinstance(d, dict):
                return False
            keys_ok = all(isinstance(k, str)
                          for k in d.keys())
            values_ok = all(isinstance(v, str)
                            for v in d.values())
            return keys_ok and values_ok

        if isinstance(data, list):
            return all(is_valid_dict(item)
                       for item in data)
        elif isinstance(data, dict):
            return is_valid_dict(data)
        else:
            return False

    def ingest(self, data: dict[str, str]
               | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        if isinstance(data, list):
            for item in data:
                rank = self.count_rank()
                value = ": ".join(item.values())
                self.data.append((rank, value))
        elif isinstance(data, dict):
            rank = self.count_rank()
            value = ": ".join(data.values())
            self.data.append((rank, value))


def main() -> None:
    print("=== Code Nexus - Data Processor ===")
    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()

    print("\nTesting Numeric Processor...")
    nbr: list[int | str] = [42, "Hello"]
    for test in nbr:
        print(f" Trying to validate input '{test}':"
              f" {numeric.validate(test)}")
    print(" Test invalid ingestion of string 'foo'"
          " without prior validation:")
    try:
        numeric.ingest("foo")
    except Exception as err:
        print(f" Got exception: {err}")
    valid_list: list[int | float] = [1, 2, 3, 4, 5]
    print(f" Processing data: {valid_list}")
    numeric.ingest(valid_list)
    to_extract1 = 3
    if to_extract1 == 1:
        print(f" Extracting {to_extract1} value...")
    else:
        print(f" Extracting {to_extract1} values...")
    for _ in range(to_extract1):
        rank, value = numeric.output()
        print(f" Numeric value {rank}: {value}")

    print("\nTesting Text Processor...")
    print(f" Trying to validate input '42':"
          f" {text.validate(42)}")
    text_data: list[str] = ["Hello", "Nexus", "World"]
    print(f" Processing data: {text_data}")
    text.ingest(text_data)
    to_extract2 = 1
    if to_extract2 == 1:
        print(f" Extracting {to_extract2} value...")
    else:
        print(f" Extracting {to_extract2} values...")
    for _ in range(to_extract2):
        rank, value = text.output()
        print(f" Text value {rank}: {value}")

    print("\nTesting Log Processor...")
    print(f" Trying to validate input 'Hello':"
          f" {log.validate('Hello')}")
    log_data: list[dict[str, str]] = [
        {
            "log_level": "NOTICE",
            "log_message": "Connection to server",
        },
        {
            "log_level": "ERROR",
            "log_message": "Unauthorized access!!",
        },
    ]
    print(f" Processing data: {log_data}")
    log.ingest(log_data)
    to_extract3 = 2
    if to_extract3 == 1:
        print(f" Extracting {to_extract3} value...")
    else:
        print(f" Extracting {to_extract3} values...")
    for _ in range(to_extract3):
        rank, value = log.output()
        print(f" Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
