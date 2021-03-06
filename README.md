# Operating-Time-Deltas

The following module measures the exact number of seconds between two points in time less the number of seconds that a business is not in operation.
This allows a company to determine the exact about of time certain items in its workflow had been pending during which there were individuals able to work on said task and therefore and calculate the associated turn around time on these items.

The basic formula for determine the number of operating seconds, O<sub>s</sub>, between T<sub>1</sub> and T<sub>2</sub> can be expressed as:

> O<sub>s</sub> = (T<sub>2</sub> - T<sub>1</sub>) - W(T<sub>1</sub>, T<sub>2</sub>) - H(T<sub>1</sub>, T<sub>2</sub>) - N(T<sub>1</sub>, T<sub>2</sub>)

Where W(T<sub>1</sub>, T<sub>2</sub>) represents the number of weekend elapsed seconds between the two points in time, H(T<sub>1</sub>, T<sub>2</sub>) represents the number of holiday based seconds between the two points in time, and N(T<sub>1</sub>, T<sub>2</sub>) represents the number of non-operation hours that occur on normal days of business. For example, the time spans of [12am - 9am) and [5pm - 12am) if the business is operating [9am - 5pm).

This module was made to be as flexible as possible and allows the user to set his or her own holidays when calculating total amount of business time elapsed. It takes advantage of some of the core functionality of `Pandas` and its timeseries modules in order to perform most of the computation.

