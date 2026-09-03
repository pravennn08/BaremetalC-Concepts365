# Daily Backend Concepts

One backend-engineering study prompt is published automatically each day. My notes and implementations are added manually.

<!-- daily-concept-date: 2026-09-01 -->
<!-- daily-concept-index: 1 -->
## 2026-09-01 — Memory Layout of a C Program

**Core question:** What lives in text, data, bss, heap, and stack?

**Things to check:**

- Where are global variables stored?
- What happens to uninitialized static variables?
- How does stack frame layout work?
- How to inspect memory segments at runtime?

**Exercise:** Write a program that prints the addresses of a local variable, a global variable, a static variable, and a dynamically allocated pointer. Map these to their segments.

**My notes:**

-

<!-- daily-concept-date: 2026-09-02 -->
<!-- daily-concept-index: 2 -->
## 2026-09-02 — Idempotency

**Core question:** Can this operation be safely repeated?

**Things to check:**

- What happens when a request is retried?
- Where should the idempotency key be stored?
- How long should the result be retained?
- Can concurrent duplicate requests race?

**Exercise:** Design an idempotent POST /payments endpoint with in-memory key storage and proper mutex locking in C.

**My notes:**

-

<!-- daily-concept-date: 2026-09-03 -->
<!-- daily-concept-index: 3 -->
## 2026-09-03 — Pointer Arithmetic and Array Decay

**Core question:** How do arrays differ from pointers in practice?

**Things to check:**

- When does an array decay to a pointer?
- What is sizeof(array) vs sizeof(pointer)?
- How does pointer arithmetic handle different types?
- What are the pitfalls of multi-dimensional arrays?

**Exercise:** Implement a function that sums a 2D matrix using both array indexing and pointer arithmetic. Compare assembly output.

**My notes:**

-

<!-- daily-concept-date: 2026-09-04 -->
<!-- daily-concept-index: 4 -->
## 2026-09-04 — The Volatile Keyword

**Core question:** When should variables be marked volatile?

**Things to check:**

- How does volatile prevent compiler optimizations?
- When is volatile needed for memory-mapped I/O?
- Does volatile make variables atomic?
- Common misconceptions about volatile

**Exercise:** Write a busy-wait loop that polls a hardware register (simulated with a pointer). Show the difference with and without volatile using compiler explorer.

**My notes:**

- 
