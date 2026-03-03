# Breaking Out of Nested Loops with Labels in JavaScript

When working with multiple loops, it is sometimes necessary to abort execution of an _outer_ loop from within an inner one. JavaScript provides a clean syntax for this using **loop labels**.

## Using a Label to Exit an Outer Loop

By assigning a label to a loop and referring to it in a `break` statement, you can jump out of the labelled loop directly.

```js
outer:
for (let i = 0; i < 5; i++) {
  for (let j = 0; j < 5; j++) {
    console.log(`i: ${i}, j: ${j}`);
    if (i === 3 && j === 3) {
      // exit the loop that is labelled "outer"
      break outer;
    }
  }
}
```

The `outer:` label can be placed on any loop level (for, while, do/while) and the `break` statement will terminate that specific loop regardless of how many levels deep you are.

## What I Used to Do Before Labels

Before discovering labels, I handled the same situation with a flag variable that I checked after each inner loop:

```js
let outerFlag = true;
for (let i = 0; i < 5 && outerFlag; i++) {
  if (!outerFlag) break;
  for (let j = 0; j < 5; j++) {
    console.log(`i: ${i}, j: ${j}`);
    if (i === 3 && j === 3) {
      outerFlag = false;
      break; // only exits the inner loop
    }
  }
}
```

This pattern works, but is more verbose and harder to read than using a labeled `break`.

## Notes

- Labels are a part of the ECMAScript specification and work in all modern browsers and Node.js.
- They are not limited to a single level; you can give different labels to nested loops to control exactly which loop you want to exit.
- While useful, overusing labels can make code harder to follow. Use them judiciously in situations where breaking out of multiple nested loops is the clearest solution.

> Even after years as a backend developer, revisiting these fundamental language features can be eye-opening. Writing clean, idiomatic code often means mastering the basics.

---
