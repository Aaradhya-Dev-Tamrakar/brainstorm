# Jetson Orin Nano — Setup, Provisioning & Optimization Runbook

**Date:** 2026-10-01  
**Author:** Aaradhya Dev Tamrakar  
**Device:** NVIDIA Jetson Orin Nano Developer Kit (or Module + Carrier Board)  
**Target OS / JetPack:** JetPack 6.x (Ubuntu 22.04 LTS) / JetPack 5.1.x (Ubuntu 20.04 LTS)  
**Status:** In Progress / Active Setup  

---

## 1. Verified Physical Hardware Inventory (Inspected & Confirmed)

| Component | Verified Hardware Ground Truth | Status & Role |
| :--- | :--- | :--- |
| **DevKit / Module** | **NVIDIA Jetson Orin Nano Developer Kit 8GB** (P/N: `945-13766-0000-000`, S/N: `1423925603897`) | 8GB Unified LPDDR5 Memory |
| **Primary High-Speed Storage** | **WD PC SN5000S NVMe™ SSD 512GB** (PCIe Gen4 x4, M.2 2280, `SDEPNSJ-5126-1006`) | **Root filesystem (`/`) & fast model cache** (Installed on M.2 Key M) |
| **Secondary Storage / Boot** | **ADATA 128GB microSDXC** (A1, V10, Class 10) + SD Adapter | Initial JetPack boot & QSPI firmware initialization |
| **Wireless Connectivity** | **AW-CB375NF** M.2 Key-E Wi-Fi + Bluetooth module (Installed) | Wi-Fi 5 / Bluetooth 5.0 |
| **Power Supply** | **Official 19V DC Power Adapter** (Barrel Jack) | Supports full MAXN (15W/25W) mode without throttling |
| **Cooling System** | **Active PWM Fan + Heatsink assembly** (Pre-installed) | Automatic thermal throttling prevention |
| **Video Output** | **Full-Size DisplayPort (DP)** + Braided DP Cable to Dell Monitor | Primary visual display output |
| **Peripheral Interfaces** | 4x USB 3.2 Gen 2 Type-A (ViewSonic Keyboard & Mouse connected) | Direct desktop interaction |
| **Console & Debug Interface** | **USB-to-TTL Serial UART Cable** + USB-C UFP port | Headless fallback & serial boot logging |

### 1.1 Physical Port & Jumper Layout

```
                        [ REAR I/O PORTS ]
 [USB-C]   [Gigabit Ethernet]   [4x USB 3.2 Gen 2]   [DisplayPort]   [19V DC Jack]
 ┌───────────────────────────────────────────────────────────────────────────────┐
 │                                                                               │
 │  [40-pin GPIO]         ┌──────────────────────┐          [MIPI CSI CAM 1]     │
 │  Pin 1..40             │  NVIDIA ORIN NANO    │                               │
 │                        │    HEATSINK + FAN    │                               │
 │                        └──────────────────────┘                               │
 │  [Button Header]       [microSD Slot (Under)]            [MIPI CSI CAM 0]     │
 └───────────────────────────────────────────────────────────────────────────────┘
```


---

## 2. Flashing & Initial Provisioning

### 2.1 Method 1: The Unified Jetson ISO / USB Flow (Recommended — No Linux Host PC Required)
*Starting with recent JetPack releases, NVIDIA provides a Unified ISO installer that flashes directly to your 512GB NVMe SSD and enables **Super Mode** automatically.*

