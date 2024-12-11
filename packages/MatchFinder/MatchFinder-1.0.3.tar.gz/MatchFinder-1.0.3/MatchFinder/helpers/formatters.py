import csv
from io import StringIO

from .calculations import find_matches


def get_similar(input_str, match_list, n=1, include_score=False,case_insensitive=False, output_format="text"):
    """
    Main function to get similar matches with the desired output format.

        args:
        :param input_str:(str) The input string to match.
        :param match_list:(list) The list of strings to search in.
        :param n:(int) Maximum number of matches to return.

        :param output_format: (str) Desired output format ("text" or "json")
        :param include_score:(bool) Whether to include similarity scores.
        :param case_insensitive:
    returns:
        list: Matches formatted as per the output_format.

    """
    if not all(isinstance(item, str) for item in match_list) or not isinstance(input_str,str):
        raise TypeError(
            "Oops! The input has some impostors that aren't strings. Check your input before it becomes self-aware!")
    if n <= 0:
        raise ValueError("n must be greater than 0")
    if case_insensitive:
        input_str = input_str.lower()
        match_list = [match.lower() for match in match_list]
    results = find_matches(input_str, match_list, n, include_score)

    if output_format == "text":
        if include_score:
            return [f"Match: {item['match']}, Score: {item['score']}" for item in results]
        else:
            return [f"Match: {item['match']}" for item in results]

    elif output_format == "json":
        return results
    elif output_format == "csv":
        if include_score:
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=["match", "score"])
            writer.writeheader()
            writer.writerows(results)
            return output.getvalue().strip()
        else:
            output = StringIO()
            csv.writer(output).writerow(["match"])
            csv.writer(output).writerows([[r['match']] for r in results])
            return output.getvalue().strip()


    else:
        raise ValueError("Invalid output_format. Choose 'text' or 'json'.")
