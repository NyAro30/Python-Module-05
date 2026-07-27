#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   data_processor.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: mny-aro- <mny-aro-@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/07/27 23:05:09 by mny-aro-            #+#    #+#            #
#   Updated: 2026/07/28 01:07:12 by mny-aro-           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import typing
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    def __init__(self):
        self.rank = 0
        self.data : list[tuple[int, str]] = []


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
        if isinstance(data, list):
            is_int = all(isinstance(element, (int, float))
                         for element in data)
            return is_int
        elif isinstance(data, (int, float)):
            return True
        else:
            return False

    def ingest(self, data: int | float |
               list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                rank = self.count_rank()
                item = str(item)
                self.data.append((rank, item))
        elif isinstance(data, (int, float)):
            rank = self.count_rank()
            value = str(data)
            self.data.append((rank, value))                


class TextProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, list):
            is_int = all(isinstance(element, str)
                for element in data)
            return is_int
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
        elif isinstance(data,dict):
            return is_valid_dict(data)
        else:
            return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        if isinstance(data, list):
            for item in data:
                rank = self.count_rank()
                value = f"{item['log_level']}: {item['log_message']}"
                self.data.append((rank, value))
        elif isinstance(data, dict):
            rank = self.count_rank()
            value = f"{data['log_level']}: {data['log_message']}"
            self.data.append((rank, value))


def main() -> None:
    pass

if __name__ == "__main__":
    main()
