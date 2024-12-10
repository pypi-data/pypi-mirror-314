from typing import Callable, List, Dict, Optional
from algo_provider.utils.parser import extract_algorithm_metadata
from algo_provider.models.algorithm import Algorithm
from algo_provider.app import start_api_server
from rich.console import Console
from rich.panel import Panel


class AlgoProvider:
    def __init__(self):
        self.algorithms: Dict[str, Algorithm] = {}
        self.algorithms_functions: Dict[str, Callable] = {}

    def add_algo(
        self,
        func: Callable,
        tags: List[str] = [],
        author: Optional[str] = None,
        version: Optional[str] = None,
        creation_date: Optional[str] = None,
        update_date: Optional[str] = None,
    ) -> Algorithm:
        """
        Adds an algorithm to the provider.

        Parameters:
            func (Callable): The function to add as an algorithm.
            tags (List[str]): The tags of the algorithm.
            version (Optional[str]): The version of the algorithm.
            creation_date (Optional[str]): The creation date of the algorithm.
            update_date (Optional[str]): The update date of the algorithm.

        Returns:
            Algorithm: The algorithm object.
        """
        algo_metadata = extract_algorithm_metadata(func)

        algorithm = Algorithm(
            **algo_metadata,
            tags=tags,
            author=author,
            version=version,
            creationDate=creation_date,
            updateDate=update_date,
        )

        self.algorithms[algorithm.id] = algorithm
        self.algorithms_functions[algorithm.id] = func
        return algorithm

    def get_algorithms(self) -> List[Algorithm]:
        return list(self.algorithms.values())

    def run_algorithm(self, algorithm_id: str, inputs: Dict):
        # Verify if the algorithm exists
        if algorithm_id not in self.algorithms:
            raise ValueError(f"Algorithm '{algorithm_id}' not found.")

        # Inputs Example:
        # {
        #     "inputs": [
        #         {"name": "input1", "value": 12},
        #         {"name": "input2", "value": 22},
        #     ],
        # }

        # Transform this to a dictionary {input_name: input_value}
        inputs = {input["name"]: input["value"] for input in inputs["inputs"]}

        # Call the algorithm function
        try:
            function = self.algorithms_functions[algorithm_id]
            result = function(**inputs)
        except Exception as e:
            # Print the error message
            error_message = f"[bold red]Error running algorithm \
 '{algorithm_id}':\n{str(e)}[/bold red]"
            console = Console()
            console.print(
                Panel(
                    error_message,
                    title="[bold red]Error[/bold red]",
                    width=80,
                    border_style="bold",
                    style="red",
                )
            )

            # Raise the error
            raise ValueError(str(e))

        # Return the result
        return [{"name": "result", "value": result}]

    def start_server(self, host="0.0.0.0", port=8000):
        # Print the server information
        console = Console()
        console.print(
            Panel(
                "The Easy Algorithm Provider is being started..."
                + f"\n\n[bold]API Server[/bold]: http://{host}:{port}"
                + f"\n[bold]Number of Algorithms[/bold]: {len(self.get_algorithms())}",
                title="Easy Algorithm Provider",
                width=80,
                border_style="bold",
            )
        )

        # Print the creation message of each algorithm
        for algorithm in self.get_algorithms():
            algorithm.print_table()

        start_api_server(self, host, port)
