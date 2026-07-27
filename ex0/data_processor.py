#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   data_processor.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: mny-aro- <mny-aro-@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/07/26 01:13:25 by mny-aro-            #+#    #+#            #
#   Updated: 2026/07/27 22:03:33 by mny-aro-           ###   ########.fr      #
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
        if not isinstance(data, dict):
            return False
        if isinstance(data, dict):
            keys_ok = all(isinstance(k, str) for k in data.keys())
            values_ok = all(isinstance(v, str) for v in data.values())
            return keys_ok and values_ok
        elif isinstance(data, list) and all(isinstance(item, dict)
                        for item in data):
            return True
        else:
            return False

        


def main() -> None:
    pass

if __name__ == "__main__":
    main()
