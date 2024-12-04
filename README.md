# AdventOfCode2024
 
## Development Environment
```
uv venv --python 3.12
.venv\Scripts\activate
```

## Day 1 Notes
I felt pretty confident with my solution for both parts of the problem. In part one you simply need to 
parse the input into two lists and sort them. Then you can iterate through the lists and find the
distance. The second part was similar, but instead you create a dictionary with the occurrences of each
number in the right list. The small trick is to use `defaultdict` so you default to 0 if the key is not
found.

## Day 2 Notes
I must admit, the second part of this problem took me way longer than I like to admit. I must have tried
for an hour and a half trying to account for all the tiny details and edge cases. 
I finally realized the simple solution was the best one. Simply try omitting 1 level at a time from
a report until you either find that it is safe (using my solution from part 1). If you do not
find a solution, then the report is not safe. This does have a big O of N*N since in the worst case
you have to omit all the levels, but it is a simple solution that works and it MUCH less complicated
to implement and understand. Sometimes code that is readable is worth it.

## Day 3 Notes
Regular Expressions to the rescue! The first part was very easy with the proper regular expression.
The second part was a bit more tricky, but I figured it out in the end by keeping track of 
the indices in the string where `do()` and `don't()` were found. Once I have the indices,
I can then cut up the string into "enabled" strings where I can calculate the sum of the products.
I don't love the solution as it requires a few for loops, but it works.

## Day 4 Notes
I feel like today's puzzle was just mean. I was able to do the first part by breaking the puzzle into
a 2d array of characters. I would then iterate through the rows and look for the string `XMAS`.
The trick for part one was doing 8 transformations to the array to check for the string in all directions.
I used numpy to make the transformations more efficient. For the second part, I realized my method would be
rather tedious and it would be better to have a sliding window of 3x3 across the grid to find all occurrences
of "X-MAS". Unfortunately, I ran out of time today, so I took a solution from the [subreddit by the user
nik282000](https://www.reddit.com/r/adventofcode/comments/1h689qf/comment/m0cf7je/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button).
I adapted slightly to fit my style, but I can't take credit for the solution.