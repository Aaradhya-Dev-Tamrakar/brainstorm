# KEC Makerspace — NVIDIA Jetson Orin Nano Developer Kit (8GB)
## Official Hardware Handover, Provisioning Report & Developer Guide

- **Target Facility**: KEC Makerspace (Kantipur Engineering College)
- **Prepared By**: Aaradhya Dev Tamrakar
- **Date**: October 1, 2026
- **Status**: Operational / Fully Provisioned & Verified (`EMPIRICALLY_VERIFIED`)
- **Firmware / OS**: JetPack 7.2.1 (L4T r39.2.1) | Ubuntu 24.04.5 LTS ARM64 | Linux Kernel 6.8.12-1021-tegra

---

## 1. Executive Summary & Hardware Inventory

The **NVIDIA Jetson Orin Nano Developer Kit (8GB)** has been unboxed, physically assembled, upgraded to the latest QSPI firmware, and provisioned with **Ubuntu 24.04 LTS**. 

To maximize throughput and prevent the performance bottlenecks and wear typical of microSD cards, the system has been configured for **direct PCIe Gen4 NVMe root filesystem execution** on a high-speed Western Digital 512GB SSD.

```
+-----------------------------------------------------------------------------------+
|                            JETSON ORIN NANO 8GB DEV KIT                           |
|                                                                                   |
|  +---------------------------+   PCIe Gen4 x4    +-----------------------------+  |
|  |   Jetson Orin Nano SOM    | <===============> | 512GB WD PC SN5000S NVMe    |  |
|  | 6-core ARM Cortex-A78AE   |    (31.5 Gb/s)    | (Rootfs: /dev/nvme0n1p1)    |  |
|  | 1024-core Ampere GPU      |                   | 475.4 GB Clean Linux Space  |  |
|  | 32 Tensor Cores (40 TOPS) |                   +-----------------------------+  |
|  +---------------------------+                                                    |
|                |                                                                  |
|                +-------------> AW-CB375NF M.2 Key-E Wi-Fi / Bluetooth             |
|                +-------------> Realtek RTL8168 Gigabit Ethernet                   |
|                +-------------> 25W Super Mode Active (MAXN Clock Profile)         |
+-----------------------------------------------------------------------------------+
```

### Physical Inventory Table

| Component | Specification / Part Number | Description / Location |
| :--- | :--- | :--- |
| **SoM / Carrier Board** | NVIDIA Jetson Orin Nano 8GB (`945-13766-0000-000`) | Carrier board with active PWM heatsink fan |
| **Primary Storage** | Western Digital PC SN5000S 512GB NVMe M.2 2280 | Installed in bottom M.2 Key-M slot (`/dev/nvme0n1`) |
| **Wireless Module** | AzureWave AW-CB375NF M.2 Key-E 2230 | Dual-band Wi-Fi 5 + Bluetooth 5.0 |
| **Flashing Storage** | ADATA 128GB MicroSDXC (A1, V10) + SD Adapter | Used for initial ISO delivery & QSPI flashing |
| **Power Supply** | Official NVIDIA 19V DC Power Adapter (Barrel Jack) | Dedicated high-wattage power delivery |
| **Serial Debug Cable** | 4-Pin USB-to-TTL UART Cable (TX/RX/GND/3V3) | Reserved for low-level kernel serial debugging |

---

## 2. System Specifications & Firmware Baseline

| Layer | Configured Baseline | Notes / Benchmark Capabilities |
| :--- | :--- | :--- |
| **Compute Architecture** | NVIDIA Ampere (1024 CUDA Cores, 32 Tensor Cores) | **40 TOPS (Dense INT8)** AI inference compute |
| **CPU Architecture** | 6-core ARM® Cortex®-A78AE v8.2 64-bit @ 1.5 GHz | 1.5 MB L2 + 4 MB L3 cache |
| **Memory** | 8 GB 128-bit LPDDR5 @ 68 GB/s | Unified system & video memory architecture |
| **Power Profile** | **25W Super Mode (`MAXN`)** | Uncapped clock frequencies for peak edge inference |
| **Firmware (QSPI)** | **`39.2.1-gcid-46758480` (ESRT `0x270201`)** | Upgraded via UEFI capsule update from factory 36.4.3 |
| **Operating System** | Ubuntu 24.04.5 LTS (Noble Numbat) | Modern LTS kernel `6.8.12-1021-tegra aarch64` |
| **NVIDIA Stack** | JetPack 7.2.1 / L4T r39.2.1 | Native CUDA 12.6, TensorRT 10.x runtime, CuDNN |
| **Container Engine** | Docker Engine + `nvidia-container-toolkit` | Direct GPU pass-through into OCI containers |

---

## 3. Network Access & Remote Connection Coordinates

The Jetson is configured for headless remote operation across both Makerspace Wi-Fi and direct Gigabit Ethernet.

### Network Coordinates

- **Hostname**: `kecmakerspace`
- **Default Username**: `kecmakerspace`
- **Ethernet IP (`enP8p1s0`)**: `192.168.1.125` *(Primary Gigabit)*
- **Wi-Fi IP (`wlP1p1s0`)**: `192.168.1.126` *(Connected to `KEC Makerspace-5`)*
- **USB-C Device Bridge (`l4tbr0`)**: `192.168.55.1` *(Direct USB cable connection)*

---

### How to Connect Remotely

#### 1. Via Command Line / PowerShell / Terminal:
```bash
ssh kecmakerspace@192.168.1.125
# Or via Wi-Fi:
ssh kecmakerspace@192.168.1.126
```