1. **On your Windows PC:**
   - Go to [NVIDIA JetPack SDK Downloads](https://developer.nvidia.com/embedded/jetpack/downloads).
   - Download the **Jetson Unified ISO Image** (or JetPack 6.x SD Image).
   - Use **BalenaEtcher** to write the ISO to a USB flash drive (or microSD card).
2. **On the Jetson:**
   - Plug the flashed drive into one of the USB 3.2 ports (or microSD slot).
   - Power ON the Jetson (the UEFI firmware `36.4.3` will detect the installer).
   - Follow the graphical installer prompts on your Dell monitor.
   - Select the target destination drive: **WD PC SN5000S 512GB NVMe SSD** (`/dev/nvme0n1`).
   - The installer formats the SSD, installs Ubuntu + Jetson Linux BSP with **Super Mode**, and configures direct NVMe boot.

---

### 2.2 Method 2: NVIDIA SDK Manager (Requires Ubuntu Host PC)
*If you prefer flashing over USB from an existing Ubuntu 20.04 / 22.04 workstation:*

1. **On Ubuntu Host:**
   - Download and install SDK Manager: `sudo apt install ./sdkmanager_*.deb`.
   - Launch `sdkmanager`.
2. **Put Jetson in Force Recovery Mode:**
   - On the 12-pin button header under the module, use a jumper or DuPont wire to connect **Pin 9 (FC REC)** to **Pin 10 (GND)**.
   - Connect the 19V DC power adapter.
   - Remove the jumper.
   - Connect a USB-C to USB-A/C cable between the Jetson's USB-C port and your Ubuntu host PC.
   - Verify host sees device: `lsusb | grep 0955` (`0955:7523` or `0955:7023`).
3. **Flashing:**
   - Select **Jetson Orin Nano Developer Kit**, Target Storage **NVMe**, and click **Flash**.

---

## 3. Post-Boot System Configuration & Baseline Tuning

### 3.1 Initial System Updates & Packages
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential cmake git curl wget htop iotop tmux ufw \
                    python3-pip python3-dev python3-venv libopenblas-dev \
                    libopenmpi-dev openmpi-bin libjpeg-dev zlib1g-dev
```

### 3.2 Install `jetson-stats` (jtop)
Essential system monitor for Jetson hardware, thermals, power, clocks, and CUDA/TensorRT status:
```bash
sudo apt install -y python3-pip
sudo pip3 install -U jetson-stats
sudo systemctl restart jstats.service

# Run monitoring dashboard
jtop
```

### 3.3 Power Mode & Maximum Performance Tuning
```bash
# Check available power modes
sudo nvpmodel -p --verbose

# Set to MAXN mode (15W / 25W depending on module)
sudo nvpmodel -m 0

# Lock CPU/GPU clocks to maximum frequencies for benchmarking (optional)
sudo jetson_clocks
sudo jetson_clocks --show
```

### 3.4 NVMe Swap Space Configuration (Crucial for AI Model Loading)
Prevent Out-Of-Memory (OOM) kernel kills during PyTorch/TensorRT model builds:
```bash
# Verify existing swap
free -h
swapon --show

# Create 16GB NVMe Swapfile if needed
sudo fallocate -l 16G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make swap persistent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Set low swappiness to favor RAM until memory pressure hits
echo 'vm.swappiness=15' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

---

## 4. CUDA, TensorRT & AI Runtime Verification

### 4.1 Environment Variables
Add to `~/.bashrc`:
```bash
export CUDA_HOME=/usr/local/cuda
export PATH=${CUDA_HOME}/bin:${PATH}
export LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}
```
Reload:
```bash
source ~/.bashrc
nvcc --version
```

### 4.2 Verify CUDA & Device Capabilities
```bash
# Check CUDA Compiler
nvcc --version

# Check TensorRT
dpkg -l | grep nvinfer
python3 -c "import tensorrt; print('TensorRT Version:', tensorrt.__version__)" 2>/dev/null || echo "Check TRT python binding"
```

---

## 5. Docker & NVIDIA Container Runtime

JetPack includes NVIDIA Container Runtime out of the box with Docker.

```bash
# Configure default runtime to nvidia
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Test CUDA inside Docker
sudo docker run --rm --runtime nvidia --gpus all nvcr.io/nvidia/l4t-base:r36.2.0 nvidia-smi 2>/dev/null || \
sudo docker run --rm --runtime nvidia --gpus all nvcr.io/nvidia/l4t-cuda:12.2.2-runtime-ubuntu22.04 nvcc --version
```

---

## 6. Edge AI & LLM Inference Frameworks

### 6.1 Dusty-nv's `jetson-containers` (Best Practice for Jetson Ecosystem)
```bash
git clone --depth=1 https://github.com/dusty-nv/jetson-containers
cd jetson-containers
bash install.sh

# Run Ollama / Local LLM container optimized for Jetson Orin:
jetson-containers run $(autotag text-generation-webui)
# Or llama.cpp with CUDA support:
jetson-containers run $(autotag llama_cpp)
```

### 6.2 Native Ollama with CUDA Acceleration
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull lightweight quantized edge models (suitable for 4GB/8GB unified memory)
ollama pull qwen2.5:1.5b
ollama pull qwen2.5:3b
ollama pull phi3:mini
ollama pull deepseek-r1:1.5b
```

---

## 7. Execution & Provisioning Log

Record chronological logs, terminal outputs, issues encountered, and resolutions here:

| Timestamp | Phase / Step | Command / Action | Output / Status | Notes & Fixes |
| :--- | :--- | :--- | :--- | :--- |
| `2026-10-01 15:15` | Initialization | Created Runbook | Template Ready | Initialized baseline checklist |
| `2026-10-01 15:26` | Hardware Audit | Inspected Photos | Verified Kit & Parts | 8GB DevKit, 512GB NVMe, 128GB SD, 19V DC, Serial |
| `2026-10-01 15:38` | Physical Assembly | Connected Power, Ethernet, KB, Mouse | Powered ON | Green LED ON, Fan active |
| `2026-10-01 15:39` | First Boot | Boot Menu Loaded on Monitor | Success | DisplayPort active, UEFI/Boot Menu visible |
| `2026-10-01 15:40` | Firmware Audit | Inspected UEFI Splash Screen | **JetPack 6.x (36.4.3)** | Firmware: `36.4.3-gcid-38968081` (2025-01-08). Fell back to HTTP Boot (storage unprovisioned). |
| `2026-10-01 15:49` | Installer Acquisition | Downloaded Jetson ISO | **JetPack 7.2.1 (r39.2.1)** | File: `jetsoninstaller-r39.2.1-*.iso` (5.04 GB arm64). |
| `2026-10-01 15:52` | Media Creation | BalenaEtcher Flashing | Flashed OK | Wrote 5.04 GB to 128GB ADATA SDXC Card. |
| `2026-10-01 16:02` | Checksum Verification | BalenaEtcher Validation | **Flash Completed!** | 1 Successful Target verified (Effective speed: 14.7 MB/s). |
| `2026-10-01 16:05` | Firmware Upgrade Prompt | ISO Boot Detected Newer FW | Auto-skipped (30s) | Power cycled Jetson to re-trigger prompt. |
| `2026-10-01 16:07` | Firmware Upgrade Retry | Re-powering & Pressing [Y] | **User Confirmed** | Triggered UEFI capsule update to version `39.02.01`. |
| `2026-10-01 16:08` | QSPI Capsule Flashing | `Update Progress - 5%...100%` | Flashed OK | Internal QSPI updated to r39.02.01, auto-rebooted. |
| `2026-10-01 16:09` | Installer Boot (GRUB) | GNU GRUB 2.12 Loaded | **Selected ISO** | Triggered `*Install Jetson ISO r39.2.1`. |
| `2026-10-01 16:11` | PreIsoInstaller Logic | Firmware `39.2.1-gcid-46758480` | **Running** | ESRT verified `0x270201`. |
| `2026-10-01 16:12` | QSPI Secondary Capsule | `Update Progress - 7%...100%` | Flashed OK | Wrote secondary firmware partitions (TOS/PSC/UEFI). |
| `2026-10-01 16:13` | Final Reboot to GRUB | GNU GRUB 2.12 Loaded | **Ready** | Post-update boot. Selected `*Install Jetson ISO r39.2.1`. |
| `2026-10-01 16:16` | Target Storage Selection | Menu: `*Install on NVMe` | **Selected NVMe** | Direct rootfs installation targeting the 512GB WD PC SN5000S NVMe SSD. |
| `2026-10-01 16:18` | Linux Kernel Boot | `EFI stub: Booting Kernel` | **Booted** | Loaded initrd, exited boot services. |
| `2026-10-01 16:19` | Hardware Enumeration | Kernel Device Probe | **All Devices OK** | NVMe (`nvme0n1` @ 31.5 Gb/s Gen4), Gigabit Ethernet (`r8168`), USB KB/Mouse. |
| `2026-10-01 16:20` | Board Type Detection | `detect_board_type` | **DevKit Super** | Identified as `NVIDIA Jetson Orin Nano Engineering Reference Developer Kit Super`. |
| `2026-10-01 16:20` | NVMe Partitioning | `sgdisk -Z /dev/nvme0n1` | **475.4 GB Rootfs** | Created `/dev/nvme0n1p1` (475.4 GB root) + 14 system partitions. |
| `2026-10-01 16:20` | Automated OS Install | Subiquity / Curtin Engine | **Ubuntu 24.04.3 LTS** | Installed base system, kernel, drivers, and configured cloud-init. |
| `2026-10-01 16:21` | Package Installation | `nvidia-l4t-*`, Docker & Desktop | **Installed OK** | `nvidia-container-toolkit`, `docker.io`, `nvidia-l4t-kernel`, GNOME stack. |
| `2026-10-01 16:30` | Late Script Execution | Repo & Hardware Group Config | **Configured** | Configured `noble` repositories, `nvidia-ctk`, added `i2c`/`gpio` groups. |
| `2026-10-01 16:31` | Direct NVMe Boot | `L4TLauncher: Direct Boot` | **Success** | Direct high-speed boot from NVMe SSD `/dev/nvme0n1`. |
| `2026-10-01 16:32` | Desktop Setup Wizard | Ubuntu 24.04 GUI Setup | **Active** | Loaded graphical `Welcome!` wizard on Dell monitor. |
| `2026-10-01 16:32` | Desktop Setup Wizard | Ubuntu 24.04 GUI Setup | **Active** | Loaded graphical `Welcome!` wizard on Dell monitor. |
| `2026-10-01 16:34` | Language & License | English (US) & NVIDIA EULA | **Accepted** | Accepted license, confirmed English (US) typing layout. |
| `2026-10-01 16:35` | Wi-Fi Association | Connected `KEC Makerspace-5` | **Connected** | AW-CB375NF Wi-Fi associated successfully. |
| `2026-10-01 16:37` | Time Zone Configuration | `Kathmandu, Nepal (+0545)` | **Configured** | Synchronized local timezone. |
| `2026-10-01 16:38` | User Account Provisioning | User: `kecmakerspace` | **Created** | Hostname: `kecmakerspace`, password set. |
| `2026-10-01 16:49` | Ubuntu Pro Provisioning | Option: `Skip for now` | **Proceeded** | Skipped commercial token prompt to finish desktop load. |
| `2026-10-01 16:55` | System Telemetry | Option: `No, don't share` | **Opted Out** | Privacy preserved, finalizing desktop launch. |
| `2026-10-01 16:56` | Desktop Environment | GNOME Shell Desktop | **Live & Operational** | Booted into desktop with **25W Super Mode** indicator active in top panel. |

---

## 8. Visual Evidence & Hardware Documentation Gallery

All 57 setup photos and screenshots have been organized chronologically into [`research/media/2026-10-01_jetson_orin_nano_setup/`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/):

| Step / Artifact | Photo Reference | Description |
| :--- | :--- | :--- |
| **01. NVMe SSD & Wi-Fi** | [`01_nvme_ssd_and_wifi_bottom_view.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/01_nvme_ssd_and_wifi_bottom_view.jpg) | WD PC SN5000S 512GB NVMe SSD, AW-CB375NF Wi-Fi, DevKit P/N sticker |
| **02. Storage Media** | [`02_adata_128gb_microsd_card.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/02_adata_128gb_microsd_card.jpg) | ADATA 128GB MicroSDXC card (A1, V10) |
| **03. Power Supply** | [`03_19v_power_supply_brick.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/03_19v_power_supply_brick.jpg) | Official 19V DC Power Adapter |
| **04. Serial Debug Cable** | [`04_usb_ttl_uart_serial_cable.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/04_usb_ttl_uart_serial_cable.jpg) | USB-to-TTL Serial UART Cable (GND, TX, RX, VCC) |
| **05. SD Adapter** | [`05_adata_sd_card_adapter.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/05_adata_sd_card_adapter.jpg) | ADATA full-size SD adapter |
| **06. Desk & Display Setup** | [`06_desk_setup_displayport_cable_keyboard.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/06_desk_setup_displayport_cable_keyboard.jpg) | Braided DisplayPort cable, ViewSonic keyboard, mouse, Dell monitor |
| **07. Jetson Top View** | [`07_jetson_orin_nano_top_view_fan_heatsink.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/07_jetson_orin_nano_top_view_fan_heatsink.jpg) | DevKit top view with active PWM fan, heatsink, rear I/O |
| **08. UEFI Initial Boot** | [`08_uefi_initial_boot_firmware_36_4_3.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/08_uefi_initial_boot_firmware_36_4_3.jpg) | Splash screen showing firmware 36.4.3 & fallback to HTTP boot |
| **09. Boot Menu Prompt** | [`09_uefi_boot_menu_prompt.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/09_uefi_boot_menu_prompt.jpg) | UEFI menu prompt (ESC/F11/Enter) |
| **10. NVIDIA ISO Acquisition** | [`10_nvidia_docs_and_iso_download.png`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/10_nvidia_docs_and_iso_download.png) | Download of Jetson ISO r39.2.1 and SDK Manager |
| **11-15. BalenaEtcher Flashing** | [`11_balena_etcher_ready_to_flash.png`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/11_balena_etcher_ready_to_flash.png) – [`15_balena_etcher_flash_completed.png`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/15_balena_etcher_flash_completed.png) | Flashing & validation of `jetsoninstaller-*.iso` to SD card |
| **16. Safe Ejection** | [`16_windows_explorer_sd_card_ejected.png`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/16_windows_explorer_sd_card_ejected.png) | Windows Explorer drive ejection verification |
| **17, 20-22. QSPI Firmware Upgrade** | [`17_qspi_firmware_update_prompt.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/17_qspi_firmware_update_prompt.jpg) – [`22_qspi_capsule_flashing_progress_5_percent.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/22_qspi_capsule_flashing_progress_5_percent.jpg) | Capsule update to version `39.02.01` confirmed and written |
| **19. GNU GRUB Menu** | [`19_grub_boot_menu_install_iso_selected.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/19_grub_boot_menu_install_iso_selected.jpg) | GRUB 2.12 booting `*Install Jetson ISO r39.2.1` |
| **23-25. Firmware Verification** | [`23_pre_iso_installer_logic_running.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/23_pre_iso_installer_logic_running.jpg) – [`25_firmware_39_2_1_version_header.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/25_firmware_39_2_1_version_header.jpg) | Running PreIsoInstaller logic on verified `39.2.1` UEFI firmware |
| **26-27. Secondary Stage Capsule** | [`26_qspi_stage2_capsule_update_7_percent.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/26_qspi_stage2_capsule_update_7_percent.jpg) – [`27_qspi_stage2_capsule_update_6_percent.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/27_qspi_stage2_capsule_update_6_percent.jpg) | Finalizing secondary QSPI firmware partitions |
| **28-29. Post-Update GRUB Boot** | [`28_grub_post_firmware_update_install_iso.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/28_grub_post_firmware_update_install_iso.jpg) – [`29_grub_post_firmware_update_closeup.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/29_grub_post_firmware_update_closeup.jpg) | QSPI update complete, booting Linux installer |
| **30. Target Storage Selection** | [`30_installer_target_storage_install_on_nvme.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/30_installer_target_storage_install_on_nvme.jpg) | Selecting `*Install on NVMe` for direct high-speed PCIe Gen4 rootfs |
| **31-34. Kernel Boot & Device Init** | [`31_efi_stub_booting_linux_kernel.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/31_efi_stub_booting_linux_kernel.jpg) – [`34_kernel_tegra_memory_controller_init.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/34_kernel_tegra_memory_controller_init.jpg) | Kernel probed PCIe Gen4 NVMe (`nvme0n1` @ 31.5 Gb/s), Realtek GbE & USB |
| **35-39. Super Mode & OS Provisioning** | [`35_board_detection_orin_nano_devkit_super.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/35_board_detection_orin_nano_devkit_super.jpg) – [`39_ubuntu_24_04_3_cloud_init_boot.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/39_ubuntu_24_04_3_cloud_init_boot.jpg) | Detected `Orin Nano DevKit Super`, formatted 475.4GB NVMe rootfs, installed Ubuntu 24.04.3 LTS via Curtin / Cloud-Init |
| **40. Package Installation** | [`40_package_installation_nvidia_l4t_and_desktop_stack.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/40_package_installation_nvidia_l4t_and_desktop_stack.jpg) | Installing NVIDIA Container Toolkit, Docker, L4T kernel headers, and GNOME desktop |
| **41-43. Subiquity Post-Install Tuning** | [`41_subiquity_late_purge_and_initrd_update.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/41_subiquity_late_purge_and_initrd_update.jpg) – [`43_subiquity_late_group_add_i2c_gpio.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/43_subiquity_late_group_add_i2c_gpio.jpg) | Purged bloatware, configured `nvidia-ctk`, added `i2c`/`gpio` permissions |
| **44-45. Direct NVMe Boot & Welcome GUI** | [`44_l4tlauncher_attempting_direct_nvme_boot.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/44_l4tlauncher_attempting_direct_nvme_boot.jpg) – [`45_ubuntu_desktop_gui_welcome_screen.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/45_ubuntu_desktop_gui_welcome_screen.jpg) | `L4TLauncher` direct booted NVMe into Ubuntu 24.04 GUI Setup Wizard |
| **46-50. GUI Localization & EULA** | [`46_ubuntu_gui_welcome_language_selected.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/46_ubuntu_gui_welcome_language_selected.jpg) – [`50_ubuntu_gui_typing_keyboard_english_us.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/50_ubuntu_gui_typing_keyboard_english_us.jpg) | Selected English (US), accepted NVIDIA Driver EULA, verified keyboard input |
| **51-55. Wi-Fi, Timezone & User Account** | [`51_ubuntu_gui_wifi_kec_makerspace_connected.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/51_ubuntu_gui_wifi_kec_makerspace_connected.jpg) – [`55_ubuntu_gui_ubuntu_pro_skip_for_now.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/55_ubuntu_gui_ubuntu_pro_skip_for_now.jpg) | Connected to `KEC Makerspace-5`, set `Kathmandu, Nepal`, configured `kecmakerspace` user, skipped Ubuntu Pro |
| **56. Telemetry Opt-Out** | [`56_ubuntu_gui_help_improve_ubuntu_telemetry_opt_out.png`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/56_ubuntu_gui_help_improve_ubuntu_telemetry_opt_out.png) | Selected `No, don't share system data` |
| **57. Desktop Live with Super Mode** | [`57_jetson_orin_nano_desktop_wallpaper_25w_mode_active.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/57_jetson_orin_nano_desktop_wallpaper_25w_mode_active.jpg) | Full Ubuntu 24.04 desktop wallpaper active with **25W Super Mode** enabled in top panel |

---

## 9. Benchmark & Telemetry Ground Truth

| Metric | Target / Spec | Observed Ground Truth | Tool / Command Used |
| :--- | :--- | :--- | :--- |
| **Idle Power** | < 4.0 W | _TBD_ | `jtop` |
| **Peak MAXN Power** | 15 W / 25 W | _TBD_ | `jtop` stress test |
| **Idle Temp (CPU/GPU)** | < 45°C | _TBD_ | `jtop` |
| **Inference Token Speed (1.5B)** | ~25–40 tok/s | _TBD_ | `ollama run qwen2.5:1.5b --verbose` |
| **Inference Token Speed (3B)** | ~15–25 tok/s | _TBD_ | `ollama run qwen2.5:3b --verbose` |

