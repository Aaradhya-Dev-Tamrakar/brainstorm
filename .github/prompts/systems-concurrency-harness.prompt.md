---
description: ">-"
---

# Systems Programming & Concurrency Harness (`systems-concurrency-harness`)

Derived from **CT 612 (Operating System)**, **CT 401 (Computer Programming in C)**, and **CT 725 06 (Advanced Operating Systems)** in the BE ECIE curriculum.

This skill equips agents to design thread-safe concurrent systems, audit shared memory accesses for data races, evaluate deadlock susceptibility under the Coffman conditions, and scaffold robust multi-threaded producer-consumer queues.

---

## 1. Operating Rules & Concurrency Principles

1. **Eliminate Data Races:** Any mutable state accessed by more than one execution context (thread, ISR, process) must be protected by explicit synchronization primitives (mutex, critical section, spinlock) or atomic operations.
2. **Coffman Deadlock Prevention:**
   A system can deadlock if and only if all four Coffman conditions hold simultaneously:
   - *Mutual Exclusion:* Resources cannot be shared.
   - *Hold and Wait:* Processes hold resources while waiting for others.
   - *No Preemption:* Resources cannot be forcibly revoked.
   - *Circular Wait:* A closed chain of processes each waits for a resource held by the next.
   *Prevention Strategy:* Enforce a strict global lock hierarchy / acquisition order to eliminate Circular Wait.
3. **Lock Scope Minimization:** Hold locks only for the exact duration of critical state manipulation. Never perform I/O, network calls, or long sleeps while holding a lock.
4. **ISR / Thread Boundary Safety:** Interrupt Service Routines (ISRs) must never call blocking synchronization primitives (`wait()`, `mutex_lock()`). Use lock-free single-producer single-consumer (SPSC) ring buffers or non-blocking event flags.

---

## 2. Core Capabilities & Workflows

### Capability A: Banker's Deadlock Avoidance Validator
Model and verify whether a multi-process resource allocation state is safe:

```python
def is_safe_state(available, max_claim, allocation):
    """
    Banker's Algorithm Safety Check.
    Returns True if system is in a provably safe state, False otherwise.
    """
    num_processes = len(allocation)
    num_resources = len(available)
    work = list(available)
    finish = [False] * num_processes
    need = [[max_claim[p][r] - allocation[p][r] for r in range(num_resources)] for p in range(num_processes)]

    while True:
        found = False
        for p in range(num_processes):
            if not finish[p] and all(need[p][r] <= work[r] for r in range(num_resources)):
                for r in range(num_resources):
                    work[r] += allocation[p][r]
                finish[p] = True
                found = True
                break
        if not found:
            break

    return all(finish)
```

### Capability B: Thread-Safe Bounded Ring Buffer Scaffold (C/C++ Pattern)
```c
#include <pthread.h>
#include <stdbool.h>
#include <stddef.h>

#define RING_BUF_SIZE 64

typedef struct {
    uint8_t buffer[RING_BUF_SIZE];
    size_t head;
    size_t tail;
    size_t count;
    pthread_mutex_t lock;
    pthread_cond_t not_full;
    pthread_cond_t not_empty;
} BoundedQueue;

void queue_init(BoundedQueue *q) {
    q->head = 0;
    q->tail = 0;
    q->count = 0;
    pthread_mutex_init(&q->lock, NULL);
    pthread_cond_init(&q->not_full, NULL);
    pthread_cond_init(&q->not_empty, NULL);
}

void queue_push(BoundedQueue *q, uint8_t byte) {
    pthread_mutex_lock(&q->lock);
    while (q->count == RING_BUF_SIZE) {
        pthread_cond_wait(&q->not_full, &q->lock);
    }
    q->buffer[q->tail] = byte;
    q->tail = (q->tail + 1) % RING_BUF_SIZE;
    q->count++;
    pthread_cond_signal(&q->not_empty);
    pthread_mutex_unlock(&q->lock);
}

uint8_t queue_pop(BoundedQueue *q) {
    pthread_mutex_lock(&q->lock);
    while (q->count == 0) {
        pthread_cond_wait(&q->not_empty, &q->lock);
    }
    uint8_t val = q->buffer[q->head];
    q->head = (q->head + 1) % RING_BUF_SIZE;
    q->count--;
    pthread_cond_signal(&q->not_full);
    pthread_mutex_unlock(&q->lock);
    return val;
}
```

### Capability C: Windows NTFS ACL Security Inspection
For Windows environments, verify process security tokens and file access control descriptors matching [`win-vault`](../../tools/skills/win-vault/SKILL.md) and [`cyber-forensics`](../../tools/skills/cyber-forensics/SKILL.md).
