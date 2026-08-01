#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   data_pipeline.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: mny-aro- <mny-aro-@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/07/27 23:05:09 by mny-aro-            #+#    #+#            #
#   Updated: 2026/08/01 09:23:31 by mny-aro-           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import typing
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.rank: int = 0
        self.data: list[tuple[int, str]] = []
        self._name: str = "DataProcessor"
        self._total_processed: int = 0

    def count_rank(self) -> int:
        self.rank += 1
        return self.rank - 1

    @property
    def name(self) -> str:
        return self._name

    @property
    def total_processed(self) -> int:
        return self._total_processed

    @property
    def remaining(self) -> int:
        return len(self.data)

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
    def __init__(self) -> None:
        super().__init__()
        self._name = "Numeric Processor"

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
                self._total_processed += 1
        elif isinstance(data, (int, float)):
            rank = self.count_rank()
            value = str(data)
            self.data.append((rank, value))
            self._total_processed += 1


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
        self._name = "Text Processor"

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
                self._total_processed += 1
        elif isinstance(data, str):
            rank = self.count_rank()
            self.data.append((rank, data))
            self._total_processed += 1


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
        self._name = "Log Processor"

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
                self._total_processed += 1
        elif isinstance(data, dict):
            rank = self.count_rank()
            value = ": ".join(data.values())
            self.data.append((rank, value))
            self._total_processed += 1


class ExportPlugin(typing.Protocol):
    def process_output(
        self, data: list[tuple[int, str]]
    ) -> None:
        ...


class CSVExportPlugin:
    def process_output(
        self, data: list[tuple[int, str]]
    ) -> None:
        values = [value for _, value in data]
        print("CSV Output:")
        print(",".join(values))


class JSONExportPlugin:
    def process_output(
        self, data: list[tuple[int, str]]
    ) -> None:
        items: list[str] = []
        for rank, value in data:
            items.append(
                f'"item_{rank}": "{value}"'
            )
        json_str = "{" + ", ".join(items) + "}"
        print("JSON Output:")
        print(json_str)


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(
        self, proc: DataProcessor
    ) -> None:
        self._processors.append(proc)

    def process_stream(
        self, stream: list[typing.Any]
    ) -> None:
        for element in stream:
            processed = False
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    processed = True
                    break
            if not processed:
                print(
                    "DataStream error - Can't"
                    f" process element in stream:"
                    f" {element}"
                )

    def print_processors_stats(self) -> None:
        print("\n== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            print(
                f"{proc.name}: total"
                f" {proc.total_processed} items"
                f" processed, remaining"
                f" {proc.remaining} on processor"
            )

    def output_pipeline(
        self, nb: int, plugin: ExportPlugin
    ) -> None:
        for proc in self._processors:
            data: list[tuple[int, str]] = []
            for _ in range(nb):
                if proc.remaining == 0:
                    break
                data.append(proc.output())
            if data:
                plugin.process_output(data)


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")

    print("\nInitialize Data Stream...\n")
    ds = DataStream()
    ds.print_processors_stats()

    print("\nRegistering Processors\n")
    np = NumericProcessor()
    tp = TextProcessor()
    lp = LogProcessor()
    ds.register_processor(np)
    ds.register_processor(tp)
    ds.register_processor(lp)

    batch1: list[typing.Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": (
                    "Telnet access! Use ssh instead"
                ),
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected",
            },
        ],
        42,
        ["Hi", "five"],
    ]
    print(
        "Send first batch of data on stream:"
        f" {batch1}"
    )
    ds.process_stream(batch1)
    ds.print_processors_stats()

    csv_plugin = CSVExportPlugin()
    print(
        "\nSend 3 processed data from each"
        " processor to a CSV plugin:"
    )
    ds.output_pipeline(3, csv_plugin)
    ds.print_processors_stats()

    batch2: list[typing.Any] = [
        21,
        ["I love AI", "LLMs are wonderful",
         "Stay healthy"],
        [
            {
                "log_level": "ERROR",
                "log_message": "500 server crash",
            },
            {
                "log_level": "NOTICE",
                "log_message": (
                    "Certificate expires in 10 days"
                ),
            },
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"Send another batch of data: {batch2}")
    ds.process_stream(batch2)
    ds.print_processors_stats()

    json_plugin = JSONExportPlugin()
    print(
        "\nSend 5 processed data from each"
        " processor to a JSON plugin:"
    )
    ds.output_pipeline(5, json_plugin)
    ds.print_processors_stats()


if __name__ == "__main__":
    main()