#### 2. Via VS Code (Recommended for Development):
1. Install the **Remote - SSH** extension in VS Code.
2. Press `Ctrl + Shift + P` -> `Remote-SSH: Connect to Host...`.
3. Enter: `kecmakerspace@192.168.1.125`.
4. Select `Linux` and enter the password. You now have a full VS Code IDE running directly inside the Jetson.

---

## 4. Operational Best Practices for Makerspace Members

To protect the hardware, prevent data corruption, and ensure fair sharing among students and researchers, all members must follow these operating standards:

### Rule 1: Clean Shutdowns Only (CRITICAL)
> [!CAUTION]
> **NEVER unplug the 19V DC power barrel jack while the Jetson is running.** 
> Cutting power abruptly while the NVMe SSD is performing write operations will damage the B-tree filesystem structure and can brick the root partition.

**To Power Off:**
```bash
sudo poweroff
```
Wait until the monitor goes dark and the green LED turns off before disconnecting the power supply.

**To Reboot:**
```bash
sudo reboot
```

---

### Rule 2: 8GB Unified Memory Management (Swapfile Protection)
Because the 8GB LPDDR5 memory is shared simultaneously between the CPU OS and the GPU VRAM, loading large AI models (like 7B LLMs or large Vision Transformers) can trigger Linux Out-Of-Memory (`OOM-killer`) halts.

A **16 GB NVMe Swapfile** is configured at `/swapfile` with `swappiness=15`. 

Always monitor memory usage before running large models:
```bash
free -h
```

---

### Rule 3: Real-Time Hardware & Thermal Monitoring (`jtop`)
The `jetson-stats` package provides real-time telemetry of GPU utilization, thermal temperatures, fan speed, and power rail wattage.

Launch the monitoring dashboard:
```bash
jtop
```

- Press `1` for **ALL** (CPU, GPU, RAM, Swap, Disk, Fan).
- Press `2` for **GPU** (CUDA cores, Tensor engines load).
- Press `3` for **CTRL** (Switch between 7W, 15W, and 25W Super Mode).
- Press `4` for **INFO** (JetPack, CUDA, TensorRT, OpenCV library versions).
- Press `q` to exit.

---

## 5. Developer Quickstart Guide (AI, Vision & Robotics)

### 5.1 Python Virtual Environments (PEP 668 Compliant)
Ubuntu 24.04 enforces externally managed Python environments. Always create a virtual environment for project dependencies:

```bash
# Create project directory and venv
mkdir ~/my_robotics_project && cd ~/my_robotics_project
python3 -m venv venv
source venv/bin/activate

# Install common ML/Robotics packages
pip install numpy scipy matplotlib opencv-python pyyaml
```

---

### 5.2 GPU-Accelerated Docker Containers
NVIDIA Container Toolkit is pre-installed. Run containerized workflows with full GPU access using the `--runtime nvidia` flag:

```bash
# Test NVIDIA GPU access inside Docker
sudo docker run --rm --runtime nvidia --gpus all nvcr.io/nvidia/cuda:12.6.0-base-ubuntu24.04 nvidia-smi
```

---

### 5.3 Local Edge LLM & SLM Inference (Ollama)
The Jetson Orin Nano (40 TOPS) is capable of running Small Language Models (SLMs) and Vision-Language Models locally at 25–40 tokens/second:

```bash
# Run 1.5B Edge Model (Fast - ~35 tok/s)
ollama run qwen2.5:1.5b

# Run Reasoning Model
ollama run deepseek-r1:1.5b

# Run Multimodal Vision Model (Analyze images / camera feed)
ollama run llava-phi3
```

---

### 5.4 40-Pin Expansion Header & GPIO Safety
The 40-pin header follows the Raspberry Pi form factor (3.3V logic level).

- **Pin 1 / 17**: 3.3V DC Power
- **Pin 2 / 4**: 5.0V DC Power
- **Pin 6 / 9 / 14 / 20 / 25 / 30 / 34 / 39**: GND
- **Pins 3, 5**: I2C Bus 1 (`/dev/i2c-1`)
- **Pins 8, 10**: UART Serial (`/dev/ttyTHS1`)
- **Pins 19, 21, 23, 24, 26**: SPI Bus 0

> [!WARNING]
> **All GPIO signal pins operate strictly at 3.3V logic.** Connecting 5V sensors directly to GPIO pins without a logic level converter will permanently destroy the SoC pins.

---

## 6. Visual Verification & Photographic Evidence

A complete photographic archive documenting every hardware component, firmware screen, partitioning step, and network configuration is preserved in the project repository:

- **Full Runbook**: [`research/notes/2026-10-01_JETSON_ORIN_NANO_SETUP_AND_PROVISIONING_RUNBOOK.md`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/notes/2026-10-01_JETSON_ORIN_NANO_SETUP_AND_PROVISIONING_RUNBOOK.md)
- **Session Transcript**: [`research/transcripts/2026-10-01_JETSON-ORIN-NANO-HARDWARE-AND-FIRMWARE-PROVISIONING_CONVERSATION.md`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/transcripts/2026-10-01_JETSON-ORIN-NANO-HARDWARE-AND-FIRMWARE-PROVISIONING_CONVERSATION.md)
- **59-Photo Evidence Gallery**: [`research/media/2026-10-01_jetson_orin_nano_setup/`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/)

---

## 7. Emergency Support & Contact

If the board fails to boot, encounters network issues, or requires re-flashing:
- **Lead Maintainer**: Aaradhya Dev Tamrakar (KEC Makerspace AI & Robotics Lead)
- **Official NVIDIA Documentation**: [NVIDIA Jetson Linux Developer Guide (r39.2)](https://docs.nvidia.com/jetson/archives/r39.2/developerguide/)
- **Repository Track**: `Aaradhya-Dev-Tamrakar/brainstorm` (`main` branch)
