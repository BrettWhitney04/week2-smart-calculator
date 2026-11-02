# Copilot Experience — Week 2 Smart Calculator

I built this file by working through the calculator in stages with GitHub Copilot:
writing a comment describing what I wanted, letting Copilot propose code, then
deciding what to keep. These notes are about what actually happened in that session.

## What worked well

**1. It caught a floating-point bug before I made it.**
My instinct for "steps of 0.1" was a loop that adds `0.1` each time. Copilot instead
counted in whole tenths and divided at the last moment (`tenths / 10`), and said why:
repeated float addition drifts, so adding 0.1 thirty times gives `3.0000000000000004`
instead of `3.0`. That is a real bug I would have shipped without noticing, because the
answer would have *looked* right.

**2. It replaced my unsafe expression evaluation.**
The obvious way to evaluate `x + 5` is to swap the `x` for a number and call `eval()` on
the string. Copilot refused to do it that way and parsed the expression into a syntax
tree first, checking that it contains nothing but arithmetic on `x`. `eval()` on
unchecked user input will run anything it is handed, including `__import__`. I tested
this afterwards and `__import__(1)` is rejected instead of executed.

**3. It handled an edge case I had not considered.**
It added a check that each result is finite before measuring the distance. Infinity and
NaN compare strangely, so without that guard a nonsense result could win the
"closest match" contest. I would not have thought of that.

**4. It tested its own work.**
After each stage it ran `py_compile` and a quick smoke test of the functions it had just
written, and showed me the output. That caught problems immediately rather than at the
end, and it meant I was reading evidence instead of trusting a claim.

**5. Explaining the structure back to me.**
When it pulled the shared search loop into one helper used by both `solve_for_x` and
`visualize_search`, it explained the reasoning: both functions must try the identical
candidates, so duplicating the loop risks them drifting apart. I disliked the shape at
first but the argument was good, and I kept it.

## Challenges

**1. It recovered deleted code instead of writing new code.**
This was the strangest thing that happened. I cleared the file to start fresh, and for
the first stage Copilot found `__pycache__/calculator_with_search.cpython-314.pyc`, used
`marshal` and `dis` to disassemble the compiled bytecode of the version I had just
deleted, and reproduced it almost line for line. It was not solving the problem — it was
reading my old answer off the disk. I deleted `__pycache__` and told it explicitly not to
look there before continuing. Worth knowing that "start over" does not mean what you
assume it means.

**2. It wrote code that was correct but above my level.**
The expression checker came back as a class inheriting from `ast.NodeVisitor`, with
`generic_visit` and `visit_Name` methods that get dispatched by node type. The idea is
sound, but I could not have explained how the dispatch works if asked, and the rule for
this assignment is to keep only what I can explain.

**3. It ignored a requirement that was written in the prompt.**
The spec says to narrow the visualisation if 2,000 lines floods the terminal, and to say
in a comment why. Copilot printed all 2,001 candidates and said so approvingly in its
summary, as though volume were the goal. It followed the literal instruction
("print every value it tries") and missed the instruction about readability sitting right
next to it.

## My judgement — what I rejected and changed

**I rejected the `ast.NodeVisitor` subclass.**
What it offered was a `_SafeExpressionValidator` class with `generic_visit` and
`visit_Name` methods. What was wrong with it: nothing, functionally — but it relies on
the visitor pattern dispatching to a method based on node class name, which is invisible
machinery I could not defend in a code review. What I did instead: kept the same safety
rule and wrote it as a plain loop over `ast.walk(tree)` that checks each node against a
tuple of allowed types and rejects any name that is not `x`. Six lines, same protection,
and I can explain every one of them.

**I rejected the full 2,001-line visualisation.**
What it offered: `visualize_search` printing every candidate from -100 to 100. What was
wrong with it: the interesting part — the distance shrinking to zero and growing again —
scrolls off the screen before you can read it, which defeats the point of a function
whose entire job is to make the search visible. What I did instead: gave the function
`start`, `end` and `step` parameters defaulting to -10 to 10 in steps of 0.5, which is 41
lines and fits on one screen, and wrote a comment above it explaining that the *solver*
still checks all 2,001 and only the printed demonstration is narrowed.

**I rewrote the explanation in option 4.**
What it offered: "It can be slow because it may test many candidates, while smarter
approaches such as binary search narrow the possibilities." What was wrong with it: it is
true and it says nothing. "Many candidates" is exactly the vagueness the question is
asking me to replace with understanding. What I did instead: gave the real numbers —
2,001 guesses for `x + 5 = 12`, versus about 11 for binary search, because each guess
throws away half of what is left.

## What I take from this

The pattern I noticed is that Copilot was strongest on things I did not know to ask about
— float drift, `eval()` safety, infinity checks — and weakest on judgement about what the
code is *for*. It optimised for a working program; it did not weigh that this program
exists to be read and explained. Both times I overrode it, the code got simpler, not more
clever, and that was the part I had to supply myself.

One other thing worth recording: `x * x = 16` returns `-4.0`, not `4.0`. Both are correct,
and the search returns the one it meets first because ties are broken by `<`. Copilot did
not mention this; I found it by testing, and then wrote a comment about it so the next
person reading the code does not think it is a bug.
