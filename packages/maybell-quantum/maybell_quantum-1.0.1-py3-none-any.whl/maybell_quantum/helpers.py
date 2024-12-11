import logging

import matplotlib.pyplot


def plot(
    components: list[str],
    field: str,
    result: dict[str, dict[str, list[bool | str | float | int]]],
    saveas: str,
) -> None:
    """Plot query results for the given components.

    To plot temperature results for mxp and stp, for example, you'd pass:

    field = "temperature"
    components = ["mxp", "stp"]

    Args:
        components: name of the device components to plot, e.g. "mxp"
        field: the field/member of each component to plot.
        result: query result from fetch, fetch_all, or last.
        saveas: passed directly to matplotlib.pyplot.savefig(), so
                a good example would be: saveas="my_plot.png"

    Returns: None

    Raises: This function shouldn't throw.

    """

    for component_name in components:
        if component_name in result:
            if field in result[component_name]:
                matplotlib.pyplot.plot(
                    result[component_name][field], label=component_name
                )
            else:
                logging.error(f"field '{field}' isn't a member of '{component_name}'")
                logging.error(f"options are {result[component_name].keys()}")
        else:
            logging.error(f"component '{component_name}' doesn't exist in the result.")
            logging.error(f"options are {result.keys()}")

    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig(saveas)


def pretty_print_result(
    result: dict[str, dict[str, list[bool | str | float | int]]]
) -> None:
    """Print the result of a query to display the resulting structure.

    Args:
        result: query result from fetch, fetch_all, or last.

    Returns: None

    Raises: This function shouldn't throw.

    """
    for device_name, device_fields in result.items():
        print("{ '%s' : " % device_name)
        print("    {")
        for field, time_series_data in device_fields.items():
            print(
                "        '%s' = [%.2f, %.2f,..., %.2f, %.2f]"
                % (
                    field,
                    time_series_data[0],
                    time_series_data[1],
                    time_series_data[-2],
                    time_series_data[-1],
                )
            )
        print("    }")
        print("}")
