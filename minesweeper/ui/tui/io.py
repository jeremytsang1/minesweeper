class IO():
    OUT_OF_RANGE_MESSAGE = (
        "\nPlease enter an int in the interval"
        "[{} (inclusive) ... {} (exclusive)]"
    )

    @staticmethod
    def read_int(msg, min_val, max_val):
        """Display a prompt message to the user and get input within a given
        range.

        Keeps prompting user for input until user submits a valid integer in
        range.

        Parameters
        ----------
        msg: str
            Message to display to user.
        min_val: int
            Smallest value (inclusive) to allow user to enter.
        max_val: int
            Largest value (exclusive)_ to allow user to enter.

        Returns
        -------
        int
            User input as an int.

        """
        usr_input = None
        while usr_input is None:
            try:
                usr_input = int(input(msg))
                usr_input = IO._validate_range(usr_input, min_val, max_val)
            except ValueError:
                print("\nPlease enter an integer!")
                usr_input = None
        return usr_input

    @staticmethod
    def _validate_range(val, min_val, max_val):
        """Checks if a value is in a given range.

        In addition, prints a message if the value is not within range.

        Parameters
        ----------
        val: int
            Value to check.
        min_val: int
            Lower bound (inclusive) of the allowed range.
        max_val: int
            Upper bound (exclusive) of the allowed range.

        Returns
        -------
        int or None
            Returns the value if it is within range otherwise returns None.
        """
        if val in range(min_val, max_val):
            return val
        else:
            print(IO.OUT_OF_RANGE_MESSAGE.format(min_val, max_val))
            return None
