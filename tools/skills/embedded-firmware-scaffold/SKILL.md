---
name: embedded-firmware-scaffold
description: >-
  Embedded Systems, RTOS & Firmware Architecture skill (CT 655, EX 452, CT 725 03).
  Generates production-grade bare-metal C/C++ Hardware Abstraction Layers (HAL),
  peripheral register bitmasks, non-blocking ISR circular buffers, and FreeRTOS task graphs.
---

# Embedded Systems & Firmware Architect (`embedded-firmware-scaffold`)

Derived from **CT 655 (Embedded System)**, **EX 452 (Microprocessors)**, and **CT 725 03 (Embedded Systems Design using ARM Technology)** in the BE ECIE curriculum.

This skill equips agents to architect deterministic bare-metal and RTOS-based embedded firmware for microcontrollers (ARM Cortex-M, STM32, ESP32, AVR, PIC).

---

## 1. Operating Rules & Embedded Discipline

1. **Zero Uncontrolled Blocking:** Never use raw delay loops (`delay_ms()`) inside mission-critical loops or interrupt contexts. All delays must rely on non-blocking timer ticks (`millis()`, SysTick) or RTOS task delays (`vTaskDelay()`).
2. **Interrupt Service Routine (ISR) Minimal Footprint:**
   - Keep ISR execution time under 5 microseconds.
   - Never perform floating-point operations, blocking bus transfers, or memory allocation (`malloc`) inside an ISR.
   - Enqueue received bytes into lock-free circular buffers and set a volatile event flag for processing by the main loop/RTOS worker task.
3. **Volatile Memory Semantics:** Any variable modified inside an ISR and read by main execution must be declared `volatile` to prevent compiler register caching.
4. **Memory-Mapped Peripheral Alignment:** Enforce exact byte packing and struct alignment (`__attribute__((packed))`) when mapping hardware registers or communication protocol packets.

---

## 2. Core Capabilities & Workflows

### Capability A: Bare-Metal Non-Blocking State Machine Scaffold
```c
#include <stdint.h>
#include <stdbool.h>

typedef enum {
    SYS_STATE_INIT = 0,
    SYS_STATE_STANDBY,
    SYS_STATE_SAMPLING,
    SYS_STATE_TX_DATA,
    SYS_STATE_ERROR
} SystemState_t;

typedef struct {
    SystemState_t state;
    uint32_t lastTickMs;
    uint32_t sampleIntervalMs;
    uint16_t sensorValue;
} DeviceContext_t;

void Device_Init(DeviceContext_t *ctx) {
    ctx->state = SYS_STATE_INIT;
    ctx->lastTickMs = 0;
    ctx->sampleIntervalMs = 100; // 10 Hz
    ctx->sensorValue = 0;
}

void Device_Process(DeviceContext_t *ctx, uint32_t currentTickMs) {
    switch (ctx->state) {
        case SYS_STATE_INIT:
            // Hardware peripheral verification
            ctx->state = SYS_STATE_STANDBY;
            break;

        case SYS_STATE_STANDBY:
            if (currentTickMs - ctx->lastTickMs >= ctx->sampleIntervalMs) {
                ctx->lastTickMs = currentTickMs;
                ctx->state = SYS_STATE_SAMPLING;
            }
            break;

        case SYS_STATE_SAMPLING:
            // Read ADC register non-blocking
            ctx->sensorValue = 512; // Example ADC value
            ctx->state = SYS_STATE_TX_DATA;
            break;

        case SYS_STATE_TX_DATA:
            // Transmit via UART DMA or ring buffer
            ctx->state = SYS_STATE_STANDBY;
            break;

        case SYS_STATE_ERROR:
        default:
            // Safe fallback state
            break;
    }
}
```

### Capability B: ISR Circular Ring Buffer (Lock-Free SPSC)
```c
#define UART_RING_BUF_SIZE 128

typedef struct {
    volatile uint8_t buffer[UART_RING_BUF_SIZE];
    volatile uint16_t head; // Written by ISR
    volatile uint16_t tail; // Read by Main
} SPSC_RingBuffer_t;

bool RingBuffer_Push_From_ISR(SPSC_RingBuffer_t *rb, uint8_t byte) {
    uint16_t next_head = (rb->head + 1) % UART_RING_BUF_SIZE;
    if (next_head == rb->tail) {
        return false; // Buffer overrun
    }
    rb->buffer[rb->head] = byte;
    rb->head = next_head;
    return true;
}

bool RingBuffer_Pop_Main(SPSC_RingBuffer_t *rb, uint8_t *byte) {
    if (rb->head == rb->tail) {
        return false; // Buffer empty
    }
    *byte = rb->buffer[rb->tail];
    rb->tail = (rb->tail + 1) % UART_RING_BUF_SIZE;
    return true;
}
```

### Capability C: FreeRTOS Multi-Task Architecture
Generate structured RTOS task graphs with priorities, queue sizes, and mutex ownership conventions:
* **SensorAcqTask (Priority: High / 3):** Wakes periodically on timer semaphore, polls ADC, enqueues raw samples.
* **DSPProcessTask (Priority: Medium / 2):** Blocks on sample queue, executes digital filter, formats telemetry packets.
* **CommTelemetryTask (Priority: Low / 1):** Transmits packaged packets via UART/Radio, handles external downlink commands.
